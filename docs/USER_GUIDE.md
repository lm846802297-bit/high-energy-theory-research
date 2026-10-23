# User Guide — High-Energy Theory Research

This guide explains how to use the repository as a **multi-project research platform**. It covers project organization, the research Skill, scientific change records, calculations, evidence, validation, and Git-based change control.

The repository is a research-process and traceability framework. It is not a fully autonomous research agent, and a successful software check does not certify a physical result.

## 1. Start here

If this is your first visit:

1. Read this guide once to understand the working model.
2. Open the [project registry](../projects/README.md) and [registry file](../projects/registry.yaml) to identify the correct project and workstream.
3. Read the [Scientific Diff workflow](scientific-diff-workflow.md).
4. Read the [research Skill](../skills/high-energy-theory-research/SKILL.md) before starting a calculation.
5. Open the selected project's canonical research record and Claim–Evidence Matrix.
6. Check [repository status](REPOSITORY_STATUS.md) and [open issues](OPEN_ISSUES.md) before changing the candidate Schema or migration behavior.

The root [README](../README.md) is the short landing page; this document is the detailed operational guide.

## 2. Understand the five levels

Do not use “project” to mean every folder or calculation. The repository distinguishes five levels:

| Level | Meaning | Example in this repository |
|---|---|---|
| Project | A sustained research programme with its own scope and lifecycle | axial-vector-model-building |
| Workstream | A coherent branch of work within a project | vll-higgs-singlet-uv-eft |
| Research change | A bounded scientific change with a baseline, rationale, evidence, and impact review | RC-001 |
| Run | One actual execution with source revision, inputs, environment, and outputs | Create a run record only when the run has actually occurred |
| Claim | One assessable physical statement with a valid domain and evidence | CL-015 |

A project can contain multiple workstreams. A workstream can contain multiple research changes. A change can need several runs and affect several claims. These identifiers are not interchangeable.

**Current hierarchy:** vll-higgs-singlet-uv-eft is a workstream within axial-vector-model-building; it is not a separate top-level project. RC-001-GAUGE-SUBGRAPHS is a linked subrecord of the UV–EFT research, not an independent top-level project.

## 3. Choose the right place for new work

Use this decision rule before creating files:

- **New top-level project:** the scientific programme has an independently meaningful scope, questions, lifecycle, and evidence base. Register it in [projects/registry.yaml](../projects/registry.yaml).
- **New workstream:** the work belongs to an existing project but needs a coherent scope, separate progress tracking, or a distinct calculation pipeline. Add it beneath that project's entry.
- **New research change:** one defined derivation, correction, calculation, cross-check, or manuscript-impact task changes the research state. Use the [research-change template](../templates/research-change.md).
- **New claim:** a physical statement needs its own evidence and validity-domain assessment. Add a row to the appropriate project-level Claim–Evidence Matrix.
- **New run:** a calculation or test actually executes. Record its exact code revision, inputs/configuration, environment, command, outputs, and status using the run-record conventions available in the project. Do not fabricate a run record for a planned check.
- **New generic method or tool:** if it is reusable across projects, place it in the shared skills/, schema/, templates/, docs/, tests/, or tools/ area rather than copying it into one project.

Do not register an unrelated project because its name appears in a paper, a note, or a possible future research idea. Register only projects whose identity and relationship are known.

## 4. Register a project or workstream

### 4.1 Edit the registry

The navigation registry is [projects/registry.yaml](../projects/registry.yaml). It currently describes the project hierarchy; it is **not** a record in candidate Schema v1.4.3.7 and is deliberately not fed into the structured research-record validator.

For a new top-level project, add a new item under projects with a stable project_id, title, status, scope, and optional workstreams. For a workstream, add it under the parent project's workstreams and set parent_project_id to the enclosing project_id.

Use stable lowercase hyphenated IDs. Do not recycle an ID after a project is renamed; update its title while retaining its identifier. Supported human workflow statuses are planned, active, blocked, paused, complete, and archived. Status describes work progress, not scientific correctness.

Example structure (illustrative only; do not copy example IDs into the live registry):

~~~yaml
projects:
  - project_id: example-research-programme
    title: Example research programme
    status: planned
    scope: One independently meaningful research programme.
    workstreams:
      - workstream_id: example-loop-matching
        title: Loop matching
        kind: research_branch
        status: planned
        parent_project_id: example-research-programme
        scope: Matching calculation and its validation.
        canonical_records: []
~~~

