import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = ROOT / "tests" / "eval-cases" / "uv-eFT-hard-derivative-pilot"
sys.path.insert(0, str(CASE_DIR))
from run_record_chain import build_bundle  # noqa: E402


class UVEFTHardDerivativePilotTests(unittest.TestCase):
    def test_real_physics_task_runs_and_builds_complete_record_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle_root = Path(tmp) / "bundle"
            summary = build_bundle(bundle_root)
            self.assertTrue(summary["physics_checks"]["all_checks_passed"], summary)
            mathematica_script = bundle_root / "tests/eval-cases/uv-eFT-hard-derivative-pilot/verify_pv_derivative_mathematica.wl"
            self.assertTrue(mathematica_script.is_file())
            self.assertIn("Integrate[", mathematica_script.read_text(encoding="utf-8"))
            self.assertIn("expectedSecond", mathematica_script.read_text(encoding="utf-8"))
            self.assertEqual(summary["record_validation"]["errors"], 0, summary)
            self.assertEqual(summary["fingerprint_validation"], "passed")
            self.assertGreaterEqual(summary["record_count"], 21)

            chain = json.loads((bundle_root / "outputs" / "record-chain.json").read_text(encoding="utf-8"))
            by_type = {}
            for record in chain:
                by_type.setdefault(record["record_type"], []).append(record)
            claim = by_type["claim"][0]
            self.assertEqual(claim["claim_lifecycle_status"], "active")
            self.assertEqual(claim["evidence_status"]["theory"]["check_status"], "passed")
            self.assertEqual(len(by_type["source"]), 4)
            self.assertEqual(len(by_type["run_manifest"]), 1)
            self.assertEqual(len(by_type["validation_report"]), 1)
            self.assertEqual(len(by_type["artifact"]), 2)
            result_artifact = next(item for item in by_type["artifact"] if item["artifact_id"] == "ART-UV-EFT-RESULT-001")
            log_artifact = next(item for item in by_type["artifact"] if item["artifact_id"] == "ART-UV-EFT-LOG-001")
            self.assertEqual(claim["artifact_ids"], [result_artifact["artifact_id"]])
            run = by_type["run"][0]
            manifest = by_type["run_manifest"][0]
            self.assertEqual(run["log_artifact_ids"], [log_artifact["artifact_id"]])
            self.assertEqual(manifest["execution"]["log_artifact_ids"], [log_artifact["artifact_id"]])
            self.assertEqual(log_artifact["content_sha256"], summary["log_sha256"])
            validation_report = json.loads((bundle_root / "outputs" / "record-validation-report.json").read_text(encoding="utf-8"))
            self.assertEqual(validation_report["summary"]["errors"], 0)
            self.assertEqual(validation_report["summary"]["warnings"], 0)
            self.assertEqual(claim["validation_report_ids"], [by_type["validation_report"][0]["validation_report_id"]])
            self.assertIn("full UV diagram numerator", " ".join(claim["unresolved_items"]))

    def test_first_order_small_r_correction_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle_root = Path(tmp) / "bundle"
            summary = build_bundle(bundle_root)
            result = json.loads((bundle_root / "outputs" / "results.json").read_text(encoding="utf-8"))
            self.assertEqual(
                result["exact_coefficients"]["Fprime_hard_over_K_first_correction"],
                "4/3 - 2*L - 4*r*ln(r) - 16*r + O(r^2*ln(r))",
            )
            self.assertLess(
                result["summary"]["max_Fprime_absolute_error"],
                5e-9,
            )
            self.assertTrue(summary["physics_checks"]["checks"]["exact_rational_projection_factor_is_1_over_6"])

    def test_second_order_small_r_correction_is_recorded_and_residual_shrinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle_root = Path(tmp) / "bundle"
            summary = build_bundle(bundle_root)
            result = json.loads((bundle_root / "outputs" / "results.json").read_text(encoding="utf-8"))
            self.assertEqual(
                result["exact_coefficients"]["Fprime_hard_over_K_second_correction"],
                "4/3 - 2*L - 4*r*ln(r) - 16*r - 28*r^2*ln(r) - 32*r^2 + O(r^3*ln(r))",
            )
            checks = summary["physics_checks"]["checks"]
            self.assertTrue(checks["second_correction_residual_decreases"], summary)
            self.assertTrue(checks["second_order_scaled_residual_is_bounded_on_test_grid"], summary)
            self.assertLess(
                result["summary"]["max_scaled_second_order_residual"],
                70.0,
            )


if __name__ == "__main__":
    unittest.main()

