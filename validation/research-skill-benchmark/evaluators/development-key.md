# Development task evaluator key

Evaluator-only reference. Do not mount this file into A/B model workspaces. These are development-set keys, not sealed holdout material.

## T01 — variable-change Jacobian

- With (W^2=(m_1+m_2)^2+s), expand the Källén function:
  [
  lambda=s(s+4m_1m_2).
  ]
- Under (s=\Delta u^2), (ds/du=2\Delta u).
- The transformed integral measure is (ds=2\Delta u\,du).
- Since (s) and (Delta) have mass dimension 2, the Jacobian has mass dimension 2; (u) is dimensionless.
- If the transformed integrand is missing the global factor 2, an absolute integral is half the correct value. A unit-area shape is unchanged only if that factor is global and normalization is performed consistently.
- Critical error: claiming that normalized-shape agreement validates an absolute phase-space factor or rate.

## T02 — threshold phase-space integral

- Parameters: (m_1=1.0\,\mathrm{GeV}), (m_2=0.2\,\mathrm{GeV}), (Delta=0.5\,\mathrm{GeV}^2).
- Original-variable reference:
  [
  I=0.141975883465984392640489856748572220501161185\,\mathrm{GeV}^2
  ]
  at the recorded high precision.
- Substitution (s=\Delta u^2) gives:
  [
  I=\int_0^1 du\,
  \frac{2\Delta u\sqrt{\Delta u^2(\Delta u^2+4m_1m_2)}}
  {(m_1+m_2)^2+\Delta u^2}.
  ]
- The independent original-(s) implementation must integrate the original expression directly; do not call the transformed implementation from both routes.
- Require at least three refinement levels, a numerical error/tolerance statement, and a dimensional check.
- The integral has dimension GeV². It is not by itself a cross section or rate.

## T03 — source-grounded figure reading

- Verify the exact PDF SHA-256 before reading.
- The input is a one-page figure PDF, not a full paper. A response that invents manuscript sections, equation numbers, or paper-level conclusions fails the source-boundary check.
- The answer must cite PDF page 1 (human page numbering) and distinguish visible labels/legend/curves from interpretation.
- If a label or legend item cannot be read from the source, report it as unreadable rather than guessing.
