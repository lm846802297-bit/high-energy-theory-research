# Research Project Record

> Copy this template for a top-level research project. For a coherent branch of an existing project, use the same fields but set kind to workstream and identify parent_project_id. Do not create a separate project merely to give a calculation family its own folder.

## 1. Identity

- **Project/workstream ID:** [stable, immutable identifier]
- **Title:** [short title]
- **Kind:** [project / workstream]
- **Parent project ID:** [ID or N/A for a top-level project]
- **Status:** [planned / active / blocked / paused / complete / archived]
- **Owner / contributors:** [roles or names, if appropriate]
- **Created / updated:** [YYYY-MM-DD]
- **Source repository:** [URL or unknown; do not infer]
- **Canonical project index:** [path]

## 2. Research scope

- **Research questions:** [questions to be answered]
- **Included:** [models, calculations, observables, parameter ranges]
- **Excluded:** [explicit boundaries]
- **Model and conventions:** [canonical record or document]
- **Baseline:** [immutable commit/version or unknown]
- **Dependencies:** [project IDs, papers, datasets, software]

## 3. Workstreams and research changes

| ID | Kind | Status | Canonical record | Depends on |
|---|---|---|---|---|
| [ID] | [workstream / research change] | [status] | [path] | [IDs] |

Keep project/workstream IDs distinct from research-change IDs, run IDs, and claim IDs.

## 4. Computation and evidence

- **Calculation entry points:** [paths]
- **Run manifests / input configurations:** [paths or not yet implemented]
- **Validation records:** [paths]
- **Claim–evidence matrix:** [path]
- **Independent checks required:** [methods and status]
- **Scientific acceptance criteria:** [criteria]

A script, planned test, captured algebraic check, successful CI run, or merged commit is not by itself proof of a physical claim. Record only checks that actually ran and retain the limitations.

## 5. Current state and next actions

- **Established within stated scope:** [claims and evidence]
- **Conditional:** [assumptions and conditions]
- **Unresolved:** [questions and missing evidence]
- **Blocked by:** [dependency or resource]
- **Next action:** [one concrete, evidence-producing step]
- **Completion criteria:** [what evidence closes the task]

## 6. Change control

- Keep a stable baseline and use reviewable commits for substantive changes.
- Update dependent claims and artifacts when upstream assumptions or equations change.
- Do not move files without a path/reference audit.
- Keep project status, research-change status, claim status, and evidence status separate.
