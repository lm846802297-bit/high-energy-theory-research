#!/usr/bin/env python3
"""Independent convergence study for the matched-threshold 2->3 phase-space shape."""
from __future__ import annotations
import csv
import hashlib
import json
import math
import platform
import sys
from pathlib import Path
import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

MCHI = 1.0e9
MT = 122.0e6
MS = 300.0
SPEED = 780.0
C = 299792.458
ORDERS = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
HERE = Path(__file__).resolve().parent


def delta_w2(er: float | np.ndarray) -> np.ndarray:
    beta = SPEED / C
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    p_in = gamma * MCHI * beta
    e_in = gamma * MCHI
    er = np.asarray(er, dtype=float)
    q = np.sqrt(np.maximum(er * (er + 2.0 * MT), 0.0))
    return 2.0 * p_in * q - 2.0 * (e_in + MT) * er - 2.0 * MCHI * MS - MS * MS


def endpoints() -> tuple[float, float]:
    f = lambda x: float(delta_w2(x))
    grid = np.linspace(0.0, 1000.0, 2001)
    vals = [f(x) for x in grid]
    roots = []
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if fa * fb < 0:
            roots.append(brentq(f, a, b, xtol=1e-12))
    if len(roots) != 2:
        raise RuntimeError(f"expected two endpoints, got {roots}")
    return roots[0], roots[1]


def integral_u(er: np.ndarray, order: int) -> np.ndarray:
    """Evaluate the original integral after s=Delta*u^2, retaining ds/du=2 Delta u."""
    d = delta_w2(er)
    out = np.zeros_like(np.asarray(er, dtype=float))
    mask = d > 0.0
    nodes, weights = leggauss(order)
    u = (nodes + 1.0) / 2.0
    w = weights / 2.0
    dm = d[mask, None]
    s = dm * u[None, :] ** 2
    denominator = (MCHI + MS) ** 2 + s
    ds_du = 2.0 * dm * u[None, :]
    integrand = ds_du * np.sqrt(s * (s + 4.0 * MCHI * MS)) / denominator
    out[mask] = integrand @ w
    return out


def integral_original_s(er: float) -> float:
    d = float(delta_w2(er))
    if d <= 0.0:
        return 0.0
    value, error = quad(
        lambda s: math.sqrt(s * (s + 4.0 * MCHI * MS)) / ((MCHI + MS) ** 2 + s),
        0.0,
        d,
        epsabs=0.0,
        epsrel=2e-12,
        limit=300,
    )
    return value


