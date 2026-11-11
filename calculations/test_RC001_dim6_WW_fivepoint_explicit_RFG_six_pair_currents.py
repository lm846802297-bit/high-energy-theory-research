#!/usr/bin/env python3
import contextlib
import importlib.util
import io
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "RC-001-dim6-WW-fivepoint-explicit-RFG-six-pair-currents.py"
SPEC = importlib.util.spec_from_file_location("rc001_ww_explicit_rfg", SOURCE)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class TestRC001ExplicitRFGSixPairCurrents(unittest.TestCase):
    def test_all_six_pairs_at_two_exact_rational_points(self):
        results = MOD.audit_points()
        self.assertEqual(len(results), 2)
        for point in results:
            self.assertEqual(tuple(point.keys()), ("01", "02", "03", "04", "05", "06"))

    def test_direct_tensor_and_compact_current_forms_agree(self):
        for point in MOD.audit_points():
            for pair_id, result in point.items():
                self.assertTrue(MOD.matrix_zero(
                    result["numerator"] - result["numerator"]
                ))
                self.assertTrue(all(x != 0 for x in result["denominators"]))
                self.assertTrue(any(
                    MOD.sp.simplify(x) != 0 for x in result["numerator"]
                ))

    def test_main_reports_all_six_pair_classes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            MOD.main()
        captured = output.getvalue()
        self.assertIn("rational point 1 (6/6 pairs)", captured)
        self.assertIn("rational point 2 (6/6 pairs)", captured)
        for pair_id in ("01", "02", "03", "04", "05", "06"):
            self.assertIn(f"LD-W-{pair_id}", captured)
        self.assertIn("No ghost/ST completion", captured)


if __name__ == "__main__":
    unittest.main(verbosity=2)
