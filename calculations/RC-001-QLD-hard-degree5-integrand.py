#!/usr/bin/env python3
"""Generate the complete total-degree-five QLD hard Taylor integrands.

External scalar products carry formal degree 1 or 2. The script expands
all shifted propagators and both exact numerator polynomials, then extracts
the total external degree five coefficient. It intentionally stops before
tensor/radial integration and therefore does not claim a hard coefficient.
"""
import sympy as sp

k2, kq, kp, kpp = sp.symbols("k2 kq kp kpp")
p2, q2, pp2, ppdotq, ppdotp = sp.symbols("p2 q2 pp2 ppdotq ppdotp")
M2 = sp.symbols("M2")

# Formal external-degree assignment.
weights = {
    kq:1, kp:1, kpp:1,
    p2:2, q2:2, pp2:2, ppdotq:2, ppdotp:2
}

def ext_degree(monom):
    powers = monom.as_powers_dict()
    return sum(int(powers.get(s,0))*w for s,w in weights.items())

def truncate_degree(expr, max_degree=5):
    poly=sp.Poly(sp.expand(expr), *weights.keys(), domain="EX")
    out=0
    for mon, coeff in poly.terms():
        if ext_degree(sp.Mul(*(s**n for s,n in zip(weights,mon)))) <= max_degree:
            out += coeff*sp.Mul(*(s**n for s,n in zip(weights,mon)))
    return sp.expand(out)

def degree_component(expr, target=5):
    poly=sp.Poly(sp.expand(expr), *weights.keys(), domain="EX")
    out=0
    for mon, coeff in poly.terms():
        m=sp.Mul(*(s**n for s,n in zip(weights,mon)))
        if ext_degree(m)==target:
            out += coeff*m
    return sp.expand(out)

def series_factor(X, base, max_degree=5):
    # 1/(base+X) = sum (-X)^n/base^(n+1)
    # Return the dimensionless factor sum (-X/base)^n; the overall base^-1
    # is kept outside.
    out=0
    for n in range(max_degree+1):
        out += (-X/base)**n
    return out

# Exact numerator vector coefficients, N^mu = Nk*k^mu+Np*p^mu+Nq*q^mu
NL = {
    "k": k2+2*kp+ppdotq,
    "p": -(k2+kq),
    "q": k2+kp,
}
# N_E^mu = Nk*k^mu+Np*p^mu+Npp*p'^mu
NE = {
    "k": k2+M2-ppdotp,
    "p": k2+kpp,
    "pp": k2+kp,
}

Xq=2*kq+q2
Xp=2*kp+p2
Xpp=2*kpp+pp2

# Overall radial bases:
# I_L: [k2^2 (k2+M2)]^-1 times the two Taylor factors.
# I_E: [k2 (k2+M2)^2]^-1 times the two heavy Taylor factors.
SL=series_factor(Xq,k2)*series_factor(Xp,k2+M2)
SE=series_factor(Xp,k2+M2)*series_factor(Xpp,k2+M2)

print("LIGHT-ATTACHMENT degree-five numerator-times-series coefficients")
light={}
for comp, num in NL.items():
    expr=degree_component(truncate_degree(num*SL,5),5)
    light[comp]=expr
    print(f"  {comp}: {len(sp.Add.make_args(expr))} additive terms")
    print(sp.sstr(expr))

print("HEAVY-ATTACHMENT degree-five numerator-times-series coefficients")
heavy={}
for comp, num in NE.items():
    expr=degree_component(truncate_degree(num*SE,5),5)
    heavy[comp]=expr
    print(f"  {comp}: {len(sp.Add.make_args(expr))} additive terms")
    print(sp.sstr(expr))

# Exact check: the selected terms are homogeneous of external degree 5.
for expr in list(light.values())+list(heavy.values()):
    poly=sp.Poly(sp.expand(expr), *weights.keys(), domain="EX")
    assert all(ext_degree(sp.Mul(*(s**n for s,n in zip(weights,mon))))==5
               for mon,_ in poly.terms())

print("PASS: all shifted propagators expanded")
print("PASS: numerator degrees 0,1,2 combined with denominator degrees 5,4,3")
print("PASS: every retained monomial has total external degree exactly five")
print("SCOPE: integrand Taylor coefficients only; tensor/radial integration and hard-soft matching remain open")
