# Scientific Diff Workflow

## 1. Purpose and scope

Scientific Diff is a change-tracking and evidence-management method for theoretical and phenomenological research. Its purpose is to preserve a traceable chain from a scientific question to the physical claims and manuscript statements that depend on it.

It can be used for model building, symmetry and field-content checks, analytical derivations, loop calculations, renormalization, UV–EFT matching, symbolic or numerical computation, parameter scans, experimental constraints, figures, and reviewer responses.

The method is deliberately conservative: it records what is known, what changed, what was checked, and what remains unresolved. It does not turn a Git commit, a green CI run, or a completed notebook into proof of physical correctness.

## 2. What counts as a scientific diff?

A scientific diff compares a clearly identified baseline with a proposed or current research state. Each change should answer five questions:

1. **What changed?** Identify the model assumption, equation, implementation, input, output, constraint, claim, or manuscript passage.
2. **Why did it change?** State the scientific question or discovered problem that motivated the change.
3. **What evidence supports it?** Link derivations, calculations, source data, literature inputs, logs, figures, and independent checks.
4. **What is the scope of validity?** Record approximations, parameter ranges, conventions, schemes, benchmarks, and exclusions.
5. **What else is affected?** Trace dependencies to calculations, plots, physical claims, and manuscript text.

A textual diff is one evidence item within this process, not the whole process.

## 3. Change layers

Classify each change by one or more layers.

| Layer | Examples | Required comparison |
|---|---|---|
| Model and assumptions | Field content, charges, symmetries, couplings, mass hierarchy, benchmark | Previous and new assumptions; consequences for the model |
| Analytical derivation | Algebra, equations of motion, diagonalization, amplitudes, loop integrals | Starting expression, transformations, conventions, approximations, final expression |
| Computational implementation | Mathematica notebook, Python code, symbolic package, numerical routine | Source diff, software/package versions, settings, precision, seeds where relevant |
| Inputs and data | Parameter cards, experimental data, reference values, external constraints | Provenance, units, selection criteria, dates or versions, transformations |
| Numerical results | Matching coefficients, scan outputs, spectra, limits, figures | Reproducible run configuration, tolerances, convergence, comparison to baseline |
| Physical claims | A bound, allowed region, decoupling statement, hierarchy, mechanism | Exact claim, evidence chain, assumptions, uncertainty, counterchecks |
| Manuscript and response | Equations, prose, captions, appendices, referee replies | Textual diff mapped to the validated scientific change |

One research change can span multiple layers. Record the layers explicitly instead of assuming a code diff captures the scientific impact.

## 4. The unit of work: a research-change record

Assign each substantive change a stable identifier, such as RC-001. Do not use a Git commit hash as the scientific identifier: a research change can span multiple commits, and a commit can contain more than one research change.

For each record, capture:

- research question and motivation;
- baseline commit, document version, or artifact identifier;
- target result and scope;
- assumptions and conventions that changed or remained fixed;
- derivation and computation changes;
- inputs, environment, outputs, and artifact locations;
- validation plan and actual results;
- affected claims, figures, tables, and manuscript locations;
- unresolved questions and the decision made.

Use the template in **templates/research-change.md**.


### Project hierarchy: project → workstream → change → run → claim

The project hierarchy is separate from the Scientific Diff change record. Use the following levels consistently:

1. **Project:** a sustained research programme with an independently meaningful scope, such as axial-vector-model-building.
2. **Workstream:** a coherent branch of work within a project, such as vll-higgs-singlet-uv-eft. A workstream may have its own files, calculations, and status without becoming a separate top-level project.
3. **Research change:** a scientific change with a baseline, rationale, evidence, and impact review, such as RC-001.
4. **Run:** one actual execution identified by source revision, inputs, environment, command/configuration, and outputs. Do not invent a run record for a planned or unexecuted check.
5. **Claim:** a physical statement whose evidence and scope are assessed separately, such as CL-015.

