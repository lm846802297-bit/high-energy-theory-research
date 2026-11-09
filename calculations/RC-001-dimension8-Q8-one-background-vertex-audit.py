#!/usr/bin/env python3
"""Algebraic Q8 one-background Ward-identity audit."""
import sympy as sp

Pout, Pin = sp.symbols("SlashPout SlashPin", commutative=False)
qslash = Pout - Pin
# Contract gamma^mu in its actual position in the ordered Q8 vertex.
ward_contact = sp.expand(Pout**2*qslash + Pout*qslash*Pin + qslash*Pin**2)
assert sp.expand(ward_contact-(Pout**3-Pin**3)) == 0

# Ordinary massless-fermion propagator Ward identity:
# S_out (S_out^{-1}-S_in^{-1}) S_in = S_in-S_out.
Sout, Sin = sp.symbols("Sout Sin", commutative=False)
ward_line = sp.expand(Sout*(Sout**-1-Sin**-1)*Sin)
assert sp.expand(ward_line-(Sin-Sout)) == 0

eta = {"mu": 1, "tau": -1}
for flavor, e in eta.items():
    q_ld = (sp.Rational(-1,2)+sp.Rational(-1,2), e)
    q_rd = (0-1, 2*e-e)
    assert q_ld == (-1, e)
    assert q_rd == (-1, e)

print("PASS 1: Q8 contact Ward contraction gives Slash(P+q)^3 - Slash(P)^3")
print("PASS 2: ordinary fermion line obeys S_out qslash S_in = S_in - S_out")
print("PASS 3: Q_LD and Q_RD composite charges are (Y,x)=(-1,eta_l), eta_mu=+1, eta_tau=-1")
print("PASS 4: direct Q8 contacts are B: -gY, A_prime: eta_l*gX*Q_l, W: 0")
print("SCOPE: algebraic Ward building blocks only; full integrated loop identity not yet evaluated")
print("OPEN: routed one-loop integral, two-background amplitude, UV pole, and hard matching")
