from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import evaluate
import verify_dirac_trace
import verify_repro_package

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
        "execution": {"randomization_seed": "seed-1", "pair_order": "A_then_B", "actual_wall_time_seconds": 60, "actual_tool_calls": 5, "token_count": 1000, "commands": ["python task.py"], "tool_log_artifact": "logs/tool.json", "transcript_artifact": f"transcripts/{run_id}.json", "exit_status": 0},
        "skill": {
            "available": available,
            "source_commit": "9" * 40 if available else None,
            "manifest_sha256": "a" * 64 if available else None,
            "invocation": "$high-energy-theory-research" if available else None,
            "references_loaded": ["references/symbolic-calculation.md"] if available else [],
            "availability_evidence_artifact": f"evidence/{run_id}-skill.json",
        },
        "artifacts": [
            {"path": "logs/tool.json", "sha256": "5" * 64, "role": "tool_log"},
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


if __name__ == "__main__":
    unittest.main()
