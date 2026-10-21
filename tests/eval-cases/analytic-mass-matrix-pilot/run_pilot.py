#!/usr/bin/env python3
"""Deterministic toy pilot for the high-energy-theory research Skill.

This validates a small algebraic workflow, not a physical model or a released
schema contract. It uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

TOLERANCE = 1e-12


def _dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def _norm(vector):
    return math.sqrt(_dot(vector, vector))


def _close(left, right, tol=TOLERANCE):
    return abs(left - right) <= tol * max(1.0, abs(left), abs(right))


def solve(problem: dict) -> dict:
    matrix = problem.get("matrix")
    if (
        not isinstance(matrix, list)
        or len(matrix) != 2
        or any(not isinstance(row, list) or len(row) != 2 for row in matrix)
    ):
        raise ValueError("matrix must be a 2x2 numeric array")

    try:
        a, b = float(matrix[0][0]), float(matrix[0][1])
        c, d = float(matrix[1][0]), float(matrix[1][1])
    except (TypeError, ValueError) as exc:
        raise ValueError("matrix entries must be finite real numbers") from exc

    if not all(math.isfinite(value) for value in (a, b, c, d)):
        raise ValueError("matrix entries must be finite real numbers")
    if not _close(b, c):
        raise ValueError("pilot requires a real symmetric matrix")

    # Analytic characteristic-polynomial result for [[a,b],[b,d]].
    trace = a + d
    determinant = a * d - b * b
    discriminant = math.sqrt(max(0.0, (a - d) ** 2 + 4.0 * b * b))
    eigenvalues = sorted(((trace - discriminant) / 2.0, (trace + discriminant) / 2.0))

    eigenvectors = []
    residual_norms = []
    for eigenvalue in eigenvalues:
        if abs(b) > TOLERANCE:
            vector = [b, eigenvalue - a]
        elif abs(eigenvalue - a) <= abs(eigenvalue - d):
            vector = [1.0, 0.0]
        else:
            vector = [0.0, 1.0]
        norm = _norm(vector)
        if norm <= TOLERANCE:
            raise ArithmeticError("could not construct a nonzero eigenvector")
        vector = [component / norm for component in vector]
        eigenvectors.append(vector)

        product = [a * vector[0] + b * vector[1], b * vector[0] + d * vector[1]]
        residual = [product[i] - eigenvalue * vector[i] for i in range(2)]
        residual_norms.append(_norm(residual))

    trace_from_eigenvalues = sum(eigenvalues)
    determinant_from_eigenvalues = eigenvalues[0] * eigenvalues[1]
    masses = [math.sqrt(value) for value in eigenvalues] if all(value >= 0 for value in eigenvalues) else None
    checks = {
        "matrix_is_symmetric": _close(b, c),
        "trace_reproduced": _close(trace_from_eigenvalues, trace),
        "determinant_reproduced": _close(determinant_from_eigenvalues, determinant),
        "eigenvectors_normalized": all(_close(_dot(v, v), 1.0) for v in eigenvectors),
        "eigenvectors_orthogonal": _close(_dot(eigenvectors[0], eigenvectors[1]), 0.0),
        "eigenpair_residuals_small": all(value <= TOLERANCE for value in residual_norms),
        "positive_definite_by_sylvester": a > 0.0 and determinant > 0.0,
    }

    return {
        "pilot_id": problem.get("problem_id", "ANALYTIC-MATRIX-PILOT"),
        "method": "closed-form eigenvalues plus independent trace, determinant, eigenvector, and positivity checks",
        "matrix": [[a, b], [b, d]],
        "matrix_units": problem.get("matrix_units", "unspecified"),
        "eigenvalues": eigenvalues,
        "eigenvalue_units": problem.get("matrix_units", "unspecified"),
        "masses": masses,
        "mass_units": problem.get("mass_units", "unspecified"),
        "eigenvectors_as_columns": eigenvectors,
        "invariants": {
            "trace": trace,
            "determinant": determinant,
            "trace_from_eigenvalues": trace_from_eigenvalues,
            "determinant_from_eigenvalues": determinant_from_eigenvalues,
            "eigenpair_residual_norms": residual_norms,
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "claim_scope": "the supplied 2x2 real symmetric matrix only",
        "limitations": [
            "synthetic algebraic pilot, not a complete particle-physics model",
            "does not establish potential stability, perturbativity, experimental allowance, or phenomenological validity",
            "does not validate the candidate schema's full run-manifest or claim-evidence semantics",
        ],
    }


def run(input_path: Path, output_path: Path) -> dict:
    problem = json.loads(input_path.read_text(encoding="utf-8"))
    result = solve(problem)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("problem.json"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args(argv)
    result = run(args.input, args.output)
    print(json.dumps({
        "pilot_id": result["pilot_id"],
        "eigenvalues": result["eigenvalues"],
        "masses": result["masses"],
        "all_checks_passed": result["all_checks_passed"],
    }, ensure_ascii=False, indent=2))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
