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

## T03 — axial-vector manuscript reading

Pinned source:
- PDF: `lm846802297-bit/axial-vector-review-response/archive/manuscript-baselines/axial_vector_model_building-v6.pdf`
- Commit: `a7ac6456dafb27492183912fe4abbaa73a9455f7`
- Git blob SHA-1: `be8f472a8cc3c35975dcb5970c9be996fde2d985`
- Companion TeX: `overleaf-source/axial-vector-model-building-v6/main-v6.tex`, blob SHA-1 `b99f9e26a0b57acd0a4938ea6e03fc691a82becb`.

Evaluator facts from the companion TeX:
- The effective-current interaction is labelled `eq:phenomenology-coupling-convention`. It contains axial charged-muon and charged-tau currents with opposite signs for the muon/tau terms as written, and left-chiral neutrino currents with the corresponding opposite signs.
- The existing-constraints figure is labelled `fig:allconstraints`; by its position in the manuscript figure sequence it is Fig. 2 (Fig. 1 is the representative topology diagram; the muon-collider angular comparison follows as Fig. 3).
- The figure's left panel is in the ((m_{A'},g_X)) plane; the right panel is in the ((g_X,v_s)) plane. The right panel is a reparameterization, not additional likelihood information.
- The caption identifies PIENU, indicative NA62 recast, CCFR/CHARM II, scalar-decoupled ((g-2)_\mu), NA64-mu recast, and BaBar/Belle II/CMS four-muon searches. The dashed line corresponds to (v_s=m_{A'}/(2g_X)=2\,\mathrm{GeV}); above it the stated (m_s\geq10\,\mathrm{GeV}), (lambda_S\leq4\pi) benchmark is not perturbative.
- The manuscript explicitly describes the NA62 curve as an indicative acceptance-dependent recast, the NA64-mu curve as a rate-level phenomenological recast, and the four-muon reinterpretations as rate-level estimates pending detector-level simulations near threshold. The contours are conditional on the stated benchmark and should not be described as model-independent.
- The PDF page number and rendered equation number must be read from the pinned PDF itself and recorded by the evaluator; do not infer them from TeX line numbers.
- Before scoring, verify the PDF Git blob SHA-1 and calculate its SHA-256. The SHA-256 is intentionally not prefilled here.
