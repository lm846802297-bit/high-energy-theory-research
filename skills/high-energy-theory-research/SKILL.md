---
name: high-energy-theory-research
description: Use for substantial high-energy theory research involving literature, multi-step derivations, symbolic or numerical calculations, or reproducibility audits. Do not invoke solely for elementary self-contained derivations or routine algebra unless requested.
---

# High-Energy Theory Research

Use this Skill when a task needs source-grounded research, a nontrivial multi-step derivation, symbolic/loop calculation, numerical study, or a reproducible manuscript/project audit. Do not treat the field label “particle physics” alone as a reason to load the full workflow. For a self-contained elementary derivation, routine algebra, a simple Jacobian, a direct dimensional check, or a focused conceptual question, answer directly unless the user explicitly requests the Skill workflow. When the Skill is explicitly invoked for a simple task, apply only the lightweight path below; invocation does not make tools, manifests, or archival steps mandatory. Reviewer-response work is one supported workflow, not the primary purpose.

## Using the Skill across repositories

Follow the active repository's research instructions, conventions, and specialized Skills. Read task references relative to this Skill's installed directory. Apply the active project's archival and validation policies. The source repository's governance, registry, schema, and migration examples below apply to projects that explicitly adopt them. Run those commands from a compatible source checkout with the expected repository files available. The standalone user-level installation contains the Skill, references, and scripts. Its `skill-install-manifest.json` identifies the published source commit.

## Task-complexity gate and proportionality

Classify the task before loading references or selecting tools. Choose the lowest-effort path that satisfies the user's requested result and the actual evidence requirements.

- **Quick analytic task:** a self-contained identity, elementary factorization, simple Jacobian, short exact integral, dimensional check, or focused conceptual question. State only assumptions/conventions that affect the result, derive directly, and perform one appropriate low-cost check. Do not search, run code, load specialist references, create a run manifest, or archive a chat answer by default.
- **Focused research task:** a specific paper, equation, figure, source claim, or nontrivial analytic derivation. For source-dependent work, inspect the relevant primary source; for a self-contained derivation, derive from the stated inputs and assumptions without inventing a source-search requirement. Load only the matching reference when it adds useful guidance. Keep source claims traceable and perform an independent check when it adds useful evidence.
- **Numerical/computational task:** numerical integration, parameter scans, fitting, Monte Carlo, generated data, or code whose output supports a quantitative claim. Load the numerical reference and use the corresponding run-record, convergence, uncertainty, and provenance requirements.
- **Project-level task:** a long-running or multi-stage calculation, manuscript/reviewer-response package, multi-file research deliverable, or collaborative repository workflow. Use the full planning, dependency, provenance, archival, and review process required by the active project.

The task's physics domain alone does not determine its tier. A particle-physics question can be a quick analytic task. Escalate only when a concrete feature requires it: missing source evidence, nontrivial numerical uncertainty, substantial code/data, multiple dependent workstreams, or an explicit user requirement for reproducibility or archival.

For optional tools and extra checks, ask: **Which specific failure mode will this detect, what new evidence will it add, and is that evidence worth the cost?** If no concrete answer exists, skip the tool or check. A second check need not be a second computation. Prefer exact substitution, a distinct algebraic factorization, dimensions, or a relevant limit when those are sufficient. Do not run a numerical integral merely to demonstrate that a second method was used.

Stop when the requested deliverable and its preselected acceptance checks are satisfied. Do not add searches, calculations, caveats, manifests, or archival steps solely for completeness or appearance of rigor. If the user requests a more complete audit, expand the workflow to that scope.


## Mandatory research discipline

