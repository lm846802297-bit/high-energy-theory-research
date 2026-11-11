#!/usr/bin/env python3
"""RC-001 B2c-IVc: exact Lorentz endpoint and scalar-seagull audit.

This script checks the Lorentz algebra of the external-W insertions before
loop integration. It does not perform the full weak-index/phase-weighted
24-graph sum and does not claim a complete Slavnov-Taylor identity.

Index convention in the three-W chain:
  D^{mu nu}(k) = g^{mu nu}/k^2,
  K_{mu nu}(k) = k^2 g_{mu nu} - k_mu k_nu,
  R_FG^{mu nu} = [k^mu k^nu-(k+q)^mu(k+q)^nu]/[k^2(k+q)^2].
Thus the propagator chain is D^{mu alpha}(k+q) K_{alpha beta} D^{beta nu}(k).
"""
from itertools import product
import sympy as sp

I = sp.I
ETA = (1, -1, -1, -1)
SIGMA = (
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, -I], [I, 0]]),
    sp.Matrix([[1, 0], [0, -1]]),
)
GAMMA = [sp.diag(1, 1, -1, -1)]
for sigma in SIGMA:
    GAMMA.append(sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(2), sigma),
        sp.Matrix.hstack(-sigma, sp.zeros(2)),
    ))
METRIC = sp.diag(*ETA)


def dot(a, b):
    return sp.expand(sum(ETA[i] * a[i] * b[i] for i in range(4)))


def slash(a):
    return sum((ETA[i] * a[i] * GAMMA[i] for i in range(4)), sp.zeros(4))


def matrix_zero(m):
    return all(sp.simplify(m[i, j]) == 0
               for i in range(m.rows) for j in range(m.cols))


def metric(mu, nu):
    return sp.Integer(ETA[mu]) if mu == nu else sp.Integer(0)


def K_down(mu, nu, p):
    """K_{mu nu}=p^2 g_{mu nu}-p_mu p_nu."""
    return sp.expand(
        dot(p, p) * metric(mu, nu)
        - ETA[mu] * p[mu] * ETA[nu] * p[nu]
    )


def gamma3(alpha, mu, nu, q, k):
    """Gamma_{alpha mu nu}(q,k,-k-q), all momenta incoming."""
    return (
        metric(alpha, mu) * ETA[nu] * (q[nu] - k[nu])
        + metric(mu, nu) * ETA[alpha] * (2*k[alpha] + q[alpha])
        + metric(nu, alpha) * ETA[mu] * (-k[mu] - 2*q[mu])
    )


def verify_fermion_endpoints():
    q = list(sp.symbols("qF0:4", real=True))
    r = list(sp.symbols("rF0:4", real=True))
    r_w = r
    r_y_a = [r[i] - q[i] for i in range(4)]
    r_y_b = [r[i] + q[i] for i in range(4)]

    # A orientation: (-slash rW) slash q (-slash rY) over both denominators.
    lhs_a = slash(r_w) * slash(q) * slash(r_y_a) / (
        dot(r_w, r_w) * dot(r_y_a, r_y_a)
    )
    rhs_a = slash(r_y_a) / dot(r_y_a, r_y_a) - slash(r_w) / dot(r_w, r_w)
    assert matrix_zero(lhs_a - rhs_a), "A fermion endpoint"

    # B orientation: slash rY slash q slash rW over both denominators.
    lhs_b = slash(r_y_b) * slash(q) * slash(r_w) / (
        dot(r_y_b, r_y_b) * dot(r_w, r_w)
    )
    rhs_b = slash(r_w) / dot(r_w, r_w) - slash(r_y_b) / dot(r_y_b, r_y_b)
    assert matrix_zero(lhs_b - rhs_b), "B fermion endpoint"
    return 16, 16


