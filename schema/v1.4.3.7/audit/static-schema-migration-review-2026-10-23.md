# Static Schema and Migration Review — 2026-10-23

**Status: static review plus owner-reported local verification addenda.** The initial static pass did not execute tests; the owner later reported rules-v5 local validation on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. A subsequent rules-v6 migration guard and tests have been added but are not yet execution-verified. Schema v1.4.3.7 remains an unreleased candidate; `commit_allowed=false`.

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
9. **Rule/version drift was possible.** The migration rule version was `v1.4.3.7-migration-rules-4` at the time of the original review. A later static finding added the dependent-reference withholding rule MIG-014 and advanced the candidate contract to rules v5. The owner subsequently reported rules-v5 local verification on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`: directory-manifest tests 7/7, migration regression 33/33, integration 30/30, full repository unit tests 83/83, Python compilation passed, and Schema validation 68/68 with 83/83 candidate fixtures, 16/16 semantic cases, and 125 trace rows. Candidate field mappings remain historically unverified.
10. **Unresolved records could still be emitted to staging.** A migration row with unresolved mappings previously retained a non-null target record and the staging writer emitted it. The prototype now withholds target JSON and `target_sha256` whenever a record has unresolved items; only clearly labelled provisional candidate digests remain in the report.
11. **The ID-mapping output did not satisfy its declared provenance contract.** Mapping rows now include the source-relative URI, target/candidate identities and hashes, migration rule ID, applied field-mapping IDs, review status, collision check, rewritten-reference count, UTC timestamp, and operator field. An omitted operator is explicitly `not_recorded`, and every clean row remains `pending_review` rather than approved.
12. **Quarantined unknown fields and pending normative artifact transforms could still yield a target record.** Unknown values remain preserved in the warning report but now create an unresolved review item. The candidate rules that insert `alternative_identity: null` or downgrade hashless external artifact integrity are also unresolved pending explicit normative approval; neither can produce a target record in staging.

13. **Directory-manifest normalization could silently change entry meaning.** The helper previously required the FileEntry keys to be present but accepted additional keys and then rebuilt entries using only the known keys. Extra caller data could therefore be silently discarded before hashing. The `allow_symlinks` argument was also accepted even though symlink entries were always rejected and no filesystem-root containment proof exists. The helper now requires the exact FileEntry key set and explicitly rejects `allow_symlinks=True`; new unit tests cover extra/missing keys, NFC collisions, traversal, ordering, and symlink behavior. The owner later reported that the directory-manifest tests passed 7/7 on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. The helper still does not walk the filesystem or prove that entry hashes/sizes match actual bytes.

At the time of the initial static review, the corresponding regression tests had not been run. The owner subsequently reported that the rules-v5 suites passed on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`; the later rules-v6 MIG-015 tests have not yet been run.

## Static Schema observations

