from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import verify_figure_regeneration as verifier


class SvgSemanticComparisonTests(unittest.TestCase):
    def test_numeric_serialization_and_known_punctuation_are_semantic_match(self):
        reference = (
            b'<svg width="1200" height="760" viewBox="0 0 1200 760">'
            b'<text x="600" y="42">m_V = 10 GeV; v = 776 km/s</text>'
            b'<line x1="145" y1="554.285714" x2="1135" y2="554.285714"/>'
            b'<path d="M145.00,615.89 L154.52,615.82"/></svg>'
        )
        generated = (
            b'<svg width="1200" height="760" viewBox="0 0 1200 760">'
            b'<text x="600.0" y="42.0">m_V = 10 GeV, v = 776 km/s</text>'
            b'<line x1="145.00" y1="554.29" x2="1135.00" y2="554.29"/>'
            b'<path d="M145.00,615.89 L154.52,615.82"/></svg>'
        )
        result = verifier.compare_svg_semantics(reference, generated)
        self.assertTrue(result["semantic_match"])
        self.assertTrue(result["path_data_exact"])
        self.assertFalse(result["byte_identity_match"])
        self.assertLessEqual(result["max_coordinate_delta_px"], 0.01)

    def test_transform_float_serialization_is_tolerated_but_rotation_change_is_not(self):
        reference = b'<svg><text transform="translate(35 365) rotate(-90)">label</text></svg>'
        generated = b'<svg><text transform="translate(35.0 365.0) rotate(-90.0)">label</text></svg>'
        result = verifier.compare_svg_semantics(reference, generated)
        self.assertTrue(result["semantic_match"])
        bad = b'<svg><text transform="translate(35.0 365.0) rotate(-89.9)">label</text></svg>'
        with self.assertRaisesRegex(ValueError, "transform numeric mismatch"):
            verifier.compare_svg_semantics(reference, bad)

    def test_plotted_path_change_is_rejected(self):
        reference = b'<svg><path d="M0,0 L1,1"/></svg>'
        generated = b'<svg><path d="M0,0 L1,1.01"/></svg>'
        with self.assertRaisesRegex(ValueError, "plotted path data differ"):
            verifier.compare_svg_semantics(reference, generated)

    def test_coordinate_change_above_tolerance_is_rejected(self):
        reference = b'<svg><line x1="0" y1="0" x2="1" y2="1"/></svg>'
        generated = b'<svg><line x1="0" y1="0.02" x2="1" y2="1"/></svg>'
        with self.assertRaisesRegex(ValueError, "coordinate mismatch"):
            verifier.compare_svg_semantics(reference, generated)

    def test_non_element_text_content_is_compared(self):
        reference = b"<svg>archived</svg>"
        generated = b"<svg>generated</svg>"
        with self.assertRaisesRegex(ValueError, "SVG text mismatch"):
            verifier.compare_svg_semantics(reference, generated)

    def test_unapproved_label_change_is_rejected(self):
        reference = b'<svg><text x="0" y="0">d sigma / d E_R [cm^2 / keV]</text></svg>'
        generated = b'<svg><text x="0" y="0">d sigma / d E_R [cm^2]</text></svg>'
        with self.assertRaisesRegex(ValueError, "SVG text mismatch"):
            verifier.compare_svg_semantics(reference, generated)

    def test_submitted_outputs_must_match_fresh_trusted_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model_root = root / "model"
            golden_root = root / "golden"
            submitted_root = root / "submitted"
            generated_root = root / "trusted-generated"
            slug = "LZ-3-body-for-hdm"
            generator_rel = "research/plot_user_dsigma_curve.py"
            csv_rel = "research/results/input.csv"
            minima_rel = "research/results/minima.csv"
            output_rel = "research/results/plots"
            generator = model_root / slug / generator_rel
            csv_path = model_root / slug / csv_rel
            minima_path = model_root / slug / minima_rel
            generator.parent.mkdir(parents=True)
            csv_path.parent.mkdir(parents=True)
            minima_path.parent.mkdir(parents=True, exist_ok=True)
            svg_a = '<svg width="10" height="10"><path d="M0,0 L1,1"/></svg>'
            svg_b = '<svg width="10" height="10"><path d="M0,1 L1,0"/></svg>'
            code = (
                "import argparse\nfrom pathlib import Path\n"
                "p=argparse.ArgumentParser(); p.add_argument('--csv'); p.add_argument('--minima'); p.add_argument('--out-dir'); a=p.parse_args()\n"
                "o=Path(a.out_dir); o.mkdir(parents=True,exist_ok=True)\n"
                f"(o/'fixed_speed_xe131_dsigma_450kev.svg').write_text({svg_a!r},encoding='utf-8')\n"
                f"(o/'xe131_gcn_jj55_response_ratio_450kev.svg').write_text({svg_b!r},encoding='utf-8')\n"
            )
            generator.write_text(code, encoding="utf-8")
            csv_path.write_text("x,y\n0,1\n", encoding="utf-8")
            minima_path.write_text("x,y\n0,1\n", encoding="utf-8")
            golden_dir = golden_root / slug / output_rel
            golden_dir.mkdir(parents=True)
            (golden_dir / "fixed_speed_xe131_dsigma_450kev.svg").write_text(svg_a, encoding="utf-8")
            (golden_dir / "xe131_gcn_jj55_response_ratio_450kev.svg").write_text(svg_b, encoding="utf-8")

            def identity(path: Path):
                data = path.read_bytes()
                return {"git_blob_sha1": verifier.git_blob_sha1(data), "size_bytes": len(data)}

            manifest = {
                "deterministic_evaluators": [{
                    "id": "E-T05B-DATA-TO-FIGURE",
                    "repository": "owner/" + slug,
                    "generator": {"path": generator_rel, **identity(generator)},
                    "model_visible_inputs": [
                        {"path": csv_rel, **identity(csv_path)},
                        {"path": minima_rel, **identity(minima_path)},
                    ],
                    "evaluator_only_reference_outputs": [
                        {"path": output_rel + "/fixed_speed_xe131_dsigma_450kev.svg", **identity(golden_dir / "fixed_speed_xe131_dsigma_450kev.svg")},
                        {"path": output_rel + "/xe131_gcn_jj55_response_ratio_450kev.svg", **identity(golden_dir / "xe131_gcn_jj55_response_ratio_450kev.svg")},
                    ],
                }]
            }
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            submitted_root.mkdir()
            (submitted_root / "fixed_speed_xe131_dsigma_450kev.svg").write_text(svg_a, encoding="utf-8")
            (submitted_root / "xe131_gcn_jj55_response_ratio_450kev.svg").write_text(svg_b, encoding="utf-8")

            passed = verifier.verify_figure_regeneration(
                manifest_path, model_root, golden_root,
                generated_output_root=generated_root,
                submitted_output_root=submitted_root,
            )
            self.assertEqual(passed["status"], "PASS")
            self.assertTrue(passed["submission_pass"])

            (submitted_root / "fixed_speed_xe131_dsigma_450kev.svg").write_text(svg_a + " ", encoding="utf-8")
            failed = verifier.verify_figure_regeneration(
                manifest_path, model_root, golden_root,
                generated_output_root=generated_root,
                submitted_output_root=submitted_root,
            )
            self.assertEqual(failed["status"], "FAIL")
            self.assertFalse(failed["submission_pass"])


if __name__ == "__main__":
    unittest.main()
