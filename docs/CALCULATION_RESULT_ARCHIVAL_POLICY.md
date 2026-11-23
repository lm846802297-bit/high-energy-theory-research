# Calculation-result archival policy

**Status:** Adopted shared policy for repositories that explicitly adopt the central standards framework.

This policy applies to calculations, simulations, parameter scans, data processing, phenomenology, and computational validation in adopting project repositories. It supplements the [User Guide](USER_GUIDE.md) and the [Scientific Diff workflow](scientific-diff-workflow.md). Each project repository defines its own artifact index or `artifacts/README.md` for immutable-bundle navigation. This policy governs how results are retained; it does not certify their scientific correctness.

## 1. Use project-local canonical research locations

- Project-specific research repositories hold the canonical project/workstream records, study-specific code, inputs, results, figures, and audit records. Keep each result beside its canonical research-change record; the shared infrastructure repository retains navigation metadata only.
- Within each project repository, `calculations/` holds reusable or reproducible symbolic/algebraic calculation sources.
- Within each project repository, `validation/` holds captured run outputs, numerical checks, and validation logs. Keep completed checks distinct from planned or unexecuted checks.
- Within each project repository, `artifacts/<bundle-id>/` holds immutable, hashed snapshots of large or binary sources and computational artifacts. Follow that repository's artifact index or `artifacts/README.md`; add a new bundle for a new snapshot rather than overwriting an existing one.

Follow the existing project/workstream layout and record conventions. Do not create duplicate competing authoritative copies or move historical records merely to satisfy this policy.

## 2. Commit usable native result files, not a newly packed archive

- Commit the essential result files directly in their native, machine-readable formats where practical: CSV, JSON/JSONL, TXT, ROOT, HDF5, Parquet, notebooks, source code, plots, and other formats actually produced or consumed by the calculation.
- **Extract-before-upload is mandatory.** If a calculation or result delivery arrives as ZIP/TAR—including a ChatGPT handoff bundle, local-runner output package, GitHub Actions artifact, or collaborator delivery—extract it before committing/publishing and commit the required extracted native files individually, preserving their useful filenames and directory structure.
- A newly generated delivery ZIP/TAR is a transfer container only. **Do not commit it as the sole or substitute archive of the extracted outputs.** Reviewers must be able to inspect and use the actual source, inputs, CSV/JSON/ROOT/HDF5/Parquet/TXT outputs, reports, metadata, and manifests directly from the repository.
- An original upstream archive may be retained when the exact container is necessary for provenance/reproducibility or when extracted source files cannot legally be redistributed. Record its source/version, byte size, SHA-256, extraction command, and checksums of extracted files; still commit all extracted files that may be redistributed.
- Tool-native compressed formats that are themselves the original data product may be retained when necessary and documented; this exception does not permit wrapping ordinary outputs in a newly generated ZIP/TAR.
- If an upstream source is supplied as an archive, extract the files required for the calculation and commit those extracted files when redistribution is permitted. Record the original archive filename, source/version, byte size, SHA-256, extraction command, and checksums of the extracted files in the provenance record. Do not silently alter precision, units, columns, line endings, or raw data.
- Keep raw inputs, transformed inputs, and derived outputs distinguishable. If a conversion or post-processing step changes the data, preserve the raw source where permitted and record the transformation and the output checksum.
- Tool-native compressed formats that are themselves the original data product may be retained when necessary; document the format and command. This exception does not justify wrapping ordinary outputs in a newly created ZIP/TAR.


## 2A. Generated figures and report PDFs

Apply the separate [Generated Figure and Report Artifact Policy](GENERATED_FIGURE_AND_REPORT_POLICY.md) to rendered plots, multi-panel figures, annotated PDFs, and combined figure reports. The default is to archive the scientific data, reference curves, plotting/assembly source, configuration, dependencies, provenance, and hashes, then regenerate routine PDF/PNG/SVG outputs when needed. Do not commit every preview or intermediate rendering. Archive an exact rendered snapshot only when it is a frozen manuscript/report deliverable, a formally approved milestone, required by an external process, or cannot be faithfully regenerated. Preserve its source data and generation provenance alongside it. This rule clarifies the treatment of reproducible presentation derivatives; it does not relax the native-data and run-provenance requirements above.

## 3. Large or restricted files

- Commit directly to Git when file size, licensing, and repository policy permit.
- For files too large for ordinary GitHub Git storage, use Git LFS or another repository-approved, durable, versioned storage location. Do not silently omit the file or replace it with an untraceable archive.


### 3.1 Select the storage tier by data role

Use the following storage tiers; choose the least complex tier that preserves practical inspection, reproducibility, and durable retrieval:

