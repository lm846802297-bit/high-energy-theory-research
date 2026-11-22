---
name: high-energy-theory-research
description: Conduct rigorous, reproducible high-energy theoretical physics and phenomenology research, including literature analysis, derivations, symbolic checks, parameter scans, and manuscript verification.
---

# High-Energy Theory Research

Use this Skill for general high-energy theory and phenomenology research. Reviewer-response work is one supported workflow, not the primary purpose.

## Using the Skill across repositories

Follow the active repository's research instructions, conventions, and specialized Skills. Read task references relative to this Skill's installed directory. Apply the active project's archival and validation policies. The source repository's governance, registry, schema, and migration examples below apply to projects that explicitly adopt them. Run those commands from a compatible source checkout with the expected repository files available. The standalone user-level installation contains the Skill, references, and scripts. Its `skill-install-manifest.json` identifies the published source commit.

## Mandatory research discipline

1. **State conventions first.** Record the model/Lagrangian, fields and charges, metric and gamma-matrix conventions, normalization, renormalization scheme/scale, approximations, and units whenever they affect the result.
2. **Separate evidence classes.** Label what is derived in the current analysis, assumed, borrowed from literature, numerically checked, experimentally constrained, or still unverified.
3. **Keep claims traceable.** Every consequential claim should point to equations, source passages, code, numerical output, or a validation record. Do not treat a citation alone as verification.
4. **Check independently.** For important formulas, use a second route when feasible: dimensional analysis, limiting cases, symbolic algebra, numerical spot checks, an independent derivation, or a separate tool such as Mathematica/FeynCalc.
5. **Do not overstate validation.** A schema test does not establish physics correctness; a benchmark point does not represent a full parameter space; a successful run does not prove reproducibility unless its inputs and environment are identified.
6. **Preserve uncertainty.** Record unresolved ambiguities, failed checks, assumptions, and software/tool limitations. Never silently convert a failed or missing check into a pass.
7. **Do not promote candidate rules.** Candidate schemas and recommendations remain candidates until the decision register records explicit approval.
8. **Archive completed calculations.** For every substantial run, commit the essential native/uncompressed outputs, exact source revision, inputs, run manifest, and checksums under the canonical research record. Do not create a ZIP/TAR archive as a substitute for extracted result files. For large files, use durable versioned storage with a committed manifest, then verify the remote files after pushing. Follow the active repository's archival policy.

## Workflow

1. **Intake:** identify the research question, source papers/data, model definitions, symbols, conventions, requested deliverable, and relevant software versions.
2. **Plan:** break the question into testable tasks; define expected artifacts, dependencies, validation methods, and stopping criteria.
3. **Evidence:** retrieve primary sources where possible; record DOI/arXiv identifiers, version/date, exact supporting sections or equations, and source hashes for local artifacts.
4. **Derive and compute:** show intermediate steps for nontrivial derivations; use symbolic or numerical tools when they add independent evidence; record code, inputs, outputs, and environment.
5. **Verify:** test dimensions, signs, limiting cases, gauge/symmetry constraints, numerical stability, and independent formulations as applicable.
6. **Synthesize:** map conclusions to supporting evidence and distinguish established, conditional, excluded, allowed, not-assessed, and unresolved statements.
7. **Archive:** retain the run manifest, artifact identities, validation reports, and unresolved issues. Commit essential native/uncompressed result files and verify their remote hashes under the active repository's archival policy. Invalidate downstream results when relevant inputs or code change.

## Formula and loop-calculation checklist

- Define external momentum routing, index conventions, propagator and vertex conventions, and regularization scheme.
- Verify mass dimension and symmetry properties before relying on an expression.
- State approximations such as small mixing, decoupling, leading order, or EFT truncation explicitly.
- For FeynCalc, provide a runnable minimal example, package/version assumptions, expected symbolic structure, and at least one independent check.
- Distinguish a formal symbolic result from a finite renormalized observable.

## Parameter-space and experimental-constraint checklist

Report the parameter mapping, scan ranges, priors/sampling method, perturbativity and stability criteria, applicable experiments, likelihood/limit assumptions, and validity domain. Separate theoretical realizability from experimental allowance, exclusion, EFT-inapplicability, and unassessed regions. Label benchmark-dependent results in figures and captions; do not collapse disconnected allowed regions into one interval.

## Project and workstream selection

In the central source repository, consult `projects/README.md` and `projects/registry.yaml` before creating a research record. Identify the parent project and workstream rather than treating every calculation family as a top-level project. The current UV–EFT matching workstream belongs to axial-vector-model-building; do not register it as a separate top-level project.

The registry is navigation metadata, not a record in candidate Schema v1.4.3.7. To validate project/workstream IDs and declared local canonical paths, run:

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

Do not pass the navigation registry to validate_project_records.py. Use the structured-record validator only for a directory containing JSON/YAML records that follow the candidate record schemas. Neither validator establishes scientific correctness.

## Project record validation

When a project stores structured research records as JSON or YAML, run the bundled validator against the project record directory:

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
~~~

The record directory should contain only project record JSON/YAML files. The default schema directory is this repository's Schema v1.4.3.7 candidate bundle. The report checks declared schemas, mapped cross-record references, ID uniqueness, status/reason consistency, and local source/artifact paths. A clean report is a bounded software check; it does not certify a physics derivation, full state-machine coverage, or scientific acceptance.

## Migration safety

Treat schema migration as a separate, review-gated workflow. The bundled v1.3-to-v1.4 migration prototype is dry-run by default; even staging mode never commits or overwrites source records, and its report must keep `commit_allowed=false`.

For legacy `validation_ids`, resolve references only from the read-only source snapshot, using a unique primary ID within the same project. Map to `validation_plan_ids` only when the target record is a Validation Plan. Map to `validation_activity_ids` only when the target is a uniquely identified Validation Activity with `execution_status` in `in_progress`, `succeeded`, or `failed` and a non-empty `started_at`. Missing targets, duplicate IDs, project mismatches, unstarted activities, and unclear states remain unresolved; do not guess from the field name alone. An empty legacy list may be represented as two empty typed lists because it contains no references to classify.

The migration resolver does not implement transactional commit or rollback and does not recover a missing source-schema archive. Keep unresolved items visible, preserve source hashes, and do not treat a successful dry run as migration approval. Candidate Artifact decisions DD-ART-007 through DD-ART-010 remain pending until explicitly approved.

## Task-specific references

Load only the module required by the current task:

- Task selection: [references/task-router.md](references/task-router.md)
- Claim and evidence gates: [references/evidence-and-claim-gates.md](references/evidence-and-claim-gates.md)
- Source/version audit: [references/source-and-version-audit.md](references/source-and-version-audit.md)
- Symbolic algebra and loop calculations: [references/symbolic-calculation.md](references/symbolic-calculation.md)
- Numerical integration, scans, convergence, and error analysis: [references/numerical-scans-and-uncertainty.md](references/numerical-scans-and-uncertainty.md)
- Scientific figure design and QA: [references/scientific-figure-audit.md](references/scientific-figure-audit.md)
- Source-grounded paper reading: [references/paper-reading.md](references/paper-reading.md)
- Optional third-party tools, reviewed commit pins, license and dependency notes: [references/optional-tooling.md](references/optional-tooling.md)
- Central source checkout design and schema governance: `docs/design/README.md` and `docs/governance/DECISION_REGISTER.md`

The optional-tooling map does not install dependencies or make a tool mandatory. Choose methods from the problem's mathematical and physical structure, then use tools only when they add useful evidence.
