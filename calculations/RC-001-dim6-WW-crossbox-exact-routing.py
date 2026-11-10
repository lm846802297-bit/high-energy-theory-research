#!/usr/bin/env python3
"""Exact-rational hard/soft split for the fixed-routing Q_LD pure-WW cross boxes.

Scope:
- one fixed ordered external amplitude barL(p1) H(p2) Hdag(p3) L(p4);
- p1=p3=0, p2=P, p4=-P as a local-matching projection;
- one unit of each of the four cross-vertex attachment classes;
- Feynman gauge, d=4-2 eps, and the common scalar-master UV/IR split.

This is not a FeynArts/QGRAF diagram count and does not assign any extra
charge-conjugate/crossed-channel multiplicity beyond the stated fixed ordering.
"""
import sympy as sp

eps = sp.symbols("eps", positive=True)
DeltaUV, DeltaIR, L, M2 = sp.symbols(
    "Delta_UV Delta_IR L M_E2", real=True
)
cUV, cIR = sp.symbols("c_UV c_IR", real=True)
d = 4 - 2*eps


def scalar_masters():
    """Return the common J and K masters in hard, soft and full regions."""
    J_hard = (DeltaUV + 1 - L) / M2
    J_soft = (-DeltaUV + DeltaIR) / M2
    J_full = (DeltaIR + 1 - L) / M2

    # K = int 1/[k^2 (k^2-M_E^2)^2].
    # Its hard/full part is finite; the O(M_E^-2) soft expansion is a
    # scaleless power integral int d^d k/k^2 and vanishes in dimensional
    # regularization (there is no logarithmic 1/eps pole at this order).
    K_hard = -sp.Integer(1) / M2
    K_soft = sp.Integer(0)
    K_full = K_hard
    return {
        "hard": (J_hard, K_hard),
        "soft": (J_soft, K_soft),
        "full": (J_full, K_full),
    }


def pair_kernels(J, K):
    """Lorentz kernels for LD-W-01, 02, 05, 06 before SU(2) weights."""
    return {
        "LD-W-01": sp.simplify(2*(d-2)/d*K),
        "LD-W-02": sp.simplify(-J + 2*K/d),
        "LD-W-05": sp.simplify((1 + 2/d)*J),
        "LD-W-06": sp.simplify(-4*J/d),
    }


def weak_weighted_sum(kernels):
    """Apply the already-checked SU(2) tensors (-,+,+,-) T3/4."""
    return sp.simplify((
        -kernels["LD-W-01"]
        +kernels["LD-W-02"]
        +kernels["LD-W-05"]
        -kernels["LD-W-06"]
    ) / 4)


def pole_expansion(expr):
    """Expand with Delta_UV and Delta_IR kept as distinct pole labels."""
    # Each pole has 1/eps plus its own MS-bar constant. Keeping cUV and cIR
    # distinct preserves the UV/IR bookkeeping while retaining eps*1/eps.
    substituted = expr.subs({
        DeltaUV: 1/eps + cUV,
        DeltaIR: 1/eps + cIR,
    })
    return sp.simplify(sp.series(substituted, eps, 0, 1).removeO())


def expected_hard():
    return (
        sp.Rational(3,8)*(1/eps + cUV)
        -sp.Rational(3,8)*L
        +sp.Rational(11,16)
    ) / M2


def expected_soft():
    return sp.Rational(3,8)*(cIR-cUV)/M2


def expected_full():
    return (
        sp.Rational(3,8)*(1/eps + cIR)
        -sp.Rational(3,8)*L
        +sp.Rational(11,16)
    ) / M2


def main():
    masters = scalar_masters()
    kernels = {
        region: pair_kernels(*masters[region])
        for region in ("hard", "soft", "full")
    }
    sums = {
        region: weak_weighted_sum(kernels[region])
        for region in ("hard", "soft", "full")
    }

    # Exact pairwise UV = hard + soft decomposition.
    for pair in kernels["hard"]:
        assert sp.simplify(
            kernels["full"][pair]
            - kernels["hard"][pair]
            - kernels["soft"][pair]
        ) == 0

    JH, KH = masters["hard"]
    JS, KS = masters["soft"]
    JF, KF = masters["full"]
    assert sp.simplify(JF - JH - JS) == 0
    assert sp.simplify(KF - KH - KS) == 0

    # Closed weighted form.
    for region in ("hard", "soft", "full"):
        J, K = masters[region]
        expected = sp.simplify((6*J/d - 2*(d-3)*K/d) / 4)
        assert sp.simplify(sums[region] - expected) == 0

    # Hard/soft/full pole and finite structure.
    hard_exp = pole_expansion(sums["hard"])
    soft_exp = pole_expansion(sums["soft"])
    full_exp = pole_expansion(sums["full"])
    expected_hard = (
        sp.Rational(3,8)*(1/eps + cUV)
        -sp.Rational(3,8)*L
        +sp.Rational(11,16)
    ) / M2
    expected_soft = sp.Rational(3,8)*(cIR-cUV)/M2
    expected_full = (
        sp.Rational(3,8)*(1/eps + cIR)
        -sp.Rational(3,8)*L
        +sp.Rational(11,16)
    ) / M2
    assert sp.simplify(hard_exp - expected_hard) == 0
    assert sp.simplify(soft_exp - expected_soft) == 0
    assert sp.simplify(full_exp - expected_full) == 0
    assert sp.simplify(hard_exp + soft_exp - full_exp) == 0

    # If d is prematurely set to four, the hard finite constant is 1/2.
    # The retained (3/4 eps)*Delta_UV term contributes +3/16, giving 11/16.
    naive_d4 = sp.Rational(1,2)/M2
    exact_finite = sp.Rational(11,16)/M2
    assert sp.simplify(exact_finite-naive_d4-sp.Rational(3,16)/M2) == 0

    print("RC-001 Q_LD pure-WW cross-box exact-routing audit")
    print("External ordering: barL(p1) H(p2) Hdag(p3) L(p4)")
    print("Local projection: p1=p3=0, p2=P, p4=-P; q_E=k-P.")
    print("SU(2) weights from the independent attachment projection: (-,+,+,-) T3/4.")
    print("Per-pair Lorentz kernels:")
    print("  LD-W-01: 2(d-2) K/d")
    print("  LD-W-02: -J + 2K/d")
    print("  LD-W-05: (1+2/d) J")
    print("  LD-W-06: -4J/d")
    print("PASS: each pair satisfies full = hard + soft.")
    print("PASS: J_full = J_hard + J_soft; K_soft is a scaleless power integral.")
    print("Weighted hard:")
    print("  A_hard = (3 Delta_UV/8 - 3 L/8 + 11/16)/M_E^2")
    print("Weighted soft:")
    print("  A_soft = 3(-Delta_UV + Delta_IR)/(8 M_E^2)")
    print("Weighted full:")
    print("  A_full = (3 Delta_IR/8 - 3 L/8 + 11/16)/M_E^2")
    print("PASS: the hard UV pole cancels the EFT-soft UV pole; the full amplitude retains only the IR pole.")
    print("PASS: retaining O(eps)*Delta_UV adds +3/16 to the hard finite constant.")
    print("SCOPE: unit multiplicity for one fixed ordered tree contraction only.")
    print("NOT CLAIMED: all charge-conjugate/crossed tree routings, FeynArts/QGRAF multiplicities, full Ward sum, or complete Wilson coefficient.")


if __name__ == "__main__":
    main()
