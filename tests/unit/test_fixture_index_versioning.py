import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schema" / "v1.4.3.7"


class FixtureIndexVersioningTests(unittest.TestCase):
    def test_manifest_points_to_version_matched_candidate_index(self):
        manifest = json.loads((SCHEMA_ROOT / "manifest.json").read_text(encoding="utf-8"))
        candidate_path = SCHEMA_ROOT / manifest["fixture_index"]
        legacy_path = SCHEMA_ROOT / manifest["legacy_fixture_index"]
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        legacy = json.loads(legacy_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["bundle_status"], "candidate")
        self.assertEqual(manifest["release_status"], "not_released")
        self.assertEqual(candidate["schema_version"], manifest["schema_version"])
        self.assertEqual(legacy["schema_version"], manifest["legacy_fixture_index_schema_version"])
        self.assertEqual(hashlib.sha256(candidate_path.read_bytes()).hexdigest(), manifest["fixture_index_sha256"])
        self.assertEqual(hashlib.sha256(legacy_path.read_bytes()).hexdigest(), manifest["legacy_fixture_index_sha256"])
        self.assertEqual(len(legacy["fixtures"]), len(candidate["fixtures"]))
        self.assertEqual({x["fixture_id"] for x in legacy["fixtures"]}, {x["fixture_id"] for x in candidate["fixtures"]})


if __name__ == "__main__":
    unittest.main()
