from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import evaluate
import verify_dirac_trace
import verify_repro_package
import verify_figure_regeneration

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "protocol" / "run-record.schema.json"
RUBRIC = ROOT / "protocol" / "scoring-rubric.yaml"


def score_map(value=3):
    return {name: value for name in evaluate.DIMENSIONS}


def make_record(arm: str, run_id: str, score=3):
    available = arm == "with-skill"
    return {
        "run_id": run_id,
        "pair_id": "pair-T01-r1",
        "task_id": "T01",
        "arm": arm,
        "repeat": 1,
        "started_at_utc": "2026-11-23T00:00:00Z",
        "ended_at_utc": "2026-11-23T00:01:00Z",
        "protocol": {
            "version": "1.0",
            "commit": "a" * 40,
            "skill_source_commit": "9" * 40,
            "environment_lock_sha256": "b" * 64,
            "scoring_rubric_sha256": "c" * 64,
            "evaluator_manifest_sha256": "d" * 64,
            "task_manifest_sha256": "e" * 64,
        },
        "model": {"label": "test-model", "immutable_id": None, "reasoning_effort": "high", "sampling": None},
        "runtime": {"os": "Linux", "codex_product": "Codex", "codex_version": "1.0", "python_version": "3.13", "architecture": "x86_64", "hardware": {"cpu": "test"}},
        "project_context": {"repository": "test/repo", "source_commit": "f" * 40, "instructions_sha256": "1" * 64, "workspace_snapshot_sha256": "2" * 64, "shared_skill_routing_removed": True},
        "task_input": {"prompt_sha256": "3" * 64, "input_manifest_sha256": "4" * 64, "source_commit": "f" * 40, "source_files": []},
        "tools": {"allowlist": ["python"], "network_policy": "offline", "versions": {"python": "3.13"}},
        "budget": {"wall_time_seconds": 600, "token_limit": 10000, "tool_call_limit": 30},
        "execution": {"randomization_seed": "seed-1", "pair_order": "A_then_B", "actual_wall_time_seconds": 60, "actual_tool_calls": 5, "token_count": 1000, "commands": ["python task.py"], "tool_log_artifact": f"logs/{run_id}.json", "transcript_artifact": f"transcripts/{run_id}.json", "exit_status": 0},
        "skill": {
            "available": available,
            "source_commit": "9" * 40 if available else None,
            "manifest_sha256": "a" * 64 if available else None,
            "invocation": "$high-energy-theory-research" if available else None,
            "references_loaded": ["references/symbolic-calculation.md"] if available else [],
            "availability_evidence_artifact": f"evidence/{run_id}-skill.json",
        },
        "artifacts": [
            {"path": f"logs/{run_id}.json", "sha256": "5" * 64, "role": "tool_log"},
            {"path": f"transcripts/{run_id}.json", "sha256": "6" * 64, "role": "transcript"},
            {"path": f"evidence/{run_id}-skill.json", "sha256": "7" * 64, "role": "skill_availability_evidence"},
        ],
        "evaluation": {
            "hard_gates": {name: "pass" for name in evaluate.GATES},
            "dimension_scores": score_map(score),
            "autonomy_score": 3,
            "weighted_score": 25 * score,
            "deterministic_checks": [],
            "reviewer_assessments": [
                {"reviewer_id": "reviewer-1", "arm_label_hidden": True, "dimension_scores": score_map(score), "autonomy_score": 3, "hard_gates": {name: "pass" for name in evaluate.GATES}},
                {"reviewer_id": "reviewer-2", "arm_label_hidden": True, "dimension_scores": score_map(score), "autonomy_score": 3, "hard_gates": {name: "pass" for name in evaluate.GATES}},
            ],
            "reviewer_consensus_note": None,
            "adjudication": None,
        },
        "deviations": [],
    }


