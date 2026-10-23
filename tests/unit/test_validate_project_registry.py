import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "high-energy-theory-research" / "scripts" / "validate_project_registry.py"
SPEC = importlib.util.spec_from_file_location("project_registry_validator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
validate_registry = MODULE.validate_registry


class ProjectRegistryValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "research").mkdir()
        (self.root / "research" / "record.md").write_text("# record\n", encoding="utf-8")
        (self.root / "research" / "claims.md").write_text("# claims\n", encoding="utf-8")
        (self.root / "research" / "index.md").write_text("# index\n", encoding="utf-8")
        self.registry = self.root / "projects" / "registry.yaml"
        self.registry.parent.mkdir()
        self._write_registry()

    def tearDown(self):
        self.temp.cleanup()

    def _write_registry(self, parent_id="parent-project", workstream_id="loop-matching",
                        canonical="research/record.md", status="active"):
        self.registry.write_text(
            "registry_version: 1\n"
            "registry_status: draft\n"
            "projects:\n"
            "  - project_id: " + parent_id + "\n"
            "    title: Parent project\n"
            "    status: active\n"
            "    scope: Parent scope\n"
            "    workstreams:\n"
            "      - workstream_id: " + workstream_id + "\n"
            "        title: Loop matching\n"
            "        kind: research_branch\n"
            "        status: " + status + "\n"
            "        parent_project_id: " + parent_id + "\n"
            "        scope: Loop matching scope\n"
            "        canonical_records:\n"
            "          - " + canonical + "\n"
            "        claim_evidence_matrix: research/claims.md\n"
            "        index: research/index.md\n",
            encoding="utf-8",
        )

    def test_valid_registry_and_existing_paths_pass(self):
        report = validate_registry(self.registry, self.root)
        self.assertEqual(report["summary"]["errors"], 0, report["errors"])
        self.assertEqual(report["summary"]["projects"], 1)
        self.assertEqual(report["summary"]["workstreams"], 1)

    def test_parent_mismatch_is_rejected(self):
        self._write_registry()
        text = self.registry.read_text(encoding="utf-8").replace(
            "parent_project_id: parent-project", "parent_project_id: wrong-parent"
        )
        self.registry.write_text(text, encoding="utf-8")
        report = validate_registry(self.registry, self.root)
        self.assertTrue(any(e["code"] == "WORKSTREAM_PARENT_MISMATCH" for e in report["errors"]))

    def test_missing_canonical_path_is_rejected(self):
        self._write_registry(canonical="research/not-there.md")
        report = validate_registry(self.registry, self.root)
        self.assertTrue(any(e["code"] == "CANONICAL_RECORD_MISSING" for e in report["errors"]))

    def test_path_escape_is_rejected(self):
        self._write_registry(canonical="../outside.md")
        report = validate_registry(self.registry, self.root)
        self.assertTrue(any(e["code"] == "CANONICAL_RECORD_OUTSIDE_ROOT" for e in report["errors"]))

    def test_duplicate_project_id_is_rejected(self):
        self._write_registry()
        text = self.registry.read_text(encoding="utf-8")
        duplicate = (
            "  - project_id: parent-project\n"
            "    title: Duplicate project\n"
            "    status: active\n"
            "    scope: Duplicate scope\n"
            "    workstreams: []\n"
        )
        self.registry.write_text(text.replace("projects:\n", "projects:\n" + duplicate, 1), encoding="utf-8")
        report = validate_registry(self.registry, self.root)
        self.assertTrue(any(e["code"] == "PROJECT_ID_DUPLICATE" for e in report["errors"]))


if __name__ == "__main__":
    unittest.main()
