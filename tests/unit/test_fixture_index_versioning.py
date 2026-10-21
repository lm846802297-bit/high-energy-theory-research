import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schema" / "v1.4.3.7"


class FixtureIndexVersioningTests(unittest.TestCase):
    def test_historical_fixture_index_is_not_relabelled(self):
        manifest = json.loads((SCHEMA_ROOT / "manifest.json").read_text(encoding="utf-8"))
        legacy = json.loads((SCHEMA_ROOT / manifest["fixture_index"]).read_text(encoding="utf-8"))
        candidate = json.loads((SCHEMA_ROOT / manifest["candidate_fixture_index"]).read_text(encoding="utf-8"))
        self.assertEqual(legacy["schema_version"], "1.4.3.6-candidate")
        self.assertEqual(candidate["schema_version"], manifest["schema_version"])
        self.assertEqual(manifest["fixture_index_sha256"], hashlib.sha256((SCHEMA_ROOT / manifest["fixture_index"]).read_bytes()).hexdigest())
        self.assertEqual(manifest["candidate_fixture_index_sha256"], hashlib.sha256((SCHEMA_ROOT / manifest["candidate_fixture_index"]).read_bytes()).hexdigest())
        self.assertEqual(len(legacy["fixtures"]), len(candidate["fixtures"]))
        self.assertEqual({x["fixture_id"] for x in legacy["fixtures"]}, {x["fixture_id"] for x in candidate["fixtures"]})


if __name__ == "__main__":
    unittest.main()
