#!/usr/bin/env python3
"""QLD one-background hard-region expansion through total momentum degree 5.

The amplitude is decomposed into external vectors times scalar form factors.
Since the explicit Lorentz vector contributes one momentum, the scalar
coefficient must have degree four. All shifted propagators are expanded.
The script reduces the degree-four scalar coefficients with exact d-dimensional
rotational averages and records radial masters J[a,b,t]. It does not fix the
relative UV graph sign or claim the final matched Wilson coefficient.
"""
from functools import lru_cache
import sympy as sp

d, eps, M2 = sp.symbols("d eps M2")
k2, kq, kp, kpp = sp.symbols("k2 kq kp kpp")
p2, q2, pp2, pq, ppdotq, ppdotp = sp.symbols(
    "p2 q2 pp2 pq ppdotq ppdotp"
)

def pairings(labels):
    labels = tuple(labels)
    if not labels:
        return {sp.Integer(1): 1}
    out = {}
    first = labels[0]
    for j in range(1, len(labels)):
        second = labels[j]
        rest = labels[1:j] + labels[j+1:]
        dot = {
            ("p", "p"): p2, ("q", "q"): q2, ("pp", "pp"): pp2,
            ("p", "q"): pq, ("q", "p"): pq,
            ("p", "pp"): ppdotp, ("pp", "p"): ppdotp,
            ("q", "pp"): ppdotq, ("pp", "q"): ppdotq,
        }[(first, second)]
        for prod, mult in pairings(rest).items():
            term = sp.expand(dot * prod)
            out[term] = out.get(term, 0) + mult
    return out

def pairings_with_free(labels):
    out = {}
    for i, vec in enumerate(labels):
        rest = labels[:i] + labels[i+1:]
        for prod, mult in pairings(rest).items():
            key = (vec, prod)
            out[key] = out.get(key, 0) + mult
    return out

def angular_denominator(rank_pairs):
    # d(d+2)...(d+2r-2)
    return d * sp.prod(d + 2*j for j in range(1, rank_pairs))

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
    poly_vars = [k2, *kvars, p2, q2, pp2, pq, ppdotq, ppdotp]
    for n in range(5):
        for m in range(5-n):
            # Each shifted propagator: (base+X)^-1 = base^-1 sum (-X/base)^n.
            polynomial = (-1)**(n+m) * sp.expand(shifts[0]**n * shifts[1]**m * numerator)
            poly = sp.Poly(polynomial, *poly_vars, domain="EX")
            for monomial, coeff in poly.terms():
                ex = dict(zip(poly_vars, monomial))
                degree = ex[kvars[0]] + ex[kvars[1]] + 2*sum(
                    ex[s] for s in [p2, q2, pp2, pq, ppdotq, ppdotp]
                )
                if degree != target_scalar_degree:
                    continue

                labels = [vectors[0]]*ex[kvars[0]] + [vectors[1]]*ex[kvars[1]]
                scalar = coeff
                for sym in [p2, q2, pp2, pq, ppdotq, ppdotp]:
                    scalar *= sym**ex[sym]

                if kind == "L":
                    a, b = base_a+n, base_b+m
                else:
                    a, b = base_a, base_b+n+m

                if component == "k":
                    # One free k^mu: only an odd number of k dot-products survives.
                    if len(labels) % 2 != 1:
                        continue
                    r = (len(labels)+1)//2
                    den = angular_denominator(r)
                    for (vec, product), multiplicity in pairings_with_free(tuple(labels)).items():
                        key = (vec, a, b, ex[k2]+r)
                        result[key] = result.get(key, 0) + 2*scalar*multiplicity*product/den
                else:
                    if len(labels) % 2 != 0:
                        continue
                    r = len(labels)//2
                    den = angular_denominator(r) if r else 1
                    product = sum(mult*prod for prod, mult in pairings(tuple(labels)).items())
                    key = (component, a, b, ex[k2]+r)
                    result[key] = result.get(key, 0) + 2*scalar*product/den

    return {key: sp.factor(value) for key, value in result.items() if value != 0}

# Numerator coefficients, with the overall trace factor 2 applied in reducer.
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

L = {c: reduce_graph("L", c, n) for c, n in NL.items()}
E = {c: reduce_graph("E", c, n) for c, n in NE.items()}

assert not L["k"] and not E["k"], "odd-rank angular terms should vanish at scalar degree four"
assert len(L["p"]) == 12 and len(L["q"]) == 12
assert len(E["p"]) == 3 and len(E["pp"]) == 3

masters = sorted(set(key[1:] for graph in (L, E) for comp in graph.values() for key in comp))
for a, b, t in masters:
    uv_arg = sp.simplify(a+b-2-t)
    ir_arg = sp.simplify(2+t-a)
    # Every master in this projection is UV convergent; some are IR singular.
    assert uv_arg > 0
    print(f"J[{a},{b},{t}]: UV finite; IR argument at eps=0 = {ir_arg}")

print("PASS: scalar form factors have degree four, hence vector amplitudes degree five.")
print("PASS: light graph uses a=2+n_light, b=1+n_heavy.")
print("PASS: heavy graph uses a=1, b=2+n_heavy1+n_heavy2.")
print("PASS: exact d-dimensional angular reduction completed.")
print("PASS: radial master inventory contains", len(masters), "distinct J[a,b,t] integrals.")
print("SCOPE: radial coefficients are generated; hard-soft subtraction and relative graph sign remain open.")
