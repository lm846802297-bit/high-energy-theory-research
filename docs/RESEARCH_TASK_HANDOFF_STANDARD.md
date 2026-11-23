# Research Task Handoff Standard

简体中文版：[RESEARCH_TASK_HANDOFF_STANDARD.zh-CN.md](RESEARCH_TASK_HANDOFF_STANDARD.zh-CN.md)。

**Status:** adopted shared standard  
**Effective date:** 2026-11-23  
**Scope:** substantive research tasks and cross-model/collaborator handoffs in adopting project repositories

A research task must be reproducible as an instruction, not reconstructed from chat history or inferred from a previous model's summary. The Research Task Brief defines the question, sources, fixed conventions, assumptions, independent work, checks, expected outputs, and unresolved issues.

The brief is a task specification. It is not evidence that a derivation, calculation, test, or validation has been completed. Completion evidence belongs in the research-change record, study README, audit report, run manifest, and/or pull request.

## 1. When a brief is required

Create a completed brief before substantial work involving one or more of:

- a physical derivation, matching calculation, or interpretation of a paper;
- a numerical calculation, simulation, substantial parameter scan, data transformation, or scientific figure/dataset intended to support a claim or benchmark;
- a change to production code, physical conventions, input data, or validation logic;
- independent work by multiple models, agents, researchers, or collaborators;
- a result intended to support a benchmark, scientific conclusion, manuscript statement, or formal repository record.

A trivial editorial or repository-maintenance change with no scientific content may omit the brief when the PR explains why it is not applicable. Keep the brief proportional to the task: concise answers are sufficient, and it is not a research proposal. Historical work does not need retroactive briefs; apply the standard to new substantive work and follow-up tasks.

## 2. Canonical location and identity

Use the [Research Task Brief template](../templates/research-task-brief.md).

Preferred locations are a topic-local task_briefs directory or a repository-level research/docs/task_briefs directory. These are defaults, not a mandate to restructure an existing project. If a project already has an established task-record location, use it and link the brief from the relevant study README, issue, or PR. Do not create a new research directory solely to host a task brief.

Use a stable ID such as YYYYMMDD-short-kebab-case. A branch name, chat message, or PR title is not a substitute.

## 3. Required brief fields

Complete all ten fields. If a field does not apply, write N/A and explain why. Do not leave ambiguous blanks.

1. **Research question:** one answerable question, the object studied, requested parameter/kinematic range, included/excluded scope, and the level of claim the task may support.
2. **Primary sources and materials:** papers with title/authors/DOI or arXiv/version and exact equations/pages; repositories with path/branch/full commit; data/files with source/version/license and SHA-256 where content identity matters. Identify inaccessible sources and their impact.
3. **Git baseline and versions:** repository, branch, full baseline SHA, relevant code/input/submodule/package versions, working-tree state, and exact comparison baseline. Resolve moving branch names to a commit at handoff time.
4. **Conventions:** every definition that can change a sign, factor, variable meaning, or numerical value. As applicable include metric, units, momentum definitions, Fourier phases, gamma matrices, propagator/width signs, state/current normalization, coupling conventions, spin averages, symmetry factors, frames, and angular/energy definitions. Mark unresolved conventions explicitly.
5. **Assumptions and approximations:** model content, degrees of freedom, parameter benchmark, kinematic regime, truncation, omitted contributions, and validity range. Distinguish adopted assumptions from facts established by derivation or data.
6. **Known validated results:** only results with identifiable evidence and scope. Record claim, benchmark/range, code/input revision, method, residual/tolerance, and status. Treat unsupported prior summaries as hypotheses.
7. **Required independent derivation:** identify the exact equations/conclusions to reconstruct from primary sources, definitions, or data; expose intermediate steps, signs, normalization, and approximations. State comparison targets without using them as proof.
8. **Required numerical/technical checks:** specify method and acceptance criterion for dimensions/units, analytic limits, conservation, signs/normalization, independent comparison, convergence, regression, uncertainty, and output integrity as applicable.
9. **Expected outputs:** paths, formats, metadata, reproduction commands, tests, run manifests, figures, audit records, PR, and the permitted conclusion level.
10. **Unresolved questions:** competing definitions/values, source of each, impact, whether blocking, and next discriminating check.

## 3A. Standards provenance

For each substantive task, record the central standards source and the profiles actually applied in the Research Task Brief. Use the downstream repository's `research/standards-lock.yaml` (or its declared canonical path) as the adoption authority; do not resolve a moving central branch during execution.

The task record must identify the exact central commit, lock-file path and SHA-256, task-brief path and SHA-256, applied profile IDs, project-local extensions, and the predeclared acceptance criteria. Select only profiles relevant to the task. Do not claim a profile was applied merely because it appears in the lock.

For RCRPS v1.0.1 numerical runs, repeat this provenance in `run_manifest.extensions.standards_provenance` so the execution record remains independently traceable after the task brief is archived. Generate file hashes from the actual bytes; never use placeholders. The central adoption validator checks record structure and supplied file fingerprints, not whether an agent's reasoning complied with every normative statement.

## 4. Execution and change control

1. Derive independently from primary sources; previous model outputs are leads and comparison points, not authorities.
2. Do not silently change conventions. Record the old and proposed definitions, reason, and impact before changing a convention that affects the requested physics.
3. Separate derivation from implementation; independently check the implementation.
4. Define relevant acceptance criteria before judging outputs whenever practical. Report actual residuals, tolerances, commands, logs, and exact revisions.
5. Mark failed, partial, blocked, and unrun checks truthfully.
6. Preserve exact source revisions, input hashes, runtime/dependencies, commands, numerical settings, and output checksums.
7. Preserve historical results. A changed convention or implementation creates a new versioned result; do not overwrite the previous one.

If the scope, source revision, assumptions, or conventions change, add a dated change-log entry or create a linked successor brief. Do not silently replace the original task definition.

## 5. Required return record

The receiving researcher/model returns the answer and scope actually resolved; independent derivation and key equations; conventions confirmed or justified deviations; assumptions and validity range; numerical/technical checks, methods, tolerances, residuals, and statuses; prior results reused with exact provenance; unresolved discrepancies and next checks; artifact paths, formats, checksums, commands, and exact commit/PR; and final scientific status with the precise claim it supports.

## 6. Relationship to other standards

The task brief defines what is requested before execution. It does not replace the [Scientific Diff Workflow](scientific-diff-workflow.md), which records the scientific change and its impact; [RCRPS v1.0.1](STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.md), which records actual runs, results, and validation; the [Calculation-result archival policy](CALCULATION_RESULT_ARCHIVAL_POLICY.md); or the project-specific AGENTS.md, scientific conventions, and domain-validation profile.

CI remains optional unless a task brief explicitly requests a particular independent workflow run. A green CI badge does not replace the derivation and checks specified in the brief.
