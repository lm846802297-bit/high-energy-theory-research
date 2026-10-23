# Schema v1.4.3.7 candidate

简体中文版本：[README.zh-CN.md](README.zh-CN.md)。

This directory contains an unapproved candidate schema bundle. It is not a released normative version.

## Versioned fixture sets

- `tests/fixture-index.json` is the inherited `1.4.3.6-candidate` fixture index. Its bytes and version label are preserved as provenance; it is not silently relabeled.
- `tests/fixture-index-v1.4.3.7.json` is the candidate-specific fixture index used for acceptance against the current schemas. The four Run Plan/Run Manifest valid/conditional fixture records are regenerated in `tests/v1.4.3.7/` with non-empty structured payloads that meet the candidate contracts.
- The validator reports mismatches between the inherited fixture expectations and current candidate schemas separately as compatibility drift. Those mismatches do not replace or weaken the version-matched candidate test suite.

## FingerprintInputs

`run_plan.fingerprint_inputs` uses the candidate-only `fingerprint-inputs-v1` contract described in `docs/governance/fingerprint-inputs-contract-review.md`. The RFC 8785 deterministic hashing implementation, golden vector and negative tests are in the research Skill scripts and `tests/unit/test_fingerprint_inputs.py`.

## Validation-report provenance

The workflow regenerates `audit/validation-report.json` in the runner and uploads it as the `candidate-schema-validation-report` Actions artifact. The checked-in report file is an imported repository snapshot and is not by itself evidence of the latest CI run. Use the report artifact attached to the specific workflow run when auditing current counts and fixture outcomes.


## Migration prototype and validation_ids boundary

The migration tool uses rules version v1.4.3.7-migration-rules-2.

- The tool loads the read-only source snapshot first and resolves references only by unique primary key within the same project.
- A uniquely resolved validation_plan maps to validation_plan_ids.
- A validation_activity maps to validation_activity_ids only when execution_status is in_progress, succeeded, or failed and started_at is non-empty.
- Missing targets, cross-type duplicate IDs, unsupported record types, project mismatches, and insufficient launch evidence remain unresolved.
- An empty legacy validation_ids list maps to empty validation_activity_ids and validation_plan_ids arrays.
- Dry-run and staging remain non-committing. The report always sets commit_allowed=false; transactional commit, active-pointer switching, rollback, and full migration validation are not implemented.
- Regression tests: tests/unit/test_migration_reference_resolution.py. The existing audit/migration-dry-run-summary.json is a historical report generated under rules version 1.

This resolver reduces avoidable ambiguity only when source evidence is complete. It does not make the migration source bundle available and does not approve any normative decision.

## Release constraints

- DD-ART-007 through DD-ART-010 remain unapproved.
- `validation_ids` migration remains staging-only and blocked while ambiguous.
- Schema/CI success is not a physics correctness certificate. A real research task must independently verify provenance → configuration → run → artifact → validation → evidence → Claim before any release decision.
