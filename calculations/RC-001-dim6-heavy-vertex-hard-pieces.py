#!/usr/bin/env python3
"""Exact symbolic checks for RC-001 heavy-line Yukawa-vertex hard sub-blocks."""
import sympy as sp

eps, delta_bar, L, eta = sp.symbols("eps delta_bar L eta")
Delta = 1/eps + delta_bar
B0 = Delta + 1 - L
dB0_exact = (4 - 2*eps) * B0
dB0 = sp.series(dB0_exact, eps, 0, 1).removeO()
expected_dB0 = 4*Delta + 2 - 4*L
assert sp.simplify(dB0 - expected_dB0) == 0

# Pair factors in the all-fields-incoming convention. For the two
# heavy-containing topologies, the oriented graph ratio is -F times its kernel.
factors = {
    "LD_B": (sp.Rational(-1, 2), sp.Rational(-1, 2)),
    "LD_X": (-1, 0),
    "LD_BX": (sp.Rational(3, 2)*eta, sp.Rational(1, 2)*eta),
    "RD_B": (-1, 0),
    "RD_X": (1, -2),
    "RD_BX": (0, 2*eta),
}
v = {name: sp.expand(-(f_ff*dB0 + f_fs*B0))
     for name, (f_ff, f_fs) in factors.items()}
expected = {
    "LD_B": sp.Rational(5, 2)*Delta + sp.Rational(3, 2) - sp.Rational(5, 2)*L,
    "LD_X": 4*Delta + 2 - 4*L,
    "LD_BX": -sp.Rational(13, 2)*eta*Delta - sp.Rational(7, 2)*eta + sp.Rational(13, 2)*eta*L,
    "RD_B": 4*Delta + 2 - 4*L,
    "RD_X": -2*Delta + 2*L,
    "RD_BX": -2*eta*Delta - 2*eta + 2*eta*L,
}
for name in factors:
    assert sp.simplify(v[name] - expected[name]) == 0, (name, v[name], expected[name])

# Both conjugate vertices give equal real factors, so the coefficient gets 2*v.
for name in factors:
    doubled = sp.expand(2*v[name])
    assert sp.simplify(doubled - 2*expected[name]) == 0
for flavor_eta in (+1, -1):
    for name in ("LD_BX", "RD_BX"):
        assert sp.simplify((v[name] - expected[name]).subs(eta, flavor_eta)) == 0

# Matching-scale finite parts are evaluated only after separating Delta_UV.
finite = {name: sp.expand(expr.subs({Delta: 0, L: 0}))
          for name, expr in expected.items()}
assert finite["LD_B"] == sp.Rational(3, 2)
assert finite["LD_X"] == 2
assert finite["LD_BX"] == -sp.Rational(7, 2)*eta
assert finite["RD_B"] == 2
assert finite["RD_X"] == 0
assert finite["RD_BX"] == -2*eta

print("d*B0 = 4*Delta_UV + 2 - 4*L: PASS")
print("All six one-vertex hard factors: PASS")
print("Conjugate-vertex doubling: PASS")
print("Mixed factors for eta_mu=+1 and eta_tau=-1: PASS")
print("Matching-scale finite sub-blocks: PASS")
print("SCOPE: vertex sub-block only; no full Wilson coefficients or diagram-level validation.")
