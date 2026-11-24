from __future__ import annotations

import csv
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

import verify_public_t05 as verifier


ROOT = Path(__file__).resolve().parents[1]
PLOT_SCRIPT = ROOT / "tools" / "plot_afh_xe131_responses.py"
SPEC = importlib.util.spec_from_file_location("plot_afh_xe131_responses", PLOT_SCRIPT)
PLOT = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(PLOT)


class PublicT05IdentityTests(unittest.TestCase):
    def test_empty_git_blob_identity(self):
        self.assertEqual(
            verifier.git_blob_sha1(b""),
            "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
        )

    def test_sha256_identity(self):
        self.assertEqual(
            verifier.sha256_bytes(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )

    def test_verify_inputs_rejects_wrong_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            file_path = root / "input.bin"
            file_path.write_bytes(b"actual")
            task = {
                "input_sources": [{
                    "repository": "owner/repo",
                    "commit": "0" * 40,
                    "path": "input.bin",
                    "staged_path": "input.bin",
                    "role": "test",
                    "size_bytes": 6,
                    "git_blob_sha1": verifier.git_blob_sha1(b"actual"),
                    "sha256": hashlib.sha256(b"not-actual").hexdigest(),
                }]
            }
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                verifier.verify_inputs(task, root)


class PublicAFHPlotTests(unittest.TestCase):
    def make_csv(self, path: Path, rows: int = 2401, imaginary: float = 0.0) -> None:
        diagonal = [name for name, _ in PLOT.DIAGONAL]
        interference = [name for name, _ in PLOT.INTERFERENCE]
        fields = ["A", "q_GeV", "y", *diagonal, *interference]
        fields += ["Im_" + name for name in diagonal + interference]
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for index in range(rows):
                q = 0.6 * index / (rows - 1)
                record = {"A": 131, "q_GeV": q, "y": q * q}
                for n, column in enumerate(diagonal):
                    record[column] = (n + 1.0) * (1.0 + q) * (10.0 ** (-n))
                for n, column in enumerate(interference):
                    record[column] = ((-1.0) ** (index // 400)) * (n + 1.0) * (1.0 + q)
                for column in ["Im_" + name for name in diagonal + interference]:
                    record[column] = imaginary
                writer.writerow(record)

    def test_pinned_native_grid_produces_two_deterministic_svgs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            csv_path = root / "xe131.csv"
            self.make_csv(csv_path)
            first = PLOT.generate(csv_path, root / "first")
            second = PLOT.generate(csv_path, root / "second")
            self.assertEqual(first["status"], "PASS")
            self.assertEqual(first["row_count"], 2401)
            self.assertEqual(first["outputs"], second["outputs"])
            self.assertEqual(
                {item["path"] for item in first["outputs"]},
                {"xe131_diagonal_responses.svg", "xe131_signed_interferences.svg"},
            )
            for item in first["outputs"]:
                self.assertEqual(
                    (root / "first" / item["path"]).read_bytes(),
                    (root / "second" / item["path"]).read_bytes(),
                )

    def test_imaginary_residual_above_tolerance_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            csv_path = root / "xe131.csv"
            self.make_csv(csv_path, imaginary=1.0e-6)
            with self.assertRaisesRegex(ValueError, "imaginary response residual"):
                PLOT.load_rows(csv_path)


if __name__ == "__main__":
    unittest.main()
