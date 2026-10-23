import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "schema" / "v1.4.3.7"
INDEX_PATH = BUNDLE / "tests" / "fixture-index.json"
MANIFEST_PATH = BUNDLE / "manifest.json"
PROVENANCE_PATH = BUNDLE / "IMPORT_PROVENANCE.json"
VALIDATOR_PATH = BUNDLE / "tools" / "schema-v1.4.3.6-validate.py"
AUDIT_PATH = BUNDLE / "audit" / "fixture-index-version-audit.md"


class FixtureIndexVersionAuditTests(unittest.TestCase):
    def test_mismatch_and_source_lineage_are_explicitly_preserved(self):
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        audit = AUDIT_PATH.read_text(encoding="utf-8")

        self.assertEqual(manifest["schema_version"], "1.4.3.7-candidate")
        self.assertEqual(index["schema_version"], "1.4.3.6-candidate")
        self.assertEqual(
            provenance["source_lineage_recorded_in_audit"]["archive"],
            "schema-v1.4.3.6-integrated-candidate-bundle.zip",
        )
        archive_name = provenance["source_lineage_recorded_in_audit"]["archive"]
        self.assertFalse(any(ROOT.rglob(archive_name)), "The source ZIP should not be assumed present unless it is actually committed.")
        actual_index_hash = hashlib.sha256(INDEX_PATH.read_bytes()).hexdigest()
        self.assertEqual(actual_index_hash, manifest["fixture_index_sha256"])
        self.assertIn("unresolved", audit.lower())
        self.assertIn("does not interpret", audit.lower())

    def test_current_validator_checks_index_digest_not_its_top_level_version(self):
        validator = VALIDATOR_PATH.read_text(encoding="utf-8")
        self.assertIn("fixture_index_hash", validator)
        self.assertNotIn('idx["schema_version"]', validator)
        self.assertNotIn("idx['schema_version']", validator)


if __name__ == "__main__":
    unittest.main()
