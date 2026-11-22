# Development task T02 — reduced three-body threshold phase-space kernel

Status: development only; may be used to improve the Skill.

## Definition and scope

Let
`W^2=(m_1+m_2)^2+s, with s >= 0`.
Then
`\lambda(W^2,m_1^2,m_2^2)=s(s+4m_1m_2)`.

Evaluate the reduced one-dimensional threshold phase-space kernel
`I(\Delta)=\int_0^{\Delta}ds\,\frac{\sqrt{s(s+4m_1m_2)}}{(m_1+m_2)^2+s}`
for `m_1=1.0 GeV`, `m_2=0.2 GeV`, and `\Delta=0.5 GeV^2`.

This is a reduced three-body phase-space integral in a specified constant-amplitude benchmark. It isolates the threshold measure and numerical integration. It is **not** a complete three-body rate: no process-specific matrix element, angular dependence, nuclear response, halo folding, detector acceptance, or event-rate normalization is included.

## Required work

1. Derive the transformed integral under `s=\Delta u^2`, `0\leq u\leq1`, retaining `ds/du=2\Delta u`.
2. Compute the integral using deterministic quadrature.
3. Demonstrate convergence over at least three refinement levels.
4. Independently compute the original-`s` integral using a different integration route; do not call the transformed implementation from both routes.
5. Check mass dimensions of the integral and transformed measure.
6. Report absolute/relative differences, tolerances, method limitations, and native machine-readable output.

## Acceptance scope

The integral has dimension GeV². A unit-area normalized shape can hide a missing global Jacobian factor; validate the absolute integral as well. Do not infer a cross section, event rate, or detector prediction from this kernel alone.

Evaluator reference for these inputs:
`0.141975883465984392640489856748572220501161185 GeV^2`.
The high-precision reference is evaluator-only and must not be mounted into the model workspace.