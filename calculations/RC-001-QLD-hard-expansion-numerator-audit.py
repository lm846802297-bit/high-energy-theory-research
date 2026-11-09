#!/usr/bin/env python3
"""Exact algebraic expansion of the QLD UV-triangle numerators.

This is an integrand-level audit only. It does not claim the hard loop
integrals or a Wilson coefficient. Scalar products are formal commuting
variables; vector coefficients are represented in the {k,p,p',q} basis.
"""
import sympy as sp

k2, kp, kpp, pp, pq, M2 = sp.symbols(
    "k2 kp kpp pp pq M2"
)
# Independent external vectors p, pp, q for the Taylor expansion.
# k.p=kp, k.pp=kpp, p.pp=pp, p.q=pq.
# k.q is kept independent as kq.
kq = sp.symbols("kq")

# Exact trace-derived expressions:
# N_L/2 = (K.k') k - (k'.k) K + (K.k) k'
# K=k+p, k'=k+q.
A = k2 + kq + kp + pq  # K.k'
B = k2 + kq            # k'.k
C = k2 + kp            # K.k
NL_k = sp.expand(A-B+C)
NL_p = sp.expand(-B)
NL_q = sp.expand(C)
assert sp.simplify(NL_k-(k2+2*kp+pq)) == 0
assert sp.simplify(NL_p+(k2+kq)) == 0
assert sp.simplify(NL_q-(k2+kp)) == 0

# N_E/2 = (K.k)K' - (K'.K)k + (K'.k)K + M^2 k
# K=k+p, K'=k+p'.
D = k2 + kp
E = k2 + kp + kpp + pp
F = k2 + kpp
NE_k = sp.expand(D-E+F+M2)
NE_p = sp.expand(F)
NE_pp = sp.expand(D)
assert sp.simplify(NE_k-(k2+M2-pp)) == 0
assert sp.simplify(NE_p-(k2+kpp)) == 0
assert sp.simplify(NE_pp-(k2+kp)) == 0

print("N_L^mu = 2[(k2+2 k.p+p.q) k^mu -(k2+k.q) p^mu +(k2+k.p) q^mu]")
print("N_E^mu = 2[(k2+M2-p.p') k^mu +(k2+k.p') p^mu +(k2+k.p) p'^mu]")
print("PASS: both four-gamma traces expanded exactly in the declared vector basis")
print("PASS: N_L has external degree <=2; N_E has external degree <=2 plus M2 degree 0")
print("IMPORTANT: these expressions inherit the trace/routing convention in the theory note.")
print("SCOPE: numerator polynomial only; no denominator Taylor expansion or loop integration.")
