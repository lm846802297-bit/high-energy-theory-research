# Open issues and known limitations

This list separates verified software behavior from unresolved design, provenance, and scientific questions.

## P0 — Must resolve before calling the schema package a release

1. **Four normative decisions remain pending.** DD-ART-007 through DD-ART-010 are recommendations, not approvals. No normative Schema change or formal release may treat them as approved until the repository owner explicitly decides each one. See docs/governance/DECISION_REGISTER.md and docs/governance/schema-v1.4.3.7-four-decisions-review.md.
2. **Historical v1.3 compatibility is unverified.** The exact v1.3 machine-readable source bundle and historical record corpus are unavailable in the repository/inspected Library inventory. The migration prototype's synthetic tests do not replace that baseline. See schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. **Migration remains staging-only.** The owner reports rules-v5 local verification on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`: directory-manifest tests 7/7, migration regression 33/33, integration tests 30/30, full `tests/unit` 83/83, Python compilation passed, and the full Schema validator passed (68/68 checks, 83/83 candidate fixtures, 16/16 semantic cases, 125 trace rows). Those results do not validate the later rules-v6 change. Rules v6 adds MIG-015 for the pending DD-ART-010 Task Execution Contract hash/registry gate and has not yet run locally. The report was generated outside the repository; the checked-in historical validation report was not overwritten. GitHub Actions remains unverified for this phase. Transactional commit/pointer-based rollback remain unimplemented; `commit_allowed=false` is an intentional safety invariant.
4. **The integrated candidate is not released.** Schema v1.4.3.7 remains candidate-only. The checked-in `audit/validation-report.json` is intentionally a historical snapshot; the owner-generated local report was kept in a temporary directory and did not overwrite it. Local verification results are recorded in `schema/v1.4.3.7/audit/current-head-test-execution-2026-10-23.md`.

## Resolved in the candidate metadata contract

- **Fixture-index version semantics.** The canonical manifest.fixture_index now points to the version-matched v1.4.3.7 candidate index. manifest.legacy_fixture_index preserves the 1.4.3.6 expectation baseline. The validator checks both file digests and both version relationships. The original source ZIP is not committed, so byte-for-byte equality with that archive is not claimed. See schema/v1.4.3.7/audit/fixture-index-version-audit.md.

## P1 — Coverage and implementation gaps

- The schemas are candidate envelopes, not a complete transcription of every normative field and condition in the design document.
- The existing `字段与约束覆盖差距矩阵.md/.csv` is a historical Schema v1.4.1 / design v1.6.5 snapshot, not current v1.4.3.7 / v1.6.6 coverage evidence. Regenerate it against the current design before release.
- `claim.schema.json` allows `evidence_ids` to be an array, object, number, string, or null, while the current normative Claim contract calls for typed evidence references and structured evidence status. Reconcile this permissive legacy property with the normative contract.
- **Schema identity/version metadata blocks release.** All inspected schema `$id` URIs use `schemas.example.invalid`, which the design's §69.4 forbids for a released bundle; most labels retain v1.4.2 and `artifact`/`task_execution_contract` retain v1.4.3.6. Separately, Manifest `schema_version` means `1.4.3.7-candidate` while the design's §69.2 contract uses `1.4`, matching the record schemas. Obtain an owner-approved stable URI and decide whether to introduce a separate `bundle_version` or revise the contract. Do not invent a URI or silently reinterpret these fields.
- **Validation Activity time-field semantics need reconciliation.** The candidate schema requires nullable `completed_at` while separately defining optional `finished_at`; compare with the source design before changing either field.
- **DD-ART-010 Task Execution Contract migration gate.** The rules-v5 migrator could preserve a source `contract_hash` as `contract_sha256` without target-payload revalidation and could accept a missing `alternative_identity_methods` registry. Rules v6 adds MIG-015 and two tests to withhold these records. A separate source-inventory fix now checks the input root for symlinks and has a regression test. These three new migration tests have not yet been locally executed; DD-ART-010 remains pending owner approval.
- **DD-ART-008 symlink policy mismatch.** The Artifact Schema allows `FileEntry.entry_type: "symlink"`, but the manifest helper rejects symlink entries. Resolve the normative Schema/helper contract after owner approval; filesystem-aware symlink verification is not implemented.
- Full per-record JSON Schema validation is locally verified on the tested code HEAD. Cross-record/state-machine validation remains separate and must be implemented and evidenced before any migration is accepted.
- FingerprintInputs has a candidate contract and deterministic tests, but its normative status still requires review. The fingerprint contract does not establish scientific correctness.
- Cross-record validation does not cover every polymorphic reference or every state-machine namespace.
- Event payload hashes are not comprehensively recomputed.
- The directory-manifest helper validates a restricted FileEntry representation; it does not walk the filesystem or prove that the manifest matches disk contents. A static review found and fixed silent dropping of extra FileEntry keys and made `allow_symlinks=True` fail closed. The owner reports the new directory-manifest tests passed 7/7 on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. Filesystem traversal and byte-for-byte verification remain unimplemented. Symlinks are rejected.
- The Skill instruction scaffold is not yet a complete executable workflow for all research tasks.

## Scientific acceptance — Not yet implemented

- No physical calculation, phenomenological scan, experimental recast, or manuscript claim is certified merely because software tests pass.
- The synthetic 2x2 matrix pilot exercises exact results and independent algebraic checks, but is not a real phenomenology task. A later acceptance suite must test a real research task, including source provenance, conventions, independent symbolic/numerical checks, software versions, and result-to-claim traceability.
- Parameter-space reports must distinguish theoretically realizable, experimentally allowed, excluded, not assessed, and EFT-inapplicable regions; benchmark-dependent results must label their benchmark assumptions.
