# Static Schema and Migration Review — 2026-10-23

**Status: static review only. No unit tests, integration tests, CI jobs, or migration runs were executed for this review.** Schema v1.4.3.7 remains an unreleased candidate; `commit_allowed=false`.

## Scope

Reviewed the current candidate Manifest and all 25 record schemas, the candidate validator, the v1.3-to-v1.4 migration prototype, the migration mapping contract, existing migration tests, and related audit documentation.

## Concrete implementation defects corrected

1. **Source Activity status could be accepted as launch evidence but remain invalid in the target schema.** The migration resolver accepted `in_progress`, while the v1.4 `validation_activity.execution_status` enum uses `running` rather than `in_progress`. The migration now leaves a source status unresolved unless it has an explicit mapping to a target enum value. It does not silently infer `in_progress → running`.
2. **Launch evidence used a non-empty timestamp check.** `started_at` must now match a timezone-bearing ISO date-time form and parse as timezone-aware before it is accepted as launch evidence.
3. **Legacy aliases were applied across unrelated record types.** A shared alias dictionary could attempt to map artifact fields onto Task Execution Contract fields, or apply those mappings to `run` records. Aliases are now scoped by record type: artifact aliases apply only to `artifact`; `version` and `contract_hash` aliases apply only to `task_execution_contract`.
4. **Source files could be silently skipped or parsed ambiguously.** The inventory now includes `.json`, `.yaml`, and `.yml`; non-object inputs and objects without a non-empty `record_type` are reported as unresolved, malformed files retain their source SHA-256, duplicate JSON/YAML mapping keys and non-finite values are rejected, YAML aliases and non-JSON YAML values are rejected, and an empty source snapshot is not treated as a clean dry-run.
5. **Schema loading and provenance failed open.** Malformed schemas were previously ignored and schema bytes were not checked against the candidate manifest. The migration now requires the exact unreleased v1.4.3.7 candidate manifest, checks each schema SHA-256 against its manifest entry, checks the full expected record-type set, verifies each schema's `record_type.const` against its filename and `schema_version.const == "1.4"`, and checks that the runtime mapping contract, rule IDs, and ID-mapping output fields match the implementation.
6. **Source identity checks were incomplete.** The migration now requires a non-empty string `project_id` and string primary key, and records duplicate same-project/same-record-type primary keys as unresolved. Cross-type collisions remain unresolved when an untyped `validation_ids` reference cannot uniquely resolve.
7. **Existing typed Claim references could violate the target contract.** The migration now reports invalid reference-list shapes, blank/non-string values, and duplicate values in `validation_activity_ids` or `validation_plan_ids`. Top-level target enum mismatches are also reported as unresolved.
8. **Staging output could retain stale files or be re-ingested as input.** Staging now refuses an output directory inside the input tree and refuses a non-empty output directory. The report distinguishes total source JSON files from loaded and migratable records.
9. **Rule/version drift was possible.** The migration rule version was advanced to `v1.4.3.7-migration-rules-3`; the mapping contract now lists the implemented candidate field mappings and marks their historical compatibility as unverified.
10. **Unresolved records could still be emitted to staging.** A migration row with unresolved mappings previously retained a non-null target record and the staging writer emitted it. The prototype now withholds target JSON and `target_sha256` whenever a record has unresolved items; only clearly labelled provisional candidate digests remain in the report.
11. **The ID-mapping output did not satisfy its declared provenance contract.** Mapping rows now include the source-relative URI, target/candidate identities and hashes, migration rule ID, applied field-mapping IDs, review status, collision check, rewritten-reference count, UTC timestamp, and operator field. An omitted operator is explicitly `not_recorded`, and every clean row remains `pending_review` rather than approved.
12. **Quarantined unknown fields and pending normative artifact transforms could still yield a target record.** Unknown values remain preserved in the warning report but now create an unresolved review item. The candidate rules that insert `alternative_identity: null` or downgrade hashless external artifact integrity are also unresolved pending explicit normative approval; neither can produce a target record in staging.

The corresponding regression tests were added or updated, but **they have not been run**.

## Static Schema observations

