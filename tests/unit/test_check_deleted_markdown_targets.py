from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / (
    "skills/high-energy-theory-research/scripts/check_deleted_markdown_targets.py"
)


@unittest.skipUnless(importlib.util.find_spec("markdown_it"), "optional Markdown parser not installed")
class DeletionReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")

    def git(self, *argv):
        return subprocess.check_output(["git", "-C", str(self.repo), *argv], text=True)

    def write(self, path, data="evidence\n"):
        new = self.repo / path
        new.parent.mkdir(parents=True, exist_ok=True)
        new.write_text(data, encoding="utf-8")

    def commit(self):
        self.git("add", "-A")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD").strip()

    def check(self, base, head="HEAD"):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo),
             "--base", base, "--head", head], capture_output=True, text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def test_retained_links_and_images_report_deleted_targets(self):
        self.write("data/notes (v1).md")
        self.write("figs/figure.png")
        self.write("docs/index.md", "\n".join([
            "# Introduction", "",
            "[details](../data/notes%20%28v1%29.md?mode=raw#results)", "",
            "![figure][Fig]", "",
            "[Fig]: ../figs/figure.png", "",
            "[directory](../data/)", "",
            "| Evidence |", "| --- |", "| [table](../figs/figure.png) |",
        ]))
        base = self.commit()
        self.git("mv", "data/notes (v1).md", "data/notes-v2.md")
        self.git("rm", "figs/figure.png")
        head = self.commit()
        code, report = self.check(base, head)
        self.assertEqual(code, 1, report)
        self.assertEqual(report["base"], base)
        self.assertEqual(report["head"], head)
        self.assertEqual([(v["block_line"], v["deleted_path"]) for v in report["findings"]],
                         [(3, "data/notes (v1).md"), (5, "figs/figure.png"),
                          (13, "figs/figure.png")])

    def test_nonlinks_unchanged_links_and_already_broken_links_are_ignored(self):
        self.write("old.md")
        self.write("keep.txt")
        self.write("folder/sub.md")
        self.write("README.md", """
[still here](keep.txt#anchor) [already broken](never.md)
[external](https://example.invalid/old.md) [absolute](/old.md)
[fragment](#old.md) [query](?name=old.md) [outside](../old.md)
`[inline sample](old.md)`

```md
[fenced sample](old.md)
```

<!-- [comment](old.md) -->
<a href="old.md">raw HTML is out of scope</a>
""")
        base = self.commit()
        self.git("rm", "old.md", "folder/sub.md")
        head = self.commit()
        self.assertEqual(self.check(base, head), (0, {
            "base": base, "head": head, "findings": [],
        }))

    def test_directory_removed_new_candidate_link_dirty_file_ignored(self):
        self.write("retired/entry.txt")
        base = self.commit()
        self.write("docs/new.md", "[directory](../retired/)")
        self.git("rm", "retired/entry.txt")
        head = self.commit()
        self.write("docs/new.md", "The working tree no longer contains the old link.")
        self.write("retired/entry.txt", "Untracked.")
        code, report = self.check(base, head)
        self.assertEqual(code, 1, report)
        self.assertEqual(report["findings"], [{
            "source": "docs/new.md", "block_line": 1,
            "destination": "../retired/", "deleted_path": "retired",
        }])

    def test_invalid_base_fails_with_error(self):
        self.write("README.md")
        self.commit()
        code, report = self.check("does-not-exist")
        self.assertEqual(code, 2)
        self.assertIn("error", report)


if __name__ == "__main__":
    unittest.main()
