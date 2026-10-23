# Task router

Choose a workflow based on the research objective, then record inputs, outputs, dependencies, and validation gates.

| Task class | Minimum workflow | Typical independent checks |
|---|---|---|
| Literature review | Search primary papers, compare assumptions and versions, extract claim-level evidence | Compare original equations, errata, follow-up work, and independent sources |
| Analytic derivation | Define conventions, derive stepwise, record approximations | Dimensions, limits, symmetry identities, independent derivation |
| Symbolic or loop calculation | Minimal reproducible code, package versions, input expression, renormalization scheme | Compare analytic limits, alternative algebraic form, numerical point |
| Model consistency | Gauge/charge assignments, anomalies where applicable, potential/stability, mixing and perturbativity | Independent symbolic checks and explicit assumption table |
| Phenomenology scan | Define UV-to-observable mapping, ranges, priors, likelihood/limits, validity domain | Benchmark reproduction, scan convergence, boundary tests |
| Experimental reinterpretation | Identify dataset/release, signal model, efficiency/response, statistical prescription | Official analysis documentation, limit reproduction, uncertainty propagation |
| Manuscript/reviewer response | Map each comment to claims, equations, evidence, and changed text | Cross-check response letter against manuscript and computations |

Do not select a single workflow merely because a task is urgent. Mixed tasks should be split into linked subtasks.

## Routing rules

- If model definitions or conventions are missing and affect correctness, request the smallest essential clarification.
- If a task depends on a previous project record, retrieve that record rather than reconstructing it from memory.
- If a source is paywalled or inaccessible, label what was and was not inspected.
- If a calculation is too large to verify in one pass, split it into derivation, implementation, and independent-check stages.
