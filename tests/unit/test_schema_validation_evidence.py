import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schema" / "v1.4.3.7"
MANIFEST_PATH = SCHEMA_ROOT / "manifest.json"
TRACE_PATH = SCHEMA_ROOT / "audit" / "requirement-test-trace.csv"
REPORT_PATH = SCHEMA_ROOT / "audit" / "validation-report.json"
VALIDATOR_PATH = SCHEMA_ROOT / "tools" / "schema-v1.4.3.6-validate.py"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "schema-validation.yml"
MIGRATION_PATH = SCHEMA_ROOT / "migrations" / "v1.3-to-v1.4-mapping.json"


class SchemaValidationEvidenceTests(unittest.TestCase):
    def test_manifest_traceability_counts_match_the_csv(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        with TRACE_PATH.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))

        self.assertEqual(len(rows), manifest["requirement_traceability_rows"])
        self.assertEqual(len(rows), manifest["release_evidence"]["traceability_rows"])
        self.assertIn("Runtime-generated", manifest["release_evidence"]["traceability"])

    def test_candidate_and_migration_safety_states_remain_explicit(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        migration = json.loads(MIGRATION_PATH.read_text(encoding="utf-8"))

        self.assertEqual(manifest["bundle_status"], "candidate")
        self.assertEqual(manifest["release_status"], "not_released")
        self.assertFalse(migration["commit_allowed"])
        self.assertTrue(migration["staging_only"])
        self.assertEqual(migration["compatibility_status"], "unverified")

    def test_validator_emits_run_scoped_provenance_and_count_checks(self):
        validator = VALIDATOR_PATH.read_text(encoding="utf-8")
        for token in (
            "candidate_release_status",
            "manifest_traceability_row_count_matches",
            "manifest_release_evidence_traceability_rows_matches",
            "validated_commit_sha",
            "workflow_run_id",
            "generated_at_utc",
            "validator_sha256",
            "manifest_sha256",
            "traceability_csv_sha256",
            "execution_environment",
        ):
            with self.subTest(token=token):
                self.assertIn(token, validator)

    def test_checked_in_report_is_not_misrepresented_as_current_evidence(self):
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        provenance = report.get("provenance", {})
        status = provenance.get("validation_status")

        if status == "historical_snapshot_not_current_head":
            self.assertIn("historical_snapshot", report)
            self.assertIsNone(provenance.get("validated_commit_sha"))
            self.assertEqual(report["summary"]["validation_status"], "not_run_for_current_head")
        else:
            self.assertIn(status, {"passed", "failed"})
            self.assertTrue(provenance.get("validated_commit_sha"))
            self.assertTrue(provenance.get("workflow_run_id"))
            self.assertTrue(provenance.get("validator_sha256"))

    def test_schema_ci_does_not_execute_the_physics_pilot(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("Remove historical validation report", workflow)
        self.assertIn("Verify generated evidence provenance", workflow)
        self.assertIn("ref: ${{ github.event.pull_request.head.sha || github.sha }}", workflow)
        self.assertIn("report workflow_run_id does not match this Actions run", workflow)
        self.assertIn("report workflow_run_attempt does not match this Actions attempt", workflow)
        self.assertIn("report validator_sha256 does not match the checked validator", workflow)
        self.assertIn("candidate-schema-validation-report", workflow)
        self.assertNotIn("run_record_chain.py", workflow)
        self.assertNotIn("verify_pv_derivative_mathematica.wl", workflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
