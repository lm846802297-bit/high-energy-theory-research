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
        ):
            with self.subTest(name=name):
                self.assertTrue((refs / name).is_file())

    def test_candidate_status_is_explicit(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("candidate", readme)
        self.assertIn("not", readme)
        self.assertIn("formal schema release", readme)


if __name__ == "__main__":
    unittest.main()
