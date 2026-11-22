# Development task T02 — threshold phase-space integral

Status: development only; may be used to improve the Skill.

## Prompt

Evaluate

[
I=\int_0^{\Delta} ds\,
\frac{\sqrt{s(s+4m_1m_2)}}{(m_1+m_2)^2+s}
]

for (m_1=1.0\,\mathrm{GeV}), (m_2=0.2\,\mathrm{GeV}), and (Delta=0.5\,\mathrm{GeV}^2).

1. Derive the transformed integral under (s=\Delta u^2), retaining the full Jacobian.
2. Compute the integral using a deterministic quadrature method.
3. Demonstrate convergence over at least three refinement levels.
4. Independently compute the original-(s) integral using a different integration route.
5. Report units, absolute/relative differences, method limitations, and the native machine-readable output.

The task is an integration-method benchmark, not a complete physical rate calculation. Do not infer cross sections or event rates from this integral alone.

## Evaluator notes (not shown to the model)

Reference value at the recorded benchmark precision:
(I=0.141975883465984392640489856748572220501161185\,\mathrm{GeV}^2).

The transformed integrand contains (2\Delta u). Independent routes must not share a single transformed-integrand implementation.