1. **State conventions first.** Record the model/Lagrangian, fields and charges, metric and gamma-matrix conventions, normalization, renormalization scheme/scale, approximations, and units whenever they affect the result.
2. **Separate evidence classes.** Label what is derived in the current analysis, assumed, borrowed from literature, numerically checked, experimentally constrained, or still unverified.
3. **Keep claims traceable.** Every consequential claim should point to equations, source passages, code, numerical output, or a validation record. Do not treat a citation alone as verification.
4. **Check independently, in proportion to the task.** For important formulas, choose the least costly genuinely useful check for the relevant failure mode: substitution into the original expression, dimensions, a limiting case, a distinct algebraic derivation, or an independent tool. A second route need not be a numerical computation. Do not add a numerical calculation when an exact analytic/algebraic check already provides the needed evidence. If a numerical check is chosen, follow the numerical reference's evidence and run-record requirements.
5. **Do not overstate validation.** A schema test does not establish physics correctness; a benchmark point does not represent a full parameter space; a successful run does not prove reproducibility unless its inputs and environment are identified.
6. **Preserve uncertainty.** Record unresolved ambiguities, failed checks, assumptions, and software/tool limitations. Never silently convert a failed or missing check into a pass.
7. **Do not promote candidate rules.** Candidate schemas and recommendations remain candidates until the decision register records explicit approval.
8. **Archive substantial work.** For production calculations, substantial computational runs, or project-level deliverables, commit the essential native/uncompressed outputs, exact source revision, inputs, run manifest, and checksums under the canonical research record. Do not create a ZIP/TAR archive as a substitute for extracted result files. For large files, use durable versioned storage with a committed manifest, then verify the remote files after pushing. Follow the active repository's archival policy. Do not create a project record, run manifest, commit, or archive for a short self-contained analytic answer unless the user or active project explicitly requires it.

## Workflow

Apply only the stages relevant to the selected task tier; this is not a mandatory seven-step checklist for every question. For a quick analytic task, the normal path is: state relevant assumptions, derive the result, perform one appropriate low-cost check, and answer. Use the full sequence below for focused research, numerical work, or project-level tasks as needed.

1. **Intake:** identify the research question, source papers/data, model definitions, symbols, conventions, requested deliverable, and relevant software versions.
2. **Plan:** break the question into testable tasks; define expected artifacts, dependencies, validation methods, and stopping criteria.
3. **Evidence:** retrieve primary sources where possible; record DOI/arXiv identifiers, version/date, exact supporting sections or equations, and source hashes for local artifacts.
4. **Derive and compute:** show intermediate steps for nontrivial derivations; use symbolic or numerical tools when they add independent evidence; record code, inputs, outputs, and environment.
5. **Verify:** test dimensions, signs, limiting cases, gauge/symmetry constraints, numerical stability, and independent formulations as applicable.
6. **Synthesize:** map conclusions to supporting evidence and distinguish established, conditional, excluded, allowed, not-assessed, and unresolved statements.
7. **Archive when warranted:** for substantial computations and project deliverables, retain the run manifest, artifact identities, validation reports, and unresolved issues. Commit essential native/uncompressed result files and verify their remote hashes under the active repository's archival policy. Invalidate downstream results when relevant inputs or code change. Skip this stage for a quick analytic response unless explicitly required.

## Formula and loop-calculation checklist

- Define external momentum routing, index conventions, propagator and vertex conventions, and regularization scheme.
- Verify mass dimension and symmetry properties before relying on an expression.
- State approximations such as small mixing, decoupling, leading order, or EFT truncation explicitly.
- For FeynCalc, provide a runnable minimal example, package/version assumptions, expected symbolic structure, and at least one independent check.
- Distinguish a formal symbolic result from a finite renormalized observable.

## Parameter-space and experimental-constraint checklist

Report the parameter mapping, scan ranges, priors/sampling method, perturbativity and stability criteria, applicable experiments, likelihood/limit assumptions, and validity domain. Separate theoretical realizability from experimental allowance, exclusion, EFT-inapplicability, and unassessed regions. Label benchmark-dependent results in figures and captions; do not collapse disconnected allowed regions into one interval.

## Project-specific governance

The central source repository has its own project registry, candidate schemas, and migration rules. Load [references/central-repository-governance.md](references/central-repository-governance.md) only when the active repository is `high-energy-theory-research` or the project explicitly adopts that registry/schema contract. Do not apply its project IDs, candidate schemas, validators, or migration rules to unrelated repositories.

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
- Central-repository project registry, candidate schemas, and migration governance: [references/central-repository-governance.md](references/central-repository-governance.md) (load only when applicable)

The optional-tooling map does not install dependencies or make a tool mandatory. Choose methods from the problem's mathematical and physical structure, then use tools only when they add useful evidence.
