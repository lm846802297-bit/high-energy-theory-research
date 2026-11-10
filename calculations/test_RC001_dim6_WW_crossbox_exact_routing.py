#!/usr/bin/env python3
import importlib.util
import pathlib
import sympy as sp
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "RC-001-dim6-WW-crossbox-exact-routing.py"
SPEC = importlib.util.spec_from_file_location("rc001_ww_routing", SOURCE)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class TestRC001Dim6WWCrossboxExactRouting(unittest.TestCase):
    def test_explicit_numerator_denominator_reductions(self):
        derived = MOD.derive_pair_integrands()
        Jden = 1/(MOD.x**2*(MOD.x-MOD.M2_local))
        Kden = 1/(MOD.x*(MOD.x-MOD.M2_local)**2)
        expected = {
            "LD-W-01": 2*(MOD.d-2)*Kden/MOD.d,
            "LD-W-02": -Jden+2*Kden/MOD.d,
            "LD-W-05": 2*(1-1/MOD.d)*Jden-2*Kden/MOD.d,
            "LD-W-06": -Jden+2*Kden/MOD.d,
        }
        for pair, (actual, _, _) in derived.items():
            self.assertEqual(sp.simplify(actual-expected[pair]), 0, pair)

    def test_pair02_equals_pair06_by_q2_cancellation(self):
        derived = MOD.derive_pair_integrands()
        self.assertEqual(
            sp.simplify(derived["LD-W-02"][0]-derived["LD-W-06"][0]), 0
        )

    def test_integrated_pair_kernels(self):
        J, K = sp.symbols("J K")
        got = MOD.derive_pair_kernels(J, K)
        expected = {
            "LD-W-01": 2*(MOD.d-2)*K/MOD.d,
            "LD-W-02": -J+2*K/MOD.d,
            "LD-W-05": 2*(1-1/MOD.d)*J-2*K/MOD.d,
            "LD-W-06": -J+2*K/MOD.d,
        }
        for pair in expected:
            self.assertEqual(sp.simplify(got[pair]-expected[pair]), 0, pair)

    def test_weak_weighted_sum_collapses_to_J_minus_K(self):
        J, K = sp.symbols("J K")
        got = MOD.weak_weighted_sum(MOD.derive_pair_kernels(J, K))
        self.assertEqual(
            sp.simplify(got-(MOD.d-1)*(J-K)/(2*MOD.d)), 0
        )

    def test_scalar_master_hard_soft_full(self):
        m = MOD.scalar_masters()
        self.assertEqual(sp.simplify(m["full"][0]-m["hard"][0]-m["soft"][0]), 0)
        self.assertEqual(sp.simplify(m["full"][1]-m["hard"][1]-m["soft"][1]), 0)

    def test_each_pair_hard_soft_full(self):
        m = MOD.scalar_masters()
        ks = {
            region: MOD.derive_pair_kernels(*m[region])
            for region in ("hard", "soft", "full")
        }
        for pair in ks["hard"]:
            self.assertEqual(
                sp.simplify(ks["full"][pair]-ks["hard"][pair]-ks["soft"][pair]),
                0,
                pair,
            )

    def test_uv_ir_pole_bookkeeping(self):
        m = MOD.scalar_masters()
        sums = {
            region: MOD.weak_weighted_sum(MOD.derive_pair_kernels(*m[region]))
            for region in ("hard", "soft", "full")
        }
        hard = MOD.pole_expansion(sums["hard"])
        soft = MOD.pole_expansion(sums["soft"])
        full = MOD.pole_expansion(sums["full"])
        self.assertEqual(sp.simplify(hard-MOD.expected_hard()), 0)
        self.assertEqual(sp.simplify(soft-MOD.expected_soft()), 0)
        self.assertEqual(sp.simplify(full-MOD.expected_full()), 0)
        self.assertEqual(sp.simplify(hard+soft-full), 0)

    def test_d_dimensional_finite_term(self):
        eps = MOD.eps
        f = sp.series((MOD.d-1)/(2*MOD.d), eps, 0, 2).removeO()
        self.assertEqual(sp.simplify(f-(sp.Rational(3,8)-eps/sp.Integer(16))), 0)
        self.assertEqual(
            sp.simplify(sp.Rational(3,8)*2-sp.Rational(1,16)-sp.Rational(11,16)),
            0,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
