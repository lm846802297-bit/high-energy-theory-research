import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_project_records import validate_project_records


class ProjectRecordValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.records = self.root / "records"
        self.schemas = self.root / "schemas"
        self.records.mkdir()
        self.schemas.mkdir()
        self._write_schema(
            "task",
            required=[
                "record_type", "project_id", "task_id", "task_status",
                "dependency_task_ids", "claim_ids", "completion_evidence_ids",
                "status_reason",
            ],
            properties={
                "record_type": {"const": "task"},
                "project_id": {"type": "string"},
                "task_id": {"type": "string"},
                "task_status": {
                    "type": "string",
                    "enum": [
                        "queued", "blocked", "in_progress", "needs_review",
                        "needs_revision", "complete", "not_applicable", "cancelled",
                    ],
                },
                "dependency_task_ids": {"type": "array", "items": {"type": "string"}},
                "claim_ids": {"type": "array", "items": {"type": "string"}},
                "completion_evidence_ids": {"type": "array", "items": {"type": "string"}},
                "status_reason": {"type": ["string", "null"]},
            },
        )
        self._write_schema(
            "source",
            required=["record_type", "project_id", "source_id", "uri_or_path"],
            properties={
                "record_type": {"const": "source"},
                "project_id": {"type": "string"},
                "source_id": {"type": "string"},
                "uri_or_path": {"type": "string"},
            },
        )

    def tearDown(self):
        self.temp.cleanup()

    def _write_schema(self, name, required, properties):
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "additionalProperties": False,
            "required": required,
            "properties": properties,
        }
        (self.schemas / f"{name}.schema.json").write_text(
            json.dumps(schema), encoding="utf-8"
        )

    def _write_json(self, name, record):
        path = self.records / name
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def _task(self, **updates):
        record = {
            "record_type": "task",
            "project_id": "PROJECT-001",
            "task_id": "TASK-001",
            "task_status": "queued",
            "dependency_task_ids": [],
            "claim_ids": [],
            "completion_evidence_ids": [],
            "status_reason": None,
        }
        record.update(updates)
        return record

    def _validate(self):
        return validate_project_records(self.records, self.root, self.schemas)

    def test_valid_json_and_yaml_records_pass(self):
        self._write_json("task.json", self._task())
        (self.records / "source.yaml").write_text(
            "record_type: source\n"
            "project_id: PROJECT-001\n"
            "source_id: SRC-001\n"
            "uri_or_path: https://example.org/paper.pdf\n",
            encoding="utf-8",
        )
        report = self._validate()
        self.assertEqual(report["summary"]["errors"], 0, report["errors"])

    def test_missing_foreign_key_is_reported(self):
        self._write_json("task.json", self._task(dependency_task_ids=["TASK-MISSING"]))
        report = self._validate()
        self.assertTrue(any(e["code"] == "REF_TARGET_MISSING" for e in report["errors"]))

    def test_primary_ids_must_be_unique_across_record_types(self):
        self._write_json("task.json", self._task(task_id="SHARED-001"))
        self._write_json(
            "source.json",
            {
                "record_type": "source",
                "project_id": "PROJECT-001",
                "source_id": "SHARED-001",
                "uri_or_path": "https://example.org/paper.pdf",
            },
        )
        report = self._validate()
        self.assertTrue(
            any(e["code"] == "DUPLICATE_ID_ACROSS_TYPES" for e in report["errors"]),
            report["errors"],
        )

    def test_not_applicable_requires_a_reason(self):
        self._write_json(
            "task.json",
            self._task(task_status="not_applicable", status_reason="  "),
        )
        report = self._validate()
        self.assertTrue(
            any(e["code"] == "NOT_APPLICABLE_REASON_REQUIRED" for e in report["errors"]),
            report["errors"],
        )

    def test_missing_local_source_path_is_reported(self):
        self._write_json(
            "source.json",
            {
                "record_type": "source",
                "project_id": "PROJECT-001",
                "source_id": "SRC-001",
                "uri_or_path": "sources/missing-paper.pdf",
            },
        )
        report = self._validate()
        self.assertTrue(any(e["code"] == "LOCAL_PATH_MISSING" for e in report["errors"]))

    def test_existing_local_source_path_passes(self):
        (self.root / "sources").mkdir()
        (self.root / "sources" / "paper.pdf").write_bytes(b"fixture")
        self._write_json(
            "source.json",
            {
                "record_type": "source",
                "project_id": "PROJECT-001",
                "source_id": "SRC-001",
                "uri_or_path": "sources/paper.pdf",
            },
        )
        report = self._validate()
        self.assertEqual(report["summary"]["errors"], 0, report["errors"])

    def test_invalid_status_is_rejected_by_schema(self):
        self._write_json("task.json", self._task(task_status="finished"))
        report = self._validate()
        self.assertTrue(any(e["code"] == "SCHEMA_INVALID" for e in report["errors"]))

    def test_duplicate_yaml_keys_are_rejected(self):
        (self.records / "bad.yaml").write_text(
            "record_type: task\n"
            "project_id: PROJECT-001\n"
            "task_id: TASK-001\n"
            "task_id: TASK-002\n"
            "task_status: queued\n"
            "dependency_task_ids: []\n"
            "claim_ids: []\n"
            "completion_evidence_ids: []\n"
            "status_reason: null\n",
            encoding="utf-8",
        )
        report = self._validate()
        self.assertTrue(any(e["code"] == "RECORD_PARSE_ERROR" for e in report["errors"]))
        self.assertTrue(any("duplicate key" in e.get("message", "") for e in report["errors"]))


if __name__ == "__main__":
    unittest.main()
