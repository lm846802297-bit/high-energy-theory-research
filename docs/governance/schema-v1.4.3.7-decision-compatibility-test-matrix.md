# Schema v1.4.3.7 — DD-ART-007–010 Compatibility and Test Matrix

**Status: review aid only.** This matrix does not approve any normative decision. The four recommendations remain pending owner approval. The matrix separates tests that can be implemented now from tests whose expected normative behavior depends on the owner decision or unavailable historical source data.

## Summary

| Decision | Candidate recommendation | Compatibility impact | Required tests | Current evidence / gate |
|---|---|---|---|---|
| DD-ART-007 | Require `artifact_storage_kind: file|directory`; never infer it from extension, URI, or artifact type | Legacy records may omit the field; migrate only from source evidence, otherwise quarantine for review | Schema: missing field rejected; enum outside file/directory rejected. Migration: explicit source evidence maps; absent/contradictory evidence is unresolved. Semantic: file and directory hashing policies cannot be interchanged | Recommendation only; owner approval pending; historical corpus unavailable |
| DD-ART-008 | Normalize relative paths to Unicode NFC and POSIX separators; reject traversal, absolute paths, NFC collisions and disallowed symlinks; hash deterministically serialized normalized manifests with SHA-256 | Existing hashes may change if path normalization, entry ordering, or serialization changes; do not overwrite historical hashes before approval | Unit: NFC-equivalent collision; `..` and absolute paths; backslash rejection; deterministic ordering; exact FileEntry key set; symlink rejection; golden canonical bytes/hash. Integration: compare manifest entries with actual filesystem bytes and directory tree | Static review found the helper previously discarded extra FileEntry keys and exposed an `allow_symlinks` flag that did not enable safe symlink verification. The helper now rejects missing/extra keys and explicitly rejects `allow_symlinks=True`; the owner reports 7/7 directory-manifest tests passed on rules-v5 code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. Filesystem traversal/byte verification remains unimplemented. The later rules-v6 migration changes do not validate or implement that filesystem verification. Owner approval pending |
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
- `DDART008-HASH-003`: add a dedicated directory-manifest canonical UTF-8 byte/hash golden vector, separate from the migration target-record JCS vector.

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
| Directory-manifest fail-closed tests | Owner reports 7/7 passed on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` |
| Directory-manifest JCS numeric-domain/path-ordering golden vectors | Static gap identified; not implemented or executed |
| Rules-v6 MIG-015 TEC hash/registry guard and new tests | Added after the rules-v5 validation above; not yet executed locally |
| MIG-010 source-root symlink guard | Fixed in code; regression test added, but not yet executed locally |
| Artifact Schema symlink enum vs helper policy | Mismatch found; DD-ART-008 decision required |
| Historical v1.3 source baseline and compatibility run | Unavailable / unverified |
| Actual filesystem directory-manifest verification | Not implemented |
| Transaction/commit/rollback verification | Not implemented; `commit_allowed=false` |

The matrix is intended to guide implementation and review without pre-empting normative approval.
