#!/usr/bin/env python3
"""Candidate dimension-eight potential projection of the RC-001 constant pole.

This projects only the already-derived bubble-plus-contact subset pole onto
one pure-potential representative, (H^dagger H)^2(S^dagger S)^2. It does not
claim a unique full-basis assignment or include all same-order EFT soft terms.
"""
import sympy as sp

Y2, Lam2, vh, vs, ME, Delta = sp.symbols(
    "abs_y_squared abs_lambda_squared v_h v_s M_E Delta_UV", positive=True
)
h, s, c8 = sp.symbols("h s c8", real=True)

# Leading seesaw counting, with ME the heavy mass (not its square).
q_lead = Y2 * Lam2 * vh * vs / (2 * ME**2)
x_lead = Y2 * Lam2 * vh**2 * vs**2 / (4 * ME**2)
subset_pole = sp.simplify(8 * q_lead * x_lead * Delta / (16 * sp.pi**2))
expected_pole = Y2**2 * Lam2**2 * vh**3 * vs**3 * Delta / (16 * sp.pi**2 * ME**4)
assert sp.simplify(subset_pole - expected_pole) == 0
print("PASS 1: 8 q_l x_l Delta/(16 pi^2) scales as |y|^4 |lambda|^4 v_h^3 v_s^3/(16 pi^2 M_E^4)")

X = (vh + h)**2 / 2
Y = (vs + s)**2 / 2
mixed_hessian = sp.diff(X**2 * Y**2, h, s).subs({h: 0, s: 0})
assert sp.simplify(mixed_hessian - vh**3 * vs**3) == 0
print("PASS 2: mixed Hessian of (H^dagger H)^2(S^dagger S)^2 is v_h^3 v_s^3")

# Gamma_inv = p^2 - M_loc^2 + Pi. A potential counterterm enters Pi as
# minus the mixed Hessian of V_ct, since L_ct = -V_ct.
Pi_ct_from_potential = -c8 * mixed_hessian / ME**4
c8_candidate = -Y2**2 * Lam2**2 * Delta / (16 * sp.pi**2)
assert sp.simplify(Pi_ct_from_potential.subs(c8, c8_candidate) - expected_pole) == 0
print("PASS 3: the candidate pole counterterm is delta c_8 = -|y|^4 |lambda|^4 Delta/(16 pi^2)")

assert sp.simplify(subset_pole * ME**4 / (vh**3 * vs**3) - Y2**2 * Lam2**2 * Delta / (16 * sp.pi**2)) == 0
print("PASS 4: the candidate is dimension-eight order O(M_E^-4), not the leading portal threshold")
print("LIMIT: this is one pure-potential representative for the restricted subset pole, not a unique full-basis assignment.")
print("OPEN: complete same-order EFT soft/source insertions and freeze the gauge-invariant dimension-eight basis/EOM convention before promoting this coefficient.")
