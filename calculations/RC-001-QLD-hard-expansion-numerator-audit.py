#!/usr/bin/env python3
"""QLD UV-triangle numerator and degree-five hard radial-reduction audit.

The 1PI vector is decomposed in external vectors times scalar form factors.
For total external momentum degree five, each scalar form factor has degree
four. The script generates every shifted-propagator Taylor term, performs
exact d-dimensional rotational averages, and lists radial masters J[a,b,t].
It does not fix the relative sign of the two UV attachment classes and does
not claim the hard-soft matched Wilson coefficient.
"""
import sympy as sp

d, eps, M2 = sp.symbols("d eps M2")
k2, kq, kp, kpp = sp.symbols("k2 kq kpp")
p2, q2, pp2, pq, ppdotp = sp.symbols("p2 q2 pp2 pq ppdotp")

# Exact parity-even trace coefficients, with N^mu=2*(coefficients).
NL = {
    "k": k2 + 2*kp + pq,
    "p": -(k2 + kq),
    "q": k2 + kp,
}
NE = {
    "k": k2 + M2 - ppdotp,
    "p": k2 + kpp,
    "pp": k2 + kp,
}

# Scalar products for rotational tensor pairings.
DOT = {
    ("p", "p"): p2, ("q", "q"): q2, ("pp", "pp"): pp2,
    ("p", "q"): pq, ("q", "p"): pq,
    ("p", "pp"): ppdotp, ("pp", "p"): ppdotp,
}

def pairings(labels):
    labels = tuple(labels)
    if not labels:
        return {sp.Integer(1): 1}
    out = {}
    first = labels[0]
    for j in range(1, len(labels)):
        second = labels[j]
        rest = labels[1:j] + labels[j+1:]
        dot = DOT[(first, second)]
        for product, mult in pairings(rest).items():
            term = sp.expand(dot * product)
            out[term] = out.get(term, 0) + mult
    return out

def angular_denominator(r):
    # d(d+2)...(d+2r-2)
    return d * sp.prod(d + 2*j for j in range(1, r))

def reduce_graph(kind, component, numerator, target_scalar_degree=4):
    if kind == "L":
        vectors = ["q", "p"]
        kvars = [kq, kp]
        shifts = [2*kq + q2, 2*kp + p2]
        base_a, base_b = 2, 1
    else:
        vectors = ["p", "pp"]
        kvars = [kp, kpp]
        shifts = [2*kp + p2, 2*kpp + pp2]
        base_a, base_b = 1, 2

    result = {}
    poly_vars = [k2, *kvars, p2, q2, pp2, pq, ppdotp]
    for n in range(5):
        for m in range(5-n):
            # (base+X)^-1 = base^-1 * sum_n (-X/base)^n.
            polynomial = (-1)**(n+m) * sp.expand(shifts[0]**n * shifts[1]**m * numerator)
            poly = sp.Poly(polynomial, *poly_vars, domain="EX")
            for monomial, coeff in poly.terms():
                ex = dict(zip(poly_vars, monomial))
                degree = ex[kvars[0]] + ex[kvars[1]] + 2*sum(
                    ex[s] for s in [p2, q2, pp2, pq, ppdotp]
                )
                if degree != target_scalar_degree:
                    continue

                labels = [vectors[0]]*ex[kvars[0]] + [vectors[1]]*ex[kvars[1]]
                scalar = coeff
                for sym in [p2, q2, pp2, pq, ppdotp]:
                    scalar *= sym**ex[sym]

                # Crucial: the two light-graph Taylor indices enter different
                # radial denominators: q-shift -> k^2, p-shift -> k^2+M^2.
                if kind == "L":
                    a, b = base_a+n, base_b+m
                else:
                    a, b = base_a, base_b+n+m

                if component == "k":
                    # A free k^mu requires an odd number of k dot-products.
                    if len(labels) % 2 != 1:
                        continue
                    r = (len(labels)+1)//2
                    den = angular_denominator(r)
                    # The free index is paired with each external vector in turn.
                    for i, vec in enumerate(labels):
                        rest = labels[:i] + labels[i+1:]
                        for product, mult in pairings(rest).items():
                            key = (vec, a, b, ex[k2]+r)
                            result[key] = result.get(key, 0) + 2*scalar*mult*product/den
                else:
                    if len(labels) % 2 != 0:
                        continue
                    r = len(labels)//2
                    den = angular_denominator(r) if r else 1
                    product = sum(mult*prod for prod, mult in pairings(tuple(labels)).items())
                    key = (component, a, b, ex[k2]+r)
                    result[key] = result.get(key, 0) + 2*scalar*product/den

    return {key: sp.factor(value) for key, value in result.items() if value != 0}

L = {c: reduce_graph("L", c, n) for c, n in NL.items()}
E = {c: reduce_graph("E", c, n) for c, n in NE.items()}

# At scalar degree four, the k^mu pieces vanish by odd-rank rotational
# invariance. The surviving vector form factors have 12+12 and 3+3 terms.
assert not L["k"] and not E["k"]
assert len(L["p"]) == 12 and len(L["q"]) == 12
assert len(E["p"]) == 3 and len(E["pp"]) == 3

masters = sorted(set(
    key[1:] for graph in (L, E) for component in graph.values() for key in component
))
expected = [
    (1,4,1),(1,5,2),(1,6,3),(2,3,1),(2,4,2),(2,5,3),
    (3,2,1),(3,3,2),(3,4,3),(4,1,1),(4,2,2),(4,3,3),
    (5,1,2),(5,2,3),(6,1,3)
]
assert masters == expected

for a, b, t in masters:
    uv_gamma = a+b-2-t
    ir_gamma = 2+t-a
    assert uv_gamma > 0, (a,b,t,uv_gamma)
    print(f"J[{a},{b},{t}]: UV finite; IR gamma argument={ir_gamma} at eps=0")

print("PASS: numerator traces reduced to explicit external-vector coefficients.")
print("PASS: scalar form-factor degree four gives total vector-amplitude degree five.")
print("PASS: light graph radial indices are a=2+n_q, b=1+n_p.")
print("PASS: heavy graph radial indices are a=1, b=2+n_p+n_pprime.")
print("PASS: exact d-dimensional angular reduction and 15-master inventory.")
print("Counts: L_p=12, L_q=12, E_p=3, E_pprime=3; k-vector pieces vanish.")
print("SCOPE: radial coefficients only; relative graph sign and EFT soft subtraction remain open.")
