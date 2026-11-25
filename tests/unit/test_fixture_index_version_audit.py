import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "schema" / "v1.4.3.7"
MANIFEST_PATH = BUNDLE / "manifest.json"
PROVENANCE_PATH = BUNDLE / "IMPORT_PROVENANCE.json"
VALIDATOR_PATH = BUNDLE / "tools" / "schema-v1.4.3.6-validate.py"
AUDIT_PATH = BUNDLE / "audit" / "fixture-index-version-audit.md"


class FixtureIndexVersionAuditTests(unittest.TestCase):
    def test_candidate_and_legacy_indexes_have_distinct_declared_roles(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        candidate_path = BUNDLE / manifest["fixture_index"]
        legacy_path = BUNDLE / manifest["legacy_fixture_index"]
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        legacy = json.loads(legacy_path.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        audit = AUDIT_PATH.read_text(encoding="utf-8")

        self.assertEqual(manifest["schema_version"], "1.4.3.7-candidate")
        self.assertEqual(candidate["schema_version"], manifest["schema_version"])
        self.assertEqual(legacy["schema_version"], manifest["legacy_fixture_index_schema_version"])
        self.assertEqual(legacy["schema_version"], "1.4.3.6-candidate")
        self.assertEqual(
            manifest["fixture_index_version_semantics"],
            "schema_version identifies the target schema bundle whose fixture expectations are declared; it is not the index-format version or source archive lineage.",
        )
        self.assertEqual(hashlib.sha256(candidate_path.read_bytes()).hexdigest(), manifest["fixture_index_sha256"])
        self.assertEqual(hashlib.sha256(legacy_path.read_bytes()).hexdigest(), manifest["legacy_fixture_index_sha256"])

        archive_name = provenance["source_lineage_recorded_in_audit"]["archive"]
        self.assertEqual(archive_name, "schema-v1.4.3.6-integrated-candidate-bundle.zip")
        self.assertFalse(any(ROOT.rglob(archive_name)), "The historical source ZIP is not committed in this repository.")
        self.assertIn("resolved at metadata-contract level", audit.lower())
        self.assertIn("byte-for-byte equality", audit.lower())

    def test_validator_enforces_candidate_and_legacy_index_contracts(self):
        validator = VALIDATOR_PATH.read_text(encoding="utf-8")
        self.assertIn("fixture_index_hash", validator)
        self.assertIn("legacy_fixture_index_hash", validator)
        self.assertIn("fixture_index_version_matches_bundle", validator)
        self.assertIn("legacy_fixture_index_version_matches_declared_baseline", validator)
        self.assertNotIn("candidate_fixture_index", validator)


if __name__ == "__main__":
    unittest.main()
