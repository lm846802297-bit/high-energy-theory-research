from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCHEMA_DIR))
from validate_result_records import verify_source_control  # noqa: E402
from rcrps_v1_0_1_fixtures import minimal_manifest  # noqa: E402


class SourceControlSemanticTests(unittest.TestCase):
    def errors(self, record: dict) -> list[str]:
        return verify_source_control(record)

    def test_valid_pr_merge_checkout(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_merge")
        self.assertEqual(self.errors(record), [])

    def test_merge_checkout_sha_must_equal_source_commit(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_merge")
        record["execution"]["source_control"]["tested_merge_sha"] = "e" * 40
        self.assertTrue(any("tested_merge_sha" in error for error in self.errors(record)))

    def test_valid_pr_head_checkout(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_head")
        self.assertEqual(self.errors(record), [])

    def test_head_checkout_sha_must_equal_pr_head(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_head")
        record["source"]["commit_sha"] = "e" * 40
        self.assertTrue(any("pr_head_sha" in error for error in self.errors(record)))

    def test_head_checkout_rejects_tested_merge_sha(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_head")
        record["execution"]["source_control"]["tested_merge_sha"] = "e" * 40
        self.assertTrue(any("tested_merge_sha" in error for error in self.errors(record)))

    def test_valid_pr_base_checkout(self):
        record = minimal_manifest(event="pull_request_target", mode="pull_request_base")
        self.assertEqual(self.errors(record), [])

    def test_pr_base_checkout_requires_base_sha(self):
        record = minimal_manifest(event="pull_request_target", mode="pull_request_base")
        record["source"]["commit_sha"] = "e" * 40
        self.assertTrue(any("base_sha" in error for error in self.errors(record)))

    def test_valid_unknown_pr_checkout(self):
        record = minimal_manifest(event="pull_request", mode="unknown")
        self.assertEqual(self.errors(record), [])

    def test_unknown_pr_checkout_rejects_tested_merge_sha(self):
        record = minimal_manifest(event="pull_request", mode="unknown")
        record["execution"]["source_control"]["tested_merge_sha"] = "e" * 40
        self.assertTrue(any("tested_merge_sha" in error for error in self.errors(record)))

    def test_non_pr_events_accept_explicit_null_pr_fields(self):
        for event in ("local", "push", "workflow_dispatch", "schedule", "workflow_run"):
            with self.subTest(event=event):
                record = minimal_manifest(event=event, mode="branch_commit")
                self.assertEqual(self.errors(record), [])

    def test_non_pr_rejects_non_null_pr_fields(self):
        values = {
            "pr_number": 104,
            "pr_url": "https://github.com/example/research/pull/104",
            "pr_head_sha": "b" * 40,
            "base_sha": "c" * 40,
            "tested_merge_sha": "a" * 40,
            "head_ref": "feature/example",
            "base_ref": "main",
        }
        for field, value in values.items():
            with self.subTest(field=field):
                record = minimal_manifest()
                record["execution"]["source_control"][field] = value
                self.assertTrue(self.errors(record), field)

    def test_pr_checkout_mode_rejected_for_non_pr(self):
        record = minimal_manifest()
        record["execution"]["source_control"]["checkout_mode"] = "pull_request_head"
        self.assertTrue(any("checkout_mode" in error for error in self.errors(record)))

    def test_non_pr_checkout_mode_rejected_for_pr(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_merge")
        record["execution"]["source_control"]["checkout_mode"] = "branch_commit"
        self.assertTrue(any("checkout_mode" in error for error in self.errors(record)))

    def test_workflow_run_id_and_attempt_must_be_paired(self):
        record = minimal_manifest()
        record["execution"]["source_control"]["workflow_run_id"] = 123
        self.assertTrue(any("workflow_run_id" in error for error in self.errors(record)))
        record = minimal_manifest()
        record["execution"]["source_control"]["workflow_run_attempt"] = 1
        self.assertTrue(any("workflow_run_attempt" in error for error in self.errors(record)))

    def test_clean_tree_requires_empty_dirty_paths(self):
        record = minimal_manifest()
        record["execution"]["source_control"]["dirty_paths"] = ["src/model.py"]
        self.assertTrue(any("clean" in error for error in self.errors(record)))

    def test_dirty_tree_requires_paths(self):
        record = minimal_manifest()
        record["execution"]["source_control"]["working_tree_state"] = "dirty"
        self.assertTrue(any("dirty" in error for error in self.errors(record)))

    def test_dirty_paths_must_be_safe_and_unique(self):
        for paths in (["/etc/passwd"], ["../escape.py"], ["src\\model.py"], ["./src/model.py"], ["src//model.py"], ["src/model.py", "src/model.py"]):
            with self.subTest(paths=paths):
                record = minimal_manifest()
                record["execution"]["source_control"]["working_tree_state"] = "dirty"
                record["execution"]["source_control"]["dirty_paths"] = list(paths)
                self.assertTrue(self.errors(record))

    def test_v100_manifest_bypasses_source_control_semantics(self):
        record = minimal_manifest(version="1.0.0")
        record["execution"].pop("source_control", None)
        self.assertEqual(self.errors(record), [])

    def test_source_branch_is_not_misread_as_checkout_ref(self):
        record = minimal_manifest(event="pull_request", mode="pull_request_merge")
        record["source"]["branch"] = "104/merge"
        self.assertEqual(self.errors(record), [])


if __name__ == "__main__":
    unittest.main()
