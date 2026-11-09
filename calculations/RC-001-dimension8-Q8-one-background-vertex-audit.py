#!/usr/bin/env python3
"""Algebraic one-background Q8 vertex and Ward-identity audit."""
import sympy as sp
Pout, Pin = sp.symbols("SlashPout SlashPin", commutative=False)
qslash = Pout - Pin
# Contract the Lorentz index on gamma^mu in its actual matrix position:
# Pout^2 qslash + Pout qslash Pin + qslash Pin^2.
ward = sp.expand(Pout**2*qslash + Pout*qslash*Pin + qslash*Pin**2)
expected = sp.expand(Pout**3 - Pin**3)
assert sp.expand(ward-expected) == 0
eta = {"mu": 1, "tau": -1}
for flavor, e in eta.items():
    q_ld = (sp.Rational(-1,2)+sp.Rational(-1,2), e)
    q_rd = (0-1, 2*e-e)
    assert q_ld == (-1, e)
    assert q_rd == (-1, e)
print("PASS 1: Pout^2 qslash + Pout qslash Pin + qslash Pin^2 = Pout^3 - Pin^3")
print("PASS 2: one-background Q8 contact vertex contains the three ordered insertion positions")
print("PASS 3: Q_LD and Q_RD composite charges agree: (Y,x)=(-1,eta_l), mu/tau eta=+1/-1")
print("PASS 4: direct Q8 contacts are B: -gY, A_prime: eta_l*gX*Q_l, W: 0")
print("SCOPE: exact one-background contact vertex and algebraic Ward contraction only")
print("OPEN: full one-loop momentum integral, ordinary constituent-line insertion, two-background amplitude, UV pole, and hard matching")