def verify_scalar_endpoints():
    q = list(sp.symbols("qS0:4", real=True))
    r = list(sp.symbols("rS0:4", real=True))
    r_w = r
    r_y_a = [r[i] - q[i] for i in range(4)]
    r_y_b = [r[i] + q[i] for i in range(4)]

    lhs_a = dot(q, [r_w[i] + r_y_a[i] for i in range(4)]) / (
        dot(r_w, r_w) * dot(r_y_a, r_y_a)
    )
    rhs_a = 1/dot(r_y_a, r_y_a) - 1/dot(r_w, r_w)
    assert sp.simplify(lhs_a - rhs_a) == 0

    lhs_b = dot(q, [r_w[i] + r_y_b[i] for i in range(4)]) / (
        dot(r_w, r_w) * dot(r_y_b, r_y_b)
    )
    rhs_b = 1/dot(r_w, r_w) - 1/dot(r_y_b, r_y_b)
    assert sp.simplify(lhs_b - rhs_b) == 0
    return 2


def verify_phase_weighted_scalar_seagulls():
    q = list(sp.symbols("qSG0:4", real=True))
    r = list(sp.symbols("rSG0:4", real=True))
    p_a = list(sp.symbols("pA0:4", real=True))
    p_b = list(sp.symbols("pB0:4", real=True))
    k = list(sp.symbols("kSG0:4", real=True))

    r_w = r
    r_y_a = [r[i] - q[i] for i in range(4)]
    r_y_b = [r[i] + q[i] for i in range(4)]
    d_aw = 1/dot(r_w, r_w)
    d_ay = 1/dot(r_y_a, r_y_a)
    d_bw = 1/dot(r_w, r_w)
    d_by = 1/dot(r_y_b, r_y_b)

    v_a = sp.Matrix([2*p_a[i] - k[i] for i in range(4)])
    v_b = sp.Matrix([-2*p_b[i] - k[i] for i in range(4)])
    qv = sp.Matrix(q)

    # Relative phases after factoring the common four-point skeleton:
    # ordinary scalar-line insertion -g2; seagull +g2.
    # The stripped scalar-line WTI numerators are (rW+rY) on both sides.
    a_line = -(d_ay - d_aw) * v_a
    a_seagull = d_ay * qv
    a_sum = sp.simplify(a_line + a_seagull)
    a_target = sp.simplify(d_aw*v_a - d_ay*(v_a-qv))
    assert all(sp.simplify(a_sum[i]-a_target[i]) == 0 for i in range(4))

    b_line = -(d_bw - d_by) * v_b
    b_seagull = d_by * qv
    b_sum = sp.simplify(b_line + b_seagull)
    b_target = sp.simplify(d_by*(v_b+qv) - d_bw*v_b)
    assert all(sp.simplify(b_sum[i]-b_target[i]) == 0 for i in range(4))
    return 4, 4


def verify_three_w_and_feynman_gauge_chain():
    q = list(sp.symbols("qW0:4", real=True))
    k = list(sp.symbols("kW0:4", real=True))
    kq = [k[i] + q[i] for i in range(4)]

    # q^alpha Gamma_{alpha mu nu}=K_{mu nu}(k+q)-K_{mu nu}(k).
    checks = 0
    for mu, nu in product(range(4), repeat=2):
        lhs = sp.expand(sum(
            q[alpha] * gamma3(alpha, mu, nu, q, k)
            for alpha in range(4)
        ))
        rhs = K_down(mu, nu, kq) - K_down(mu, nu, k)
        assert sp.simplify(lhs-rhs) == 0
        checks += 1

    # D^{mu alpha} K_{alpha beta} D^{beta nu}:
    # D is upper-upper, K is lower-lower, and R_FG is upper-upper.
    cov_k = sp.Matrix([ETA[i] * k[i] for i in range(4)])
    cov_kq = sp.Matrix([ETA[i] * kq[i] for i in range(4)])
    K_k = dot(k, k)*METRIC - cov_k*cov_k.T
    K_kq = dot(kq, kq)*METRIC - cov_kq*cov_kq.T
    D_k = METRIC/dot(k, k)
    D_kq = METRIC/dot(kq, kq)
    lhs_chain = sp.simplify(D_kq*(K_kq-K_k)*D_k)
    remainder = (
        sp.Matrix(k)*sp.Matrix(k).T
        - sp.Matrix(kq)*sp.Matrix(kq).T
    )/(dot(k, k)*dot(kq, kq))
    rhs_chain = D_k-D_kq+remainder
    assert matrix_zero(lhs_chain-rhs_chain)
    return checks, 16


