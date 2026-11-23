from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "skills/high-energy-theory-research/scripts/validate_central_archive_boundary.py"
)


class CentralArchiveBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.git("init", "-q")
        self.git("config", "user.name", "Boundary Tester")
        self.git("config", "user.email", "boundary@example.test")
        self.git("config", "core.autocrlf", "false")
        self.write("research/legacy.md", "existing note")
        self.write("validation/old.txt", "existing log")
        self.base = self.commit("baseline")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def write(self, relative_path, content):
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def guard(self, head="HEAD", base=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(self.repo),
             "--base", base or self.base, "--head", head],
            text=True, capture_output=True,
        )

    def test_reports_new_payload_without_name_or_extension_heuristics(self):
        paths = ["artifacts/raw/数 据.bin", "calculations/example.py",
                 "research/project-new/README.md", "validation/project-run/log.json"]
        for path in paths:
            self.write(path, "payload")
        self.commit("project material")
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["blocked_new_paths"], paths)

    def test_allows_history_repairs_removals_and_explicit_infrastructure(self):
        self.write("research/legacy.md", "correct a history link")
        (self.repo / "validation/old.txt").unlink()
        allowed = ["projects/registry.yaml", "docs/policy.md", "schema/example.json",
                   "tests/fixtures/synthetic.json", "tests/eval-cases/pilot/input.json",
                   "skills/any/SKILL.md", ".github/workflows/ci.yml",
                   "validation/skill-benchmark/synthetic-run.json",
                   "validation/workflow-tests/fixtures/sample.yml",
                   "validation/infrastructure-tests/input.json",
                   "validation/research-skill-benchmark/fake.json",
                   "validation/skill-module-evaluation-2026-11-22/example.csv"]
        for path in allowed:
            self.write(path, "fixture")
        head = self.commit("infrastructure")
        self.write("research/not-committed.md", "ignored")
        result = self.guard(head=head)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["blocked_new_paths"], [])
        self.assertEqual(report["merge_base"], self.base)
        self.assertEqual(report["head"], head)
        self.assertEqual(report["new_paths_checked"], len(allowed))

    def test_new_destination_is_checked_even_for_exact_rename_and_copy(self):
        self.git("mv", "research/legacy.md", "research/moved.md")
        self.write("research/copied.txt", "existing log")
        self.commit("rename and copy")
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["blocked_new_paths"],
                         ["research/copied.txt", "research/moved.md"])

    def test_allowlist_matches_real_directory_prefix_not_lookalike(self):
        file = "validation/research-skill-benchmark-extra/evidence.txt"
        self.write(file, "project evidence")
        self.commit("lookalike")
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["blocked_new_paths"], [file])

    def test_uses_pr_merge_base_instead_of_a_moving_base_tree(self):
        self.git("switch", "-qc", "topic")
        self.write("research/introduced.md", "new topic")
        head = self.commit("topic adds project path")
        self.git("switch", "-qC", "upstream", self.base)
        self.write("research/introduced.md", "coincident same bytes")
        new_base = self.commit("upstream independent addition")
        result = self.guard(base=new_base, head=head)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["merge_base"], self.base)

    def test_bad_ref_is_not_reported_as_success(self):
        result = self.guard(head="not-a-ref")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not-a-ref", result.stderr)


if __name__ == "__main__":
    unittest.main()
