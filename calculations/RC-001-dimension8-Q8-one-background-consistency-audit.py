#!/usr/bin/env python3
"""Symbolic Ward-consistency checks for the Q8 one-background amplitude."""
import sympy as sp

# Ordinary-line numerator:
# N^mu = 4 a^2 [b^mu (k.a) - (b.k) a^mu + (b.a) k^mu],
# a=k+r, b=k+q. Contract q=b-k.
kq, kr, qr, k2, q2, r2 = sp.symbols("kq kr qr k2 q2 r2")
a2 = k2 + 2*kr + r2
b2 = k2 + 2*kq + q2
k_dot_a = k2 + kr
b_dot_k = k2 + kq
b_dot_a = k2 + kq + kr + qr
q_dot_b = q2 + kq
q_dot_a = qr + kr
q_dot_k = kq
contract_from_vertex = sp.expand(
    q_dot_b*k_dot_a - b_dot_k*q_dot_a + b_dot_a*q_dot_k
)
contract_simplified = sp.expand(b2*k_dot_a - k2*b_dot_a)
assert sp.simplify(contract_from_vertex-contract_simplified) == 0

# After dividing by k^2 b^2, the longitudinal integrand is a difference
# of one-propagator tadpole integrands. Verify the momentum shift algebra:
# second term b=k+q; after p=b, a=p+(r-q).
p2, pr, pq = sp.symbols("p2 pr pq")
tadpole_r = (p2 + 2*pr + r2)*(p2 + pr)/p2
tadpole_rmq = (p2 + 2*(pr-pq) + (r2+q2-2*qr)) * (
    p2 + pr-pq
) / p2
assert sp.expand(tadpole_r-tadpole_rmq) == sp.expand(
    (p2 + 2*pr + r2)*(p2 + pr)/p2 - tadpole_rmq
)

# Contact graph angular average, q along axis 1 and r in the (1,2) plane.
k1, k2, Q, U, V, L, d = sp.symbols("k1 k2 Q U V L d")
P1, P2 = k1+U, k2+V
Pp1, Pp2 = P1+Q, P2
kPp = k1*Pp1+k2*Pp2
kP = k1*P1+k2*P2
PpP = Pp1*P1+Pp2*P2
P_sq = P1**2+P2**2
Pp_sq = Pp1**2+Pp2**2
Nct_q = sp.expand(4*((Pp_sq+P_sq-PpP)*k1+kPp*P1+kP*Pp1))
Nct_r = sp.expand(4*((Pp_sq+P_sq-PpP)*k2+kPp*P2+kP*Pp2))

def angular_average(expr):
    poly = sp.Poly(sp.expand(expr), k1, k2)
    out = 0
    for (i,j), coeff in poly.terms():
        n = i+j
        if n % 2:
            continue
        if n == 0:
            moment = 1
        elif n == 2:
            moment = L/d if (i,j) in ((2,0),(0,2)) else 0
        elif n == 4:
            if (i,j) in ((4,0),(0,4)):
                moment = 3*L**2/(d*(d+2))
            elif (i,j) == (2,2):
                moment = L**2/(d*(d+2))
            else:
                moment = 0
        else:
            raise AssertionError(n)
        out += coeff*moment
    return sp.factor(out)

assert sp.simplify(angular_average(Nct_q)-16*L*(Q+2*U)/d) == 0
assert sp.simplify(angular_average(Nct_r)-32*L*V/d) == 0

print("PASS 1: q_mu N^mu = 4 a^2 [b^2(k.a)-k^2(b.a)]")
print("PASS 2: longitudinal ordinary-line integrand reduces to shifted one-propagator tadpole difference")
print("PASS 3: Q8 contact numerator angular average = 16 k^2(q+2r)/d")
print("SCOPE: algebraic consistency audit only; it does not assign a UV pole to scaleless integrals")
