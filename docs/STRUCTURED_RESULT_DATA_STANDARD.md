# Structured Research Result Data Standard v1.0.1

**Status:** Proposed for adoption; applies to new substantial numerical, simulation, scan, and computational-validation runs after merge.  
**Schema:** JSON Schema Draft 2020-12 (`research-result-record-v1.0.1.schema.json`). Backward-compatible validation of v1.0.0 records is retained.  
**Purpose:** Standardize data structure, run provenance, and archival. This standard does not certify scientific correctness.

## 1. Standard result bundle

For a substantial run, use the following roles where applicable:

- `run_manifest.json`: exact source revision, inputs, configuration, environment, command, outputs, checksums, and archive status.
- `result_summary.json`: benchmark, physical scope, observables with units, interpretation, and references to pointwise data.
- `validation_report.json`: actual analytic, numerical, convergence, independent, and integrity checks.
- Native `*.csv`, ROOT, HDF5, or Parquet files: pointwise arrays, spectra, scans, response grids, event/cutflow tables.
- `SHA256SUMS.txt`: hashes for archived data.
- `README.md`: human-readable conclusions and reproduction instructions.

Do not force every task to create every file. A substantial execution needs a machine-readable run manifest; a completed numerical result needs a result summary. Keep large arrays in native tabular/binary files rather than embedding them in JSON.

## 2. JSON record roles

The local `research-result-record-v1.0.1.schema.json` validates three record types and remains backward-compatible with v1.0.0 records:

- **run_manifest:** records what actually ran, including the commit SHA used at execution time, script path/fingerprint, input provenance (for repository-local inputs, both a repository-relative path and SHA-256; when input bytes are unavailable, an immutable URI plus version), physical/numerical configuration, software/hardware environment, exact command, output inventory, validation status, and archival status. The schema requires the entry-script SHA-256 and explicit runtime, dependency, and hardware records.
- **result_summary:** records what was calculated, the benchmark, scope, observables as numeric values plus separate unit fields, scientific status, interpretation, and data-file references.
- **validation_report:** records each check by ID, category, status, method, observed value, threshold, unit, and evidence path.

Use numeric JSON values rather than unit-bearing strings. Use `null` plus an explicit `not_computed` status for quantities not evaluated; never substitute zero. Do not encode NaN or Infinity.

### Source revision semantics (v1.0.1)

For a new v1.0.1 `run_manifest`, `source.revision_context` is required. It separates the PR source revision from the commit that the runner actually checked out:

- `source.commit_sha` remains the compatibility field for the exact checked-out Git commit and must equal `source.revision_context.checked_out_sha`.
- `pr_head_sha` identifies the commit at the tip of the pull-request source branch.
- `base_sha` identifies the target branch commit used for the pull request.
- `tested_merge_sha` identifies GitHub's synthetic pull-request merge commit only when that merge commit was actually checked out and tested. It is `null` when the workflow tested the PR head directly or no synthetic merge ref was used.
- `head_ref` and `base_ref` identify the actual source and target branch names. For a `pull_request` event, `source.branch` must be `head_ref`; do not use `GITHUB_REF_NAME` as the source branch because GitHub exposes a synthetic `<number>/merge` ref for merge-based pull-request runs.
- `checkout_mode` records whether the runner tested `pull_request_merge`, `pull_request_head`, a normal branch commit, a detached commit, or an unknown checkout mode.

For non-PR runs, the PR-specific fields (`pr_number`, `pr_head_sha`, `base_sha`, and `tested_merge_sha`) are explicitly `null`. This prevents a synthetic merge SHA from being mistaken for the contributor's source commit. The v1.0.1 schema continues to accept existing v1.0.0 records unchanged; only new v1.0.1 run manifests require this revision context.

## 3. CSV and numeric arrays

Use a header row with stable column names and explicit units (for example `r_km`, `omega_MeV`, `ER_keV`). Use long/tidy format: one row per grid point or sample, with polarization, isotope, channel, coupling, or process as separate dimensions. Keep numeric columns numeric; preserve useful precision; distinguish missing data from physical zero; record row count, columns, units, byte size, and SHA-256 in the manifest. Do not silently resample, reorder, round, or change units.

## 4. Separate statuses

Keep execution, validation, scientific maturity, and archival status separate:

- execution: `not_started`, `running`, `succeeded`, `partial`, `failed`, `cancelled`, `blocked`;
- validation: `not_run`, `partial`, `passed`, `failed`, `blocked`, `inconclusive`;
- scientific status: `diagnostic`, `provisional`, `reproducible`, `validated`, `historical`, `superseded`;
- archive: `local_only`, `committed_to_pr_branch`, `merged_and_verified_on_main`.

A successful process exit is not numerical convergence; passing tests are not physical validation; an upload is not a verified main-branch archive.

## 5. Domain extensions

Keep shared fields at the top level. Put domain-specific physics fields under a namespaced `extensions` object. Preserve the exact conventions and dimensions required by each research area; do not flatten physically distinct quantities into one field.

For UV–EFT and loop calculations, record the model/Lagrangian version, field content, mass basis, coupling normalization, loop order, topology/subgraph, momentum conventions, gauge and gamma5 prescriptions, renormalization scheme/scale, IR regulator/subtraction, operator basis, matching scale, and counterterm coverage. Wilson coefficients must include basis order, dimensions, and units; per-diagram contributions should be tabulated separately.

For purely analytic derivations with no numerical arrays, do not create empty CSV files. Archive editable derivation sources and the run record for any symbolic execution.

## 6. Schema and archive validation

Validate JSON records with the local Draft 2020-12 validator:

```bash
python -m pip install -r docs/schemas/requirements-result-validation.txt
python docs/schemas/validate_result_records.py --repo-root . results/<run_label>/run_manifest.json results/<run_label>/result_summary.json results/<run_label>/validation_report.json
```

The script checks schema validity, strict JSON numbers, referenced file paths/byte counts/SHA-256, and CSV row counts, headers, per-column units, and non-finite values. Pass only record files that exist for the run.

Run the validator's regression suite with `python -m unittest discover -s docs/schemas/tests -v`. It covers non-standard JSON constants, float overflow/underflow, and input provenance locator requirements. A validation status of `passed` requires at least one check and every check to be `passed`; otherwise use `partial`, `failed`, or `inconclusive`. Check CSV headers, units, row counts, finite numeric values, and grid coverage. Verify every referenced output's path, byte size, and SHA-256. After pushing, retrieve the remote files and compare paths, sizes, counts, and hashes. Report archive status separately from scientific validation.

## 7. Historical records

Apply this standard to new runs from adoption onward. Preserve existing JSON, CSV, logs, plots, and historical manifests byte-for-byte. Do not fabricate missing metadata or rewrite raw values to satisfy the new profile. A new index or manifest may reference a legacy file, clearly labelling it as legacy and only adding fields supported by source evidence.