A project may contain multiple workstreams; a workstream may contain multiple research changes; a change may require multiple runs and may affect multiple claims. Do not reuse one identifier namespace for these distinct entities.

The navigation registry in projects/README.md and projects/registry.yaml is currently descriptive metadata only. It is not a new normative schema and is not a substitute for the candidate structured-record system. Registering a project does not migrate files or validate the physics. Before moving existing artifacts, audit relative links, schema path rules, validator assumptions, scripts, tests, and CI references.

## 5. Recommended workflow

### Stage 0 — Freeze the baseline

Identify the last interpretable state before changing it. Record its commit or version, relevant files, parameter configuration, generated outputs, and current claim wording. Preserve the original outputs where practical.

A baseline is a reference point, not a declaration that its results are correct.

### Stage 1 — State one scientific question

Write the question so that an answer could be supported or rejected by evidence. Separate the scientific question from the proposed solution.

Good: “Under the stated coupling and mass assumptions, can the finite vector component change the exclusion obtained in the pure axial limit?”

Not sufficient: “Improve the exclusion plot.”

Do not presuppose that a new effect is negligible or important.

### Stage 2 — Define the delta and the controls

Specify what will change and what is held fixed. Record model conventions, units, signs, normalization, renormalization scheme and scale where relevant, benchmark assumptions, parameter ranges, and approximations.

If several changes are logically independent, split them into separate records or clearly separate their evidence and conclusions.

### Stage 3 — Map dependencies before computing

Identify upstream inputs and downstream products. A useful dependency chain is:

Scientific question → assumptions/model → derivation → implementation → outputs → verification → physical claim → figure/table → manuscript/reply.

If an upstream node changes, review every dependent node. Do not reuse an old plot or result merely because its filename has not changed.

### Stage 4 — Derive and implement

Keep analytical reasoning distinguishable from software implementation. Record important intermediate expressions, definitions, conventions, and transformations. Where a symbolic tool is used, identify the notebook or script and the relevant cells, functions, or outputs.

A computer algebra system can validate manipulations under its assumptions; it does not establish that the assumptions represent the intended physical model.

### Stage 5 — Run calculations reproducibly

For each result that matters, record as applicable:

- source revision and script/notebook identity;
- input files and parameter values;
- software and relevant package versions;
- numerical precision, tolerances, convergence criteria, and random seeds;
- command or execution procedure;
- output paths and hashes for large or binary artifacts;
- warnings, failures, discarded runs, and post-processing steps.

Do not record a run as reproducible if the input configuration or necessary environment is missing. Archive substantial runs under the canonical research record with directly accessible native outputs, provenance, and checksums; follow the mandatory [calculation-result archival policy](CALCULATION_RESULT_ARCHIVAL_POLICY.md). Do not use a newly created ZIP/TAR archive as a substitute for extracted result files.

### Stage 6 — Verify using checks appropriate to the physics

Choose checks based on the specific derivation and observable. Examples include:

- dimensional analysis and sign/convention checks;
- symmetry, gauge-invariance, charge assignment, and anomaly-cancellation checks where applicable;
- known limits, decoupling limits, perturbative order, and consistency with analytically controlled cases;
- independent derivations or implementations for high-impact results;
- comparison with established results only when conventions and assumptions match;
- numerical convergence, stability, precision sensitivity, and scan coverage;
- matching-scale and renormalization-scheme consistency where relevant;
- experimental-constraint applicability, likelihood or confidence-level interpretation, and correct mapping from model parameters to observables.

Not every item applies to every calculation. Mark a check “N/A” only with a brief reason. A check that has not been run is “not checked,” not “passed.”

### Stage 7 — Evaluate the claim, not just the output

For each important physical statement, ask:

- Does the evidence directly support this statement?
- Is the statement valid across the claimed parameter range or only at a benchmark?
- Are important assumptions and uncertainties visible?
- Are there counterexamples, missing constraints, or untested regimes?
- Does the result change the qualitative conclusion, a quantitative boundary, or neither?
- Is the strongest defensible statement narrower than the original claim?

Track the answer in the claim–evidence matrix. A numerical difference alone does not establish phenomenological significance.

### Stage 8 — Synchronize the manuscript

Only after the scientific status is clear should manuscript wording be updated. Link each changed equation, plot, caption, or paragraph to the relevant research-change and claim identifiers.

The manuscript must not state that a calculation, validation, exclusion, or independent cross-check has been completed before the evidence exists. Unresolved work belongs in the internal research record; the formal paper and referee response must describe the actual state of the analysis accurately.

### Stage 9 — Close or carry forward

A record can be closed when its stated scope has been addressed and its outputs, evidence, decision, and downstream impact are documented. It need not have produced a positive result. A well-supported null result, a failed hypothesis, or a documented blocker can be a valid outcome.

If unresolved work remains, keep the record open and list the next concrete action. Do not silently promote an unresolved claim to confirmed.

## 6. Keep three status systems separate

### Work status

| Status | Meaning |
|---|---|
| Planned | Question and intended scope recorded |
| Derivation complete | Analytical work for the stated scope recorded; not necessarily independently checked |
| Calculation complete | A result was produced with identifiable inputs |
| Verification in progress | One or more required checks remain |
| Independently checked | The specified independent checks passed and their evidence is recorded |
| Claim assessed | The evidence has been evaluated against the exact claim |
| Manuscript synchronized | The relevant manuscript and response text match the assessed claim |
| Blocked | Progress depends on a missing input, decision, tool, or external result |
| Superseded | A later record replaces this record for a clearly stated reason |

### Claim status

| Status | Meaning |
|---|---|
| Proposed | A statement to investigate |
| Supported | Evidence supports the statement within its recorded scope |
| Conditionally supported | Evidence supports it only under explicit assumptions or in a restricted domain |
| Unresolved | Evidence is insufficient, conflicting, or incomplete |
| Contradicted | Available evidence conflicts with the statement |
| Superseded | A later result replaces the statement |

### Evidence status

Use “verified,” “partially verified,” “not verified,” “blocked,” or “contradicted” for individual checks. State the method and evidence; the label alone is insufficient.

These systems must not be collapsed into one status. For example, a calculation can be complete while its physical claim remains unresolved.

## 7. Example: finite vector effects in an axial-vector analysis

This is an illustration of the workflow, not a conclusion about any particular model or existing result.

**Question:** Can a finite vector interaction change a bound obtained in a pure axial limit?

1. Freeze the original model definitions, assumptions, exclusion procedure, parameter ranges, and baseline plot.
2. Record exactly which vector coupling or mixing effect is introduced and which quantities remain fixed.
3. Derive the relevant observables using the same conventions as the baseline; document any changed assumptions.
4. Recompute only the affected constraints and parameter regions, with inputs and software settings recorded.
5. Check the pure axial limit, relevant coupling limits, numerical stability, and applicability of each experiment.
6. Compare the resulting regions and assess whether the difference is significant for the stated claim.
7. Retain the original result if the evidence supports it within a clearly defined regime; otherwise qualify or revise it. Do not decide in advance which outcome is correct.
8. Update figures, captions, manuscript statements, and reviewer replies only to the extent justified by the verified result.

This pattern also applies to UV–EFT matching, finite loop terms, neutrino mass construction, perturbativity bounds, and other high-energy theory tasks.

## 8. Git, artifacts, and reproducibility