class EvaluatorTests(unittest.TestCase):
    def test_score_formula_zero_and_maximum(self):
        weights = evaluate.read_rubric(RUBRIC)["weights"]
        self.assertEqual(evaluate.score_dimensions(score_map(0), weights), 0.0)
        self.assertEqual(evaluate.score_dimensions(score_map(4), weights), 100.0)
        self.assertEqual(evaluate.score_dimensions(score_map(3), weights), 75.0)

    def test_valid_pair_passes(self):
        a = make_record("no-skill", "run-a")
        b = make_record("with-skill", "run-b")
        a2, b2 = evaluate.validate_pair(a, b, SCHEMA, RUBRIC)
        self.assertEqual(a2["arm"], "no-skill")
        self.assertEqual(b2["arm"], "with-skill")

    def test_no_skill_cannot_claim_skill_available(self):
        a = make_record("no-skill", "run-a")
        a["skill"]["available"] = True
        with self.assertRaises(evaluate.EvaluationError):
            evaluate.validate_run(a, SCHEMA, RUBRIC)

    def test_pair_rejects_control_mismatch(self):
        a = make_record("no-skill", "run-a")
        b = make_record("with-skill", "run-b")
        b["tools"]["allowlist"] = ["python", "browser"]
        with self.assertRaisesRegex(evaluate.EvaluationError, "controls differ"):
            evaluate.validate_pair(a, b, SCHEMA, RUBRIC)

    def test_pair_rejects_skill_commit_mismatch(self):
        a = make_record("no-skill", "run-a")
        b = make_record("with-skill", "run-b")
        b["skill"]["source_commit"] = "8" * 40
        with self.assertRaisesRegex(evaluate.EvaluationError, "Skill commit differs"):
            evaluate.validate_pair(a, b, SCHEMA, RUBRIC)

    def test_one_point_reviewer_difference_requires_consensus_note(self):
        a = make_record("no-skill", "run-a")
        a["evaluation"]["reviewer_assessments"][1]["dimension_scores"]["efficiency"] = 2
        with self.assertRaisesRegex(evaluate.EvaluationError, "consensus note"):
            evaluate.validate_run(a, SCHEMA, RUBRIC)
        a["evaluation"]["reviewer_consensus_note"] = "Reviewers discussed and agreed on the recorded final score."
        self.assertEqual(evaluate.validate_run(a, SCHEMA, RUBRIC), 75.0)

    def test_pair_rejects_shared_transcript(self):
        a = make_record("no-skill", "run-a")
        b = make_record("with-skill", "run-b")
        b["execution"]["transcript_artifact"] = a["execution"]["transcript_artifact"]
        b["artifacts"][1]["path"] = a["execution"]["transcript_artifact"]
        with self.assertRaisesRegex(evaluate.EvaluationError, "separate transcript"):
            evaluate.validate_pair(a, b, SCHEMA, RUBRIC)

    def test_git_blob_sha1_matches_git_object_algorithm(self):
        data = b"abc\n"
        expected = hashlib.sha1(b"blob 4\0abc\n").hexdigest()
        self.assertEqual(evaluate.git_blob_sha1(data), expected)

    def test_verify_source_record(self):
        data = b"benchmark source\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.txt"
            path.write_bytes(data)
            record = {
                "path": "source.txt",
                "size_bytes": len(data),
                "git_blob_sha1": evaluate.git_blob_sha1(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
            actual = evaluate.verify_source_record(record, path)
            self.assertEqual(actual["sha256"], record["sha256"])
            record["git_blob_sha1"] = "0" * 40
            with self.assertRaisesRegex(evaluate.EvaluationError, "Git blob SHA-1 mismatch"):
                evaluate.verify_source_record(record, path)

    def test_cluster_bootstrap_is_deterministic(self):
        values = {"family-a": 4.0, "family-b": 6.0, "family-c": 8.0}
        first = evaluate.cluster_bootstrap_interval(values, seed=123, resamples=1000)
        second = evaluate.cluster_bootstrap_interval(values, seed=123, resamples=1000)
        self.assertEqual(first, second)
        self.assertLessEqual(first["lower"], first["upper"])

    def test_round_one_is_never_confirmatory(self):
        a = make_record("no-skill", "run-a")
        b = make_record("with-skill", "run-b", score=4)
        manifest = {"tasks": [{"id": "T01", "dimension": "theoretical_derivation", "task_family": "threshold_kinematics", "skill_reference": "references/symbolic-calculation.md"}]}
        report = evaluate.compare_records([a, b], manifest, "round_1_pilot", seed=123, schema_path=SCHEMA, rubric_path=RUBRIC)
        self.assertEqual(report["decision"], "inconclusive")
        self.assertIsNone(report["summary"]["confidence_interval_95"])
        self.assertEqual(report["summary"]["macro_mean_delta_q"], 25.0)
        self.assertEqual(report["summary"]["reviewer_agreement"]["exact_agreement_rate"], 1.0)
        self.assertEqual(report["summary"]["reviewer_agreement"]["quadratic_weighted_cohen_kappa"], 1.0)

    def test_duplicate_run_id_rejected(self):
        a = make_record("no-skill", "run-a")
        b = make_record("with-skill", "run-a")
        manifest = {"tasks": [{"id": "T01", "dimension": "theoretical_derivation", "task_family": "threshold_kinematics", "skill_reference": "references/symbolic-calculation.md"}]}
        with self.assertRaisesRegex(evaluate.EvaluationError, "Duplicate run_id"):
            evaluate.compare_records([a, b], manifest, "round_1_pilot", seed=1, schema_path=SCHEMA, rubric_path=RUBRIC)

    def test_round_two_holdout_positive_requires_full_design(self):
        dimensions = ["theoretical_derivation", "numerical_integration", "paper_reading", "symbolic_calculation", "figure_audit", "reproducibility"]
        records = []
        tasks = []
        for dim_index, dimension in enumerate(dimensions):
            for family_index in range(2):
                task_id = f"H{dim_index + 1}{family_index + 1}"
                family = f"family-{task_id}"
                tasks.append({"id": task_id, "dimension": dimension, "task_family": family, "skill_reference": "references/symbolic-calculation.md"})
                for repeat in range(1, 4):
                    pair_id = f"pair-{task_id}-r{repeat}"
                    a = make_record("no-skill", f"{pair_id}-A", score=2)
                    b = make_record("with-skill", f"{pair_id}-B", score=3)
                    for record in (a, b):
                        record["pair_id"] = pair_id
                        record["task_id"] = task_id
                        record["repeat"] = repeat
                        record["execution"]["transcript_artifact"] = f"transcripts/{record['run_id']}.json"
                        record["artifacts"][1]["path"] = record["execution"]["transcript_artifact"]
                        record["skill"]["availability_evidence_artifact"] = f"evidence/{record['run_id']}-skill.json"
                        record["artifacts"][2]["path"] = record["skill"]["availability_evidence_artifact"]
                    records.extend([a, b])
        report = evaluate.compare_records(
            records,
            {"tasks": tasks},
            "round_2_full",
            seed=17,
            schema_path=SCHEMA,
            rubric_path=RUBRIC,
        )
        self.assertEqual(report["decision"], "positive")
        self.assertEqual(report["summary"]["paired_run_count"], 36)
        self.assertEqual(report["summary"]["independent_task_family_count"], 12)
        self.assertEqual(report["summary"]["macro_mean_delta_q"], 25.0)
        report["protocol_commit"] = "a" * 40
        report["analysis_plan_sha256"] = "b" * 64
        report["environment_lock_sha256"] = "c" * 64
        evaluate.validate_schema(report, ROOT / "protocol" / "comparison-report.schema.json")

    def test_round_two_single_b_only_gate_failure_is_mixed(self):
        dimensions = ["theoretical_derivation", "numerical_integration", "paper_reading", "symbolic_calculation", "figure_audit", "reproducibility"]
        records = []
        tasks = []
        pair_counter = 0
        for dim_index, dimension in enumerate(dimensions):
            for family_index in range(2):
                task_id = f"H{dim_index + 1}{family_index + 1}"
                family = f"family-{task_id}"
                tasks.append({"id": task_id, "dimension": dimension, "task_family": family, "skill_reference": "references/symbolic-calculation.md"})
                for repeat in range(1, 4):
                    pair_counter += 1
                    pair_id = f"pair-{task_id}-r{repeat}"
                    a = make_record("no-skill", f"{pair_id}-A", score=2)
                    b = make_record("with-skill", f"{pair_id}-B", score=3)
                    for record in (a, b):
                        record["pair_id"] = pair_id
                        record["task_id"] = task_id
                        record["repeat"] = repeat
                        record["execution"]["transcript_artifact"] = f"transcripts/{record['run_id']}.json"
                        record["artifacts"][1]["path"] = record["execution"]["transcript_artifact"]
                        record["skill"]["availability_evidence_artifact"] = f"evidence/{record['run_id']}-skill.json"
                        record["artifacts"][2]["path"] = record["skill"]["availability_evidence_artifact"]
                    if pair_counter == 1:
                        b["evaluation"]["hard_gates"]["critical_physics_error"] = "fail"
                        for reviewer in b["evaluation"]["reviewer_assessments"]:
                            reviewer["hard_gates"]["critical_physics_error"] = "fail"
                    records.extend([a, b])
        report = evaluate.compare_records(records, {"tasks": tasks}, "round_2_full", seed=17, schema_path=SCHEMA, rubric_path=RUBRIC)
        self.assertEqual(report["decision"], "mixed")
        self.assertEqual(report["summary"]["hard_gate_summary"]["b_only_failure_pair_count"], 1)

    def test_explicit_dirac_representation_trace(self):
        result = verify_dirac_trace.evaluate((2.3, 0.4, -0.7, 1.1), (1.8, -0.2, 0.9, 0.3), 0.6)
        self.assertEqual(result["status"], "PASS")
        self.assertLessEqual(result["max_clifford_residual"], 1e-10)
        self.assertLessEqual(result["max_trace_residual"], 1e-10)

    def test_reproducibility_package_independent_weighted_mean(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "solution.py"
            input_csv = root / "input.csv"
            output_json = root / "result.json"
            manifest_path = root / "manifest.json"
            source_bytes = b"# test source\nprint('not executed')\n"
            input_bytes = verify_repro_package.EXPECTED_CSV
            output_bytes = b'{"weighted_mean": 1.0}\n'
            source.write_bytes(source_bytes)
            input_csv.write_bytes(input_bytes)
            output_json.write_bytes(output_bytes)
            manifest = {
                "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
                "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
                "command": "python solution.py",
                "environment": {"python_version": "3.13", "os": "Linux", "architecture": "x86_64"},
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = verify_repro_package.verify(source, input_csv, output_json, manifest_path)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["weighted_mean_independent"], 1.0)
            self.assertFalse(result["source_executed_by_evaluator"])

    def test_reproducibility_package_rejects_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "solution.py"
            input_csv = root / "input.csv"
            output_json = root / "result.json"
            manifest_path = root / "manifest.json"
            source.write_text("print(1)\n", encoding="utf-8")
            input_csv.write_bytes(verify_repro_package.EXPECTED_CSV)
            output_json.write_text('{"weighted_mean":1.0}\n', encoding="utf-8")
            manifest = {"source_sha256":"0"*64,"input_sha256":"0"*64,"output_sha256":"0"*64,"command":"python solution.py","environment":{"python_version":"3.13","os":"Linux","architecture":"x86_64"}}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source_sha256 mismatch"):
                verify_repro_package.verify(source, input_csv, output_json, manifest_path)


    def test_pinned_figure_generator_matches_golden_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model_root = root / "model-inputs"
            golden_root = root / "golden"
            repo_slug = "LZ-3-body-for-hdm"
            generator_rel = "research/three_body_calculation_and_validation/plot_user_dsigma_curve.py"
            csv_rel = "research/three_body_calculation_and_validation/results/fixed_speed_xe131_dsigma_450kev.csv"
            minima_rel = "research/three_body_calculation_and_validation/results/local_minima_refinement_1keV.csv"
            output_rel = "research/three_body_calculation_and_validation/results/plots"
            generator = model_root / repo_slug / generator_rel
            csv_path = model_root / repo_slug / csv_rel
            minima_path = model_root / repo_slug / minima_rel
            generator.parent.mkdir(parents=True)
            csv_path.parent.mkdir(parents=True)
            minima_path.parent.mkdir(parents=True, exist_ok=True)
            generator.write_text(
                "import argparse\nfrom pathlib import Path\np=argparse.ArgumentParser()\np.add_argument('--csv')\np.add_argument('--minima')\np.add_argument('--out-dir')\na=p.parse_args()\no=Path(a.out_dir)\no.mkdir(parents=True,exist_ok=True)\n(o/'fixed_speed_xe131_dsigma_450kev.svg').write_bytes(b'<svg>cross</svg>')\n(o/'xe131_gcn_jj55_response_ratio_450kev.svg').write_bytes(b'<svg>ratio</svg>')\n",
                encoding="utf-8",
            )
            csv_path.write_text("ER_keV,value\n1,2\n", encoding="utf-8")
            minima_path.write_text("ER_keV,value\n1,2\n", encoding="utf-8")
            golden_dir = golden_root / repo_slug / output_rel
            golden_dir.mkdir(parents=True)
            golden_cross = golden_dir / "fixed_speed_xe131_dsigma_450kev.svg"
            golden_ratio = golden_dir / "xe131_gcn_jj55_response_ratio_450kev.svg"
            golden_cross.write_bytes(b"<svg>cross</svg>")
            golden_ratio.write_bytes(b"<svg>ratio</svg>")

            def identity(path):
                data = path.read_bytes()
                return {"git_blob_sha1": evaluate.git_blob_sha1(data), "size_bytes": len(data)}

            evaluator_manifest = {
                "deterministic_evaluators": [{
                    "id": "E-T05B-DATA-TO-FIGURE",
                    "repository": "owner/" + repo_slug,
                    "generator": {"path": generator_rel, **identity(generator)},
                    "model_visible_inputs": [
                        {"path": csv_rel, **identity(csv_path)},
                        {"path": minima_rel, **identity(minima_path)},
                    ],
                    "evaluator_only_reference_outputs": [
                        {"path": output_rel + "/" + golden_cross.name, **identity(golden_cross)},
                        {"path": output_rel + "/" + golden_ratio.name, **identity(golden_ratio)},
                    ],
                }]
            }
            manifest_path = root / "evaluator-manifest.json"
            manifest_path.write_text(json.dumps(evaluator_manifest), encoding="utf-8")
            result = verify_figure_regeneration.verify_figure_regeneration(manifest_path, model_root, golden_root)
            self.assertEqual(result["status"], "PASS")
            self.assertTrue(result["trusted_pinned_source_executed"])
            self.assertFalse(result["model_generated_code_executed"])

    def test_pinned_figure_generator_rejects_input_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.py"
            source.write_text("print('x')\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Size mismatch"):
                verify_figure_regeneration.verify_identity(source, "0" * 40, 1)


    def test_hard_gate_disagreement_requires_adjudication(self):
        record = make_record("no-skill", "run-a")
        record["evaluation"]["reviewer_assessments"][1]["hard_gates"]["critical_physics_error"] = "fail"
        with self.assertRaisesRegex(evaluate.EvaluationError, "third-party adjudication"):
            evaluate.validate_run(record, SCHEMA, RUBRIC)

    def test_final_hard_gates_must_match_unanimous_reviewers(self):
        record = make_record("no-skill", "run-a")
        record["evaluation"]["hard_gates"]["critical_physics_error"] = "fail"
        with self.assertRaisesRegex(evaluate.EvaluationError, "final hard gates differ"):
            evaluate.validate_run(record, SCHEMA, RUBRIC)

    def test_artifact_hash_verification_passes(self):
        record = make_record("no-skill", "run-a")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for artifact in record["artifacts"]:
                path = root / artifact["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                data = ("artifact:" + artifact["path"]).encode("utf-8")
                path.write_bytes(data)
                artifact["sha256"] = hashlib.sha256(data).hexdigest()
            score = evaluate.validate_run(record, SCHEMA, RUBRIC, artifact_root=root)
            self.assertEqual(score, 75.0)

    def test_artifact_hash_mismatch_rejected(self):
        record = make_record("no-skill", "run-a")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = record["artifacts"][0]
            path = root / artifact["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"tampered")
            with self.assertRaisesRegex(evaluate.EvaluationError, "Artifact SHA-256 mismatch"):
                evaluate.validate_run(record, SCHEMA, RUBRIC, artifact_root=root)

    def test_artifact_path_escape_rejected(self):
        record = make_record("no-skill", "run-a")
        record["artifacts"][0]["path"] = "../outside.txt"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(evaluate.EvaluationError, "escapes artifact root"):
                evaluate.verify_run_artifacts(record, Path(tmp))

    def test_task_source_bundle_must_match_manifest_and_staged_bytes(self):
        record = make_record("no-skill", "run-a")
        data = b"pinned source bytes\n"
        source = {
            "repository": "owner/repo",
            "commit": "f" * 40,
            "path": "data/input.csv",
            "git_blob_sha1": evaluate.git_blob_sha1(data),
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        record["task_input"]["source_commit"] = "f" * 40
        record["task_input"]["source_files"] = [source]
        task = {"id": "T-test", "input_sources": [{
            "repository": "owner/repo",
            "commit": "f" * 40,
            "path": "data/input.csv",
            "staged_path": "repo/data/input.csv",
            "git_blob_sha1": source["git_blob_sha1"],
            "size_bytes": len(data),
        }]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "repo" / "data" / "input.csv"
            path.parent.mkdir(parents=True)
            path.write_bytes(data)
            verified = evaluate.validate_task_source_bundle(record, task, root)
            self.assertEqual(verified[0]["sha256"], source["sha256"])
            task["input_sources"][0]["git_blob_sha1"] = "0" * 40
            with self.assertRaisesRegex(evaluate.EvaluationError, "source identity differs"):
                evaluate.validate_task_source_bundle(record, task, root)


    def test_pinned_figure_generator_preserves_and_reports_golden_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model_root = root / "model-inputs"
            golden_root = root / "golden"
            generated_root = root / "generated"
            repo_slug = "LZ-3-body-for-hdm"
            generator_rel = "research/three_body_calculation_and_validation/plot_user_dsigma_curve.py"
            csv_rel = "research/three_body_calculation_and_validation/results/fixed_speed_xe131_dsigma_450kev.csv"
            minima_rel = "research/three_body_calculation_and_validation/results/local_minima_refinement_1keV.csv"
            output_rel = "research/three_body_calculation_and_validation/results/plots"
            generator = model_root / repo_slug / generator_rel
            csv_path = model_root / repo_slug / csv_rel
            minima_path = model_root / repo_slug / minima_rel
            generator.parent.mkdir(parents=True)
            csv_path.parent.mkdir(parents=True)
            minima_path.parent.mkdir(parents=True, exist_ok=True)
            generator.write_text(
                "import argparse\nfrom pathlib import Path\np=argparse.ArgumentParser()\np.add_argument('--csv')\np.add_argument('--minima')\np.add_argument('--out-dir')\na=p.parse_args()\no=Path(a.out_dir)\no.mkdir(parents=True,exist_ok=True)\n(o/'fixed_speed_xe131_dsigma_450kev.svg').write_bytes(b'<svg>generated</svg>')\n(o/'xe131_gcn_jj55_response_ratio_450kev.svg').write_bytes(b'<svg>ratio</svg>')\n",
                encoding="utf-8",
            )
            csv_path.write_text("ER_keV,value\n1,2\n", encoding="utf-8")
            minima_path.write_text("ER_keV,value\n1,2\n", encoding="utf-8")
            golden_dir = golden_root / repo_slug / output_rel
            golden_dir.mkdir(parents=True)
            (golden_dir / "fixed_speed_xe131_dsigma_450kev.svg").write_bytes(b"<svg>archived</svg>")
            (golden_dir / "xe131_gcn_jj55_response_ratio_450kev.svg").write_bytes(b"<svg>ratio</svg>")

            def identity(path):
                data = path.read_bytes()
                return {"git_blob_sha1": evaluate.git_blob_sha1(data), "size_bytes": len(data)}

            evaluator_manifest = {
                "deterministic_evaluators": [{
                    "id": "E-T05B-DATA-TO-FIGURE",
                    "repository": "owner/" + repo_slug,
                    "generator": {"path": generator_rel, **identity(generator)},
                    "model_visible_inputs": [
                        {"path": csv_rel, **identity(csv_path)},
                        {"path": minima_rel, **identity(minima_path)},
                    ],
                    "evaluator_only_reference_outputs": [
                        {"path": output_rel + "/fixed_speed_xe131_dsigma_450kev.svg", **identity(golden_dir / "fixed_speed_xe131_dsigma_450kev.svg")},
                        {"path": output_rel + "/xe131_gcn_jj55_response_ratio_450kev.svg", **identity(golden_dir / "xe131_gcn_jj55_response_ratio_450kev.svg")},
                    ],
                }]
            }
            manifest_path = root / "evaluator-manifest.json"
            manifest_path.write_text(json.dumps(evaluator_manifest), encoding="utf-8")
            result = verify_figure_regeneration.verify_figure_regeneration(
                manifest_path, model_root, golden_root, generated_output_root=generated_root
            )
            self.assertEqual(result["status"], "FAIL")
            self.assertFalse(result["semantic_golden_match"])
            self.assertIn("SVG text mismatch", result["semantic_checks"][0]["error"])
            self.assertTrue((generated_root / "fixed_speed_xe131_dsigma_450kev.svg").is_file())
            self.assertEqual(
                result["historical_serialization_differences"][0],
                "fixed_speed_xe131_dsigma_450kev.svg",
            )


if __name__ == "__main__":
    unittest.main()
