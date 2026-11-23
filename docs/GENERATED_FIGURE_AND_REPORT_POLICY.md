# Generated Figure and Report Artifact Policy

**Status:** proposed shared policy; becomes normative for adopting repositories after central PR review and merge.  
**Scope:** generated scientific plots, figure panels, figure collections, annotated PDFs, and other reproducible visual/report derivatives in project repositories.

This policy supplements the [Calculation-result archival policy](CALCULATION_RESULT_ARCHIVAL_POLICY.md). It distinguishes canonical scientific inputs and results from files rendered only to display those results. It does not change project-specific physics conventions or scientific acceptance criteria.

## 1. Core rule

**Archive the data and the procedure that define a figure; generate routine rendered files when they are needed.**

A PDF, PNG, or SVG produced deterministically from already archived scientific data and a versioned plotting program is normally a derived presentation artifact, not a new scientific result. Repositories should not accumulate a new copy of every preview or every plotting iteration.

The canonical record is the smallest complete set that allows the figure to be regenerated and scientifically interpreted:

1. source data and derived numerical tables used by the plot;
2. plotting/assembly source code;
3. plotting configuration and figure-specific labels, captions, legend definitions, and panel layout;
4. a manifest binding the source revision, input paths and SHA-256 hashes, runtime/dependency versions, and output-generation command;
5. digitized external reference curves or other non-reconstructible reference data, together with their source, extraction method, and checksums.

## 2. Default retention rules

| Item | Default treatment | Reason |
|---|---|---|
| Raw and derived numerical data (CSV, HDF5, ROOT, Parquet, JSON, etc.) | Archive in native form | Canonical scientific content |
| External/digitized reference data used in comparisons | Archive with source and extraction provenance | Cannot be reconstructed from plotting code alone |
| Plotting and PDF-assembly source code | Archive and version-control | Defines how the figure is produced |
| Plot configuration, captions, legend text, style and panel definitions | Archive as source/configuration | Makes presentation reproducible and reviewable |
| Run/figure manifest and input/output hashes | Archive | Binds the rendered view to exact scientific inputs |
| Routine PDF/PNG/SVG previews and intermediate revisions | Generate on demand; do not commit by default | Reproducible derivatives; avoid repository clutter |
| Final frozen publication figure or formally approved report | Archive when it is an approved deliverable | Preserves the exact version actually submitted, reviewed, or cited |

The absence of a committed preview PDF does not mean that the figure was not produced or checked. Record the generation and visual-inspection status in the relevant research record or run manifest.

## 3. When a rendered PDF or image should be archived

Archive a rendered figure/report snapshot when at least one of the following applies:

- it is the exact figure included in a submitted or published manuscript, thesis, conference contribution, or formally approved report;
- it is a formally frozen milestone deliverable whose exact appearance must be preserved for review or citation;
- the rendering cannot be reliably regenerated from the archived data and source (for example, an essential manual annotation or a proprietary external rendering step cannot be represented in source form);
- an external process requires the exact rendered file as a deliverable.

When archiving such a snapshot:

- retain the native source data and plotting/assembly source as well;
- record the exact source commit, input hashes, plotting configuration, software/runtime and relevant font versions, generation command, output format, dimensions/page count, and output SHA-256;
- give the snapshot a stable versioned path or release identifier; do not silently overwrite an earlier frozen figure;
- label it as a frozen presentation snapshot, not as the canonical numerical result.

Do not archive every intermediate PDF/PNG/SVG merely because it was generated during exploration.

## 4. Regeneration requirements

A plotting workflow should be callable from a clean project checkout using documented commands and declared dependencies. It should:

- read the archived numerical data and reference data by explicit paths;
- use versioned configuration rather than hidden interactive state or undocumented manual edits;
- write outputs to a designated generated-output directory;
- preserve units, normalization, axis definitions, and the distinction between rates and event counts;
- include legends and captions that identify every curve, panel, and physical prescription;
- fail clearly when required inputs or expected columns are missing;
- avoid modifying the source data while plotting;
- record output hashes after generation.

For a combined PDF containing several figures, archive the assembly script and the text/configuration defining page order, captions, and legends. Generate the combined PDF on demand unless it meets a frozen-snapshot condition in §3.

## 5. CI and temporary previews

- CI may generate PDFs/PNGs/SVGs for visual review and upload them as temporary workflow artifacts.
- An expiring CI artifact is a preview/transfer mechanism, not the canonical archive of the scientific data or plotting source.
- Do not make a routine CI job commit every regenerated preview. Commit source, configuration, numerical data, manifests, and only those frozen rendered snapshots required by §3.
- CI success does not establish scientific correctness. Numerical validation and visual inspection must be recorded separately and only when actually performed.
- A changed input data hash or plotting-source commit invalidates the provenance of a previous rendering. Regenerate before using the figure in a manuscript or report.

## 6. Review checklist

Before accepting a figure-generation change, check:

- [ ] Every plotted curve is traceable to an archived data column or a clearly documented analytic expression.
- [ ] External/reference curves have source and digitization provenance.
- [ ] Plotting source, configuration, captions, legends, and dependencies are versioned.
- [ ] Units, exposure normalization, rate/count definitions, axes, and panel labels are explicit.
- [ ] The figure can be regenerated from a clean checkout.
- [ ] The output is visually inspected when the task requires visual acceptance; record who/when and the exact input/source hashes.
- [ ] Routine previews are not committed unnecessarily.
- [ ] A frozen deliverable, if required, is stored with its own provenance and checksum.
- [ ] The figure's scientific interpretation is not stronger than the underlying validated result.

## 7. Project-local authority and adoption

- Project repositories own their figure data, plotting programs, visual conventions, and frozen manuscript figures.
- This central repository owns only this reusable minimum policy and its navigation entry; it does not store project-specific plots or research outputs.
- Downstream repositories adopt this policy through a separate reviewed PR that records the full central commit SHA and any compatible project-local extensions.
- Existing frozen publication figures and historical plots are not deleted or migrated merely because this policy is adopted. Apply the default to new work and future revisions.

## 8. Relationship to calculation-result archival

This policy specializes the archival treatment of generated visual derivatives. The [Calculation-result archival policy](CALCULATION_RESULT_ARCHIVAL_POLICY.md) remains authoritative for raw/derived scientific data, run provenance, checksums, native outputs, large files, and remote verification. Where a plot is itself a non-reproducible measurement or primary data product, archive it as data rather than treating it as a disposable rendering.