def verify_nonzero_remainder_diagnostic():
    # One generic nonsingular point demonstrates that R_FG is not identically zero.
    k = [sp.Integer(3), sp.Integer(2), sp.Integer(0), sp.Integer(0)]
    q = [sp.Integer(1), sp.Integer(0), sp.Integer(1), sp.Integer(0)]
    kq = [k[i]+q[i] for i in range(4)]
    rem = (
        sp.Matrix(k)*sp.Matrix(k).T
        - sp.Matrix(kq)*sp.Matrix(kq).T
    )/(dot(k, k)*dot(kq, kq))
    assert any(rem[i, j] != 0 for i in range(4) for j in range(4))
    return rem


def pair_census():
    # (A type, B type, scalar seagulls, three-W insertions).
    pairs = {
        "LD-W-01": ("F", "F", 0, 1),
        "LD-W-02": ("F", "S", 1, 1),
        "LD-W-03": ("F", "S", 1, 1),
        "LD-W-04": ("S", "F", 1, 1),
        "LD-W-05": ("S", "F", 1, 1),
        "LD-W-06": ("S", "S", 2, 1),
    }
    matter = sum(2 for _ in pairs)
    seagulls = sum(v[2] for v in pairs.values())
    three_w = sum(v[3] for v in pairs.values())
    assert (matter, seagulls, three_w) == (12, 6, 6)
    return pairs, matter, seagulls, three_w


def main():
    a_f, b_f = verify_fermion_endpoints()
    scalar = verify_scalar_endpoints()
    a_sg, b_sg = verify_phase_weighted_scalar_seagulls()
    three_w, fg = verify_three_w_and_feynman_gauge_chain()
    remainder = verify_nonzero_remainder_diagnostic()
    pairs, matter, seagulls, n3w = pair_census()

    print("RC-001 B2c-IVc Lorentz endpoint audit")
    print(f"PASS: A-side fermion numerator difference ({a_f}/16 Dirac components).")
    print(f"PASS: B-side fermion numerator difference ({b_f}/16 Dirac components).")
    print(f"PASS: A/B scalar propagator differences ({scalar}/2).")
    print(f"PASS: A scalar-line + seagull vector identity ({a_sg}/4 Lorentz components).")
    print(f"PASS: B scalar-line + seagull vector identity ({b_sg}/4 Lorentz components).")
    print(f"PASS: three-W contraction ({three_w}/16 Lorentz components).")
    print(f"PASS: Feynman-gauge W-chain decomposition including R_FG ({fg}/16 components).")
    print("PASS: R_FG is generically nonzero (explicit rational diagnostic point).")
    print("PAIR CENSUS:")
    for name, (a_type, b_type, nsg, _) in pairs.items():
        print(f"  {name}: A={a_type}, B={b_type}, scalar seagulls={nsg}, three-W=1")
    print(f"TOTAL: {matter} matter-line insertions + {seagulls} scalar seagulls + {n3w} three-W insertions = 24")
    print("BOUNDARY: exact Lorentz endpoint identities and topology census only.")
    print("No complete weak-index/phase-weighted 24-graph cancellation, ghost/ST closure,")
    print("external-leg/counterterm sum, loop integration, or Wilson coefficient is claimed.")


if __name__ == "__main__":
    main()
