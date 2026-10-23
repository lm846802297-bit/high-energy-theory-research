import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "schema" / "v1.4.3.7" / "tools" / "directory_manifest.py"
SPEC = importlib.util.spec_from_file_location("directory_manifest", HELPER)
directory_manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(directory_manifest)


def file_entry(path, *, extra=None):
    entry = {
        "relative_path": path,
        "entry_type": "file",
        "size_bytes": 1,
        "content_sha256": "a" * 64,
        "symlink_target": None,
    }
    if extra:
        entry.update(extra)
    return entry


class DirectoryManifestFailClosedTests(unittest.TestCase):
    def test_manifest_bytes_are_stable_and_paths_are_sorted(self):
        entries = [file_entry("z.txt"), file_entry("a.txt")]
        self.assertEqual(
            directory_manifest.canonical_manifest_bytes(entries),
            directory_manifest.canonical_manifest_bytes(list(reversed(entries))),
        )
        normalized = directory_manifest.normalize_manifest(entries)
        self.assertEqual([entry["relative_path"] for entry in normalized], ["a.txt", "z.txt"])

    def test_extra_file_entry_key_is_rejected_instead_of_silently_dropped(self):
        entry = file_entry("a.txt", extra={"unreviewed_metadata": "must-not-be-ignored"})
        with self.assertRaisesRegex(directory_manifest.ManifestError, "extra=.*unreviewed_metadata"):
            directory_manifest.normalize_manifest([entry])

    def test_missing_file_entry_key_is_rejected(self):
        entry = file_entry("a.txt")
        del entry["content_sha256"]
        with self.assertRaisesRegex(directory_manifest.ManifestError, "missing=.*content_sha256"):
            directory_manifest.normalize_manifest([entry])

    def test_nfc_equivalent_paths_collide(self):
        composed = "\u00e9.txt"
        decomposed = "e\u0301.txt"
        with self.assertRaisesRegex(directory_manifest.ManifestError, "duplicate path after NFC normalization"):
            directory_manifest.normalize_manifest([file_entry(composed), file_entry(decomposed)])

    def test_traversal_and_backslash_paths_are_rejected(self):
        for path in ("../escape.txt", "a/../escape.txt", "/absolute.txt", "a\\\\b.txt", "a//b.txt"):
            with self.subTest(path=path):
                with self.assertRaises(directory_manifest.ManifestError):
                    directory_manifest.normalize_manifest([file_entry(path)])

    def test_symlink_entries_are_rejected(self):
        entry = {
            "relative_path": "link",
            "entry_type": "symlink",
            "size_bytes": None,
            "content_sha256": None,
            "symlink_target": "outside",
        }
        with self.assertRaisesRegex(directory_manifest.ManifestError, "symlinks are not supported"):
            directory_manifest.normalize_manifest([entry])

    def test_allow_symlinks_flag_cannot_silently_claim_support(self):
        with self.assertRaisesRegex(directory_manifest.ManifestError, "allow_symlinks=True is unsupported"):
            directory_manifest.normalize_manifest([], allow_symlinks=True)


if __name__ == "__main__":
    unittest.main()