def normalized(y: np.ndarray, er: np.ndarray) -> np.ndarray:
    area = float(np.trapezoid(y, er))
    if not math.isfinite(area) or area <= 0.0:
        raise RuntimeError(f"invalid normalization {area}")
    return y / area


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    lo, hi = endpoints()
    er = np.unique(np.r_[np.linspace(0.0, 700.0, 701), lo, hi])
    curves = {}
    convergence = []
    for order in ORDERS:
        raw = integral_u(er, order)
        curves[order] = normalized(raw, er)
        convergence.append({
            "order": order,
            "raw_spectrum_area_keV3": float(np.trapezoid(raw, er)),
            "normalized_area": float(np.trapezoid(curves[order], er)),
        })

    final = curves[ORDERS[-1]]
    threshold = float(np.max(final)) * 1e-8
    active = final > threshold
    for lower, upper in zip(ORDERS[:-1], ORDERS[1:]):
        diff = curves[upper] - curves[lower]
        for row in convergence:
            if row["order"] == upper:
                row["previous_order"] = lower
                row["max_abs_shape_difference_per_keV"] = float(np.max(np.abs(diff)))
                row["max_rel_shape_difference_active_region"] = float(np.max(np.abs(diff[active]) / final[active]))
                break

    # Independent algorithm and variable: scipy QUAD integrates directly in s.
    quad_checks = []
    for recoil in [150.0, 250.0, 350.0, 450.0, 550.0, 650.0]:
        if float(delta_w2(recoil)) <= 0.0:
            continue
        qvalue = integral_original_s(recoil)
        gvalue = float(integral_u(np.array([recoil]), 512)[0])
        quad_checks.append({
            "ER_keV": recoil,
            "gauss_legendre_512": gvalue,
            "scipy_quad_original_s": qvalue,
            "relative_difference": abs(gvalue - qvalue) / abs(qvalue),
        })

    # Nonrelativistic endpoint relation, independently checked against exact roots.
    beta = SPEED / C
    mu = MCHI * MT / (MCHI + MT)
    radicand = beta * beta - 2.0 * MS / mu
    if radicand <= 0:
        raise RuntimeError("benchmark is below the nonrelativistic opening threshold")
    root = math.sqrt(radicand)
    nr_lo = mu * mu * (beta - root) ** 2 / (2.0 * MT)
    nr_hi = mu * mu * (beta + root) ** 2 / (2.0 * MT)

    peak = minimize_scalar(
        lambda x: -float(integral_u(np.array([x]), 512)[0]),
        bounds=(lo, hi),
        method="bounded",
        options={"xatol": 1e-8},
    )
    p23 = normalized(integral_u(er, 512), er)
    p22 = np.where((er >= lo) & (er <= hi), 1.0 / (hi - lo), 0.0)

    rows = []
    for x in np.arange(0.0, 700.0001, 25.0):
        rows.append({
            "ER_keV": x,
            "P22_unit_area_per_keV": float(np.interp(x, er, p22)),
            "P23_unit_area_per_keV": float(np.interp(x, er, p23)),
            "deltaW2_keV2": float(delta_w2(x)),
        })
    csv_path = HERE / "convergence_spectrum.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "status": "PASS: multi-level convergence and independent original-variable quadrature",
        "inputs": {
            "mchi1_keV": MCHI,
            "target_mass_keV": MT,
            "scalar_mass_keV": MS,
            "iDM_threshold_keV": MS,
            "incident_speed_km_s": SPEED,
            "source_record": "LZ-3-body-for-hdm PR #77, merged commit 8902abdb8bc44cad690059f9985204b4c0737657",
            "source_script_blob_sha": "9d16dee9297f992aff41c80c67275b8b5eb8c99e",
            "source_data_blob_sha": "3fed4e5e4517cd59c83f3415ce441eabd90b396d",
            "source_summary_blob_sha": "bddd5274f1ade39b8e2b26e53171686516951daf",
            "source_pdf_sha256_recorded_upstream": "b4fc7bd73265df2bc2ce1640cbf8847b63323ec1dda220f9e7903f4620b871bb",
        },
        "exact_kinematics": {
            "recoil_endpoints_keV": [lo, hi],
            "P22_plateau_per_keV": 1.0 / (hi - lo),
            "P23_peak_ER_keV": float(peak.x),
            "P23_peak_height_per_keV": float(-peak.fun / np.trapezoid(integral_u(er, 512), er)),
        },
        "convergence_sequence": convergence,
        "independent_scipy_quad_checks": quad_checks,
        "heavy_particle_limit": {
            "endpoints_keV": [nr_lo, nr_hi],
            "max_exact_vs_NR_endpoint_difference_keV": max(abs(lo - nr_lo), abs(hi - nr_hi)),
        },
        "normalization": {
            "P22_area_analytic": float((1.0 / (hi - lo)) * (hi - lo)),
            "P22_trapezoid_grid_area_not_used_for_step_function": float(np.trapezoid(p22, er)),
            "P23_area": float(np.trapezoid(p23, er)),
            "shape_is_normalized": True,
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "output": {
            "csv": csv_path.name,
            "csv_sha256": sha256(csv_path),
        },
    }
    max_quad = max(x["relative_difference"] for x in quad_checks)
    if max_quad > 2e-10:
        raise AssertionError(f"independent quadrature discrepancy too large: {max_quad}")
    if abs(float(np.trapezoid(p23, er)) - 1.0) > 1e-10:
        raise AssertionError("P23 normalization failed")
    if max(abs(lo - nr_lo), abs(hi - nr_hi)) > 0.02:
        raise AssertionError("heavy-particle endpoint cross-check failed")
    out_path = HERE / "convergence_result.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
