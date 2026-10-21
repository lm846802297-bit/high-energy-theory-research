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
            self.assertEqual(summary["record_validation"]["summary"]["errors"], 0, summary)
            self.assertEqual(summary["fingerprint_validation"], "passed")
            self.assertGreaterEqual(summary["record_count"], 19)

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
            self.assertEqual(len(by_type["artifact"]), 1)
            self.assertEqual(claim["artifact_ids"], [by_type["artifact"][0]["artifact_id"]])
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


if __name__ == "__main__":
    unittest.main()

