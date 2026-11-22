"""Regression tests for the structured research-result validator."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCHEMA_DIR))
from validate_result_records import load_json, verify_revision_context, verify_source  # noqa: E402

SCHEMA_PATH = SCHEMA_DIR / "research-result-record-v1.0.1.schema.json"


def minimal_manifest(input_record: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "record_type": "run_manifest",
        "run_id": "TEST-RUN-001",
        "created_at": "2026-11-21T00:00:00Z",
        "project": {"repository": "example/research", "project_id": "validator-test"},
        "source": {"commit_sha": "a" * 40, "script_path": "run.py", "script_sha256": "c" * 64},
        "inputs": [input_record],
        "configuration": {"physics": {}, "numerics": {}, "conventions": {}},
        "environment": {"platform": "Linux", "runtime": {"python": "3.x"}, "dependencies": {}, "hardware": {"cpu": "test"}},
        "execution": {
            "status": "succeeded",
            "command": "python run.py",
            "started_at": "2026-11-21T00:00:00Z",
            "finished_at": "2026-11-21T00:00:01Z",
        },
        "outputs": [],
        "validation": {"status": "not_run", "checks": []},
        "archive": {"status": "local_only"},
    }


class StrictJsonNumberTests(unittest.TestCase):
    def load_text(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(text, encoding="utf-8")
            return load_json(path)

    def test_rejects_nonstandard_constants(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token), self.assertRaises(ValueError):
                self.load_text('{"value": ' + token + '}')

    def test_rejects_float_overflow(self):
        with self.assertRaisesRegex(ValueError, "overflows"):
            self.load_text('{"value": 1e9999}')

    def test_rejects_float_underflow_to_zero(self):
        with self.assertRaisesRegex(ValueError, "underflows"):
            self.load_text('{"value": 1e-9999}')

    def test_accepts_finite_float(self):
        self.assertEqual(self.load_text('{"value": 1.25e-4}')["value"], 1.25e-4)


class InputProvenanceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open("r", encoding="utf-8") as stream:
            cls.schema = json.load(stream)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def valid(self, input_record: dict) -> bool:
        return self.validator.is_valid(minimal_manifest(input_record))

    def test_local_input_requires_path_and_sha256(self):
        self.assertTrue(self.valid({
            "name": "local-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
            "sha256": "b" * 64,
        }))

    def test_external_input_requires_immutable_uri_and_version(self):
        self.assertTrue(self.valid({
            "name": "external-table",
            "source": "external dataset",
            "format": "csv",
            "uri": "https://example.org/data.csv",
            "version": "v1",
        }))

    def test_hash_without_locator_is_rejected(self):
        self.assertFalse(self.valid({
            "name": "unlocatable-table",
            "source": "unknown",
            "format": "csv",
            "sha256": "b" * 64,
        }))

    def test_path_without_hash_is_rejected(self):
        self.assertFalse(self.valid({
            "name": "unhashed-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
        }))

    def test_empty_path_is_rejected(self):
        self.assertFalse(self.valid({
            "name": "empty-path",
            "source": "repository input",
            "format": "csv",
            "path": "",
            "sha256": "b" * 64,
        }))

    def test_uri_without_version_is_rejected(self):
        self.assertFalse(self.valid({
            "name": "unversioned-external-table",
            "source": "external dataset",
            "format": "csv",
            "uri": "https://example.org/data.csv",
        }))

    def test_invalid_uri_is_rejected(self):
        self.assertFalse(self.valid({
            "name": "invalid-uri",
            "source": "external dataset",
            "format": "csv",
            "uri": "not-a-uri",
            "version": "v1",
        }))

    def test_script_fingerprint_is_required(self):
        record = minimal_manifest({
            "name": "local-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
            "sha256": "b" * 64,
        })
        record["source"].pop("script_sha256")
        self.assertFalse(self.validator.is_valid(record))

    def test_dependencies_are_required(self):
        record = minimal_manifest({
            "name": "local-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
            "sha256": "b" * 64,
        })
        record["environment"].pop("dependencies")
        self.assertFalse(self.validator.is_valid(record))

    def test_hardware_is_required(self):
        record = minimal_manifest({
            "name": "local-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
            "sha256": "b" * 64,
        })
        record["environment"].pop("hardware")
        self.assertFalse(self.validator.is_valid(record))


class RevisionContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open("r", encoding="utf-8") as stream:
            cls.schema = json.load(stream)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def manifest(self, *, event="pull_request", mode="pull_request_merge"):
        record = minimal_manifest({
            "name": "local-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
            "sha256": "b" * 64,
        })
        record["schema_version"] = "1.0.1"
        record["source"]["branch"] = "feature/archive-provenance"
        record["source"]["revision_context"] = {
            "event_name": event,
            "checked_out_sha": "a" * 40,
            "pr_number": 104 if event in {"pull_request", "pull_request_target"} else None,
            "pr_head_sha": "b" * 40 if event in {"pull_request", "pull_request_target"} else None,
            "base_sha": "c" * 40 if event in {"pull_request", "pull_request_target"} else None,
            "tested_merge_sha": "a" * 40 if mode == "pull_request_merge" else None,
            "head_ref": "feature/archive-provenance" if event in {"pull_request", "pull_request_target"} else "main",
            "base_ref": "main" if event in {"pull_request", "pull_request_target"} else None,
            "checkout_mode": mode,
        }
        if event not in {"pull_request", "pull_request_target"}:
            record["source"]["branch"] = "main"
        return record

    def test_v101_pull_request_merge_context_is_valid(self):
        record = self.manifest()
        self.assertTrue(self.validator.is_valid(record))
        self.assertEqual(verify_revision_context(record), [])

    def test_v101_pull_request_head_checkout_is_valid(self):
        record = self.manifest(mode="pull_request_head")
        context = record["source"]["revision_context"]
        context["checked_out_sha"] = context["pr_head_sha"]
        record["source"]["commit_sha"] = context["pr_head_sha"]
        self.assertTrue(self.validator.is_valid(record))
        self.assertEqual(verify_revision_context(record), [])

    def test_v101_local_context_is_valid(self):
        record = self.manifest(event="local", mode="branch_commit")
        self.assertTrue(self.validator.is_valid(record))
        self.assertEqual(verify_revision_context(record), [])

    def test_v101_requires_revision_context(self):
        record = self.manifest()
        record["source"].pop("revision_context")
        self.assertFalse(self.validator.is_valid(record))

    def test_merge_sha_must_equal_checked_out_sha(self):
        record = self.manifest()
        record["source"]["revision_context"]["tested_merge_sha"] = "d" * 40
        self.assertTrue(self.validator.is_valid(record))
        self.assertTrue(any("tested_merge_sha" in error for error in verify_revision_context(record)))

    def test_pr_branch_must_not_be_the_synthetic_merge_ref(self):
        record = self.manifest()
        record["source"]["branch"] = "104/merge"
        self.assertTrue(self.validator.is_valid(record))
        self.assertTrue(any("head_ref" in error for error in verify_revision_context(record)))

    def test_v100_manifest_remains_valid_without_revision_context(self):
        record = minimal_manifest({
            "name": "local-table",
            "source": "repository input",
            "format": "csv",
            "path": "data/input.csv",
            "sha256": "b" * 64,
        })
        self.assertTrue(self.validator.is_valid(record))
        self.assertEqual(verify_revision_context(record), [])

    def test_source_script_fingerprint_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "run.py"
            script.write_text("print('original')\n", encoding="utf-8")
            record = {
                "record_type": "run_manifest",
                "source": {
                    "script_path": "run.py",
                    "script_sha256": __import__("hashlib").sha256(script.read_bytes()).hexdigest(),
                },
            }
            self.assertEqual(verify_source(record, root), [])
            script.write_text("print('modified')\n", encoding="utf-8")
            self.assertTrue(verify_source(record, root))


if __name__ == "__main__":
    unittest.main()
