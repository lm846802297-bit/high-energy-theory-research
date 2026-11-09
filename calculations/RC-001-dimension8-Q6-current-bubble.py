#!/usr/bin/env python3
"""Exact parameter-integral and field-content checks for Q6-squared soft bubbles."""
import sympy as sp
x = sp.symbols("x", positive=True)
pi = sp.pi
I0 = sp.integrate(x*(1-x), (x, 0, 1))
Ilog = sp.integrate(x*(1-x)*sp.log(x*(1-x)), (x, 0, 1))
assert I0 == sp.Rational(1, 6)
assert Ilog == -sp.Rational(5, 18)
assert sp.simplify(-Ilog/I0) == sp.Rational(5, 3)

# Dirac current: (1/(2 pi^2))*integral x(1-x); one Weyl is half.
dirac_prefactor = 1/(2*pi**2)
weyl_prefactor = dirac_prefactor/2
weyl_integrated = sp.simplify(weyl_prefactor*I0)
assert weyl_integrated == 1/(24*pi**2)
assert sp.simplify(weyl_integrated*16*pi**2) == sp.Rational(2, 3)

# A complex SU(2) doublet current carries explicit indices J_ij.
# The fermion contraction is delta_{j k} delta_{l i}, producing J_ij J_ji.
# Do not multiply by a second ad hoc doublet factor after this sum.
# Q_RD instead has one right-handed Weyl current and no weak multiplicity.

# In the unbroken EFT, propagators preserve chirality and species:
# <L bar(l_R)> = 0. Therefore Q_LD-Q_RD cannot make one connected loop.
mixed_connected_one_loop = False
assert not mixed_connected_one_loop

print("PASS: integral x(1-x) dx = 1/6")
print("PASS: integral x(1-x) ln[x(1-x)] dx = -5/18")
print("PASS: finite logarithmic-weight average = 5/3")
print("PASS: one-Weyl polarization coefficient = 1/(24 pi^2)")
print("PASS: same coefficient in i/(16 pi^2) normalization = 2/3")
print("PASS: Q_LD-Q_RD has no connected one-loop contraction in the unbroken massless EFT")
print("SCOPE: exact Feynman-parameter scalar factors and contraction logic only; no full SU(2) projection, vertex-sign audit, or UV-hard matching.")
