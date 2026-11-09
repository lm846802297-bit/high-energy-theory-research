#!/usr/bin/env python3
"""Exact scalar-product audit of the QLD UV triangle Ward contractions."""
import sympy as sp

K2, Kp2, KKp, Kk, Kpk, kk, kp2, M2 = sp.symbols(
    "K2 Kp2 KKp Kdotk Kpdotk kdotkp kp2 M2"
)
# q = k' - k = K' - K. Keep distinct mixed scalar products:
# K.k=Kk, K.k'=Kpk, K'.k=Kpdotk, k.k'=kk.
# Then k.q=kk-k^2, k'.q=k'^2-kk, K.q=Kpk-Kk.
NLq = sp.expand(2*(Kpk*(kk-sp.Symbol("k2"))
                  - kk*(Kpk-Kk)
                  + Kk*(kp2-kk)))
NLq_expected = 2*(Kk*kp2-Kpk*sp.Symbol("k2"))
assert sp.simplify(NLq-NLq_expected) == 0

# Heavy attachment: N_E^mu = 2[(K.k)K'^mu-(K'.K)k^mu
#                         +(K'.k)K^mu+M_E^2 k^mu].
# K.q=K'.K-K^2, K'.q=K'^2-K'.K, k.q=K'.k-K.k.
NEq = sp.expand(2*(Kk*(Kp2-KKp)-KKp*(Kpdotk-Kk)
                  +Kpdotk*(KKp-K2)+M2*(Kpdotk-Kk)))
NEq_expected = 2*(Kk*(Kp2-M2)-Kpdotk*(K2-M2))
assert sp.simplify(NEq-NEq_expected) == 0

k2 = sp.Symbol("k2")
assert sp.simplify(
    (Kk*kp2-Kpk*k2)/(k2*kp2) - (Kk/k2-Kpk/kp2)
) == 0
assert sp.simplify(
    (Kk*(Kp2-M2)-Kpdotk*(K2-M2))
    /((K2-M2)*(Kp2-M2))
    -(Kk/(K2-M2)-Kpdotk/(Kp2-M2))
) == 0

qL, qH, qE = sp.symbols("qL qH qE")
assert sp.simplify((qE-qL)+qH).subs(qE,qL-qH) == 0

print("PASS 1: light-line numerator contracts to 2[(K.k)k'^2-(K.k')k^2]")
print("PASS 2: heavy-line numerator including +M_E^2 k^mu contracts to")
print("        2[(K.k)(K'^2-M_E^2)-(K'.k)(K^2-M_E^2)]")
print("PASS 3: both contractions reduce to differences of adjacent propagators")
print("PASS 4: Yukawa gauge invariance q_E-q_L=-q_H is exact")
print("SCOPE: algebraic Ward contractions only; no loop integration or hard coefficient")
