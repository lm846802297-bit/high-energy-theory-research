"""Regression tests for the v1.0.1 pull-request execution provenance extension."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "research-result-record-v1.0.1.schema.json"


def manifest():
    return {
        "schema_version": "1.0.1",
        "record_type": "run_manifest",
        "run_id": "RCRPS-PR-TEST-001",
        "created_at": "2026-11-22T00:00:00Z",
        "project": {"repository": "example/research", "project_id": "provenance-test"},
        "source": {
            "commit_sha": "a" * 40,
            "branch": "feature/test",
            "script_path": "run.py",
            "script_sha256": "b" * 64,
        },
        "inputs": [],
        "configuration": {"physics": {}, "numerics": {}, "conventions": {}},
        "environment": {
            "platform": "Linux",
            "runtime": {"python": "3.11.18"},
            "dependencies": {},
            "hardware": {"cpu_model": "test"},
        },
        "execution": {
            "status": "succeeded",
            "command": "python run.py",
            "started_at": "2026-11-22T00:00:00Z",
            "finished_at": "2026-11-22T00:00:01Z",
        },
        "outputs": [],
        "validation": {"status": "not_run", "checks": []},
        "archive": {"status": "local_only"},
    }


class PullRequestExecutionProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open("r", encoding="utf-8") as stream:
            cls.schema = json.load(stream)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(
            cls.schema, format_checker=FormatChecker()
        )

    def test_local_execution_does_not_require_pull_request_fields(self):
        record = manifest()
        record["execution"]["source_control"] = {"event": "local"}
        self.assertTrue(self.validator.is_valid(record))

    def test_pull_request_requires_head_base_and_tested_merge_shas(self):
        record = manifest()
        record["execution"]["source_control"] = {
            "event": "pull_request",
            "pr_number": 104,
            "pr_url": "https://github.com/example/research/pull/104",
            "pr_head_sha": "c" * 40,
            "base_sha": "d" * 40,
            "tested_merge_sha": "e" * 40,
            "workflow_run_id": 123456,
            "workflow_run_attempt": 1,
        }
        self.assertTrue(self.validator.is_valid(record))

    def test_pull_request_rejects_missing_tested_merge_sha(self):
        record = manifest()
        record["execution"]["source_control"] = {
            "event": "pull_request",
            "pr_number": 104,
            "pr_head_sha": "c" * 40,
            "base_sha": "d" * 40,
        }
        self.assertFalse(self.validator.is_valid(record))

    def test_pull_request_rejects_malformed_commit_shas(self):
        record = manifest()
        record["execution"]["source_control"] = {
            "event": "pull_request",
            "pr_number": 104,
            "pr_head_sha": "not-a-sha",
            "base_sha": "d" * 40,
            "tested_merge_sha": "e" * 40,
        }
        self.assertFalse(self.validator.is_valid(record))


if __name__ == "__main__":
    unittest.main()
