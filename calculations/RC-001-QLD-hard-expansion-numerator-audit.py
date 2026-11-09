#!/usr/bin/env python3
"""QLD one-background hard-region degree-five radial-reduction audit.

For Gamma^mu = p^mu F_p + q^mu F_q, explicit-vector coefficients need
scalar degree four. A free loop-vector term k^mu instead needs scalar degree
five, because its angular average pairs one k with an external momentum.
All shifted propagators are expanded and all angular averages are d-dimensional.
The script evaluates radial masters through O(eps^0), but does not include
overall Wick/Feynman-rule factors or perform EFT-soft subtraction.
"""
import sympy as sp

d, eps, M2 = sp.symbols("d eps M2")
k2, kq, kp, kpp = sp.symbols("k2 kq kp kpp")
p2, q2, pp2, pq, ppdotp = sp.symbols("p2 q2 pp2 pq ppdotp")
L_M = sp.symbols("L_M")

# Numerator coefficients, N^mu=2*(coefficients).
NL = {"k": k2+2*kp+pq, "p": -(k2+kq), "q": k2+kp}
NE = {"k": k2+M2-ppdotp, "p": k2+kpp, "pp": k2+kp}

DOT = {
    ("p","p"):p2, ("q","q"):q2, ("pp","pp"):pp2,
    ("p","q"):pq, ("q","p"):pq,
    ("p","pp"):ppdotp, ("pp","p"):ppdotp,
}
def pairings(labels):
    labels=tuple(labels)
    if not labels:
        return {sp.Integer(1):1}
    out={}
    first=labels[0]
    for j in range(1,len(labels)):
        second=labels[j]
        rest=labels[1:j]+labels[j+1:]
        dot=DOT[(first,second)]
        for product,mult in pairings(rest).items():
            term=sp.expand(dot*product)
            out[term]=out.get(term,0)+mult
    return out

def angular_denominator(r):
    return d*sp.prod(d+2*j for j in range(1,r))

def reduce_graph(kind,component,numerator):
    if kind=="L":
        vectors=["q","p"]; kvars=[kq,kp]
        shifts=[2*kq+q2,2*kp+p2]
        base_a,base_b=2,1
    else:
        vectors=["p","pp"]; kvars=[kp,kpp]
        shifts=[2*kp+p2,2*kpp+pp2]
        base_a,base_b=1,2

    # The free k^mu index is converted to an external vector by angular
    # averaging, so its scalar coefficient must carry degree five.
    target=5 if component=="k" else 4
    result={}
    poly_vars=[k2,*kvars,p2,q2,pp2,pq,ppdotp]
    for n in range(5):
        for m in range(5-n):
            polynomial=(-1)**(n+m)*sp.expand(shifts[0]**n*shifts[1]**m*numerator)
            poly=sp.Poly(polynomial,*poly_vars,domain="EX")
            for mon,coeff in poly.terms():
                ex=dict(zip(poly_vars,mon))
                degree=ex[kvars[0]]+ex[kvars[1]]+2*sum(
                    ex[s] for s in [p2,q2,pp2,pq,ppdotp]
                )
                if degree!=target:
                    continue
                labels=[vectors[0]]*ex[kvars[0]]+[vectors[1]]*ex[kvars[1]]
                scalar=coeff
                for sym in [p2,q2,pp2,pq,ppdotp]:
                    scalar*=sym**ex[sym]

                # Light graph: q shift belongs to the massless denominator;
                # p shift belongs to the massive denominator.
                if kind=="L":
                    a,b=base_a+n,base_b+m
                else:
                    a,b=base_a,base_b+n+m

                if component=="k":
                    if len(labels)%2!=1:
                        continue
                    r=(len(labels)+1)//2
                    den=angular_denominator(r)
                    for i,vec in enumerate(labels):
                        rest=labels[:i]+labels[i+1:]
                        for product,mult in pairings(rest).items():
                            key=(vec,a,b,ex[k2]+r)
                            result[key]=result.get(key,0)+2*scalar*mult*product/den
                else:
                    if len(labels)%2:
                        continue
                    r=len(labels)//2
                    den=angular_denominator(r) if r else 1
                    product=sum(mult*term for term,mult in pairings(tuple(labels)).items())
                    key=(component,a,b,ex[k2]+r)
                    result[key]=result.get(key,0)+2*scalar*product/den
    return {key:sp.factor(value) for key,value in result.items() if value!=0}