- All 25 candidate schema files inspected declare their required fields in `properties`, set `additionalProperties: false`, and constrain `schema_version` to `1.4`. This is a structural observation only; it is not proof of complete coverage against the source design document.
- The Manifest now declares the design's `test_id_pattern`; the validator checks that it is non-empty and matches `test_case.schema.json`, and separately enforces `strict_unknown_fields: true` and `extensions_supported: false`. These checks are implemented but unexecuted.
- The schema `$id` and `title` values retain mixed source-version labels: 23 files identify themselves as v1.4.2 candidate schemas, while `artifact` and `task_execution_contract` identify as v1.4.3.6 integrated candidates. This may be intentional preservation of per-schema identity/lineage. The bundle does not explicitly say whether these are immutable source identifiers or should be normalized to the integrated v1.4.3.7 candidate. **Do not rewrite them until the identity/versioning contract is clarified**, because `$id` can be consumed as a schema identifier.
- All inspected schema `$id` URIs also use the `schemas.example.invalid` host. The source design's §69.4 explicitly says a released bundle must use stable, versioned `$id` values and must not publish `example.invalid` identifiers. A real schema URI has not been supplied; do not invent one. This is a release blocker requiring an owner-approved URI policy.
- The Manifest uses `schema_version: "1.4.3.7-candidate"` as the integrated bundle label, while the v1.6.6 design's §69.2 manifest contract example uses `schema_version: "1.4"`; individual record schemas also constrain `schema_version` to `"1.4"`. The current validator and fixture-index contract depend on the candidate-label interpretation. Decide whether to separate `bundle_version` from the record schema version or explicitly revise the design contract; do not silently reinterpret this field.
- The existing `字段与约束覆盖差距矩阵.md/.csv` is labelled as a Schema v1.4.1 snapshot based on the v1.6.5 design baseline, not the current v1.4.3.7 bundle and v1.6.6 design. It is useful historical evidence but cannot be treated as the current coverage matrix; regenerate it against the current source design before release.
- `claim.schema.json` still allows `evidence_ids` to be an array, object, number, string, or null. The current normative Claim contract describes typed evidence references and structured `evidence_status`; this permissive legacy property needs explicit reconciliation rather than being treated as full contract coverage.
- `validation_activity.schema.json` declares both required `completed_at` (nullable) and an optional `finished_at`. Their intended relationship should be reconciled with the source design before changing the schema.
- The migration prototype now says explicitly that it does **not** perform full JSON Schema validation of target records. Top-level property filtering and enum checks are not a substitute for validating each staged target against the complete candidate schema.

## Remaining blockers and decisions

1. The original historical v1.3 schema bundle and representative/complete record corpus are unavailable. The 12 listed candidate field mappings therefore remain historically unverified.
2. Source values such as `in_progress`, `planned`, and `not_run` need an explicit, evidence-backed mapping decision before they can be converted to target statuses. No mapping has been approved by this review.
3. Full JSON Schema validation of every staged target and complete cross-record validation remain to be implemented or performed as a separately evidenced gate.
4. Obtain an owner-approved stable, versioned schema `$id` URI and define whether inherited schema titles/IDs preserve source identity or are versioned to the integrated bundle.
5. Refresh the field/constraint coverage matrix against the current v1.6.6 design and v1.4.3.7 schemas; reconcile the permissive `claim.evidence_ids` type and the `completed_at`/`finished_at` mismatch.
6. Transactional commit, active-dataset pointer switching, and rollback remain unimplemented. `commit_allowed=false` must remain unchanged.
7. DD-ART-007 through DD-ART-010 remain pending explicit owner approval.
8. No CI or test result is claimed for the current PR HEAD. All newly added regression cases remain unexecuted.

## Review disposition

**Keep PR #6 open and Draft. Do not merge or release Schema v1.4.3.7 on the basis of this static review.**

## Follow-up static findings — deterministic migration evidence

The following points were rechecked against the current migration implementation and are not test results.

### P0 — Target records can be written without complete JSON Schema validation

The migration loader reads and hashes all candidate schemas, but retains only each schema's properties object. migrate_record checks unknown properties and top-level enum values; it does not validate the complete output against the schema. Consequently, a record with no unresolved migration rule can be emitted to staging even if a required field is absent or a nested object violates its schema. The report currently states target_schema_validation: not_performed_by_migration_prototype, but the staging writer itself does not make that limitation a hard stop.

**Required correction before staging can be treated as usable:** retain the complete schema objects, validate every candidate target with the declared JSON Schema dialect and format checker, and withhold any schema-invalid record from staging. Add regression cases for missing required properties and invalid nested payloads. Until that is implemented and exercised, staging output must be treated as an unvalidated proposal, not a migration-ready dataset.

### P1 — Target digest serialization is deterministic within this Python implementation, but not specified as cross-language canonical JSON

The migration code computes provisional/target digests using json.dumps(..., sort_keys=True, separators=(",", ":"), allow_nan=False) via stable_json. This is deterministic for the supported Python values, but it is not declared or implemented as RFC 8785 JCS. In particular, Python's JSON number rendering and key ordering are not a general guarantee of JCS-compatible canonical bytes. Therefore, the contract's requirement that repeated migrations yield identical hashes is currently demonstrated only as an implementation-local convention, not a cross-language canonicalization contract.

**Required correction:** either explicitly define the migration digest as a versioned Python-specific serialization (not recommended for portable evidence), or use the repository's pinned RFC 8785 implementation for target digests and publish a golden vector. Keep the fingerprint algorithm's canonicalization contract distinct from migration source-byte hashes.

### P1 — Target schema $id values are not release-ready

The candidate schema files retain schemas.example.invalid identifiers and mixed inherited version labels. These may be intentional source identities, but the repository design requires stable versioned identifiers for a released bundle. No real canonical URI has been approved. Do not invent or rewrite identifiers in this PR; obtain the owner's URI policy and document whether $id preserves immutable source identity or names the integrated candidate.

### Verification boundary

No unit test, integration test, local migration, or CI job was executed for these follow-up findings. They are source-level review conclusions only. PR #6 must remain Draft, and commit_allowed=false must remain unchanged until the P0 staging-validation gap and the other release gates are addressed.
