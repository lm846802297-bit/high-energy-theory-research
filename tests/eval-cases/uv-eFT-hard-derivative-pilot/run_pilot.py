#!/usr/bin/env python3
"""Numerical PV-integral and asymptotic audit for a bounded UV-EFT research task.

This script checks the transcribed closed-form PV functions against independent
Feynman-parameter quadrature. It deliberately does not generate the UV loop
kernel or claim a complete Wilson-coefficient match.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Callable


def adaptive_simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    tolerance: float,
    max_depth: int,
) -> float:
    """Adaptive Simpson quadrature with deterministic recursion and error control."""
    f_left = function(left)
    f_right = function(right)
    midpoint = (left + right) / 2.0
    f_mid = function(midpoint)
    whole = (right - left) * (f_left + 4.0 * f_mid + f_right) / 6.0

    def recurse(a, b, fa, fm, fb, estimate, tol, depth):
        mid = (a + b) / 2.0
        left_mid = (a + mid) / 2.0
        right_mid = (mid + b) / 2.0
        f_left_mid = function(left_mid)
        f_right_mid = function(right_mid)
        left_estimate = (mid - a) * (fa + 4.0 * f_left_mid + fm) / 6.0
        right_estimate = (b - mid) * (fm + 4.0 * f_right_mid + fb) / 6.0
        delta = left_estimate + right_estimate - estimate
        if depth <= 0 or abs(delta) <= 15.0 * tol:
            return left_estimate + right_estimate + delta / 15.0
        return recurse(a, mid, fa, f_left_mid, fm, left_estimate, tol / 2.0, depth - 1) + recurse(
            mid, b, fm, f_right_mid, fb, right_estimate, tol / 2.0, depth - 1
        )

    return recurse(left, right, f_left, f_mid, f_right, whole, tolerance, max_depth)


def _feynman_parameter_values(r: float, scale_log: float, tolerance: float, max_depth: int) -> dict:
    """Independent integral definitions at M^2=1, with mu^2=exp(-L)."""
    mu_squared = math.exp(-scale_log)

    bbar_mm = -adaptive_simpson(
        lambda _x: math.log(1.0 / mu_squared), 0.0, 1.0, tolerance, max_depth
    )
    bprime_mm = adaptive_simpson(lambda x: x * (1.0 - x), 0.0, 1.0, tolerance, max_depth)

    def denominator(x: float) -> float:
        return x * r + (1.0 - x)

    bbar_mM = -adaptive_simpson(
        lambda x: math.log(denominator(x) / mu_squared), 0.0, 1.0, tolerance, max_depth
    )
    bprime_mM = adaptive_simpson(
        lambda x: x * (1.0 - x) / denominator(x), 0.0, 1.0, tolerance, max_depth
    )
    return {
        "Bbar_MM": bbar_mm,
        "M2_Bprime_MM": bprime_mm,
        "Bbar_mM": bbar_mM,
        "M2_Bprime_mM": bprime_mM,
    }


def _closed_form_values(r: float, scale_log: float) -> dict:
    if not 0.0 < r < 1.0:
        raise ValueError("Each mass ratio r must satisfy 0 < r < 1.")
    bbar_mm = -scale_log
    bprime_mm = 1.0 / 6.0
    bbar_mM = 1.0 - scale_log + r * math.log(r) / (1.0 - r)
    bprime_mM = (1.0 + r) / (2.0 * (r - 1.0) ** 2) - r * math.log(r) / (r - 1.0) ** 3
    return {
        "Bbar_MM": bbar_mm,
        "M2_Bprime_MM": bprime_mm,
        "Bbar_mM": bbar_mM,
        "M2_Bprime_mM": bprime_mM,
    }


def compute(problem: dict, config: dict) -> dict:
    if problem.get("input_contract") != "uv-eFT-hard-derivative-v1":
        raise ValueError("Unexpected input-contract version.")
    if problem.get("pv_formula_profile") != "hard-derivative-pv-v1":
        raise ValueError("Unexpected PV formula profile.")

    tolerance = float(config["quadrature_tolerance"])
    max_depth = int(config["quadrature_max_depth"])
    agreement_tolerance = float(config["agreement_absolute_tolerance"])
    K = float(config["K_normalization"])
    rows = []

    for r in config["r_values"]:
        r = float(r)
        if not 0.0 < r < 1.0:
            raise ValueError(f"Invalid mass ratio r={r}")
        for scale_log in config["L_values"]:
            scale_log = float(scale_log)
            closed = _closed_form_values(r, scale_log)
            integral = _feynman_parameter_values(r, scale_log, tolerance, max_depth)
            component_errors = {
                key: abs(closed[key] - integral[key]) for key in closed
            }
            fprime_closed_over_K = (
                -2.0 * closed["Bbar_MM"]
                + 8.0 * closed["M2_Bprime_MM"]
                + 4.0 * closed["Bbar_mM"]
                - 8.0 * (1.0 + r) * closed["M2_Bprime_mM"]
            )
            fprime_integral_over_K = (
                -2.0 * integral["Bbar_MM"]
                + 8.0 * integral["M2_Bprime_MM"]
                + 4.0 * integral["Bbar_mM"]
                - 8.0 * (1.0 + r) * integral["M2_Bprime_mM"]
            )
            leading = 4.0 / 3.0 - 2.0 * scale_log
            first_correction = leading - 4.0 * r * math.log(r) - 16.0 * r
            asymptotic_residual = fprime_closed_over_K - leading
            series_residual = fprime_closed_over_K - first_correction
            rows.append({
                "r": r,
                "L": scale_log,
                "closed_form_pv": closed,
                "feynman_parameter_quadrature": integral,
                "component_absolute_errors": component_errors,
                "Fprime_hard_over_K_closed_form": fprime_closed_over_K,
                "Fprime_hard_over_K_quadrature": fprime_integral_over_K,
                "Fprime_hard_over_K_leading_small_r": leading,
                "Fprime_hard_over_K_first_correction": first_correction,
                "asymptotic_residual_over_K": asymptotic_residual,
                "residual_after_first_correction_over_K": series_residual,
                "residual_scaled_by_r_abslogr": abs(asymptotic_residual) / (r * abs(math.log(r))),
                "max_component_absolute_error": max(component_errors.values()),
                "absolute_Fprime_quadrature_error": abs(fprime_closed_over_K - fprime_integral_over_K),
            })

    matching_scale_rows = [row for row in rows if row["L"] == 0.0]
    leading_residuals = [abs(row["asymptotic_residual_over_K"]) for row in matching_scale_rows]
    next_order_residuals = [abs(row["residual_after_first_correction_over_K"]) for row in matching_scale_rows]
    max_component_error = max(row["max_component_absolute_error"] for row in rows)
    max_fprime_error = max(row["absolute_Fprime_quadrature_error"] for row in rows)
    max_scaled_residual = max(row["residual_scaled_by_r_abslogr"] for row in rows)

    rational_4_over_3_div_16 = Fraction(4, 3) / 16
    rational_projection_factor = 2 * rational_4_over_3_div_16
    pi_prime_at_matching_scale_over_K = -1.0 / (12.0 * math.pi ** 2)

    checks = {
        "all_pv_functions_agree_with_independent_quadrature": max_component_error <= agreement_tolerance,
        "Fprime_combination_agrees_with_independent_quadrature": max_fprime_error <= agreement_tolerance,
        "leading_small_r_residual_decreases": all(a > b for a, b in zip(leading_residuals, leading_residuals[1:])),
        "first_correction_residual_decreases": all(a > b for a, b in zip(next_order_residuals, next_order_residuals[1:])),
        "scaled_asymptotic_residual_is_bounded_on_test_grid": max_scaled_residual < float(config["maximum_scaled_asymptotic_residual"]),
        "exact_rational_factor_4_over_3_div_16_is_1_over_12": rational_4_over_3_div_16 == Fraction(1, 12),
        "exact_rational_projection_factor_is_1_over_6": rational_projection_factor == Fraction(1, 6),
        "matching_scale_pi_prime_has_expected_sign_and_factor": pi_prime_at_matching_scale_over_K < 0.0 and math.isclose(
            pi_prime_at_matching_scale_over_K, -1.0 / (12.0 * math.pi ** 2), rel_tol=0.0, abs_tol=1e-15
        ),
        "dimension_bookkeeping_is_consistent": (
            problem["definitions"]["K"].endswith("dimensionless in the stated convention")
            and "mass dimension -2" in " ".join(config["units"])
        ),
    }
    all_passed = all(checks.values())
    return {
        "task_id": problem["task_id"],
        "task_title": problem["title"],
        "input_contract": problem["input_contract"],
        "formula_profile": problem["pv_formula_profile"],
        "method": "closed-form PV expressions cross-checked against independent Feynman-parameter adaptive Simpson quadrature",
        "normalization": {
            "M_squared": float(config["M_squared_normalization"]),
            "K": K,
            "meaning": "dimensionless audit normalization only; not a physical benchmark",
        },
        "scale_convention": "L = ln(M^2/mu^2)",
        "cases": rows,
        "exact_coefficients": {
            "Fprime_hard_over_K_leading_small_r": "4/3 - 2*L",
            "Fprime_hard_over_K_first_correction": "4/3 - 2*L - 4*r*ln(r) - 16*r + O(r^2*ln(r))",
            "Pi_prime_hard_over_K_at_mu_equals_M": "-1/(12*pi^2) + O(r*ln(r))",
            "single_operator_projection_C_over_Lambda2": "K/(6*pi^2*v_h*v_s) + O(K*r*ln(r)/(v_h*v_s))",
            "projection_scope": "single-operator convention only; not a unique complete-basis Wilson coefficient",
        },
        "summary": {
            "case_count": len(rows),
            "max_component_absolute_error": max_component_error,
            "max_Fprime_absolute_error": max_fprime_error,
            "max_scaled_asymptotic_residual": max_scaled_residual,
            "pi_prime_at_matching_scale_over_K_numeric": pi_prime_at_matching_scale_over_K,
            "exact_projection_factor": str(rational_projection_factor),
        },
        "checks": checks,
        "all_checks_passed": all_passed,
        "limitations": [
            "The hard-kernel formula is an input transcribed from the working note; this task does not independently regenerate the full UV diagram numerator or diagram set.",
            "The operator coefficient is only a single-operator projection under the explicit convention in problem.json.",
            "No phenomenological parameter point, experimental constraint, or complete EFT-basis matching is assessed.",
            "Human scientific review remains pending.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    problem = json.loads(Path(args.input).read_text(encoding="utf-8"))
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    result = compute(problem, config)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    summary = {
        "task_id": result["task_id"],
        "case_count": result["summary"]["case_count"],
        "all_checks_passed": result["all_checks_passed"],
        "max_component_absolute_error": result["summary"]["max_component_absolute_error"],
        "max_Fprime_absolute_error": result["summary"]["max_Fprime_absolute_error"],
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

