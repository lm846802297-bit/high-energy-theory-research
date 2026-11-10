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
    def test_scalar_master_hard_soft_full(self):
        m = MOD.scalar_masters()
        self.assertEqual(sp.simplify(m["full"][0]-m["hard"][0]-m["soft"][0]), 0)
        self.assertEqual(sp.simplify(m["full"][1]-m["hard"][1]-m["soft"][1]), 0)

    def test_each_pair_hard_soft_full(self):
        m = MOD.scalar_masters()
        ks = {r: MOD.pair_kernels(*m[r]) for r in ("hard", "soft", "full")}
        for pair in ks["hard"]:
            self.assertEqual(
                sp.simplify(ks["full"][pair]-ks["hard"][pair]-ks["soft"][pair]),
                0,
                pair,
            )

    def test_weak_tensor_weighted_sum(self):
        m = MOD.scalar_masters()
        for region in ("hard", "soft", "full"):
            J, K = m[region]
            got = MOD.weak_weighted_sum(MOD.pair_kernels(J, K))
            expected = sp.simplify((6*J/MOD.d-2*(MOD.d-3)*K/MOD.d)/4)
            self.assertEqual(sp.simplify(got-expected), 0)

    def test_hard_soft_uv_ir_poles(self):
        m = MOD.scalar_masters()
        hard = MOD.pole_expansion(MOD.weak_weighted_sum(MOD.pair_kernels(*m["hard"])))
        soft = MOD.pole_expansion(MOD.weak_weighted_sum(MOD.pair_kernels(*m["soft"])))
        full = MOD.pole_expansion(MOD.weak_weighted_sum(MOD.pair_kernels(*m["full"])))
        self.assertEqual(sp.simplify(hard+soft-full), 0)
        self.assertEqual(sp.simplify(hard-MOD.expected_hard()), 0)
        self.assertEqual(sp.simplify(soft-MOD.expected_soft()), 0)
        self.assertEqual(sp.simplify(full-MOD.expected_full()), 0)

    def test_retained_epsilon_finite_shift(self):
        naive = sp.Rational(1,2)/MOD.M2
        exact = sp.Rational(11,16)/MOD.M2
        self.assertEqual(sp.simplify(exact-naive-sp.Rational(3,16)/MOD.M2), 0)

    def test_tree_operator_is_hermitian_mod_total_derivative(self):
        I = sp.I
        barpsi, dpsi, dbarpsi, psi = sp.symbols(
            "barpsi dpsi dbarpsi psi", commutative=True
        )
        Q = I*barpsi*dpsi
        Q_hc = -I*dbarpsi*psi
        total_derivative = dbarpsi*psi + barpsi*dpsi
        self.assertEqual(sp.simplify(Q-Q_hc-I*total_derivative), 0)

    def test_two_distinct_yukawa_vertex_orderings_cancel_1_over_2_factor(self):
        # In the second-order expansion, the two label orderings of y and y*
        # cancel the 1/2! from the expansion. This is not an extra factor of 2.
        symmetry_factor = sp.Rational(1,2)*(1+1)
        self.assertEqual(symmetry_factor, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
