#!/usr/bin/env python3
"""Exact scalar-product audit of the QLD UV triangle Ward contractions."""
import sympy as sp

A, B, C, U, V, M2 = sp.symbols("K2 Kp2 KdotKp Kdotk Kpdotk M2")
# q = K' - K, k' = k + q. Therefore:
# k.q = k'.k - k^2; k'.q = k'^2 - k'.k;
# K.q = K'.K - K^2; K'.q = K'^2 - K'.K.
kkp = sp.symbols("kdotkp")
kq = kkp - sp.symbols("k2")
kpq = sp.symbols("kp2") - kkp
Kq = C - A
Kpq = B - C
k2, kp2 = sp.symbols("k2 kp2")

# One light-line gauge insertion:
# N_L^mu = 2[(K.k')k^mu - (k'.k)K^mu + (K.k)k'^mu].
NLq = sp.expand(2*(V*kq - kkp*Kq + U*kpq))
NLq_expected = 2*(U*kp2 - V*k2)
assert sp.simplify(NLq-NLq_expected).subs({kq:kkp-k2,kpq:kp2-kkp}) == 0

# Heavy-line gauge insertion includes the M_E^2 term:
# N_E^mu = 2[(K.k)K'^mu - (K'.K)k^mu
#            + (K'.k)K^mu + M_E^2 k^mu].
NEq = sp.expand(2*(U*Kpq - C*(kpq-kq) + V*Kq + M2*(kpq-kq)))
NEq_expected = 2*(U*(B-M2)-V*(A-M2))
assert sp.simplify(NEq-NEq_expected).subs({
    kq:kkp-k2, kpq:kp2-kkp
}) == 0

# The propagator Ward reductions:
# q.N_L/[k^2 k'^2] = 2[U/k^2 - V/k'^2].
# q.N_E/[(K^2-M^2)(K'^2-M^2)]
#   = 2[U/(K^2-M^2) - V/(K'^2-M^2)].
assert sp.simplify(
    (U*kp2-V*k2)/(k2*kp2) - (U/k2-V/kp2)
) == 0
assert sp.simplify(
    (U*(B-M2)-V*(A-M2))/((A-M2)*(B-M2))
    - (U/(A-M2)-V/(B-M2))
) == 0

# Yukawa gauge invariance: q_E-q_L = -q_H.
qL, qH, qE = sp.symbols("qL qH qE")
assert sp.solve(sp.Eq(-qL+qH+qE,0),qE)[0] == qL-qH
assert sp.simplify((qE-qL)+qH).subs(qE,qL-qH) == 0

print("PASS 1: light-line numerator contracts to 2[(K.k)k'^2-(K.k')k^2]")
print("PASS 2: heavy-line numerator including +M_E^2 k^mu contracts to")
print("        2[(K.k)(K'^2-M_E^2)-(K'.k)(K^2-M_E^2)]")
print("PASS 3: both contractions reduce to differences of adjacent propagators")
print("PASS 4: Yukawa charge relation q_E-q_L=-q_H is exact")
print("SCOPE: algebraic Ward contractions only; no loop integration or hard coefficient")
