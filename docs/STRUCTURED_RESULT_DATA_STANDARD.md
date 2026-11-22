# Structured Research Result Data Standard v1.0.0

**Status:** Proposed for adoption; applies to new substantial numerical, simulation, scan, and computational-validation runs after merge.  
**Schema:** JSON Schema Draft 2020-12.  
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

The local `research-result-record-v1.0.0.schema.json` validates three record types:

- **run_manifest:** records what actually ran, including the commit SHA used at execution time, script path/fingerprint, input provenance (for repository-local inputs, both a repository-relative path and SHA-256; when input bytes are unavailable, an immutable URI plus version), physical/numerical configuration, software/hardware environment, exact command, output inventory, validation status, and archival status. The schema requires the entry-script SHA-256 and explicit runtime, dependency, and hardware records.
- **result_summary:** records what was calculated, the benchmark, scope, observables as numeric values plus separate unit fields, scientific status, interpretation, and data-file references.
- **validation_report:** records each check by ID, category, status, method, observed value, threshold, unit, and evidence path.

Use numeric JSON values rather than unit-bearing strings. Use `null` plus an explicit `not_computed` status for quantities not evaluated; never substitute zero. Do not encode NaN or Infinity.

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

## 7. Pull-request execution provenance (Schema v1.0.1)

Schema v1.0.1 is a backward-compatible record-profile update. It preserves the v1.0.0 record roles and adds the optional `execution.source_control` object. For a GitHub `pull_request` execution, the object requires three distinct 40-character commit identifiers:

- `pr_head_sha`: the exact source-branch commit under review;
- `base_sha`: the exact target-branch commit used for the test merge;
- `tested_merge_sha`: the synthetic merge commit checked out and actually executed by the workflow.

These values are not interchangeable. In particular, GitHub's `GITHUB_SHA` for a `pull_request` event normally identifies the tested merge commit, not the PR head. Keep `source.commit_sha` as the actual checkout/source tree commit; use `execution.source_control` to make the PR relationship explicit. The optional object may also record `pr_number`, `pr_url`, `workflow_run_id`, and `workflow_run_attempt`.

For local, push, and manually dispatched runs, set `event` accordingly; the PR-specific SHA triplet is required only when `event="pull_request"`. Do not fabricate PR fields for a non-PR run. Existing v1.0.0 records remain valid under the v1.0.0 schema and are not rewritten. To validate a v1.0.1 record, select its versioned schema explicitly:

```bash
python docs/schemas/validate_result_records.py --schema docs/schemas/research-result-record-v1.0.1.schema.json --repo-root . results/<run_label>/run_manifest.json
python -m unittest discover -s docs/schemas/tests -v
```

## 8. Historical records

Apply this standard to new runs from adoption onward. Preserve existing JSON, CSV, logs, plots, and historical manifests byte-for-byte. Do not fabricate missing metadata or rewrite raw values to satisfy the new profile. A new index or manifest may reference a legacy file, clearly labelling it as legacy and only adding fields supported by source evidence.
