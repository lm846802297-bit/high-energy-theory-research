# Schema v1.4.3.7 — DD-ART-007–010 Compatibility and Test Matrix

**Status: review aid only.** This matrix does not approve any normative decision. The four recommendations remain pending owner approval. The matrix separates tests that can be implemented now from tests whose expected normative behavior depends on the owner decision or unavailable historical source data.

## Summary

| Decision | Candidate recommendation | Compatibility impact | Required tests | Current evidence / gate |
|---|---|---|---|---|
| DD-ART-007 | Require `artifact_storage_kind: file|directory`; never infer it from extension, URI, or artifact type | Legacy records may omit the field; migrate only from source evidence, otherwise quarantine for review | Schema: missing field rejected; enum outside file/directory rejected. Migration: explicit source evidence maps; absent/contradictory evidence is unresolved. Semantic: file and directory hashing policies cannot be interchanged | Recommendation only; owner approval pending; historical corpus unavailable |
| DD-ART-008 | Normalize relative paths to Unicode NFC and POSIX separators; reject traversal, absolute paths, NFC collisions and disallowed symlinks; hash deterministically serialized normalized manifests with SHA-256 | Existing hashes may change if path normalization, entry ordering, or serialization changes; do not overwrite historical hashes before approval | Unit: NFC-equivalent collision; `..` and absolute paths; backslash rejection; deterministic ordering; exact FileEntry key set; symlink rejection; golden canonical bytes/hash. Integration: compare manifest entries with actual filesystem bytes and directory tree | Static review found the helper previously discarded extra FileEntry keys and exposed an `allow_symlinks` flag that did not enable safe symlink verification. The helper now rejects missing/extra keys and explicitly rejects `allow_symlinks=True`; the owner reports 7/7 directory-manifest tests passed on rules-v5 HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. A separate provisional vector now locks the current helper's exact UTF-8 bytes and SHA-256; its test has not been run on the post-patch HEAD and does not approve JCS interoperability, a safe-integer limit, or cross-language path ordering. Filesystem traversal/byte verification remains unimplemented. Owner approval pending |
| DD-ART-009 | External file without source-byte SHA-256 remains `needs_review`, even when alternative identity is verified | Legacy records marked `passed` based only on DOI/version/URL identity may need downgrade to `needs_review`; do not claim local bytes equal source bytes | Semantic positive: byte hash present and verified may pass. Negative: hashless external file cannot be `passed`. Alternative identity cannot establish byte equality. State transitions require a new review/check event | Candidate semantic subset exists, but rule remains pending approval; test results on current HEAD are unverified |
| DD-ART-010 | Include the normalized `alternative_identity_methods` registry in the versioned Task Execution Contract hash payload | Contract hashes may change; if historical payload cannot be reconstructed, retain original hash as source evidence and mark new verification unresolved | Golden vector: registry changes change contract digest. Method order canonicalization is deterministic. Method ID/version must resolve uniquely to an approved applicable method. Missing registry must not be silently defaulted unless an explicit migration rule is approved | Static review found the rules-v5 migrator could emit a TEC with a missing registry or carry forward a source hash without revalidation. Rules v6 adds MIG-015 to withhold those targets and adds two unit tests; the new code/tests are not yet run. Owner approval and historical payloads remain pending |

## Cross-cutting compatibility rules

1. Never silently rewrite historical content hashes, contract hashes, or directory-manifest hashes.
2. Preserve original source bytes and source SHA-256 independently from transformed-target canonical digests.
3. Any absent, ambiguous, contradictory, or unsupported legacy evidence becomes an explicit unresolved item; no inference from filename extension, URI shape, or current defaults.
4. Candidate schema validation, cross-record semantics, source-archive lineage, and transaction safety are separate gates.
5. Test pass on synthetic records is not proof of historical compatibility.
6. Any normative change requires an explicit decision record before implementation is treated as authoritative.

## Proposed test IDs

The IDs below are planning identifiers, not claims that tests have run or passed.

### DD-ART-007 — Storage kind

- `DDART007-SCHEMA-001`: reject missing `artifact_storage_kind`.
- `DDART007-SCHEMA-002`: reject values outside `file|directory`.
- `DDART007-MIG-001`: preserve explicit source-backed value.
- `DDART007-MIG-002`: absent or conflicting source evidence remains unresolved.
- `DDART007-SEM-001`: prevent file-byte and directory-manifest integrity rules from being interchanged.