- All 25 candidate schema files inspected declare their required fields in `properties`, set `additionalProperties: false`, and constrain `schema_version` to `1.4`. This is a structural observation only; it is not proof of complete coverage against the source design document.
- The Manifest now declares the design's `test_id_pattern`; the validator checks that it is non-empty and matches `test_case.schema.json`, and separately enforces `strict_unknown_fields: true` and `extensions_supported: false`. The owner-reported local Schema validation passed 68/68 checks on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`; this is local evidence, not GitHub Actions evidence.
- The schema `$id` and `title` values retain mixed source-version labels: 23 files identify themselves as v1.4.2 candidate schemas, while `artifact` and `task_execution_contract` identify as v1.4.3.6 integrated candidates. This may be intentional preservation of per-schema identity/lineage. The bundle does not explicitly say whether these are immutable source identifiers or should be normalized to the integrated v1.4.3.7 candidate. **Do not rewrite them until the identity/versioning contract is clarified**, because `$id` can be consumed as a schema identifier.
- All inspected schema `$id` URIs also use the `schemas.example.invalid` host. The source design's §69.4 explicitly says a released bundle must use stable, versioned `$id` values and must not publish `example.invalid` identifiers. A real schema URI has not been supplied; do not invent one. This is a release blocker requiring an owner-approved URI policy.
- The Manifest uses `schema_version: "1.4.3.7-candidate"` as the integrated bundle label, while the v1.6.6 design's §69.2 manifest contract example uses `schema_version: "1.4"`; individual record schemas also constrain `schema_version` to `"1.4"`. The current validator and fixture-index contract depend on the candidate-label interpretation. Decide whether to separate `bundle_version` from the record schema version or explicitly revise the design contract; do not silently reinterpret this field.
- The existing `字段与约束覆盖差距矩阵.md/.csv` is labelled as a Schema v1.4.1 snapshot based on the v1.6.5 design baseline, not the current v1.4.3.7 bundle and v1.6.6 design. It is useful historical evidence but cannot be treated as the current coverage matrix; regenerate it against the current source design before release.
- `claim.schema.json` still allows `evidence_ids` to be an array, object, number, string, or null. The current normative Claim contract describes typed evidence references and structured `evidence_status`; this permissive legacy property needs explicit reconciliation rather than being treated as full contract coverage.
- `validation_activity.schema.json` declares both required `completed_at` (nullable) and an optional `finished_at`. Their intended relationship should be reconciled with the source design before changing the schema.
- The migration implementation now performs full Draft 2020-12 JSON Schema validation with a format checker on each provisional target before staging. Invalid targets are withheld. An empty source snapshot, any skipped source file, or source symlink now blocks all target writes to staging. The mapping contract binds full target validation and RFC 8785 target digest semantics as MIG-012/MIG-013, and the implementation checks those exact rule texts. The owner later reported rules-v5 local verification on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`: migration regression 33/33, integration 30/30, full repository unit tests 83/83, directory-manifest tests 7/7, Python compilation passed, and the Schema validator passed 68/68 checks, 83/83 candidate fixtures, 16/16 semantic cases, and 125 trace rows. A subsequent rules-v6 change is pending local execution. The new MIG-014 dependent-reference withholding test passed.

## Remaining blockers and decisions

1. The original historical v1.3 schema bundle and representative/complete record corpus are unavailable. The 12 listed candidate field mappings therefore remain historically unverified.
2. Source values such as `in_progress`, `planned`, and `not_run` need an explicit, evidence-backed mapping decision before they can be converted to target statuses. No mapping has been approved by this review.
3. Full per-record JSON Schema validation and the new migration guards have since been executed locally by the owner on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`: migration regression tests 32/32 passed, integration tests 30/30 passed, repository unit tests 75/75 passed, Python compilation passed, and the full Schema validator passed (68/68 checks, 83/83 candidate fixture outcomes, 16/16 semantic cases, 125 trace rows). Complete cross-record/state-machine validation still needs implementation and separate evidence.
4. Obtain an owner-approved stable, versioned schema `$id` URI and define whether inherited schema titles/IDs preserve source identity or are versioned to the integrated bundle.
5. Refresh the field/constraint coverage matrix against the current v1.6.6 design and v1.4.3.7 schemas; reconcile the permissive `claim.evidence_ids` type and the `completed_at`/`finished_at` mismatch.
6. Transactional commit, active-dataset pointer switching, and rollback remain unimplemented. `commit_allowed=false` must remain unchanged.
7. DD-ART-007 through DD-ART-010 remain pending explicit owner approval.
8. At the time of this static review, no test result had yet been reported for the corrected fixtures. The owner subsequently reported the local results recorded above; those results apply to code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`. This statement is superseded: the current code-bearing PR HEAD `c69651858a9c0b6155242c25a4c09c1364284823` includes rules-v6/MIG-015 and source-root-symlink changes after the rules-v5 tested HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. Those code changes have not been execution-verified by the rules-v5 local results.

## Review disposition

**Keep PR #6 open and Draft. Do not merge or release Schema v1.4.3.7 on the basis of this static review.**

## Follow-up static findings — deterministic migration evidence

The following points were rechecked against the current migration implementation and are not test results.

### P0 — Full target JSON Schema validation before staging

**Implemented in rules v4; local execution and regression results subsequently passed on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c` (owner-reported).**

The prior implementation retained only schema properties and could emit a record that lacked a required field or contained an invalid nested object. The current candidate change now retains the complete schema objects, checks the declared Draft 2020-12 dialect and schema metaschema, constructs full validators with a format checker, and validates each transformed target. Schema errors are added to the unresolved report with JSON Pointer paths, and any record with a schema error is withheld from staging.

