# Task router

Choose the smallest workflow that satisfies the requested result and its evidence requirements. Loading this Skill does not imply that every reference, tool, or workflow stage must be used.

## Effort tiers

| Tier | Task type | Required behavior | Not required by default |
|---|---|---|---|
| **Tier 0 — Quick analytic** | Self-contained algebraic identity, elementary factorization, simple Jacobian, short exact integral, dimensional check, or focused conceptual question | State relevant assumptions, derive directly, and perform one appropriate low-cost check | Literature search, code execution, specialist references, run manifests, project records, or archival |
| **Tier 1 — Focused research** | Specific paper/equation/figure/source claim or nontrivial analytic derivation | For source-dependent work, inspect the primary source; for a self-contained derivation, derive from the stated inputs; load only the matching reference when useful; retain source locations when applicable | Broad literature review, unrelated modules, production numerical workflows |
| **Tier 2 — Numerical/computational** | Numerical integration, scans, fitting, Monte Carlo, generated data, or code supporting a quantitative claim | Load the numerical reference; define accuracy/stopping criteria; retain the appropriate run record; assess convergence/uncertainty and perform an independent physical check | Additional tools or calculations that do not address a named failure mode |
| **Tier 3 — Project-level** | Long-running or multi-stage calculations, manuscript/reviewer-response packages, multi-file deliverables, or collaborative repository work | Plan dependencies and acceptance criteria; follow project governance; preserve source/input/environment/output provenance; archive and review | Applying another repository's registry, schema, or workflow without explicit adoption |

Do not promote a task to a higher tier merely because it concerns particle physics or contains equations. Explicit user requirements and concrete evidence needs may raise the tier.

## Task-class routing

| Task class | Typical workflow after tier selection | Appropriate checks |
|---|---|---|
| Literature review | Tier 1 or 3: inspect relevant primary papers, versions, assumptions, and claim-level evidence | Compare the exact equations, errata, relevant follow-up work, and independent sources when needed |
| Analytic derivation | Tier 0 or 1: define only relevant conventions and derive stepwise | Substitute into the original expression, check dimensions or relevant limits; use a second derivation only when it adds distinct evidence |
| Symbolic or loop calculation | Tier 1, 2, or 3 depending on scope; derive a minimal symbolic representation and, if code is used, retain the minimal reproducible code, package versions, input expression, and scheme | Check analytic limits, alternative algebraic forms, conventions, and an independent representation where useful |
| Model consistency | Tier 1–3 depending on scope: gauge/charge assignments, anomalies where applicable, potential/stability, mixing, and perturbativity | Independent symbolic checks and explicit assumptions where relevant |
| Phenomenology scan | Tier 2 or 3: define UV-to-observable mapping, ranges, priors/sampling, likelihood/limits, and validity domain | Benchmark reproduction, scan convergence, boundary tests, and uncertainty analysis |
| Experimental reinterpretation | Tier 1–3 depending on data and implementation: identify dataset/release, signal model, efficiency/response, and statistical prescription | Official analysis documentation, limit reproduction, and uncertainty propagation |
| Manuscript/reviewer response | Tier 1 or 3: map each comment to claims, equations, evidence, and changed text | Cross-check the response against the manuscript and computations |

## Routing rules

- If model definitions or conventions are missing and affect correctness, request the smallest essential clarification.
- If a task depends on a previous project record, retrieve that record rather than reconstructing it from memory.
- If a source is paywalled or inaccessible, label what was and was not inspected.
- If a calculation is too large to verify in one pass, split it into derivation, implementation, and independent-check stages.
- For a simple exact derivation, do not run a numerical integral solely to satisfy an "independent check" requirement. An exact substitution, an alternative factorization, dimensional analysis, or a relevant limit may be sufficient.
- Before using an optional tool, identify the specific failure mode it addresses and the new evidence it will produce. If it adds no decision-relevant evidence, do not use it.
- Stop once the requested deliverable and its preselected acceptance checks are satisfied. Do not keep expanding the task with unrelated checks or artifacts.
