from __future__ import annotations

import unittest
from pathlib import Path

import evaluate_v1_3 as evaluate
from test_evaluate import make_record

ROOT = Path(__file__).resolve().parents[1]
V13 = ROOT / "protocol" / "v1.3"


class EvaluatorV13Tests(unittest.TestCase):
    def test_v13_environment_and_rubric_are_pinned(self):
        lock = evaluate.read_json(V13 / "environment-lock.json")
        self.assertEqual(lock["model"]["model_label"], "GPT-6")
        self.assertEqual(lock["model"]["reasoning_effort"], "Extra High")
        self.assertEqual(lock["skill_treatment"]["plugin_version"], "0.2.0")
        self.assertEqual(
            lock["skill_treatment"]["installation_manifest_sha256"],
            "0c2f09ca324cbc24d32b0be41efa07581ef73322df63ba567271df64d9e6dc0b",
        )
        weights = evaluate.read_rubric(V13 / "scoring-rubric.yaml")["weights"]
        self.assertEqual(weights, {
            "scientific_correctness": 0.35,
            "independent_validation": 0.25,
            "reproducibility": 0.20,
            "evidence_quality": 0.10,
            "efficiency": 0.10,
        })

    def test_v13_pair_validates_and_emits_v13_report(self):
        schema = V13 / "run-record.schema.json"
        rubric = V13 / "scoring-rubric.yaml"
        report_schema = V13 / "comparison-report.schema.json"
        evaluator_manifest = evaluate.read_json(V13 / "evaluator-manifest.json")
        a = make_record("no-skill", "v13-run-a")
        b = make_record("with-skill", "v13-run-b")
        for record in (a, b):
            record["protocol"]["version"] = "1.3"
            record["model"]["label"] = "GPT-6"
            record["model"]["reasoning_effort"] = "Extra High"
        tasks = {"tasks": [{
            "id": "T01",
            "dimension": "theoretical_derivation",
            "task_family": "threshold_kinematics",
            "skill_reference": "references/symbolic-calculation.md",
            "required_evaluators": [],
        }]}
        report = evaluate.compare_records(
            [a, b],
            tasks,
            "round_1_pilot",
            seed=20261124,
            schema_path=schema,
            rubric_path=rubric,
            evaluator_manifest=evaluator_manifest,
        )
        self.assertEqual(report["protocol_version"], "1.3")
        evaluate.validate_schema(report, report_schema)
        self.assertEqual(report["summary"]["paired_run_count"], 1)
        self.assertEqual(report["decision"], "inconclusive")

    def test_v13_evaluator_manifest_binds_actual_files(self):
        manifest = evaluate.read_json(V13 / "evaluator-manifest.json")
        for entry in manifest["evaluator_code"] + manifest["protocol_artifacts"]:
            path = ROOT / entry["path"]
            data = path.read_bytes()
            self.assertEqual(len(data), entry["size_bytes"], entry["path"])
            self.assertEqual(evaluate.git_blob_sha1(data), entry["git_blob_sha1"], entry["path"])

    def test_v12_evaluator_and_environment_lock_remain_unchanged(self):
        v12_lock = evaluate.read_json(ROOT / "protocol" / "environment-lock.json")
        self.assertEqual(v12_lock["model"]["model_label"], "GPT-6 Pro (Astra Pro)")
        self.assertEqual(
            v12_lock["model"]["reasoning_effort"],
            "Pro default; no separate numeric effort setting",
        )
        v12_manifest = evaluate.read_json(ROOT / "evaluators" / "manifest.json")
        entry = next(
            item for item in v12_manifest["evaluator_code"]
            if item["path"] == "evaluators/evaluate.py"
        )
        data = (ROOT / entry["path"]).read_bytes()
        self.assertEqual(len(data), entry["size_bytes"])
        self.assertEqual(evaluate.git_blob_sha1(data), entry["git_blob_sha1"])


if __name__ == "__main__":
    unittest.main()