### DD-ART-008 — Path normalization and directory identity

- `DDART008-PATH-001`: NFC-normalize paths and detect post-normalization collisions.
- `DDART008-PATH-002`: reject absolute paths, empty paths, `.` and `..` segments, and root escape.
- `DDART008-PATH-003`: normalize separators to POSIX form and sort by normalized path.
- `DDART008-PATH-004`: reject symlinks by default and do not follow them.
- `DDART008-HASH-001`: compare canonical UTF-8 bytes and SHA-256 against a reviewed golden vector.
- `DDART008-FS-001`: recompute size and file SHA-256 from actual bytes and detect missing/extra files.
- `DDART008-FS-002`: verify empty-directory treatment and directory-entry semantics.
- `DDART008-HASH-002`: reject or explicitly constrain `size_bytes` outside the RFC 8785 interoperable numeric domain; verify schema/helper contract alignment.
- `DDART008-PATH-005`: define the path-array sort comparator and test cross-language ordering with supplementary-plane and BMP characters (for example U+1F600 and U+E000).
- `DDART008-HASH-003`: provisional implementation vector `schema/v1.4.3.7/migrations/directory-manifest-candidate-v0.golden.json` is added and checked by a dedicated unit test. It captures the current Python helper's bytes only; cross-language/JCS approval and numeric-domain/path-order decisions remain open.

### DD-ART-009 — Hashless external artifacts

- `DDART009-SEM-001`: hashless external file cannot have byte-integrity status `passed`.
- `DDART009-SEM-002`: alternative identity `verified` does not imply source-byte equality.
- `DDART009-SEM-003`: `needs_review` can leave that state only with an explicit review/check event.
- `DDART009-MIG-001`: legacy `passed` without a source-byte hash is flagged for review, not silently trusted.

### DD-ART-010 — Contract hash payload

- `DDART010-HASH-001`: changing a registered identity method changes the contract digest.
- `DDART010-HASH-002`: canonicalized registry ordering is deterministic.
- `DDART010-SEM-001`: Artifact references an exact contract ID/version/hash and method ID/version.
- `DDART010-SEM-002`: unknown, duplicate, unapproved, or inapplicable methods are rejected.
- `DDART010-MIG-001`: missing registry or unrecoverable original payload is unresolved unless a separately approved migration rule permits an explicit empty registry.
- `DDART010-MIG-002`: preserve the source contract hash as provenance but withhold the target until its digest is recomputed under the owner-approved target payload contract.

## Approval and execution ledger

| Gate | Status |
|---|---|
| Owner decision on DD-ART-007 | Pending |
| Owner decision on DD-ART-008 | Pending |
| Owner decision on DD-ART-009 | Pending |
| Owner decision on DD-ART-010 | Pending |
| Owner-reported rules-v5 local validation on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` | Passed: directory-manifest tests 7/7, migration 33/33, integration 30/30, repository unit tests 83/83, Python compilation, Schema validator 68/68, candidate fixtures 83/83, semantic cases 16/16, trace rows 125; not GitHub Actions evidence |
| Directory-manifest fail-closed tests | Historical 7/7 on `0799dada`; owner reports 8/8 including provisional golden-vector test on pre-sync HEAD `9bebbdf`; local evidence only |
| Directory-manifest provisional golden vector | Owner reports exact-byte/hash vector test passed on pre-sync HEAD `9bebbdf` as part of directory-manifest 8/8; vector remains `provisional_not_normative` and does not settle numeric domain, digest scope, or cross-language ordering |
| Rules-v6 MIG-015 TEC hash/registry guard and tests | Owner reports migration regression 36/36 and full unit suite 87/87 passed on pre-sync HEAD `9bebbdf`; local evidence only, not GitHub Actions |
| MIG-010 source-root symlink guard | Owner reports regression suite passed 36/36 on pre-sync HEAD `9bebbdf`; post-sync merge HEAD still requires revalidation |
| Artifact Schema symlink enum vs helper policy | Mismatch found; DD-ART-008 decision required |
| Historical v1.3 source baseline and compatibility run | Unavailable / unverified |
| Actual filesystem directory-manifest verification | Not implemented |
| Transaction/commit/rollback verification | Not implemented; `commit_allowed=false` |

The matrix is intended to guide implementation and review without pre-empting normative approval.


## Follow-up static review — 2026-10-24

- Exact revision for the owner-reported local test run: `d4424f2012f6ec95e089019c10afb1fa95b6d619`. Reported results: directory-manifest 7/7, migration regression 36/36, integration 30/30, full unit tests 86/86, Python compilation passed, and Schema validation 68/68 checks, 83/83 candidate Fixture outcomes, 16/16 semantic cases, 125 trace rows.
- Actions Run [#39978741584](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39978741584) is `failure`, but the job has no recorded steps and the run has no artifact. This is not evidence that the tests themselves failed; it is also not passing CI evidence.
- A provisional directory-manifest golden vector and unit test have been added in a follow-up patch. They have **not** been executed on the resulting new HEAD. The vector is a regression snapshot for current implementation bytes, not an approved normative serialization contract.
- The numeric domain for `size_bytes`, cross-language ordering of normalized paths, and the Schema/helper symlink mismatch remain open under DD-ART-008. No Schema constraints, historical hashes, or decision approvals were changed. `commit_allowed=false` remains mandatory.


## Follow-up owner-reported verification and synchronization — 2026-10-24

The owner reports the following results on exact pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a`: directory-manifest 8/8, migration regression 36/36, integration 30/30, full unit tests 87/87, Python compilation passed, Schema validator 68/68, candidate Fixtures 83/83, semantic cases 16/16, trace rows 125. The report is outside the repository in a `%TEMP%\schema-validation-pr6-*` directory. Two such directories remain because recursive deletion was denied. The post-sync merge commit requires a fresh run.