L={c:reduce_graph("L",c,n) for c,n in NL.items()}
E={c:reduce_graph("E",c,n) for c,n in NE.items()}
assert len(L["k"])==31 and len(L["p"])==12 and len(L["q"])==12
assert len(E["k"])==14 and len(E["p"])==3 and len(E["pp"])==3

def combine_vectors(graph):
    out={"p":{},"q":{},"pp":{}}
    for component_dict in graph.values():
        for (vec,a,b,t),coefficient in component_dict.items():
            key=(a,b,t)
            out[vec][key]=out[vec].get(key,0)+coefficient
    return {vec:{key:sp.factor(val) for key,val in dic.items() if val!=0}
            for vec,dic in out.items()}

Lvec=combine_vectors(L)
Evec=combine_vectors(E)
masters=sorted(set(
    key for graph in (Lvec,Evec) for component in graph.values() for key in component
))
expected=[
    (1,4,1),(1,5,1),(1,5,2),(1,6,2),(1,6,3),(1,7,3),(1,7,4),
    (2,3,1),(2,4,2),(2,5,3),(2,6,4),
    (3,2,1),(3,3,2),(3,4,3),(3,5,4),
    (4,1,1),(4,2,2),(4,3,3),(4,4,4),
    (5,1,2),(5,2,3),(5,3,4),(6,1,3),(6,2,4),(7,1,4)
]
assert masters==expected
for a,b,t in masters:
    uv_arg=a+b-2-t
    ir_arg=2+t-a
    assert uv_arg>0
    print(f"J[{a},{b},{t}]: UV finite; IR gamma argument={ir_arg} at eps=0")

def J_msbar(a,b,t):
    expr=(
        sp.exp(eps*(L_M-sp.log(4*sp.pi)+sp.EulerGamma))
        /(4*sp.pi)**(2-eps)
        *M2**(2+t-a-b)
        *sp.gamma(2-eps+t-a)
        *sp.gamma(a+b-2+eps-t)
        /(sp.gamma(2-eps)*sp.gamma(b))
    )
    return sp.series(expr,eps,0,1).removeO()

def sum_form_factor(radial_terms):
    total=0
    for (a,b,t),coefficient in radial_terms.items():
        total+=coefficient.subs(d,4-2*eps)*J_msbar(a,b,t)
    return sp.series(sp.expand(total),eps,0,1).removeO()

def pole_and_finite(expr):
    pole=sp.factor(sp.limit(eps*expr,eps,0))
    finite=sp.factor(sp.limit(expr-pole/eps,eps,0))
    return pole,finite

LP=sum_form_factor(Lvec["p"])
LQ=sum_form_factor(Lvec["q"])
EP=sum_form_factor(Evec["p"])
EPP=sum_form_factor(Evec["pp"])
LPpole,LPfinite=pole_and_finite(LP)
LQpole,LQfinite=pole_and_finite(LQ)
EPpole,EPfinite=pole_and_finite(EP)
EPPpole,EPPfinite=pole_and_finite(EPP)

P,Q,R,PP,T=sp.symbols("P Q R PP T")
sub={p2:P,q2:Q,pq:R,pp2:PP,ppdotp:T}
assert sp.simplify(LPpole.subs(sub)-Q*(P-R)/(24*sp.pi**2*M2**2))==0
assert sp.simplify(LQpole.subs(sub)+R*(P-R)/(24*sp.pi**2*M2**2))==0
assert EPpole==0 and EPPpole==0
assert sp.simplify((R*LPpole+Q*LQpole).subs(sub))==0

print("PASS: scalar form factors degree four plus one external vector give degree five.")
print("PASS: all shifted propagators expanded with correct radial indices.")
print("PASS: 25 distinct radial masters; all UV convergent in the hard region.")
print("PASS: L attachment 31 k-vector, 12 p-vector, 12 q-vector structures.")
print("PASS: E attachment 14 k-vector, 3 p-vector, 3 p'-vector structures.")
print("PASS: hard light-attachment IR pole is transverse: R*F_p^pole+Q*F_q^pole=0.")
print("L attachment F_p pole:",LPpole.subs(sub))
print("L attachment F_p finite:",LPfinite.subs(sub))
print("L attachment F_q pole:",LQpole.subs(sub))
print("L attachment F_q finite:",LQfinite.subs(sub))
print("E attachment F_p finite:",EPfinite.subs(sub))
print("E attachment F_pprime finite:",EPPfinite.subs(sub))
print("SCOPE: subgraph hard form factors only; common Wick/Feynman-rule factors and EFT-soft matching remain open.")
