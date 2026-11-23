# Shared Research Quality Gate

简体中文版：[RESEARCH_QUALITY_GATE.zh-CN.md](RESEARCH_QUALITY_GATE.zh-CN.md)。

**Status:** adopted shared minimum  
**Effective date:** 2026-11-23  
**Scope:** research changes in repositories that adopt the central standards framework

The Research Quality Gate maps shared research-quality requirements to task-appropriate evidence. It is not a fixed mathematical workflow, a universal numeric tolerance, or a requirement that every task run every test.

## 1. Ten quality areas

| # | Gate | Minimum evidence |
|---:|---|---|
| 1 | Exact source and baseline identity | Repository, branch, full baseline/source commit SHA, relevant file/blob identities, and working-tree state when it affects the work |
| 2 | Input provenance and integrity | Source/version/license or access conditions, exact input identity, transformations, and SHA-256 when bytes are available; immutable versioned locator when bytes cannot be archived |
| 3 | Execution environment | Actual execution target, OS/runtime, compiler/interpreter, dependencies, command, and relevant resource details for work that executes code |
| 4 | Hardware and physical/numerical configuration | Relevant CPU/GPU/memory/storage facts plus physical parameters, units, conventions, grids, precision, tolerances, seeds, and boundary conditions; N/A for work with no such execution |
| 5 | Native outputs and archive integrity | Editable source/derivation, native data/results, logs/reports as applicable, output inventory, counts/units, hashes, and verified remote archive location |
| 6 | Numerical precision, convergence, and error | Method, precision, grid/quadrature/interpolation/integration checks, uncertainty/error estimates, actual residuals, and predeclared acceptance criteria where numerical work is performed |
| 7 | Independent scientific/physical validation | Analytic limits, dimensions, conservation/symmetry identities, independent derivation/implementation, source/table comparison, or domain-specific validation appropriate to the claim |
| 8 | Relevant software regression tests | Tests that exercise the changed code/schema/workflow behavior; exact command and result. Run in the active primary or approved verification environment; Actions is optional |
| 9 | Independent technical review | Review of the actual diff and evidence by a reviewer distinct from the authoring pass; findings, severity, disposition, and reviewed commit SHA |
| 10 | PR review and integration | Focused PR, accurate scope/status, pre-merge review and owner authorization; after integration, verified merge commit and canonical-branch state |

## 2. Task profiles

Apply the following profiles. A project may add a stricter domain profile without weakening the shared minimum.

| Task profile | Required gates | Typical N/A gates |
|---|---|---|
| Analytical derivation / theory | 1, 2, 4, 5, 7, 9, 10; 3 and 8 when symbolic/code execution is used | 3 for a purely handwritten derivation; 6 when no numerical claim is made |
| Numerical computation / simulation / scan | 1–7; Gate 8 applies when code/workflows are changed or added; Gates 9 and 10 apply when PR review and integration are used | Gates 3/4 when no code is executed; other genuinely inapplicable individual checks, with reasons |
| Code / validator / workflow change | 1, 2, 3, 5, 8, 9, 10; 4, 6, 7 when the change affects physical or numerical behavior | 6 or 7 for purely mechanical tooling that cannot affect scientific behavior |
| Data transformation / archival migration | 1–5, 8 where tooling changes, 9, 10; 6 and 7 where data meaning or physical interpretation changes | 6/7 for byte-preserving path-only migrations |
| Manuscript / document / literature review | 1, 2, 5, 7, 9, 10; 3 and 8 when compilation, extraction, or scripts are used | 4/6 when no new physical/numerical claim or calculation is involved |
| Repository maintenance | 1, 5, 8 where relevant, 9, 10 | 2–4, 6, 7 when no inputs, execution, or scientific content are affected |

A gate can be N/A only with an explicit reason. Do not mark a required but unexecuted check as PASS.

## 3. Gate status vocabulary

Use one status for each applicable gate:

- **PASS:** the required evidence exists and satisfies the stated acceptance criterion for the exact scope and commit.
- **FAIL:** an executed check or review found a concrete acceptance failure.
- **BLOCKED:** a required check cannot be performed because a specific source, resource, permission, or dependency is unavailable.
- **NOT RUN:** the check is applicable but has not been executed.
- **N/A:** the check is genuinely outside the task scope; state why.

