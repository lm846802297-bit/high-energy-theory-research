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
            "central-repository-governance.md",
        ):
            with self.subTest(name=name):
                self.assertTrue((refs / name).is_file())


    def test_task_complexity_gate_is_explicit(self):
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Task-complexity gate and proportionality", skill_text)
        self.assertIn("Quick analytic task", skill_text)
        self.assertIn("invocation does not make tools", skill_text)
        self.assertIn("Do not create a project record, run manifest", skill_text)

    def test_task_router_prefers_lowest_sufficient_tier(self):
        router = (SKILL.parent / "references" / "task-router.md").read_text(encoding="utf-8")
        self.assertIn("Tier 0 — Quick analytic", router)
        self.assertIn("Tier 2 — Numerical/computational", router)
        self.assertIn("smallest workflow", router)
        self.assertIn("Stop once the requested deliverable", router)
        self.assertIn("do not run a numerical integral solely", router)

    def test_numerical_reference_does_not_force_numeric_work(self):
        numerical = (SKILL.parent / "references" / "numerical-scans-and-uncertainty.md").read_text(encoding="utf-8")
        self.assertIn("does not create a requirement to perform numerical work", numerical)
        self.assertIn("Numerical methods are not the default independent check", numerical)
        self.assertIn("one-off diagnostic spot check", numerical)

    def test_central_repository_rules_are_isolated(self):
        skill_text = SKILL.read_text(encoding="utf-8")
        central = (SKILL.parent / "references" / "central-repository-governance.md").read_text(encoding="utf-8")
        self.assertNotIn("current UV–EFT matching workstream belongs", skill_text)
        self.assertIn("current UV–EFT matching workstream belongs", central)
        self.assertIn("only when the active repository is", skill_text)

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

    def test_windows_installer_regression_assets_exist(self):
        installer = ROOT / "scripts" / "sync_research_skill.ps1"
        helper = ROOT / "scripts" / "research-skill-installer.helpers.ps1"
        regression = ROOT / "tests" / "windows" / "test_sync_research_skill_cleanup.ps1"
        self.assertTrue(installer.is_file())
        self.assertTrue(helper.is_file())
        self.assertTrue(regression.is_file())
        helper_text = helper.read_text(encoding="utf-8")
        self.assertIn("Test-ResearchSkillScratchCleanupAllowed", helper_text)
        self.assertIn("Test-ResearchSkillManifestIntegrity", helper_text)

    def test_project_record_validator_is_referenced_and_present(self):
        script = SKILL.parent / "scripts" / "validate_project_records.py"
        self.assertTrue(script.is_file())
        skill_text = SKILL.read_text(encoding="utf-8")
        central = (SKILL.parent / "references" / "central-repository-governance.md").read_text(encoding="utf-8")
        self.assertIn("references/central-repository-governance.md", skill_text)
        self.assertIn("validate_project_records.py", central)
        self.assertIn("references/optional-tooling.md", skill_text)
        self.assertIn("Central-repository-only tooling", central)


if __name__ == "__main__":
    unittest.main()