Actions Run [#40013524904](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40013524904) failed before a runner or step was recorded and has no artifact; it is not a code-level test failure and is not passing CI evidence. The main-branch commit `d6143c2` independently notes runner allocation failure. The exact infrastructure/account-policy cause remains unresolved.

The [DD-ART-008 decision-options comparison](schema-v1.4.3.7-dd-art-008-decision-options-2026-10-24.md) now compares serialization/numeric-domain, path-ordering, digest-scope, and symlink-policy alternatives. It is a proposal, not an approval. DD-ART-007 through DD-ART-010 remain pending; `commit_allowed=false` remains mandatory.


## Post-sync execution boundary — 2026-10-24

The owner-reported local pass is for pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a`. Main was then merged into the PR branch by two-parent commit `0f65b17d066126b5a5174230856df05e276c2a05`; the final branch has a documentation-only follow-up. Re-run the full suite on the final exact HEAD before describing the synchronized branch as verified.

Actions Run [#40016709849](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40016709849) for `0f65b17` and Run [#40014204997](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40014204997) for main `d6143c2` both failed before runner assignment, with no recorded steps or artifacts. These are not code-level test failures and not passing CI evidence. The runner-allocation root cause remains unresolved.

DD-ART-008 options remain proposals only. No numeric constraint, symlink enum, digest preimage, or historical hash has been changed.


## Workflow-contract test follow-up — 2026-10-24

The test that covers the candidate validation workflow is now named `test_schema_ci_builds_and_uploads_uv_eft_bundle` in commit [`11d5637`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/11d56378f152f0db12f3b1758b1659decf7f2760). It checks PR-head checkout, report provenance (including run ID, attempt, validator SHA-256 and traceability CSV SHA-256), the `run_record_chain.py` build step, upload action/name/path, `if-no-files-found: error`, retention, and the independent Mathematica-script exclusion.

The owner reports the targeted test, full unit suite 87/87, and `git diff --check` passed before the remote commit; associated local results are directory-manifest 8/8, migration 36/36, integration 30/30, Python compilation, UV–EFT bundle 22 records/0 errors/0 warnings (human review pending), and Schema validation 68/68 checks, 83/83 candidate Fixture outcomes, 16/16 semantic cases, 125 trace rows. These are local owner-reported results, not GitHub Actions evidence. The desktop diff was not independently available and the local run preceded `11d5637`; rerun at the exact committed tree after syncing the desktop checkout.

Actions Run [#40020290127](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40020290127) failed before any runner step and produced no artifact. The four historical v1.4.3.6 Fixture differences remain. DD-ART-007–010 remain pending owner approval; `commit_allowed=false` remains mandatory.
