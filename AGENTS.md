# Repository instructions — High-Energy Theory Research

These instructions are mandatory for all agents and contributors. They complement the User Guide, Scientific Diff workflow, project-specific records, and calculation-result archival policy.

## 1. Minimal preflight

Before substantive work:

1. Read this file and the root [README](README.md) or [Chinese README](README.zh-CN.md).
2. Read [docs/USER_GUIDE.md](docs/USER_GUIDE.md) and [docs/scientific-diff-workflow.md](docs/scientific-diff-workflow.md).
3. Inspect [projects/registry.yaml](projects/registry.yaml) and [research/README.md](research/README.md) to identify the canonical project, workstream, active research-change record, and claim–evidence matrix.
4. Read only the source files, calculations, and validation records relevant to the task. Do not load or rewrite the entire repository by default.
5. Before changing candidate schemas, migrations, or governance behavior, read [docs/REPOSITORY_STATUS.md](docs/REPOSITORY_STATUS.md), [docs/OPEN_ISSUES.md](docs/OPEN_ISSUES.md), and [docs/governance/DECISION_REGISTER.md](docs/governance/DECISION_REGISTER.md).

Never invent a completed calculation, run record, validation result, source revision, or scientific decision.

## 2. Research hierarchy and record discipline

Use the repository's distinct levels consistently:

- **Project:** a sustained research programme registered in `projects/registry.yaml`.
- **Workstream:** a coherent part of a parent project; it is not automatically a separate top-level project.
- **Research change (RC):** a bounded scientific change with a frozen baseline, question, rationale, evidence, and impact review.
- **Run:** one execution that actually occurred, with exact code, inputs, environment, command, settings, and outputs.
- **Claim (CL):** one physical statement with an explicit validity domain and supporting evidence.

Do not reuse identifiers across these levels. Do not create a project or move existing files merely because a topic appears in a paper or discussion. Preserve canonical paths unless a reviewed migration covers links, scripts, tests, schemas, and downstream references.

For each substantive change, freeze the baseline SHA/source version, state one falsifiable question, identify what changes and what stays fixed, map dependencies, and update the relevant research-change record and claim–evidence matrix. Separate established, conditional, diagnostic, and unresolved conclusions.

## 3. Task-based reading routes

- **UV–EFT matching / loop calculations:** read the active RC record, its claim–evidence matrix, the exact master derivation/source revision, relevant calculation scripts, and prior audits. Identify the complete UV and EFT field content and the exact topology/subsector being evaluated.
- **Gauge invariance / Ward identities:** read the relevant gauge-subgraph record and full field/interactions definitions. A longitudinal Ward contraction or telescoping cancellation is a necessary diagnostic for the tested amplitude, not proof that hard matching is complete.
- **Higgs–singlet mixing:** inspect the full scalar potential, tadpole and VEV conventions, portal renormalization, wavefunction renormalization, relevant self-energy sectors, and the full mixed propagator. Do not use a small-mixing or isolated-pole approximation near degeneracy without demonstrating its validity.
- **Operator-basis reduction:** read the declared basis and conventions. Keep amplitude structures, operator representatives, and independent Wilson coefficients distinct. Apply IBP, equations of motion, field redefinitions, and gauge-field equations consistently before claiming basis completeness.
- **Schema / research-Skill development:** follow the governance decision register. Candidate schemas and prototypes remain candidates until decisions and release gates are explicitly approved.

## 4. Mandatory standards for analytical calculations

Before deriving or coding, state conventions that affect the answer: metric, gamma-matrix and gamma5 prescription, chiral projectors, momentum routing, Fourier/sign conventions, field and coupling normalization, mass definitions, gauge fixing, renormalization scheme and scale, and regulator.

For loop and matching calculations:

1. Enumerate the required UV diagrams, counterterm insertions, contact terms, scalar/current-source terms, and relevant gauge/Goldstone/ghost contributions before claiming completeness.
2. Separate UV and IR singularities. Do not set a scaleless integral to zero before establishing whether its UV and IR poles cancel. Use a consistent nonzero external momentum or auxiliary-mass/IR-rearrangement prescription; use an R*-type subtraction where required.
3. Apply the same IR prescription to UV theory and EFT contributions. Subtract the soft EFT contribution exactly once; do not double count light-field loops or mix different infrared regulators.
4. Keep hard matching, soft EFT matrix elements, counterterms, and operator-basis reduction as distinct auditable steps.
5. Check dimensions, symmetry factors, signs, tensor structures, limiting cases, and independent analytic/numerical representations.
6. A result for one diagram family, coupling sector, polarization, or projected amplitude is a sub-block. Do not promote it to a complete Wilson-coefficient vector or full-model result without the missing sectors and projections.

For Ward identities, include all terms required by the identity in the chosen theory: ordinary fermion-line diagrams, contact/seagull terms, scalar-current terms, Goldstone and gauge-sector terms, and counterterms as applicable. State exactly which subset was contracted and what cancellation was demonstrated. Do not infer that the residual local term already contains external-leg, Goldstone, gauge, and counterterm matching contributions unless each has been included and checked.

For numerical integrals, report grid/quadrature order, precision, tolerances, convergence, error estimates, and an independent check. Agreement between two routines sharing the same algebraic kernel is not fully independent validation.

## 5. Evidence and claim standards

Use primary sources for physical inputs and record the exact equation/table/figure, version, units, and conventions. Do not silently digitize, rescale, interpolate, or reinterpret a published curve. Record digitization and transformations as reproducible steps.

Keep these evidence levels distinct: symbolic/algebraic identity; diagram-level calculation; numerical implementation and convergence; independent implementation or literature reproduction; observable/phenomenology validation; and manuscript claim supported within a stated domain.

A unit test, exact-rational check, CI pass, successful compilation, or matching checksum validates only the property it actually tests. It does not certify gauge completeness, UV finiteness, a Wilson coefficient, or a physical exclusion.

Do not call a calculation independent if it reuses the same trace, integral reduction, interpolation, or input data without an independently derived check. Report failed, partial, blocked, and unrun checks explicitly.

## 6. Repository and manuscript boundaries

- Preserve historical source records and immutable artifacts. Do not overwrite a known baseline or silently replace an authoritative file.
- Keep reusable methods/tools in shared locations and project-specific calculations in canonical project/workstream paths.
- Treat candidate schema and Skill infrastructure as development-stage unless governance records explicitly declare otherwise. Do not bypass validation or edit candidate fixtures merely to make CI green.
- Do not edit manuscript source as a side effect of a calculation task. Manuscript synchronization must be explicit and tied to the selected source version and supporting evidence.
- Do not write internal progress notes, speculative claims, or unverified results as established scientific conclusions.

## 7. Numerical-result archival and Git workflow

Follow the mandatory [calculation-result archival policy](docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md):

- **Extract-before-upload is mandatory:** when results arrive as ZIP/TAR (including ChatGPT handoff bundles, local-runner packages, GitHub Actions artifacts, or collaborator deliveries), extract first and commit the required native files individually. A delivery archive is transport only, not a substitute for its extracted contents. Follow [§2 of the calculation-result archival policy](docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md).
- Record exact source commit, input provenance and hashes, commands, software versions, physical/numerical settings, outputs, and SHA-256 checksums.
- Use Git LFS or durable versioned storage with a committed manifest for files too large for ordinary Git.
- Retrieve committed files from GitHub after pushing and verify paths, sizes, counts, and hashes before claiming archival completion.
- Keep archival status separate from scientific validation status.

Use a focused branch and PR for a coherent change. Inspect the actual diff and relevant existing PRs touching the same files. Do not rewrite shared history or force-push over another contributor's work. A PR description must state the exact checks run against its HEAD SHA, skipped/blocked checks, scientific scope, and unresolved items.

## 8. Completion report

At the end of a task, report the research question and exact scope; baseline and resulting commit/PR; files and outputs created/changed; derivations and numerical checks actually performed; independent validation and convergence evidence; incomplete or conditional items; and exact archive status (local only, committed to PR branch, or merged and verified on main).

Never describe a task as scientifically complete solely because its code, documentation, CI, or archival step is complete.