Do not infer PASS from a plan, source-code presence, green unrelated CI, successful process exit, matching checksum, or a previous commit's result. If evidence is inconclusive, state the observed result and keep the gate BLOCKED or NOT RUN as appropriate; do not force a PASS.

## 4. Minimum sufficient acceptance

Acceptance is organized around the research question and the physical claim the task is intended to support, not around maximizing the number of checks. Before work begins, define the question, scope, task profile, the paper figure/equation/numerical conclusion/physical judgment that may be affected, and the acceptance criteria sufficient to support that claim.

1. **State the research purpose.** Identify which figure, equation, numerical result, or physical judgment may change. Do not start work solely to expand technical coverage when no connection to the research objective can be stated.
2. **Select necessary checks.** Select from the ten quality areas only those that bear on the task's claim. Task profiles are applicability guides, not mechanical instructions to run every test, grid, or workflow. Mark genuinely inapplicable items N/A with a reason; report applicable but unexecuted checks as NOT RUN or BLOCKED.
3. **Reuse historical validation.** When relevant source, inputs, conventions, execution environment, and supported claim have not changed, cite the existing validation tied to its exact version rather than repeating calculations or rerunning tests. If a relevant dependency changes, recheck only affected results and checks; an unrelated change does not justify a full revalidation.
4. **Accept once and freeze.** Define numerical methods, error/tolerance criteria, and physical acceptance conditions before execution. Once the predeclared criteria are met, freeze the result. Reopen it only for a concrete error, new evidence, relevant dependency change, or scope change; do not add new conditions at closeout or repeatedly reopen passed items.
5. **Merge and archive.** A PR requires only the evidence, review, and owner authorization necessary for its actual change scope and supported claims. Unrelated follow-up work must be recorded separately and must not block the current merge. After merging, verify the exact merge commit and canonical branch state.

Additional execution rules:

- Choose numerical methods and tolerances according to the physics and observable; the central standard prescribes no universal quadrature order, precision, or percentage tolerance.
- A software test validates only the code path/assertion it exercises; it does not automatically validate a physical derivation. A convergence check validates numerical stability within its tested setup, not the model or approximation itself.
- State what is independent in an independent validation; two wrappers sharing the same algebraic kernel are not automatically independent implementations.
- Preserve historical outputs and create new versioned results when assumptions, conventions, or code change; do not overwrite old results.
- Do not expand the current research scope merely to clear a checklist, increase CI counts, or complete a general-purpose technical platform.

## 5. Independent review and GPT review

The reviewer must inspect the actual diff, relevant source/input provenance, test coverage, claims, and acceptance evidence—not only the PR description.

A project owner may designate GPT as the default technical reviewer. The review record must identify the reviewed HEAD SHA, review scope, findings, and disposition. The review should be independent of the implementation pass; when the same agent authored the change, it must state that limitation and use a fresh review pass or other independent check where practical.

A technical review comment is not the same as a GitHub formal APPROVE. Never impersonate another GitHub account or claim an approval that GitHub did not record. Repository branch-protection and permission rules remain platform-specific; this standard does not require an additional human reviewer by default.

## 6. CI and merge

GitHub Actions is optional unless the task owner explicitly requires a particular workflow. Relevant checks may run in the primary execution environment or an approved independent environment. A queued or unavailable Actions run does not block work when the required evidence can be obtained elsewhere.

Merge decisions follow the [Git merge policy](GIT_MERGE_POLICY.md). Gate 10 has two checkpoints: before merge, the focused PR must have an accurate scope/status, completed review, required evidence, and owner authorization; after merge, the exact merge commit and integrated canonical-branch state must be verified. Before integration, all other applicable required gates must be PASS, with N/A items justified under the task profile. Mark Gate 10 fully PASS only after post-merge verification. A BLOCKED or NOT RUN item cannot replace evidence required by the task's acceptance criteria.

## 7. Relationship to structured result statuses

For numerical runs, use RCRPS v1.0.1 for machine-readable execution, validation, scientific-maturity, and archive fields. The gate statuses above describe requirement-level acceptance; they do not replace RCRPS record statuses.

See the [Central Research Standards Index](CENTRAL_STANDARDS_INDEX.md).
