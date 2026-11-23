"""Keep the two adoption contracts and the lock template's options in sync."""
from collections import Counter
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/governance/DOWNSTREAM_STANDARDS_ADOPTION"
TEMPLATE = ROOT / "templates/research-standards-lock.yaml"
PROFILE = r"[a-z0-9][a-z0-9_.-]*"


def contract_profiles(text):
    # Section 3 is the profile list in both contracts. No translated heading
    # text, descriptions, ordering, or specific IDs are part of this check.
    sections = re.split(r"^ {0,3}##[ \t]+", text, flags=re.MULTILINE)
    catalog = next(s for s in sections[1:] if re.match(r"3\.[ \t]", s))
    bullets = re.findall(r"^ {0,3}[-*+][ \t]+(.+?)\s*$", catalog, re.MULTILINE)
    return [item.strip("`") for item in bullets]


def template_profiles(text):
    # The selectable IDs are in comma-separated YAML comments immediately above
    # adopted_profiles; reading the YAML value would only yield an empty list.
    preceding, _ = re.split(r"^adopted_profiles[ \t]*:", text, maxsplit=1,
                            flags=re.MULTILINE)
    rows = []
    for line in reversed(preceding.splitlines()):
        if not line.lstrip().startswith("#"):
            break
        row = line.lstrip()[1:].strip()
        if not re.fullmatch(rf"{PROFILE}(?:\s*,\s*{PROFILE})*\s*[,\.]?", row):
            break
        rows.append(row.rstrip(",."))
    return [item.strip() for row in reversed(rows) for item in row.split(",")]


class StandardsAdoptionCatalogTests(unittest.TestCase):
    def test_selectable_profile_ids_match_both_contracts(self):
        sources = {
            CONTRACT.with_suffix(".md"): contract_profiles,
            CONTRACT.with_suffix(".zh-CN.md"): contract_profiles,
            TEMPLATE: template_profiles,
        }
        sets = {}
        for path, parse in sources.items():
            label = path.relative_to(ROOT).as_posix()
            with self.subTest(file=label):
                ids = parse(path.read_text(encoding="utf-8"))
                self.assertTrue(ids, "missing or empty profile catalog")
                self.assertEqual([i for i in ids if not re.fullmatch(PROFILE, i)], [])
                self.assertEqual(sorted(i for i, n in Counter(ids).items() if n > 1),
                                 [], "duplicate profile IDs")
                sets[label] = set(ids)
        all_ids = set().union(*sets.values())
        for label, ids in sets.items():
            with self.subTest(file=label):
                self.assertEqual(sorted(all_ids - ids), [],
                                 "profile IDs present in another catalog but missing here")
