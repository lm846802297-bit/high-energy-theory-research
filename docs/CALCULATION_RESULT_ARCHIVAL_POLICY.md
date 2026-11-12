# Calculation-result archival policy

**Status:** Mandatory repository-wide policy for numerical and computational research.

This policy applies to calculations, simulations, parameter scans, data processing, phenomenology, and computational validation. It supplements the [User Guide](USER_GUIDE.md), the [Scientific Diff workflow](scientific-diff-workflow.md), and the immutable-bundle rules in [artifacts/README.md](../artifacts/README.md). It governs how results are retained; it does not certify their scientific correctness.

## 1. Use the canonical research locations

- `research/` holds project/workstream research records, study-specific code, inputs, results, figures, and audit records. Keep each result beside its canonical research-change record.
- `calculations/` holds reusable or reproducible symbolic/algebraic calculation sources.
- `validation/` holds captured run outputs, numerical checks, and validation logs. Keep completed checks distinct from planned or unexecuted checks.
- `artifacts/<bundle-id>/` holds immutable, hashed snapshots of large or binary sources and computational artifacts. Follow [artifacts/README.md](../artifacts/README.md); add a new bundle for a new snapshot rather than overwriting an existing one.

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

## 3. Large or restricted files

- Commit directly to Git when file size, licensing, and repository policy permit.
- For files too large for ordinary GitHub Git storage, use Git LFS or another repository-approved, durable, versioned storage location. Do not silently omit the file or replace it with an untraceable archive.
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

## 5. Validate and verify the remote submission

1. Before submission, check completeness, expected file/row counts, units, numerical finiteness, and the calculation-specific acceptance criteria. Record failed, partial, or unrun checks explicitly.
2. Submit the results, source or exact source revision, provenance, and manifest in a focused branch and pull request.
3. After pushing, inspect the actual pull-request diff and retrieve the committed files from GitHub. Verify paths, file count, sizes, and SHA-256 hashes against the local submission.
4. Report repository archival separately from scientific validation. A successful commit, matching checksum, green CI, or completed run does not by itself establish a correct physical result or a confirmed claim.

These requirements apply to future projects and workstreams throughout this repository.