Do not invent repository URLs, baseline SHAs, completed checks, or scientific statuses. Use unknown, an empty optional field, or an explicit unresolved note when information is unavailable.

### 4.2 Use the project-record template

Start from the [project-record template](../templates/project-record.md). Fill in:

- identity and parent project;
- scope, included/excluded questions, model conventions, and baseline;
- workstreams and related research-change IDs;
- calculation entry points, run records, validation evidence, and Claim Matrix;
- established, conditional, and unresolved conclusions;
- one concrete next action and the evidence required to close it.

The template is a human-readable planning document. It does not automatically create structured records, run calculations, or approve the project.

### 4.3 Validate the registry

Run the dedicated registry/path checker:

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

This checker validates registry structure, stable IDs, parent/workstream relationships, and the existence and repository containment of declared canonical paths. It is a bounded navigation check, not a Schema v1.4.3.7 check and not a scientific validation.

## 5. Start a research change

For each substantive scientific change:

1. **Freeze the baseline.** Record the commit SHA, document revision, notebook version, or other immutable source.
2. **State one question.** Identify the specific formula, model assumption, observable, experimental interpretation, or manuscript claim under investigation.
3. **Define scope and controls.** Record included/excluded contributions, perturbative order, parameter range, renormalization scheme, IR prescription, approximations, and comparison baseline.
4. **Map dependencies.** Identify upstream assumptions and downstream equations, code, plots, claims, and manuscript sections that may change.
5. **Create a record.** Copy templates/research-change.md, assign a stable research-change ID, and link it to the parent project and workstream.
6. **Plan evidence before calculating.** Decide which analytical checks, numerical checks, independent derivations, package-level calculations, and experimental sources are needed.
7. **Compute and record.** Keep code, input parameters, output, environment, and limitations traceable.
8. **Assess the claim.** Update the relevant Claim–Evidence Matrix only after comparing the evidence with the exact claim and its valid domain.
9. **Review downstream impact.** Update affected figures, manuscript text, and reviewer responses only to the extent justified by the verified result.
10. **Close or carry forward.** Mark unresolved work explicitly and identify the next evidence-producing action.

See the [Scientific Diff workflow](scientific-diff-workflow.md) and [review checklist](review-checklist.md) for the full process.

## 6. Use the research Skill

The reusable instructions are in [skills/high-energy-theory-research/SKILL.md](../skills/high-energy-theory-research/SKILL.md). Use them as the research-method contract for literature work, derivations, loop calculations, parameter scans, experimental constraints, and manuscript verification.

Before starting a task, provide or locate:

- the parent project and workstream IDs;
- the research question and immutable baseline;
- the source papers/data and versions;
- the model, field content, charge assignments, notation, and conventions;
- the target order and approximation;
- expected outputs and independent validation methods;
- the current claim status and unresolved dependencies.

The Skill is an instruction scaffold plus references and scripts; it is not yet a fully executable agent that automatically performs every workflow stage. State which actions were actually performed and which remain planned.

## 7. Calculations and independent validation

Keep the following evidence categories distinct:

1. **Analytical derivation:** equations and intermediate steps under explicit assumptions.
2. **Symbolic/algebraic check:** e.g. SymPy or Mathematica simplification. State precisely which identities or coefficients were checked.
3. **Numerical check:** inputs, precision, convergence, stability, and output.
4. **Independent calculation:** a genuinely separate route, implementation, or derivation.
5. **Diagram-level validation:** e.g. a runnable FeynCalc/FeynArts calculation with package/version assumptions and documented output.
6. **Experimental validation/recast:** source version, data/likelihood, selection assumptions, recasting code, and applicable validity domain.
7. **Software/CI validation:** tests of code and workflow behavior.

One category does not imply another. A symbolic check is not diagram-level validation. A CI pass is not proof of a Wilson coefficient. A literature citation is not a reproduction. If a tool or environment is unavailable, record the missing evidence and its consequence.

For loop matching, record external momenta and flow, Feynman rules and signs, UV/IR regulators, renormalization convention, EFT subtraction prescription, counterterms, operator basis, EOM/Fierz conventions, and the order at which terms are retained.

## 8. Claim–Evidence Matrix

Use the [Claim–Evidence Matrix template](../templates/claim-evidence-matrix.md) to start a matrix for a new project, then keep the live matrix next to that project's canonical records.

Each row should contain one assessable physical statement, its assumptions and validity domain, derivation evidence, computational evidence, independent-check status, manuscript locations, and next action.

