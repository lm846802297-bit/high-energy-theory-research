#!/usr/bin/env python3
"""Independent 4x4 Dirac-representation check for development task T04.

Uses only the Python standard library. The analytic trace formula is checked
against explicit matrix multiplication with metric diag(+1,-1,-1,-1).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

ComplexMatrix = list[list[complex]]


def zeros(n: int = 4) -> ComplexMatrix:
    return [[0j for _ in range(n)] for _ in range(n)]


def identity(n: int = 4) -> ComplexMatrix:
    out = zeros(n)
    for i in range(n):
        out[i][i] = 1 + 0j
    return out


def add(a: ComplexMatrix, b: ComplexMatrix) -> ComplexMatrix:
    return [[a[i][j] + b[i][j] for j in range(4)] for i in range(4)]


def scale(a: ComplexMatrix, value: complex) -> ComplexMatrix:
    return [[value * a[i][j] for j in range(4)] for i in range(4)]


def multiply(a: ComplexMatrix, b: ComplexMatrix) -> ComplexMatrix:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def trace(a: ComplexMatrix) -> complex:
    return sum(a[i][i] for i in range(4))


def gamma_matrices() -> list[ComplexMatrix]:
    # Dirac representation, gamma^0 = diag(I_2,-I_2),
    # gamma^i = [[0,sigma_i],[-sigma_i,0]].
    g0 = zeros()
    g0[0][0] = g0[1][1] = 1
    g0[2][2] = g0[3][3] = -1
    sigma1 = [[0, 1], [1, 0]]
    sigma2 = [[0, -1j], [1j, 0]]
    sigma3 = [[1, 0], [0, -1]]
    gammas = [g0]
    for sigma in (sigma1, sigma2, sigma3):
        g = zeros()
        for i in range(2):
            for j in range(2):
                g[i][j + 2] = sigma[i][j]
                g[i + 2][j] = -sigma[i][j]
        gammas.append(g)
    return gammas


def slash(p: Sequence[float], gammas: list[ComplexMatrix]) -> ComplexMatrix:
    if len(p) != 4:
        raise ValueError("Four-vector must have four components")
    out = zeros()
    for mu in range(4):
        coefficient = p[mu] if mu == 0 else -p[mu]
        out = add(out, scale(gammas[mu], coefficient))
    return out


def minkowski_dot(p: Sequence[float], k: Sequence[float]) -> float:
    return p[0] * k[0] - sum(p[i] * k[i] for i in range(1, 4))


def evaluate(p: Sequence[float], k: Sequence[float], mass: float, tolerance: float = 1e-10) -> dict:
    gammas = gamma_matrices()
    metric = [1.0, -1.0, -1.0, -1.0]
    ident = identity()
    max_clifford_residual = 0.0
    for mu in range(4):
        for nu in range(4):
            anticommutator = add(multiply(gammas[mu], gammas[nu]), multiply(gammas[nu], gammas[mu]))
            target = scale(ident, 2.0 * metric[mu] if mu == nu else 0.0)
            for i in range(4):
                for j in range(4):
                    max_clifford_residual = max(max_clifford_residual, abs(anticommutator[i][j] - target[i][j]))

    pslash = slash(p, gammas)
    kslash = slash(k, gammas)
    pplusm = add(pslash, scale(ident, mass))
    kminusm = add(kslash, scale(ident, -mass))
    pk = minkowski_dot(p, k)
    residuals = []
    matrix_values = []
    analytic_values = []
    for mu in range(4):
        row = []
        expected_row = []
        for nu in range(4):
            actual = trace(multiply(multiply(multiply(pplusm, gammas[mu]), kminusm), gammas[nu]))
            gmunu = metric[mu] if mu == nu else 0.0
            expected = 4.0 * (p[mu] * k[nu] + p[nu] * k[mu] - (pk + mass * mass) * gmunu)
            row.append([actual.real, actual.imag])
            expected_row.append(expected)
            residuals.append(abs(actual - expected))
        matrix_values.append(row)
        analytic_values.append(expected_row)
    max_trace_residual = max(residuals)
    passed = max_clifford_residual <= tolerance and max_trace_residual <= tolerance
    return {
        "status": "PASS" if passed else "FAIL",
        "metric": "diag(+1,-1,-1,-1)",
        "representation": "Dirac",
        "p": list(p),
        "k": list(k),
        "mass": mass,
        "analytic_expression": "4*(p^mu*k^nu + p^nu*k^mu - (p.k + m^2)*g^{mu nu})",
        "max_clifford_residual": max_clifford_residual,
        "max_trace_residual": max_trace_residual,
        "matrix_trace_real_imag": matrix_values,
        "analytic_trace": analytic_values,
        "tolerance": tolerance,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    args = parser.parse_args()
    result = evaluate((2.3, 0.4, -0.7, 1.1), (1.8, -0.2, 0.9, 0.3), 0.6, args.tolerance)
    text = json.dumps(result, indent=2) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
