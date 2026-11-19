# Structured Research Result Data Standard v1.0.0

**Status:** Adopted for new substantial numerical, simulation, scan, and computational-validation runs in this repository.  
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

- **run_manifest:** records what actually ran, including the commit SHA used at execution time, script path/fingerprint, input provenance, physical/numerical configuration, software/hardware environment, exact command, output inventory, validation status, and archival status.
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

Validate JSON records against the local Draft 2020-12 schema with format checking enabled. Check CSV headers, units, row counts, finite numeric values, and grid coverage. Verify every referenced output's path, byte size, and SHA-256. After pushing, retrieve the remote files and compare paths, sizes, counts, and hashes. Report archive status separately from scientific validation.

## 7. Historical records

Apply this standard to new runs from adoption onward. Preserve existing JSON, CSV, logs, plots, and historical manifests byte-for-byte. Do not fabricate missing metadata or rewrite raw values to satisfy the new profile. A new index or manifest may reference a legacy file, clearly labelling it as legacy and only adding fields supported by source evidence.
