# Shared Research Governance Standard

**Status:** adopted shared baseline  
**Effective date:** 2026-11-23  
**Scope:** research repositories that explicitly adopt the central standards framework

This standard defines common research governance. It does not prescribe one mathematical method, physical model, numerical algorithm, or domain-specific acceptance threshold.

## 1. Repository responsibilities

### Central infrastructure repository

The central repository owns shared research-quality, reproducibility, provenance, archival, review, and communication standards; generic task-handoff and research-change templates; reusable Skills, schemas, validators, and stable automation interfaces; standards versioning, adoption guidance, and project navigation.

It does not own project-specific calculations, inputs, raw data, native numerical outputs, detailed research processes, manuscript evidence, or scientific conclusions.

### Project repositories

Each project repository owns its scientific questions, models, assumptions, conventions, derivations, code, inputs, runs, native outputs, validation records, claims, manuscripts, and domain-specific acceptance criteria.

A project may add stricter compatible rules. It must not silently weaken an adopted central minimum. A project-specific exception must identify the affected requirement, reason, scope, approving decision, and review date.

## 2. Source and authority hierarchy

The authority of a record depends on its provenance, scope, and evidence—not merely its file type or location.

| Layer | Source | What it establishes |
|---:|---|---|
| 1 | Primary literature, official experimental publications/data, original source code/data releases | What a source actually states, measures, publishes, or distributes |
| 2 | Latest explicit project-owner decisions and approved research conventions | Which model choices, definitions, and conventions the project has adopted; a decision does not turn an assumption into an experimentally established fact |
| 3 | Independently checked analytical derivations and validated calculations | Mathematical and physical statements within their explicitly tested assumptions and validity domain |
| 4 | Versioned code, tests, run manifests, native outputs, and audit records | What was implemented and actually executed, with which source, inputs, settings, and outputs |
| 5 | Manuscript drafts, response letters, figures, and presentation documents | How the current research state is communicated; these do not independently establish the correctness of a formula or result |
| 6 | Chat summaries, model-generated explanations, and informal notes | Navigation and leads for further checking; not authoritative evidence by themselves |

A primary source is authoritative for its own published content, not automatically for every later interpretation. An approved project decision governs the adopted choice, while its scientific validity remains subject to derivation and evidence. A code test or successful run proves only the property it actually tests.

The user's/latest project owner's explicit instruction or confirmed decision supersedes older project notes and historical discussions for project direction. Exploratory questions and suggestions are not decisions unless explicitly adopted.

## 3. Resolving disagreements

When a paper, derivation, code path, dataset, manuscript, or numerical result disagrees with another source:

1. Freeze the exact source revisions, equations/values, conventions, inputs, parameter point, and affected outputs.
2. Classify the disagreement as theoretical, numerical, data/provenance, implementation, statistical, or editorial.
3. Return to the primary source and independently reconstruct the relevant definition or derivation.
4. Check dimensions, units, signs, normalization, limiting cases, and numerical implementation as applicable.
5. Compare alternatives under matched assumptions and quantify their consequences.
6. Record the decision, its evidence and validity domain, affected results, and remaining uncertainty.
7. Preserve the previous source/result as historical when it has provenance value; create a new version rather than silently overwriting it.
8. Synchronize manuscripts and presentation documents only after the research decision is made.

Do not tune a calculation, input, normalization, or numerical method merely to reproduce a draft figure or desired conclusion.

## 4. Research entity and status discipline

Use the distinct levels defined by the [Scientific Diff Workflow](scientific-diff-workflow.md):

- **Project:** a sustained research programme.
- **Workstream:** a coherent part of a parent project.
- **Research change:** a bounded change with a frozen baseline, question, rationale, evidence, and impact review.
- **Run:** one actual execution tied to exact source, inputs, environment, command/settings, and outputs.
- **Claim:** one physical statement with an explicit scope and evidence.

Do not reuse one identifier namespace for different levels. A project registry is navigation metadata; it does not validate a result or imply completion.

Keep these status dimensions separate:

- **Work status:** planned, active, blocked, paused, complete, or archived.
- **Execution status:** not started, running, succeeded, partial, failed, cancelled, or blocked.
- **Validation status:** not run, partial, passed, failed, blocked, or inconclusive.
- **Scientific maturity:** diagnostic, provisional, reproducible, validated, historical, or superseded.
- **Archive status:** local only, committed to a PR branch, or merged and verified on the canonical branch.

For substantial numerical runs, use the exact RCRPS v1.0.1 field/status contract. Do not infer scientific maturity from execution or archival status.

## 5. Evidence and validation

Select validation methods according to the claim. A universal checklist must not replace physical judgment.

As applicable, distinguish symbolic/algebraic identities and analytic derivations; dimensions, units, signs, normalizations, conservation laws, and limiting cases; implementation and regression tests; numerical precision, grid/quadrature/interpolation/integration error, and uncertainty analysis; independent derivations, implementations, source/table comparisons, or benchmark reproductions; phenomenological, detector, statistical, or experimental validation.

An independent check should not merely repeat the same derivation, kernel, assumptions, or input transformation in a second wrapper. Describe the actual degree of independence.

Define the question, scope, and acceptance criteria before interpreting the result whenever practical. Record actual tolerances and residuals. A check not executed remains NOT RUN; an unavailable input remains BLOCKED; an inapplicable check is N/A with a reason. Do not add new acceptance conditions after a result passes unless new evidence reveals a real issue or the scope changes.

Report four separate facts where relevant: **computed**, **archived**, **numerically validated**, and **physically validated**. Do not promote one status to another without the corresponding evidence.

## 6. Historical and manuscript boundaries

- Preserve original inputs, historical results, source revisions, run manifests, and checksums.
- A new convention, code path, or input set produces a new versioned result with a clear relationship to its predecessor.
- Keep the original manuscript, working manuscript, reviewer response, internal audit, and research record as distinct document roles where a project uses them.
- A research/code PR must not silently change a manuscript or redefine a physical convention. Include manuscript changes only when explicitly in scope and separately identifiable in the diff.
- A manuscript may temporarily lag behind a validated research record; do not change a physical result merely to match a draft.

## 7. Relationship to other central standards

This document defines governance and authority boundaries. It does not duplicate the [Research Compute Policy](../RESEARCH_COMPUTE_POLICY.md), [Research Task Handoff Standard](RESEARCH_TASK_HANDOFF_STANDARD.md), [Scientific Diff Workflow](scientific-diff-workflow.md), [Research Quality Gate](governance/RESEARCH_QUALITY_GATE.md), [Calculation-result archival policy](CALCULATION_RESULT_ARCHIVAL_POLICY.md), [RCRPS v1.0.1](STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.md), [Scientific review checklist](review-checklist.md), or [Git merge policy](governance/GIT_MERGE_POLICY.md).

See the [Central Research Standards Index](governance/CENTRAL_STANDARDS_INDEX.md) for the authoritative source map.
