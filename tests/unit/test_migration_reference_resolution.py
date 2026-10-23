import importlib.util
import json
import shutil
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
        self.assertTrue(any(item["code"] == "TARGET_SCHEMA_VALIDATION_FAILED" for item in report["unresolved"]))
        claim_mapping = next(item for item in report["id_mapping"] if item["source_record_type"] == "claim")
        self.assertEqual(claim_mapping["mapping_basis"], "unresolved")
        self.assertTrue(any(
            change.get("from") == "validation_ids"
            and change.get("basis") == "source_record_type_and_launch_evidence"
            for change in report["changes"]
        ))
        self.assertEqual(report["migratable_record_count"], 0)
        self.assertFalse(report["commit_allowed"])


    def test_activity_status_outside_v14_enum_is_unresolved(self):
        activity = activity_record("VAL-ACT-STATUS", status="in_progress")
        _, _, unresolved, _ = migration.migrate_record(activity)
        self.assertTrue(any(item["code"] == "TARGET_ENUM_VALUE_UNMAPPED" for item in unresolved))

    def test_invalid_started_at_does_not_resolve_validation_activity(self):
        claim = claim_record(["VAL-ACT-BAD-TIME"])
        activity = activity_record("VAL-ACT-BAD-TIME", status="succeeded", started_at="2026-10-21 00:00:00Z")
        _, _, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim, activity))
        self.assertTrue(any(item["code"] == "VALIDATION_ACTIVITY_LAUNCH_EVIDENCE_INSUFFICIENT" for item in unresolved))

    def test_in_progress_reference_requires_an_explicit_target_status_mapping(self):
        claim = claim_record(["VAL-ACT-IN-PROGRESS"])
        activity = activity_record("VAL-ACT-IN-PROGRESS", status="in_progress")
        _, _, unresolved, _ = migration.migrate_record(claim, source_index=make_index(claim, activity))
        self.assertTrue(any(item["code"] == "VALIDATION_ACTIVITY_STATUS_UNMAPPED" for item in unresolved))

    def test_missing_project_id_is_unresolved(self):
        claim = claim_record([])
        claim.pop("project_id")
        _, _, unresolved, _ = migration.migrate_record(claim)
        self.assertTrue(any(item["code"] == "MISSING_OR_INVALID_PROJECT_ID" for item in unresolved))

    def test_non_record_json_files_are_reported_not_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "array.json").write_text("[]", encoding="utf-8")
            (root / "missing-type.json").write_text(json.dumps({"schema_version": "1.3"}), encoding="utf-8")
            report = migration.migrate(root)
        self.assertEqual(report["source_count"], 2)
        self.assertEqual(report["source_files_skipped_count"], 2)
        codes = {item["code"] for item in report["unresolved"]}
        self.assertIn("SOURCE_RECORD_NOT_OBJECT", codes)
        self.assertIn("SOURCE_RECORD_TYPE_MISSING", codes)

    def test_incomplete_source_snapshot_blocks_all_staging_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            valid_record = json.loads(
                (ROOT / "schema" / "v1.4.3.7" / "tests" / "valid" / "task" / "FX-TASK-VALID-001.json").read_text(encoding="utf-8")
            )
            valid_record["schema_version"] = "1.3"
            (source / "task.json").write_text(json.dumps(valid_record), encoding="utf-8")
            (source / "broken.json").write_text("{ malformed", encoding="utf-8")
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True)
            target_files = [
                path for path in output.glob("*.json")
                if path.name != "migration-report.json"
            ]
        self.assertTrue(report["staging_blocked"])
        self.assertIn("SOURCE_FILES_SKIPPED", report["staging_blockers"])
        self.assertEqual(report["staging_written_record_count"], 0)
        self.assertEqual(target_files, [])
        self.assertFalse(report["commit_allowed"])

    def test_duplicate_typed_primary_keys_block_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "claim-a.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            (root / "claim-b.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            report = migration.migrate(root)
        self.assertEqual(report["source_count"], 2)
        self.assertTrue(any(item["code"] == "DUPLICATE_SOURCE_PRIMARY_KEY" for item in report["unresolved"]))

    def test_empty_source_snapshot_is_not_reported_as_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = migration.migrate(Path(tmp))
        self.assertEqual(report["source_count"], 0)
        self.assertTrue(any(item["code"] == "EMPTY_SOURCE_SNAPSHOT" for item in report["unresolved"]))

    def test_staging_refuses_nonempty_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "claim.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            output = root / "output"
            output.mkdir()
            (output / "stale.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-empty directory"):
                migration.migrate(source, output_dir=output, write_staging=True)
            self.assertTrue((output / "stale.json").exists())

    def test_staging_output_must_be_outside_input_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            (source / "claim.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside the input tree"):
                migration.migrate(source, output_dir=source / "staging", write_staging=True)

    def test_legacy_aliases_are_scoped_to_their_record_types(self):
        artifact = {
            "schema_version": "1.3", "record_type": "artifact", "project_id": "P-1",
            "artifact_id": "ART-1", "sha256": "a" * 64, "uri": "file:///artifact",
            "producer_run_id": "RUN-1", "integrity_status": "passed",
            "version": "not-an-artifact-version", "contract_hash": "not-an-artifact-hash",
        }
        artifact_props = {name: {} for name in (
            "schema_version", "record_type", "project_id", "artifact_id", "content_sha256",
            "path_or_uri", "generated_by_run_id", "artifact_integrity_status",
            "artifact_storage_kind", "alternative_identity",
        )}
        migrated_artifact, _, _, artifact_warnings = migration.migrate_record(
            artifact, target_properties=artifact_props
        )
        self.assertEqual(migrated_artifact["content_sha256"], "a" * 64)
        self.assertEqual(migrated_artifact["path_or_uri"], "file:///artifact")
        self.assertNotIn("contract_version", migrated_artifact)
        self.assertNotIn("contract_sha256", migrated_artifact)
        artifact_quarantine = next(item for item in artifact_warnings if item["code"] == "UNKNOWN_FIELDS_QUARANTINED")
        self.assertIn("version", artifact_quarantine["fields"])
        self.assertIn("contract_hash", artifact_quarantine["fields"])

        contract = {
            "schema_version": "1.3", "record_type": "task_execution_contract", "project_id": "P-1",
            "contract_id": "TEC-1", "task_id": "TASK-1", "version": 3,
            "contract_hash": "abc", "sha256": "not-a-contract-hash", "uri": "not-a-contract-uri",
        }
        contract_props = {name: {} for name in (
            "schema_version", "record_type", "project_id", "contract_id", "task_id",
            "contract_version", "contract_sha256",
        )}
        migrated_contract, _, _, contract_warnings = migration.migrate_record(
            contract, target_properties=contract_props
        )
        self.assertEqual(migrated_contract["contract_version"], 3)
        self.assertEqual(migrated_contract["contract_sha256"], "abc")
        self.assertNotIn("content_sha256", migrated_contract)
        self.assertNotIn("path_or_uri", migrated_contract)
        contract_quarantine = next(item for item in contract_warnings if item["code"] == "UNKNOWN_FIELDS_QUARANTINED")
        self.assertIn("sha256", contract_quarantine["fields"])
        self.assertIn("uri", contract_quarantine["fields"])

        run = {
            "schema_version": "1.3", "record_type": "run", "project_id": "P-1",
            "run_id": "RUN-1", "producer_run_id": "RUN-OLD",
            "version": "run-version", "contract_hash": "hash",
        }
        run_props = {name: {} for name in ("schema_version", "record_type", "project_id", "run_id")}
        migrated_run, _, _, run_warnings = migration.migrate_record(run, target_properties=run_props)
        self.assertNotIn("generated_by_run_id", migrated_run)
        self.assertNotIn("contract_version", migrated_run)
        self.assertNotIn("contract_sha256", migrated_run)
        run_quarantine = next(item for item in run_warnings if item["code"] == "UNKNOWN_FIELDS_QUARANTINED")
        self.assertIn("producer_run_id", run_quarantine["fields"])
        self.assertIn("version", run_quarantine["fields"])
        self.assertIn("contract_hash", run_quarantine["fields"])

    def test_duplicate_existing_typed_validation_refs_are_unresolved(self):
        claim = claim_record([])
        claim["validation_activity_ids"] = ["VAL-ACT-1", "VAL-ACT-1"]
        claim["validation_plan_ids"] = []
        _, _, unresolved, _ = migration.migrate_record(claim)
        self.assertTrue(any(item["code"] == "DUPLICATE_TYPED_VALIDATION_REFERENCES" for item in unresolved))

    def test_migration_rules_version_matches_mapping_contract(self):
        mapping_path = ROOT / "schema" / "v1.4.3.7" / "migrations" / "v1.3-to-v1.4-mapping.json"
        mapping_contract = json.loads(mapping_path.read_text(encoding="utf-8"))
        self.assertEqual(migration.RULE_VERSION, mapping_contract["migration_rules_version"])
        declared = {
            (item["record_type"], item["source_field"], item["target_field"])
            for item in mapping_contract["field_mappings"]
        }
        implemented = {
            (record_type, source_field, target_field)
            for record_type, field_map in migration.FIELD_MAPS.items()
            for source_field, target_field in field_map.items()
        } | {
            (record_type, source_field, target_field)
            for record_type, field_map in migration.LEGACY_ALIASES_BY_TYPE.items()
            for source_field, target_field in field_map.items()
        }
        self.assertEqual(declared, implemented)
        declared_rule_ids = {
            (item["record_type"], item["source_field"], item["rule_id"])
            for item in mapping_contract["field_mappings"]
        }
        implemented_rule_ids = {
            (record_type, source_field, f"MAP-{record_type.upper()}-{source_field.upper()}")
            for record_type, field_map in migration.FIELD_MAPS.items()
            for source_field in field_map
        } | {
            (record_type, source_field, f"MAP-{record_type.upper()}-{source_field.upper()}")
            for record_type, field_map in migration.LEGACY_ALIASES_BY_TYPE.items()
            for source_field in field_map
        }
        self.assertEqual(declared_rule_ids, implemented_rule_ids)
        activity_schema_path = ROOT / "schema" / "v1.4.3.7" / "schemas" / "validation_activity.schema.json"
        activity_schema = json.loads(activity_schema_path.read_text(encoding="utf-8"))
        self.assertEqual(
            migration.TARGET_VALIDATION_ACTIVITY_STATUSES,
            set(activity_schema["properties"]["execution_status"]["enum"]),
        )
        self.assertEqual(
            mapping_contract["target_schema_validation"],
            "draft2020-12+format-checker-per-record; invalid-targets-withheld",
        )
        self.assertEqual(mapping_contract["target_digest_algorithm"], "RFC8785-JCS-SHA256")
        declared_migration_rules = {rule["rule_id"] for rule in mapping_contract["rules"]}
        self.assertTrue({"MIG-012", "MIG-013", "MIG-014"}.issubset(declared_migration_rules))
        declared_rules_by_id = {rule["rule_id"]: rule["rule"] for rule in mapping_contract["rules"]}
        self.assertEqual(
            declared_rules_by_id["MIG-012"],
            "Validate every provisional target against its complete Draft 2020-12 JSON Schema with a format checker; any target schema error blocks target emission to staging.",
        )
        self.assertEqual(
            declared_rules_by_id["MIG-013"],
            "Compute target_record_sha256 as SHA-256 over RFC 8785 JCS canonical UTF-8 bytes; source_sha256 remains the digest of the original source bytes.",
        )
        self.assertEqual(
            declared_rules_by_id["MIG-014"],
            "Withhold a migrated record when a validation_ids reference resolves to a source Validation Plan or Validation Activity that does not produce a valid target record; report VALIDATION_TARGET_WITHHELD.",
        )

    def test_target_schema_missing_required_field_is_blocked_from_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "claim.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True)
            target_files = [path for path in output.glob("*.json") if path.name != "migration-report.json"]
        failures = [item for item in report["unresolved"] if item["code"] == "TARGET_SCHEMA_VALIDATION_FAILED"]
        self.assertTrue(failures)
        self.assertTrue(any("task_id" in item["message"] for item in failures))
        self.assertEqual(report["migratable_record_count"], 0)
        self.assertEqual(target_files, [])
        self.assertFalse(report["commit_allowed"])

    def test_target_schema_invalid_nested_object_is_blocked_from_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            record = claim_record([])
            record["physics_assessment"] = {"theory_result": 17, "unexpected": "not allowed"}
            (source / "claim.json").write_text(json.dumps(record), encoding="utf-8")
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True)
            target_files = [path for path in output.glob("*.json") if path.name != "migration-report.json"]
        failures = [item for item in report["unresolved"] if item["code"] == "TARGET_SCHEMA_VALIDATION_FAILED"]
        self.assertTrue(any(item["instance_path"] == "/physics_assessment/theory_result" for item in failures))
        self.assertTrue(any(
            item["instance_path"] == "/physics_assessment"
            and "unexpected" in item["message"]
            for item in failures
        ))
        self.assertEqual(report["migratable_record_count"], 0)
        self.assertEqual(target_files, [])

    def test_migration_target_digest_matches_rfc8785_golden_vector(self):
        vector_path = (
            ROOT / "schema" / "v1.4.3.7" / "migrations"
            / "target-digest-jcs-v1.golden.json"
        )
        vector = json.loads(vector_path.read_text(encoding="utf-8"))
        canonical = migration.stable_json(vector["input"])
        self.assertEqual(canonical, vector["canonical_json"])
        self.assertEqual(
            migration.digest_bytes(canonical.encode("utf-8")),
            vector["sha256"],
        )
        self.assertEqual(vector["algorithm"], "RFC8785-JCS-SHA256")

    def test_id_mapping_rows_match_declared_contract(self):
        mapping_path = ROOT / "schema" / "v1.4.3.7" / "migrations" / "v1.3-to-v1.4-mapping.json"
        mapping_contract = json.loads(mapping_path.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "claim.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            report = migration.migrate(root, operator="reviewer-id")
        self.assertEqual(set(report["id_mapping"][0]), set(mapping_contract["id_mapping_fields"]))
        self.assertEqual(report["id_mapping"][0]["operator"], "reviewer-id")
        self.assertEqual(report["id_mapping"][0]["review_status"], "blocked_unresolved")
        self.assertEqual(report["id_mapping"][0]["source_record_uri"], "claim.json")
        self.assertIsNone(report["id_mapping"][0]["target_record_type"])
        self.assertEqual(report["id_mapping"][0]["candidate_target_record_type"], "claim")
        self.assertIsNone(report["id_mapping"][0]["target_sha256"])
        self.assertTrue(report["id_mapping"][0]["candidate_target_sha256"])

    def test_unresolved_record_is_not_written_to_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "claim.json").write_text(json.dumps(claim_record(["VAL-MISSING"])), encoding="utf-8")
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True, operator="reviewer-id")
            target_files = [path for path in output.glob("*.json") if path.name != "migration-report.json"]
        self.assertEqual(report["migratable_record_count"], 0)
        self.assertTrue(any(item["code"] == "VALIDATION_TARGET_NOT_FOUND" for item in report["unresolved"]))
        self.assertEqual(target_files, [])

    def test_quarantined_unknown_fields_block_staging_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            record = claim_record([])
            record["mystery_field"] = "preserve for review"
            (source / "claim.json").write_text(json.dumps(record), encoding="utf-8")
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True)
            target_files = [path for path in output.glob("*.json") if path.name != "migration-report.json"]
        self.assertTrue(any(item["code"] == "UNKNOWN_FIELDS_QUARANTINED_REQUIRES_REVIEW" for item in report["unresolved"]))
        self.assertEqual(target_files, [])

    def test_yaml_source_records_are_inventoried_and_migrated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "claim.yaml").write_text(
                'schema_version: "1.3"\nrecord_type: claim\nproject_id: P-TEST\nclaim_id: CLAIM-YAML\nvalidation_ids: []\n',
                encoding="utf-8",
            )
            report = migration.migrate(root)
        self.assertEqual(report["source_count"], 1)
        self.assertEqual(report["loaded_record_count"], 1)
        self.assertEqual(report["migratable_record_count"], 0)
        self.assertEqual(report["id_mapping"][0]["source_record_uri"], "claim.yaml")
        self.assertTrue(any(item["code"] == "TARGET_SCHEMA_VALIDATION_FAILED" for item in report["unresolved"]))
        self.assertFalse(any(item["code"] == "INVALID_YAML" for item in report["unresolved"]))

    def test_duplicate_keys_in_json_and_yaml_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "duplicate.json").write_text(
                '{"schema_version":"1.3","record_type":"claim","project_id":"P-TEST","claim_id":"A","claim_id":"B","validation_ids":[]}',
                encoding="utf-8",
            )
            (root / "duplicate.yaml").write_text(
                'schema_version: "1.3"\nrecord_type: claim\nproject_id: P-TEST\nclaim_id: A\nclaim_id: B\nvalidation_ids: []\n',
                encoding="utf-8",
            )
            report = migration.migrate(root)
        codes = {item["code"] for item in report["unresolved"]}
        self.assertIn("INVALID_JSON", codes)
        self.assertIn("INVALID_YAML", codes)
        self.assertEqual(report["source_count"], 2)
        self.assertEqual(report["loaded_record_count"], 0)

    def test_empty_snapshot_emits_the_declared_mapping_csv_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True)
            header = (output / "id-mapping.csv").read_text(encoding="utf-8-sig").splitlines()[0].split(",")
        self.assertEqual(report["source_count"], 0)
        self.assertIn("EMPTY_SOURCE_SNAPSHOT", [item["code"] for item in report["unresolved"]])
        self.assertEqual(header, migration.ID_MAPPING_FIELDS)

    def test_candidate_schema_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = root / "bundle"
            shutil.copytree(ROOT / "schema" / "v1.4.3.7", bundle)
            schema_path = bundle / "schemas" / "claim.schema.json"
            schema_path.write_text(schema_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            source = root / "source"
            source.mkdir()
            (source / "claim.json").write_text(json.dumps(claim_record([])), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA-256 does not match manifest"):
                migration.migrate(source, schemas_dir=bundle / "schemas")

    def test_valid_claim_is_withheld_when_referenced_plan_fails_target_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            claim = json.loads(
                (ROOT / "schema" / "v1.4.3.7" / "tests" / "valid" / "claim" / "FX-CLAIM-VALID-001.json").read_text(encoding="utf-8")
            )
            claim["schema_version"] = "1.3"
            claim["project_id"] = "P-TEST"
            claim["validation_ids"] = ["VAL-PLAN-INVALID"]
            claim["validation_plan_ids"] = []
            claim["validation_activity_ids"] = []
            (source / "claim.json").write_text(json.dumps(claim), encoding="utf-8")
            # This source Plan resolves uniquely but cannot produce a target record:
            # the target Schema requires method and other Plan fields absent here.
            (source / "plan.json").write_text(json.dumps(plan_record("VAL-PLAN-INVALID")), encoding="utf-8")
            output = root / "staging"
            report = migration.migrate(source, output_dir=output, write_staging=True)
            staged_targets = [
                path for path in output.glob("*.json")
                if path.name != "migration-report.json"
            ]
        claim_mapping = next(
            item for item in report["id_mapping"]
            if item["source_record_type"] == "claim"
        )
        self.assertTrue(any(
            item["code"] == "TARGET_SCHEMA_VALIDATION_FAILED"
            and item["record_type"] == "validation_plan"
            for item in report["unresolved"]
        ))
        self.assertTrue(any(
            item["code"] == "VALIDATION_TARGET_WITHHELD"
            and item["record_type"] == "claim"
            and item["target_id"] == "VAL-PLAN-INVALID"
            for item in report["unresolved"]
        ))
        self.assertIsNone(claim_mapping["target_record_type"])
        self.assertEqual(claim_mapping["review_status"], "blocked_unresolved")
        self.assertEqual(report["staging_written_record_count"], 0)
        self.assertEqual(staged_targets, [])
        self.assertFalse(report["commit_allowed"])

    def test_pending_alternative_identity_rule_blocks_artifact_target(self):
        artifact = {
            "schema_version": "1.3", "record_type": "artifact", "project_id": "P-TEST",
            "artifact_id": "ART-PENDING", "artifact_storage_kind": "file",
            "origin_kind": "generated", "path_or_uri": "artifact.bin", "format": "binary",
            "artifact_integrity_status": "passed", "artifact_lifecycle_status": "active",
            "created_at": "2026-10-20T10:00:00Z",
        }
        out, _, unresolved, _ = migration.migrate_record(artifact)
        self.assertIsNotNone(out)
        self.assertTrue(any(item["code"] == "ARTIFACT_ALTERNATIVE_IDENTITY_RULE_PENDING_APPROVAL" for item in unresolved))

    def test_pending_hashless_integrity_downgrade_blocks_artifact_target(self):
        artifact = {
            "schema_version": "1.3", "record_type": "artifact", "project_id": "P-TEST",
            "artifact_id": "ART-HASHLESS", "artifact_storage_kind": "file",
            "origin_kind": "ingested_external", "path_or_uri": "external.bin",
            "format": "binary", "content_sha256": None, "hash_unavailable_reason": "source did not provide bytes",
            "artifact_integrity_status": "passed", "artifact_lifecycle_status": "active",
            "alternative_identity": None, "created_at": "2026-10-20T10:00:00Z",
        }
        out, _, unresolved, _ = migration.migrate_record(artifact)
        self.assertEqual(out["artifact_integrity_status"], "needs_review")
        self.assertTrue(any(item["code"] == "ARTIFACT_INTEGRITY_DOWNGRADE_RULE_PENDING_APPROVAL" for item in unresolved))

if __name__ == "__main__":
    unittest.main()