- **Ordinary Git:** source code, scripts, configuration, schemas, manifests, provenance, validation reports, indexes, and small/medium native datasets that remain practical to diff, clone, and review. Git is the canonical version history for these files.
- **Git LFS:** large binary or native data files that must be versioned alongside a repository revision and are still practical to retrieve as part of that project's working set. Commit the LFS pointer and keep a dataset manifest containing the logical filename, LFS object SHA-256/OID, byte size, format, source/version, and the repository commit that references it. Verify the retrieved object bytes against the recorded SHA-256; a pointer alone is not proof that the object remains retrievable.
- **External object storage:** large raw outputs, bulk parameter scans, extensive grids, long-term datasets, or files whose volume/download pattern makes Git/LFS unsuitable. Use a durable, versioned location with immutable object/version identifiers (and retention or object-lock protection where available). Keep a repository-side manifest with the exact object URI/version, filename, byte size, format, source, SHA-256, access/retrieval instructions, and retention owner/policy. A mutable “latest” URL is not an immutable identity.

A file approaching GitHub's ordinary-Git per-file limit must be evaluated for LFS or external storage before it is committed; do not split or recompress data merely to bypass the limit unless the transformation is part of the documented native data format. Storage-tier choice is based on data role, size, access pattern, durability, licensing, and project budget—not on whether the repository is public or private.

### 3.2 Integrity and availability

- Calculate SHA-256 from the exact bytes of each archived native file. For transformed data, retain the raw-source identity where permitted and record the transformation, tool/version, and output SHA-256.
- For Git LFS and external storage, verify retrieval from the remote location after upload and compare the downloaded bytes with the manifest. Record the verification date and result in the archival/provenance record.
- Keep the manifest, retrieval instructions, and hashes in the project Git repository even when the data itself is external. Never make an expiring CI artifact, temporary workspace, or unversioned cloud object the only copy.
- Do not duplicate large data across multiple storage systems without a stated recovery or access reason. If replicas are maintained, record their identities and verify them against the same content hash.
- For externally stored files, commit a manifest with the exact filename, immutable retrieval URI or release identifier, version, byte size, format, source, and SHA-256. Prefer individual native files over newly generated archive bundles.
- An expiring GitHub Actions artifact, temporary workspace, chat attachment, or local-only file must never be the sole permanent copy of a result used in a research claim.
- Do not commit credentials, tokens, private keys, personal data, or inputs that the project is not permitted to redistribute. Record retrieval instructions and checksums for restricted inputs instead.

## 4. Required run provenance

For every substantial run, include a `run_manifest.json`/YAML or an equivalent complete record. It must identify, as applicable:

- the exact source commit and calculation script/notebook paths;
- input filenames, source/version, parameter/configuration files, and SHA-256 checksums;
- runtime, operating system, compiler, and relevant package versions;
- the exact command or execution procedure;
- physical conventions and numerical settings that affect interpretation: units, parameters, approximations, grids, quadrature, precision, tolerances, boundary conditions, and random seeds;
- output paths, formats, byte sizes, record/row counts where relevant, and SHA-256 checksums;
- warnings, failed or discarded runs, post-processing, convergence checks, and unresolved limitations.

Retain the logs and checkpoints needed to audit or resume a long calculation. Omit disposable caches, temporary build products, virtual environments, and unrelated scratch files.

## 4A. Reuse accepted calculation results; do not recompute without cause

**A result that has passed predeclared numerical and scientific acceptance criteria and has complete source/input provenance is reusable scientific evidence. A new PR, CI restart, documentation edit, archival-path change, or workflow adjustment alone is not a reason to recompute it.**

### 4A.1 Identify a reusable result

A reusable accepted result must be bound, as applicable, to:

- repository and full source commit SHA, plus hashes of the calculation scripts/notebooks actually used;
- paths, versions, and SHA-256 checksums of all input data, reference data, parameter files, and configurations;
- physical definitions and conventions: units, normalization, model assumptions, approximations, boundary conditions, and other result-affecting choices;
- numerical methods and settings: grids, integration/quadrature order, precision, tolerances, random seeds, and parallel settings;
- execution environment: operating system, runtime, compiler, and relevant dependency versions;
- native output files and their SHA-256 checksums;
- predeclared acceptance criteria, actual validation methods/results, and locatable logs/reports.

Together these fields form the result's *calculation fingerprint*. A filename, PR number, green CI status, or verbal statement alone does not establish equivalence between calculation versions.

### 4A.2 When to reuse directly

When the calculation fingerprint relevant to the current task matches the accepted record, and the supported scientific claim and scope are unchanged:

1. cite the native result and its exact version;
2. cite the existing convergence, error-analysis, and independent-validation evidence;
3. perform necessary integrity/hash checks on the existing files and verify their archival location;
4. record this task as “reuse of an accepted result,” identifying the reused run ID, commit, input/output hashes, and validation record;
5. do not rerun expensive physics calculations or duplicate a calculation merely to obtain a new CI record.

Hash verification, metadata checks, result-table comparisons, and archival checks are lightweight verification; they are not reruns of the original calculation. If the result files, source, and inputs are unchanged, the existing independent validation remains valid; do not repeat it merely to “prove it again.”

### 4A.3 When recalculation or targeted revalidation is justified

Recompute only the affected part when there is a concrete, relevant change or new evidence, for example:

- a source-code or algorithm change that may alter numerical results;
- a change in the content/version of input data, parameters, configuration, data transformation, or reference data;
- a change in physical definitions, sign conventions, normalization, approximations, model assumptions, or the target scientific claim;
- a change in numerical method, precision, grid, quadrature, tolerance, random seed, or execution environment that may affect the result;
- discovery of an actual error, numerical instability, failed convergence, checksum mismatch, or new independent evidence contradicting the old result;
- evidence that the previous validation scope is insufficient for a stronger claim now being made.

Scope revalidation along the dependency graph: check the downstream components affected by the changed input, code module, result, or claim. Do not treat unrelated documentation edits, plot-style changes, file moves, README additions, PR reopenings, or CI configuration changes as automatic reasons to recompute all physics results. If a change affects only presentation, regenerate the figure without recomputing its upstream numerical data.

### 4A.4 Keep calculation, validation, and archival status distinct

Record these separately:

- **Calculation status:** result produced, or not yet executed;
- **Scientific-validation status:** which predeclared checks passed, were not run, or are not applicable;
- **Archival status:** whether native results, source, inputs, and provenance are durably stored and verified;
- **Reuse status:** whether this task reuses an accepted result or performs targeted recalculation because of a specified change.

A historical calculation passing does not automatically validate new modifications; equally, not rerunning a calculation in a new PR does not invalidate the existing result. Do not report “not recomputed this round” as “validation failed,” and do not report a matching checksum as a new independent physics validation.

### 4A.5 CI and automation requirements

- CI should select checks according to changed paths and dependency relationships. Documentation-only, presentation-only, or non-calculation workflow changes should not automatically trigger every expensive numerical calculation.
- When a task reuses an accepted result, CI may verify source/input/output hashes, manifest completeness, and consistency of result summaries with frozen references. A full physics rerun is not required unless one of the recalculation triggers above applies.
- Multiple workflows must not concurrently recompute the same result or overwrite each other merely because an automated archive commit changed a result directory. Archival should be idempotent and keyed to an explicit result identity, with deliberate commit-conflict handling.
- Independent replay is valuable, but should be performed for initial acceptance, a relevant dependency change, or a concrete discrepancy—not as a default full recomputation for every PR.

This section applies together with the [minimum-sufficient-acceptance and historical-validation-reuse principles in the Research Quality Gate](governance/RESEARCH_QUALITY_GATE.md). Preserve the stricter provenance requirements, but do not expand the recalculation scope without evidence.

## 5. Validate and verify the remote submission

1. Before submission, check completeness, expected file/row counts, units, numerical finiteness, and the calculation-specific acceptance criteria. Record failed, partial, or unrun checks explicitly.
2. Submit the results, source or exact source revision, provenance, and manifest in a focused branch and pull request.
3. After pushing, inspect the actual pull-request diff and retrieve the committed files from GitHub. Verify paths, file count, sizes, and SHA-256 hashes against the local submission.
4. Report repository archival separately from scientific validation. A successful commit, matching checksum, green CI, or completed run does not by itself establish a correct physical result or a confirmed claim.

These requirements apply to future projects and workstreams throughout this repository.

## 6. CI is optional and is not a research or merge gate

CI is optional supporting infrastructure, not a prerequisite for calculation, scientific validation, result submission, pull-request review, or merge.

- Calculations may be run directly on a local machine or an approved compute runner. Do not wait for a CI job before starting, continuing, or completing research.
- Numerical and scientific acceptance checks remain necessary where appropriate, but they may be run locally or on an approved runner. Record the exact commands, source revision, inputs, settings, outputs, and checks actually performed. CI is neither a substitute for scientific validation nor a mandatory way to perform it.
- GitHub Actions may still be used as an optional compute or artifact-handoff service. A workflow that performs the calculation is an execution run; record its provenance and outputs. Its existence does not make a separate PR CI check mandatory.
- A queued, unavailable, disabled, billing-blocked, cancelled, or infrastructure-failed CI job must not by itself block research progress, archival, PR creation, review, or merge. Record its status truthfully and distinguish infrastructure problems from scientific failures.
- If CI is run, report the exact commit SHA and the checks that actually ran. Never claim an unrun check passed. A green CI result validates only the properties tested by that workflow.
- Review and merge according to the actual diff, reproducibility, scientific evidence, scope, and relevant checks. Do not require CI status checks as branch-protection gates under this policy. Do not change repository protection settings without explicit authorization.
- CI is mandatory for a specific task only if the author explicitly requests it.

## 7. Structured JSON/CSV result records

New substantial numerical runs must follow the adopted [Structured Research Result Data Standard v1.0.1](STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.md) and validate records against `schemas/research-result-record-v1.0.1.schema.json`. The v1.0.0 standard and schema remain available for historical compatibility; do not rewrite legacy records. Keep execution provenance, scientific results, and validation evidence as distinct records; store pointwise arrays in native tables with explicit units. This archive-data profile is independent of the unreleased research-record Schema v1.4.3.7 candidate.
