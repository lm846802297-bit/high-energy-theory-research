# Project Registry and Migration Pre-Audit

**Date:** 2026-10-23  
**Scope:** Phase A multi-project registry, onboarding guide, and the currently registered UV–EFT workstream.  
**Outcome:** Phase A established the navigation layer without moving files. A later RC-001 migration (2026-11-23) transferred the frozen 480-file research payload into its project repository; see the dated update at the end of this audit.

## 1. Confirmed hierarchy

- Top-level project: axial-vector-model-building
- Nested workstream: vll-higgs-singlet-uv-eft
- Research-change / main record: RC-001
- Gauge-subgraph record: linked subrecord under the same UV–EFT workstream
- Claim ledger: CL-015 and the other entries in the record-specific Claim–Evidence Matrix

No other top-level projects were added in this phase because their registration and parent relationships were not established by the files audited in this repository. This is deliberate, not a claim that no other research exists elsewhere.

## 2. Path and reference checks performed

| Area | Check | Result |
|---|---|---|
| Registry canonical records | Confirmed the registered main record and gauge-subgraph record exist in the current GitHub tree | Pass |
| Claim Matrix and workstream index | Confirmed declared files exist | Pass |
| README onboarding | Checked explicit relative Markdown links against the repository tree; corrected the numbered onboarding list | Pass |
| User Guide | Checked explicit relative Markdown links against the repository tree and improved navigation links | Pass |
| Project Registry guide | Checked explicit relative Markdown links against the repository tree | Pass |
| Research Skill | Added explicit parent-project/workstream selection instructions and the correct registry-validation command | Pass |
| Structured-record validator boundary | Kept registry YAML separate from candidate Schema v1.4.3.7 JSON/YAML research records | Pass |
| Test discovery | Added a unittest module under tests/unit/, which is covered by the documented unittest discovery command | Static path check only |
| File migration | No source research files were moved or renamed | Not applicable in Phase A |

The project registry validator checks declared canonical paths and rejects paths that resolve outside the repository root. Its unit tests cover a valid hierarchy, parent mismatch, missing path, path traversal, duplicate project ID, and duplicate YAML mapping key.

## 3. What has not been verified

- The new registry validator and its unit tests have **not** been executed in a local repository checkout in this work session.
- The container could not clone GitHub because DNS/network access was unavailable.
- No current-head CI result was obtained; do not infer a pass from a commit existing on main.
- This was not a complete repository-wide Markdown-link scan. The checks covered the registry and the key onboarding/usage documents listed above.
- No physical derivation, Wilson coefficient, or scientific claim was revalidated by this documentation/structure change.

## 4. Schema and validator boundary

The registry is descriptive navigation metadata. It is not a new record type in Schema v1.4.3.7 and is not passed to validate_project_records.py.

Use the dedicated command:

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

Use validate_project_records.py only for a directory containing structured JSON/YAML records that conform to the candidate schema bundle. Neither command validates physics.

No candidate schema, migration rule, normative decision, or existing structured research record was changed in this phase.

## 5. Gates before any physical-file migration

Before moving research/, calculations/, or validation/ artifacts into project-local folders:

1. Generate a complete inventory of files and all references to each proposed old path.
2. Search Markdown links, relative file references, Python imports, test fixtures, workflow YAML, shell commands, schema constraints, and validator path assumptions.
3. Define a one-to-one old-path → new-path mapping and preserve the mapping in the migration record.
4. Verify that all registered canonical paths and downstream references resolve on the candidate commit.
5. Run the registry validator, structured-record tests, relevant unit tests, and all available CI on the exact new HEAD.
6. Review the resulting diff to ensure the migration changes paths only and does not silently alter scientific content.
7. Preserve the pre-migration baseline and leave unresolved references visible.

These gates were subsequently completed for RC-001. Its 480-file frozen source snapshot was migrated to [axial-vector-review-response](https://github.com/lm846802297-bit/axial-vector-review-response/tree/main/research/rc001-vll-higgs-singlet-uv-eft) and merged through [PR #135](https://github.com/lm846802297-bit/axial-vector-review-response/pull/135). The central repository cleanup is tracked separately in [PR #34](https://github.com/lm846802297-bit/high-energy-theory-research/pull/34). Other future workstream migrations must satisfy the same gates before their source files are moved.

## 6. RC-001 archive migration update — 2026-11-23

The RC-001 research payload has now been migrated out of this central infrastructure repository into `lm846802297-bit/axial-vector-review-response`, under `research/rc001-vll-higgs-singlet-uv-eft/upstream/`.

- Frozen source commit: `b2dd8f7e4427d0292bc299d273c780c05021fdab`.
- Migration PR: [axial-vector-review-response#135](https://github.com/lm846802297-bit/axial-vector-review-response/pull/135), merged at `a1940523eb5e345a5a9c03a06b9e0f4f63f4d378`.
- Archive integrity: 480/480 mapped paths, Git blob SHAs, and file sizes matched; zero missing files or mismatches.
- The central repository's RC-001 research records, calculations, validation outputs, artifact bundle, and three RC-001-specific workflows are removed by cleanup PR [#34](https://github.com/lm846802297-bit/high-energy-theory-research/pull/34).
- Shared Skills, schemas, templates, standards, documentation, project registry, tests, and the two generic validation workflows remain in the central repository.

This migration changed repository location and navigation, not scientific content or validation status. The project repository is the canonical location for RC-001 source records and results.
