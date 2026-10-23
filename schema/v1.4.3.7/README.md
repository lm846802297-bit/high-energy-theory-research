# Schema v1.4.3.7 candidate

简体中文版本：[README.zh-CN.md](README.zh-CN.md)。

This directory contains an unapproved candidate schema bundle. It is not a released normative version.

## Versioned fixture sets

- The canonical manifest field `fixture_index` points to `tests/fixture-index-v1.4.3.7.json`, the acceptance index for this candidate. Its top-level `schema_version` must equal the bundle `schema_version`.
- The manifest field `legacy_fixture_index` points to `tests/fixture-index.json`, the preserved `1.4.3.6-candidate` expectation baseline. The legacy bytes and version label are not rewritten.
- The index `schema_version` means “the target bundle whose fixture expectations are declared”; source-archive lineage is recorded separately in `IMPORT_PROVENANCE.json`. The validator checks both index digests and both declared version relationships.
- The validator reports mismatches between legacy fixture expectations and current candidate schemas separately as compatibility drift. They do not replace or weaken the version-matched candidate test suite.

## FingerprintInputs

`run_plan.fingerprint_inputs` uses the candidate-only `fingerprint-inputs-v1` contract described in `docs/governance/fingerprint-inputs-contract-review.md`. The RFC 8785 deterministic hashing implementation, golden vector and negative tests are in the research Skill scripts and `tests/unit/test_fingerprint_inputs.py`.

## Validation-report provenance

The workflow regenerates `audit/validation-report.json` in the runner and uploads it as the `candidate-schema-validation-report` Actions artifact. The checked-in report file is an imported repository snapshot and is not by itself evidence of the latest CI run. Use the report artifact attached to the specific workflow run when auditing current counts and fixture outcomes.


## Migration prototype and validation_ids boundary

Static implementation findings, version-label questions, and unexecuted regression cases are recorded in [the 2026-10-23 static Schema/migration review](audit/static-schema-migration-review-2026-10-23.md). This review does not replace CI or target-schema validation.

The migration tool uses rules version `v1.4.3.7-migration-rules-4`. Static review tightened JSON/YAML source inventory, duplicate-key handling, project/key checks, timestamp and target-enum validation, record-type-specific aliases, manifest SHA verification, mapping-contract parity, ID-mapping provenance, and staging-output safety. Records with unresolved items are withheld from target staging. These changes have not been executed in tests or CI. Synthetic fixtures still do not establish compatibility with the full historical v1.3 corpus.

- The tool inventories `.json`, `.yaml`, and `.yml` source files before resolving references only by unique primary key within the same project. Duplicate JSON/YAML mapping keys, malformed files, non-object records, and unsupported YAML constructs are reported as unresolved rather than silently ignored.
- A uniquely resolved validation_plan maps to validation_plan_ids.
- A validation_activity reference maps to validation_activity_ids only when the target is unique in the same project, started_at is a valid timezone-aware ISO date-time, and its source status has an explicit mapping to a v1.4 enum. in_progress is not in the target enum (running is), so it remains unresolved until an explicit mapping is approved.
- Missing targets, cross-type duplicate IDs, unsupported record types, project mismatches, and insufficient launch evidence remain unresolved.
- An empty legacy validation_ids list maps to empty validation_activity_ids and validation_plan_ids arrays.
- Dry-run and staging remain non-committing. The report always sets commit_allowed=false. Every provisional target is validated against its complete Draft 2020-12 JSON Schema with a format checker before staging; schema-invalid records are withheld. This code path has not been executed in the current review. Complete cross-record validation, transactional commit, active-pointer switching, and rollback remain unimplemented. The tool also verifies schema hashes against the candidate Manifest, reports malformed JSON/YAML and duplicate keys, and refuses unsafe staging paths.
- Any record with unresolved items—including quarantined unknown fields and artifact transformations that depend on pending normative decisions—is withheld from target JSON staging. The ID-mapping report records source/target hashes, candidate-only target hashes when blocked, rule IDs, review state, collision state, rewritten-reference count, UTC timestamp, and operator identifier; an omitted operator is recorded as `not_recorded` and never implies approval.
- Regression tests: tests/unit/test_migration_reference_resolution.py. The existing audit/migration-dry-run-summary.json is a historical report generated under rules version 1.

This resolver reduces avoidable ambiguity only when source evidence is complete. The full historical v1.3 source bundle remains unavailable, so compatibility remains unverified. See `audit/v1.3-compatibility-gate.md`. No normative decision is implicitly approved.

## Release constraints

- DD-ART-007 through DD-ART-010 remain unapproved.
- `validation_ids` migration remains staging-only and blocked while ambiguous.
- Schema/CI success is not a physics correctness certificate. A real research task must independently verify provenance → configuration → run → artifact → validation → evidence → Claim before any release decision.
