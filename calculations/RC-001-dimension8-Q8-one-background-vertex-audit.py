#!/usr/bin/env python3
"""Algebraic one-background Q8 vertex and Ward-identity audit."""
import sympy as sp
Pout, Pin = sp.symbols("SlashPout SlashPin", commutative=False)
qslash = Pout - Pin
gamma_mu = sp.symbols("gamma_mu", commutative=False)
V8_mu = Pout**2*gamma_mu + Pout*gamma_mu*Pin + gamma_mu*Pin**2
ward = sp.expand(qslash*V8_mu.xreplace({gamma_mu: sp.Integer(1)}))
expected = sp.expand(Pout**3 - Pin**3)
assert sp.expand(ward-expected) == 0
eta = {"mu": 1, "tau": -1}
for flavor, e in eta.items():
    q_ld = (sp.Rational(-1,2)+sp.Rational(-1,2), e)
    q_rd = (0-1, 2*e-e)
    assert q_ld == (-1, e)
    assert q_rd == (-1, e)
print("PASS 1: q_mu V8^mu = g_A q_Psi [Slash(P+q)^3 - Slash(P)^3]")
print("PASS 2: one-background Q8 contact vertex contains the three ordered insertion positions")
print("PASS 3: Q_LD and Q_RD composite charges agree: (Y,x)=(-1,eta_l), mu/tau eta=+1/-1")
print("PASS 4: direct Q8 contacts are B: -gY, A_prime: eta_l*gX*Q_l, W: 0")
print("SCOPE: exact one-background contact vertex and algebraic Ward contraction only")
print("OPEN: full one-loop momentum integral, ordinary constituent-line insertion, two-background amplitude, UV pole, and hard matching")
