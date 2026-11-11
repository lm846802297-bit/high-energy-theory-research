#!/usr/bin/env python3
"""RC-001: graph-ordered weak tensors tied to B2c Feynman-rule phases."""
from itertools import product
import sympy as sp

I = sp.I
SIGMA = (
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, -I], [I, 0]]),
    sp.Matrix([[1, 0], [0, -1]]),
)
T = tuple(s/2 for s in SIGMA)
EPS = sp.LeviCivita
INDICES = tuple(product(range(2), repeat=4))


def delta(i, j):
    return sp.Integer(int(i == j))


def T0(i, j, k, ell):
    return delta(i, j)*delta(k, ell)


def T3(i, j, k, ell):
    return sum(SIGMA[a][i, j]*SIGMA[a][k, ell] for a in range(3))


def act(tensor, slot, generator, indices):
    i, j, k, ell = indices
    out = sp.Integer(0)
    if slot == 0:
        for m in range(2):
            out += T[generator][m, i]*tensor(m, j, k, ell)
    elif slot == 1:
        for m in range(2):
            out -= T[generator][j, m]*tensor(i, m, k, ell)
    elif slot == 2:
        for m in range(2):
            out += T[generator][m, k]*tensor(i, j, m, ell)
    elif slot == 3:
        for m in range(2):
            out -= T[generator][ell, m]*tensor(i, j, k, m)
    return sp.simplify(out)


def apply(tensor, slot, generator):
    return lambda *indices: act(tensor, slot, generator, indices)


PAIRS = (
    ("LD-W-01", 0, 3, 0, -sp.Rational(1,4)),
    ("LD-W-02", 0, 2, 0,  sp.Rational(1,4)),
    ("LD-W-03", 0, 1, -sp.Rational(3,4), 0),
    ("LD-W-04", 3, 2, -sp.Rational(3,4), 0),
    ("LD-W-05", 3, 1, 0,  sp.Rational(1,4)),
    ("LD-W-06", 2, 1, 0, -sp.Rational(1,4)),
)


def pair_tensor(slot_a, slot_b):
    return lambda *ix: sp.simplify(sum(
        act(apply(T0, slot_b, b), slot_a, b, ix)
        for b in range(3)
    ))


def G_tensor(slot_a, slot_b, external_a):
    return lambda *ix: sp.simplify(sum(
        EPS(external_a, b, c)
        * act(apply(T0, slot_b, c), slot_a, b, ix)
        for b, c in product(range(3), repeat=2)
    ))


def verify_graph_orderings():
    pair_checks = 0
    a_checks = 0
    b_checks = 0
    for pair_id, slot_a, slot_b, c0, c3 in PAIRS:
        T_ab = pair_tensor(slot_a, slot_b)
        for ix in INDICES:
            expected = c0*T0(*ix) + c3*T3(*ix)
            assert sp.simplify(T_ab(*ix)-expected) == 0, (pair_id, ix)
            pair_checks += 1

        for external_a in range(3):
            G = G_tensor(slot_a, slot_b, external_a)

            # Actual A-line graph ordering: internal-W generator first,
            # external-W generator second. Yukawa-endpoint ordering is reversed.
            graph_A = lambda *ix: sp.simplify(sum(
                act(
                    apply(apply(T0, slot_a, external_a), slot_b, b),
                    slot_a, b, ix
                )
                for b in range(3)
            ))
            yukawa_A = apply(T_ab, slot_a, external_a)
            for ix in INDICES:
                assert sp.simplify(graph_A(*ix)-yukawa_A(*ix)+I*G(*ix)) == 0
                a_checks += 1

            # Actual B-line graph ordering: external-W generator first,
            # internal-W generator second. Yukawa-endpoint ordering is reversed.
            graph_B = apply(T_ab, slot_b, external_a)
            yukawa_B = lambda *ix: sp.simplify(sum(
                act(
                    apply(apply(T0, slot_b, external_a), slot_a, b),
                    slot_b, b, ix
                )
                for b in range(3)
            ))
            for ix in INDICES:
                assert sp.simplify(graph_B(*ix)-yukawa_B(*ix)+I*G(*ix)) == 0
                b_checks += 1
    return pair_checks, a_checks, b_checks


def verify_seagulls():
    checks = 0
    for _, slot_a, slot_b, _, _ in PAIRS:
        for scalar_slot, other_slot in ((slot_a, slot_b), (slot_b, slot_a)):
            if scalar_slot not in (1, 2):
                continue
            for external_a in range(3):
                def sg(*ix):
                    total = sp.Integer(0)
                    for b in range(3):
                        after_other = apply(T0, other_slot, b)
                        total += act(
                            apply(after_other, scalar_slot, b),
                            scalar_slot, external_a, ix
                        )
                        total += act(
                            apply(after_other, scalar_slot, external_a),
                            scalar_slot, b, ix
                        )
                    return sp.simplify(total)
                for ix in INDICES:
                    expected = sp.Rational(1,2)*act(
                        T0, other_slot, external_a, ix
                    )
                    assert sp.simplify(sg(*ix)-expected) == 0
                    checks += 1
    return checks


def main():
    pair, a, b = verify_graph_orderings()
    seagull = verify_seagulls()
    assert (pair, a, b, seagull) == (96, 288, 288, 288)

    print("RC-001 graph-ordered SU(2) weak tensor / phase ledger")
    print(f"PASS: six pair tensors reproduce their T0/T3 projections ({pair}/96).")
    print(f"PASS: A-line graph ordering minus Yukawa-end ordering = -i G_AB ({a}/288).")
    print(f"PASS: B-line graph ordering minus Yukawa-end ordering = -i G_AB ({b}/288).")
    print(f"PASS: scalar seagull weak tensor = one-half opposite-endpoint generator ({seagull}/288).")
    print("ORDERED GRAPH TENSORS:")
    print("  A matter insertion: T_A^b T_A^a T_B^b")
    print("  B matter insertion: T_A^b T_B^a T_B^b")
    print("  A seagull: {T_A^a,T_A^b} T_B^b")
    print("  B seagull: T_A^b {T_B^a,T_B^b}")
    print("  three-W: epsilon^{abc} T_A^b T_B^c")
    print("PHASES RELATIVE TO THE FOUR-POINT SKELETON:")
    print("  ordinary matter line: -g2")
    print("  scalar seagull: +g2")
    print("  three-W: -i g2")
    print("BOUNDARY: group/phase ledger only; no Lorentz-weighted 24-graph sum or full STI closure.")
    

if __name__ == "__main__":
    main()
