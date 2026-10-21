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
