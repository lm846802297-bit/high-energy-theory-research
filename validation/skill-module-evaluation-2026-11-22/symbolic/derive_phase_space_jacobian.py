#!/usr/bin/env python3
"""Exact Jacobian audit for the threshold-regularized 3-body phase-space integral."""
from __future__ import annotations
import json
import platform
import sys
from pathlib import Path
import sympy as sp
import mpmath as mp

mchi, ms, delta, s, u = sp.symbols("mchi ms Delta s u", positive=True, finite=True)
w2 = (mchi + ms) ** 2 + s
kallen = sp.expand(w2**2 + mchi**4 + ms**4 - 2 * (w2 * mchi**2 + w2 * ms**2 + mchi**2 * ms**2))
kallen_expected = s * (s + 4 * mchi * ms)
assert sp.simplify(kallen - kallen_expected) == 0

s_u = delta * u**2
jacobian = sp.diff(s_u, u)
denominator = (mchi + ms) ** 2 + s_u
radicand = s_u * (s_u + 4 * mchi * ms)
correct_u_integrand = sp.simplify(jacobian * sp.sqrt(radicand) / denominator)
candidate_half_jacobian_integrand = sp.simplify(delta * u * sp.sqrt(radicand) / denominator)
ratio = sp.simplify(candidate_half_jacobian_integrand / correct_u_integrand)
assert sp.simplify(jacobian - 2 * delta * u) == 0
assert ratio == sp.Rational(1, 2)

# Independent 50-digit numerical check: integrate in the original s variable
# and in u after applying the full Jacobian.
mp.mp.dps = 50
mc = mp.mpf("1.0")
sm = mp.mpf("0.2")
dm = mp.mpf("0.5")
orig = mp.quad(lambda x: mp.sqrt(x * (x + 4 * mc * sm)) / ((mc + sm) ** 2 + x), [0, dm])
trans = mp.quad(lambda y: 2 * dm * y * mp.sqrt((dm * y**2) * (dm * y**2 + 4 * mc * sm)) / ((mc + sm) ** 2 + dm * y**2), [0, 1])
candidate_half_integral = trans / 2
relative_residual = abs(orig - trans) / abs(orig)
assert relative_residual < mp.mpf("1e-45")
assert abs(candidate_half_integral / trans - mp.mpf("0.5")) < mp.mpf("1e-48")

result = {
    "status": "PASS: Kallen factorization and transformed Jacobian; FINDING: candidate half-Jacobian expression is half the correct absolute integral",
    "symbolic": {
        "kallen_factorization": "lambda(W2,mchi2,ms2) = s*(s + 4*mchi*ms)",
        "variable_change": "s = Delta*u^2, 0 <= u <= 1",
        "jacobian_ds_du": str(jacobian),
        "correct_transformed_integrand": "2*Delta^(3/2)*u^2*sqrt(4*mchi*ms + Delta*u^2)/((mchi+ms)^2 + Delta*u^2)",
        "candidate_half_jacobian_ratio_to_correct": str(ratio),
        "normalized_shape_unchanged": True,
        "absolute_integral_requires_factor": 2,
    },
    "numeric_independent_check": {
        "mchi_GeV": str(mc),
        "ms_GeV": str(sm),
        "Delta_GeV2": str(dm),
        "mpmath_dps": mp.mp.dps,
        "original_s_integral_GeV2": mp.nstr(orig, 45),
        "transformed_u_integral_GeV2": mp.nstr(trans, 45),
        "relative_residual": mp.nstr(relative_residual, 8),
        "candidate_half_integral_over_correct": mp.nstr(candidate_half_integral / trans, 8),
    },
    "environment": {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "sympy": sp.__version__,
        "mpmath": mp.__version__,
    },
}
Path(__file__).with_name("result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