- Use branches and reviewable commits for proposed changes; preserve a stable baseline.
- Keep research-change IDs in commit or pull-request descriptions where useful.
- Use text diffs for LaTeX, Markdown, source code, configuration files, and symbolic expressions stored as text.
- For notebooks, PDFs, generated plots, large data, and binary files, record relevant metadata, content hashes, input provenance, and a human-readable summary of the scientific difference. For reproducible visual derivatives, follow the [Generated Figure and Report Artifact Policy](GENERATED_FIGURE_AND_REPORT_POLICY.md): archive source data, plotting/assembly code, configuration, and provenance; regenerate routine PDFs/PNGs/SVGs on demand; retain exact rendered files only as frozen deliverables or when they cannot be faithfully regenerated. For other essential native/uncompressed outputs, commit directly when practical; for files too large for ordinary Git, use Git LFS or durable versioned storage with an immutable manifest rather than an expiring CI artifact.
- Avoid committing credentials, private tokens, or data that the project is not permitted to redistribute.
- Separate “the source changed” from “the result was regenerated” and “the result was verified.”

A pull request can organize review, but code review and CI are only part of scientific validation. A green CI status must never automatically mark a physical claim as confirmed.

### Pull-request merge strategy

For substantive research and repository changes, use GitHub **Create a merge commit** by default. Preserve meaningful topic-branch commits and the explicit PR integration boundary so that changes to assumptions, derivations, implementations, numerical corrections, tests, and evidence can be traced independently. Use Squash and merge only for trivial, indivisible maintenance/documentation changes whose intermediate commits carry no useful research provenance. Use Rebase and merge only when a linear history is explicitly required and the commits are already meaningful and reviewable; note that rebase rewrites commit identities. Inspect the full commit list and actual diff before choosing. Do not rewrite reviewed/shared history for cosmetic reasons. After merge, verify the integrated main revision and update the research record. See the normative [Git merge policy](governance/GIT_MERGE_POLICY.md).

## 9. Completion criteria

Before declaring a research change complete, confirm that:

- [ ] the baseline and scope are identifiable;
- [ ] the scientific question and delta are explicit;
- [ ] assumptions, conventions, and approximations are recorded;
- [ ] inputs and outputs can be traced to a source revision;
- [ ] relevant checks have results and evidence, including justified N/A items;
- [ ] the claim status reflects the actual evidence;
- [ ] downstream calculations, figures, and claims have been reviewed;
- [ ] manuscript and reviewer-response wording matches the assessed result;
- [ ] unresolved issues and limitations are recorded.

Use **docs/review-checklist.md** for the operational review.

## 10. Method boundary

Scientific Diff is a research-process discipline, not an automated proof system. It improves traceability, reproducibility, and change impact analysis. Scientific correctness still depends on sound theory, appropriate calculations, valid data and constraints, independent scrutiny, and expert judgment.


## 11. Research reporting and communication standard

Use direct, evidence-led reporting. A research update records what has been established, the evidence supporting it, and the next consequential work; it is not a general disclaimer.

Use the following structure for progress reports, research-change summaries, reviews, and handoffs:

1. **Conclusion:** answer the research question and state the current decision.
2. **Evidence:** provide the governing equations, derivation, implementation path, source data, or validation.
3. **Results:** report numerical values with units and precision, benchmark parameters, comparisons, and physical interpretation.
4. **Remaining work:** list only pending tasks that affect the next stage.

Report completed calculations with actual values and checks performed. Present established derivations directly. State each approximation and its validity domain once. Mark unfinished work as pending, in progress, or blocked, with the specific missing step; do not let it obscure independent completed results. When an error is found, state the incorrect equation or implementation, give the correction, and identify affected outputs. Compare alternatives quantitatively under matched assumptions and record the recommended scheme.

This standard supplements the Scientific Diff evidence hierarchy and the project/workstream/RC/run/claim records. Preserve claim statuses and evidence links exactly: communication style must never promote a claim beyond its assessed evidence. Avoid repetitive defensive wording, generic warnings, and re-litigation of settled decisions. Do not omit genuine assumptions, physical applicability conditions, or unresolved evidence that changes the meaning of a claim.
