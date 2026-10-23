# Changelog

## 2026-10-21 — Initial repository import

- Imported the extracted contents of the Schema v1.4.3.7 integrated candidate bundle into schema/v1.4.3.7/.
- Added the v1.6.5 design baseline and the four-decision review.
- Added a reusable research Skill scaffold, reference guides, unit checks, pinned validation dependency, and GitHub Actions workflow.
- Corrected the candidate package README's integration-test count from 27 to 29; the bundled test file contains 29 tests.
- Regenerated audit/validation-report.json using the bundled validator. The fresh report records 58 checks, 83 fixture expectations, 16 semantic-case expectations, 25 schema record types, and 125 trace rows.
- No JSON Schema definitions or normative decisions were changed in this import. Four Artifact identity decisions remain pending approval.

## 2026-10-21 — P0 project-record validation and audit reconciliation

- Added `skills/high-energy-theory-research/scripts/validate_project_records.py` for JSON/YAML parsing, candidate JSON Schema checks, bounded cross-record validation, per-project primary-ID uniqueness across record types, status/reason consistency, and local source/artifact path checks.
- Added regression tests for valid JSON/YAML, missing references, cross-type duplicate IDs, missing `not_applicable` reasons, invalid status values, duplicate YAML keys, and local path checks.
- Added the pinned PyYAML dependency and included the Skill script in Python compilation checks.
- Corrected array-reference handling for artifact inputs, validation activity/report evidence, benchmark evidence, and parameter-point artifact lists; added a regression test so empty arrays are not misread as scalar IDs.
- Reconciled the traceability CSV count at 125 data rows (excluding the header) and corrected the stale audit narrative. The schema remains a candidate and scientific acceptance remains out of scope.

## 2026-10-21 — Fixture-index version-field audit

- Recorded the observed mismatch between the candidate bundle manifest (`1.4.3.7-candidate`) and the fixture index (`1.4.3.6-candidate`).
- Confirmed that CI verifies the fixture-index file digest and fixture outcomes but does not interpret the top-level index `schema_version`.
- Preserved the existing index bytes because the source ZIP is not committed and the field's intended semantics are not defined. This is an explicit unresolved release blocker, not a claimed fix.

## 2026-10-21 — Fixture-index audit guard and end-to-end pilot

- Added a regression test that verifies the fixture-index version mismatch, source-lineage record, and current validator behavior remain explicit; the index bytes were not changed.
- Added a synthetic 2x2 mass-squared matrix pilot with exact eigenvalues/masses, trace and determinant checks, eigenvector normalization/orthogonality, eigenpair residuals, and a positivity check.
- Added a synthetic Task-to-Claim record chain and tests for candidate-schema payloads that are currently rejected. The mathematical calculation passes, but full reproducibility acceptance is explicitly blocked until the structured schema envelopes are completed.

## 2026-10-21 — Structured research-record payload remediation

- Added explicit candidate-schema structures for Run Plan `execution_spec`, Run Manifest snapshots/fingerprint bundle/outputs/validation, Claim evidence dimensions and physics assessment, and Artifact Plan completeness rules.
- Allowed `schema_or_structure` to carry an opaque object or null, consistent with its design-document type.
- Updated the two positive Claim fixtures to use `physics_assessment: null` under the object-or-null contract.
- Left `run_plan.fingerprint_inputs` unchanged because the source design references `FingerprintInputs` without defining its fields or hash semantics; documented this as a release blocker rather than inventing a normative contract.

## 2026-10-23 — Multi-project registry foundation (Phase A)

- Added projects/README.md and projects/registry.yaml to register project/workstream hierarchy.
- Registered axial-vector-model-building as the parent project and vll-higgs-singlet-uv-eft as a nested workstream, not a separate top-level project.
- Added templates/project-record.md for future projects and workstreams.
- Updated the repository landing page, research index, and Scientific Diff workflow to distinguish project, workstream, research-change, run, and claim identities.
- No existing research files were moved or renamed. The registry is navigation metadata only; no candidate schema was changed and no scientific result was promoted.

## 2026-10-23 — Multi-project user guide and registry validation

- Added docs/USER_GUIDE.md as the detailed operating manual; the root README remains the short onboarding page.
- Added a dedicated project-registry validator and unit tests for hierarchy consistency, duplicate IDs, missing canonical paths, and path traversal.
- Updated the research Skill and project registry guide to distinguish navigation metadata from candidate-schema structured research records.
- Updated the README validation commands and project hierarchy references.
- No existing research files were moved. The new validator and tests have not been executed in a repository runtime in this change; treat runtime validation as pending until the command/test output is captured.

