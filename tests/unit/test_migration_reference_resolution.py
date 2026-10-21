import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATION_PATH = ROOT / "schema" / "v1.4.3.7" / "tools" / "migrate_v1_3_to_v1_4.py"
SPEC = importlib.util.spec_from_file_location("migration_reference_resolution", MIGRATION_PATH)
migration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migration)


def claim_record(validation_ids):
    return {
        "schema_version": "1.3",
        "record_type": "claim",
        "project_id": "P-TEST",
        "claim_id": "CLAIM-TEST",
        "validation_ids": validation_ids,
    }


def activity_record(activity_id, status="succeeded", started_at="2026-10-21T00:00:00Z"):
    return {
        "schema_version": "1.3",
        "record_type": "validation_activity",
        "project_id": "P-TEST",
        "validation_activity_id": activity_id,
        "execution_status": status,
        "started_at": started_at,
    }


def plan_record(plan_id):
    return {
        "schema_version": "1.3",
        "record_type": "validation_plan",
        "project_id": "P-TEST",
        "validation_plan_id": plan_id,
    }


def make_index(*records):
    index = {}
    for record in records:
        index.setdefault((record.get("project_id"), migration.primary_key(record)), []).append(record)
    return index


class ValidationReferenceResolutionTests(unittest.TestCase):
    def test_started_activity_maps_to_validation_activity_ids(self):
        claim = claim_record(["VAL-ACT-1"])
        activity = activity_record("VAL-ACT-1")
        out, changes, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim, activity))
        self.assertEqual(out["validation_activity_ids"], ["VAL-ACT-1"])
        self.assertEqual(out["validation_plan_ids"], [])
        self.assertNotIn("validation_ids", out)
        self.assertEqual(unresolved, [])
        self.assertTrue(any(c.get("basis") == "source_record_type_and_launch_evidence" for c in changes))

    def test_empty_legacy_list_maps_to_empty_typed_lists(self):
        claim = claim_record([])
        out, changes, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim))
        self.assertEqual(out["validation_activity_ids"], [])
        self.assertEqual(out["validation_plan_ids"], [])
        self.assertNotIn("validation_ids", out)
        self.assertEqual(unresolved, [])
        self.assertTrue(any(c.get("basis") == "empty_legacy_reference_list" for c in changes))

    def test_plan_maps_to_validation_plan_ids(self):
        claim = claim_record(["VAL-PLAN-1"])
        plan = plan_record("VAL-PLAN-1")
        out, _, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim, plan))
        self.assertEqual(out["validation_plan_ids"], ["VAL-PLAN-1"])
        self.assertEqual(out["validation_activity_ids"], [])
        self.assertNotIn("validation_ids", out)
        self.assertEqual(unresolved, [])

    def test_not_started_activity_remains_unresolved(self):
        claim = claim_record(["VAL-NOT-RUN"])
        activity = activity_record("VAL-NOT-RUN", status="not_run", started_at=None)
        out, _, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim, activity))
        self.assertNotIn("validation_activity_ids", out)
        self.assertTrue(any(x["code"] == "VALIDATION_ACTIVITY_NOT_STARTED" for x in unresolved))

    def test_missing_reference_remains_unresolved(self):
        claim = claim_record(["VAL-MISSING"])
        out, _, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim))
        self.assertTrue(any(x["code"] == "VALIDATION_TARGET_NOT_FOUND" for x in unresolved))
        self.assertNotIn("validation_activity_ids", out)
        self.assertNotIn("validation_plan_ids", out)

    def test_duplicate_cross_type_id_remains_unresolved(self):
        claim = claim_record(["VAL-DUP"])
        activity = activity_record("VAL-DUP")
        plan = plan_record("VAL-DUP")
        out, _, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim, activity, plan))
        self.assertTrue(any(x["code"] == "VALIDATION_TARGET_ID_AMBIGUOUS" for x in unresolved))
        self.assertNotIn("validation_activity_ids", out)
        self.assertNotIn("validation_plan_ids", out)

    def test_source_graph_resolution_is_used_by_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "claim.json").write_text(json.dumps(claim_record(["VAL-ACT-1"])), encoding="utf-8")
            (root / "activity.json").write_text(json.dumps(activity_record("VAL-ACT-1")), encoding="utf-8")
            report = migration.migrate(root)
        self.assertEqual(report["source_count"], 2)
        self.assertEqual(report["unresolved"], [])
        self.assertFalse(report["commit_allowed"])


if __name__ == "__main__":
    unittest.main()