Use conservative statuses:

- **Proposed:** the claim has been formulated but evidence assessment is incomplete.
- **Supported:** the specified evidence supports the claim within the stated domain.
- **Conditionally supported:** support depends on explicit assumptions, benchmarks, or limits.
- **Unresolved:** evidence is missing, incomplete, or conflicting.
- **Contradicted:** checked evidence conflicts with the claim.
- **Superseded:** a later assessed result replaces the earlier statement.

Do not equate task completion with claim confirmation. A task may be complete because a discrepancy has been characterized while the physical claim remains unresolved.

## 9. Structured-record validator versus project-registry validator

There are two different tools; use the correct one.

### Project navigation registry

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

This checks project hierarchy metadata and declared paths only.

### Structured research records

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
~~~

This second command expects a directory containing only JSON/YAML records that follow the current candidate Schema v1.4.3.7 conventions. Do **not** pass [projects/registry.yaml](../projects/registry.yaml) or a folder containing Markdown notes to it. The candidate schema remains a development artifact; its validation is not formal schema approval and does not certify physics.

For both commands, inspect the full report, not only the exit code. Fix errors based on source evidence; do not suppress failures by weakening the schema or inventing references. The structured-record validator's documented limitations remain applicable, including incomplete state-machine coverage and no scientific-correctness certification.

## 10. Git, review, and release discipline

- Prefer one focused research change per branch or pull request.
- Keep the baseline and working revision identifiable.
- Review the actual diff, not just the commit message or green status.
- Run the tests that are available for the latest exact commit; identify skipped, unavailable, or stale checks explicitly.
- Avoid changing candidate Schema, migrations, and research content in one inseparable change.
- Do not merge a research change merely because its documentation is tidy. Check its scientific acceptance criteria separately.
- After integration, inspect the resulting default-branch state and update the research record with the exact integrated revision.
- Do not rewrite history or move large sets of files solely for cosmetic consistency.

## 11. File organization and migration

The shared platform layer is for reusable methods, schemas, templates, documentation, tests, and tools. Project-specific physics records and outputs should ultimately be easy to identify by project/workstream.

The current registry is an initial navigation layer. Existing research/, calculations/, and validation/ paths have intentionally not been moved. Before a future migration:

1. enumerate all files to be moved;
2. audit Markdown links, script imports, tests, CI paths, schema path rules, and validator assumptions;
3. map each old path to one new canonical path;
4. update all references in one reviewable change;
5. run link/path checks and relevant tests on the new commit;
6. preserve Git history and record the migration mapping;
7. keep the old baseline identifiable and do not claim scientific changes occurred if only paths changed.

Do not make the navigation registry part of the candidate schema unless that is separately designed, reviewed, versioned, and approved.

## 12. Current project example

The current registered hierarchy is:

- **Parent project:** axial-vector-model-building
- **Workstream:** vll-higgs-singlet-uv-eft
- **Main research record:** [RC-001-vll-higgs-singlet-uv-eft.md](../research/RC-001-vll-higgs-singlet-uv-eft.md)
- **Gauge-subgraph record:** [RC-001-gauge-subgraph-change-record.md](../research/RC-001-gauge-subgraph-change-record.md)
- **Claim Matrix:** [RC-001-claim-evidence-matrix.md](../research/RC-001-claim-evidence-matrix.md)

Its status is verification in progress. Some analytic integral and symbolic/algebraic sub-blocks are documented, but the complete Wilson-coefficient vector, all relevant gauge/box contributions, common-basis reduction, and independent diagram-level validation remain open. This example demonstrates traceability and status discipline; it must not be read as a claim that the full matching is complete.

## 13. Troubleshooting

- **Should this be a project or a workstream?** Use a top-level project only for an independently meaningful research programme. If it is part of the axial-vector model programme, register it as a workstream.
- **Can I run the structured-record validator on the registry?** No. Use the project-registry checker for projects/registry.yaml.
- **The algebra check passed; can I mark the physics claim supported?** Only if that check is sufficient for the exact claim and domain. Otherwise record the missing independent evidence.
- **CI is unavailable.** Record it as not run/blocked; do not mark it passed and do not confuse this software limitation with scientific evidence.
- **Can I move the existing RC-001 files now?** Not until the path, schema, test, and workflow dependency audit is complete and the migration is reviewed.
- **Can I register another research topic?** Yes, when its parent-project relationship is known. Do not infer that relationship from a filename alone.
