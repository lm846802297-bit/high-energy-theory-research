from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "docs/schemas/validate_result_records.py"


class DependencyHelpTests(unittest.TestCase):
    def test_missing_dependency_points_to_an_existing_pinned_requirements_file(self):
        result = subprocess.run(
            [sys.executable, "-I", "-S", str(VALIDATOR), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        match = re.search(r"python -m pip install -r ([\w/\-]+\.txt)\.", result.stderr)
        self.assertIsNotNone(match, result.stderr)
        requirements = ROOT / match.group(1)
        self.assertTrue(requirements.is_file(), result.stderr)
        self.assertRegex(requirements.read_text(encoding="utf-8"), r"jsonschema(?:\[format\])?==[\d.]+")
