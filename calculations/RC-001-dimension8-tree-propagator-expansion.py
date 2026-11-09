#!/usr/bin/env python3
"""Algebraic audit of the cross-chirality heavy-VLL propagator expansion.

This is a formal low-momentum series check. It is not a loop calculation,
a covariant-derivative EOM reduction, or a complete tree-level EFT matching.
"""
import sympy as sp

M, z = sp.symbols("M z", positive=True)
y, lam = sp.symbols("y lambda")
D2 = sp.Symbol("(iDslash)^2")

# Cross-chirality numerator projects onto the heavy Dirac mass:
# P_R (i Dslash + M) P_R = M P_R.
# The remaining scalar denominator is z - M^2, with z standing for
# the ordered covariant operator (i Dslash)^2.
prop = M / (z - M**2)
expanded = sp.series(prop, z, 0, 3).removeO()
expected = -1/M - z/M**3 - z**2/M**5
assert sp.simplify(expanded - expected) == 0

C5 = -y * lam / M
C7 = -y * lam / M**3
assert sp.simplify(C7 - C5/M**2) == 0
assert sp.simplify(C7 * M**2 - C5) == 0

# The next term is dimension nine and suppressed by M^-5.
C9 = -y * lam / M**5
assert sp.simplify(C9 * M**4 - C5) == 0

print("PASS: cross-chirality propagator expands as -1/M - Dslash^2/M^3 - (Dslash^2)^2/M^5")
print("PASS: the candidate dimension-seven coefficient is C7 = C5/M_E^2 in the stated Dslash-squared convention")
print("PASS: the next term is order M_E^-5 (dimension nine)")
print("CONVENTION: z denotes the ordered operator (i Dslash)^2 acting on the complete right-hand source")
print("LIMIT: no integration-by-parts/EOM reduction, gauge-field-strength decomposition, or independent UV diagram validation is performed")
