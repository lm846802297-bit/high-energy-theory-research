from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "high-energy-theory-research" / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_front_matter_is_present(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("name: high-energy-theory-research", text)
        self.assertIn("description:", text.split("---", 2)[1])

    def test_reference_files_exist(self):
        refs = SKILL.parent / "references"
        for name in (
            "task-router.md",
            "evidence-and-claim-gates.md",
            "source-and-version-audit.md",
            "symbolic-calculation.md",
            "numerical-scans-and-uncertainty.md",
            "scientific-figure-audit.md",
            "paper-reading.md",
            "optional-tooling.md",
        ):
            with self.subTest(name=name):
                self.assertTrue((refs / name).is_file())

    def test_candidate_status_is_explicit(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("candidate", readme)
        self.assertIn("not", readme)
        self.assertIn("formal schema release", readme)

    def test_codex_discovery_paths_are_documented(self):
        tooling = (SKILL.parent / "references" / "optional-tooling.md").read_text(encoding="utf-8")
        diagnostic = SKILL.parent / "scripts" / "check_codex_skill_discovery.ps1"
        self.assertIn(".agents/skills/", tooling)
        self.assertIn("~/.agents/skills/", tooling)
        self.assertTrue(diagnostic.is_file())

    def test_codex_diagnostic_is_read_only_and_host_aware(self):
        diagnostic = (SKILL.parent / "scripts" / "check_codex_skill_discovery.ps1").read_text(encoding="utf-8")
        self.assertIn("runtime_discovery_confirmed = $false", diagnostic)
        self.assertIn("known_windows_desktop_issue", diagnostic)
        for command in ("Copy-Item", "Move-Item", "Remove-Item", "Set-Content", "New-Item"):
            with self.subTest(command=command):
                self.assertNotIn(command, diagnostic)

    def test_project_record_validator_is_referenced_and_present(self):
        script = SKILL.parent / "scripts" / "validate_project_records.py"
        self.assertTrue(script.is_file())
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertIn("validate_project_records.py", skill_text)
        self.assertIn("references/optional-tooling.md", skill_text)


if __name__ == "__main__":
    unittest.main()