Regression cases have been added for a missing required Claim field and an invalid nested physics-assessment object. The dependency declaration now requests the pinned jsonschema format extras so optional format implementations are installed rather than silently skipped. **These changes and tests have not been executed**; do not treat the code change as a passing test result. Cross-record semantic validation remains a separate acceptance gate.

### P1 — Target digest serialization

**Implementation and contract updated; golden-vector test is included in the owner-reported passing migration regression suite (32/32) on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`.**

The migration implementation uses the repository's pinned RFC 8785 package and declares target digests as `RFC8785-JCS-SHA256`: SHA-256 over canonical UTF-8 bytes of the transformed target record. Original `source_sha256` continues to hash the exact source bytes and is not replaced by canonicalization. A machine-readable golden vector and a unit test are included. The digest change was introduced in rules v4; a later dependent-reference safety fix advanced the migration contract to rules v5.

This is an implementation proposal until the test is run and the candidate is reviewed; it does not establish historical compatibility or scientific validity.

### P1 — Target schema $id values are not release-ready

The candidate schema files retain schemas.example.invalid identifiers and mixed inherited version labels. These may be intentional source identities, but the repository design requires stable versioned identifiers for a released bundle. No real canonical URI has been approved. Do not invent or rewrite identifiers in this PR; obtain the owner's URI policy and document whether $id preserves immutable source identity or names the integrated candidate.

### Verification boundary

The follow-up findings began as source-level review conclusions. The latest completed local verification reported by the owner is rules-v5 code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` (directory-manifest 7/7, migration 33/33, integration 30/30, unit tests 83/83, compilation passed, Schema validator 68/68, fixtures 83/83, semantic cases 16/16, trace rows 125). The rules-v6 MIG-015 guard and tests were added afterward and are not yet execution-verified. None of these results establish historical v1.3 compatibility, resolve normative decisions, implement transaction safety, or authorize release. PR #6 must remain Draft, and `commit_allowed=false` must remain unchanged.

### Additional static finding — DD-ART-010 Task Execution Contract migration

The candidate Task Execution Contract Schema does not require `alternative_identity_methods`. The migration previously mapped legacy `contract_hash` to `contract_sha256` and could stage the record without recomputing that digest under the candidate payload rule. Because DD-ART-010 remains pending and the matrix says a missing registry must not be silently defaulted, this was a concrete fail-open gap. The migration is now rules v6 and implements MIG-015: missing registries and unverified source contract hashes produce unresolved items and withhold the target. Two Task Execution Contract regression tests and a contract-rule assertion were added. The source-root symlink guard has a third regression test. They have not yet run locally; do not treat the rules-v5 pass as validation of these changes.



### Additional static finding — source-root symlink bypass

The source inventory originally checked `is_symlink()` only on descendants returned by `inp.rglob("*")`, not on `input_dir` itself. A symlinked directory supplied as the migration root could therefore evade the explicit root-level symlink policy. The migrator now checks the input root and descendants; `test_symlinked_source_root_blocks_all_staging_targets` was added. Together with the two MIG-015 Task Execution Contract tests, three new migration tests are pending local execution. This is a correction to the existing MIG-010 source-symlink rule, not a new normative decision.

### Additional static finding — symlink policy mismatch

The Artifact Schema's `FileEntry.entry_type` enum includes `symlink`, while `directory_manifest.py` rejects symlink entries and the DD-ART-008 recommendation proposes rejecting symlinks by default. This is an unresolved Schema/helper contract mismatch. Keep it open until the owner approves whether symlinks are forbidden in the normative Schema or require a filesystem-aware verifier. No Schema change has been made because DD-ART-008 is still pending.

### Follow-up — canonicalization and branch evidence

The latest static review records the exact local/remote revision boundary and the directory-manifest JCS interoperability questions in the [Normalization and migration boundary review](schema/v1.4.3.7/audit/normalization-and-migration-boundary-review-2026-10-23.md). In particular, the current helper accepts unbounded non-negative `size_bytes` integers while the Schema has no maximum, and sorts paths using Python code-point order without a cross-language comparator contract. Dedicated directory-manifest canonical-byte/hash, numeric-domain and Unicode ordering vectors are still needed. These are static contract gaps, not observed test failures. No normative Schema change was made because DD-ART-008 remains pending.
