# Migration Transaction and Rollback Design Review

**Status: design review only — no transaction or commit implementation is authorized.** Schema v1.4.3.7 remains an unreleased candidate; `commit_allowed=false`.

## Current implementation boundary

The v1.3-to-v1.4 tool supports read-only source inventory, dry-run reporting, and isolated staging output. It does not implement an active-dataset pointer, atomic publication, transaction journal, writer lock, commit protocol, or rollback. The current staging output must not be treated as the active dataset. No migration has been run against the complete historical v1.3 corpus.

The latest code change adds full Draft 2020-12 target-schema validation and RFC 8785 target digests, but neither code nor tests have been executed in this review. Schema validation is necessary but not sufficient for a commit: cross-record constraints, source compatibility, and operational atomicity remain separate gates.

## Required transaction model

The following is a proposed state machine, not implemented behavior:

1. **SOURCE_SNAPSHOTTED** — identify a read-only source snapshot; hash every source byte; record the source manifest and migration-rule version.
2. **SOURCE_VALIDATED** — validate against the authentic v1.3 schemas and inventory all IDs, types, projects, fields, and references. Missing baseline evidence blocks progress.
3. **TARGET_STAGED** — write only to a new, empty staging directory outside the source tree. Every target has source provenance and a deterministic target digest.
4. **TARGET_VALIDATED** — validate every target against the full candidate JSON Schema, then run cross-record semantic validation over the entire staged graph. Any error or unresolved item blocks progress.
5. **REVIEW_APPROVED** — require an explicit, attributable approval tied to the exact source snapshot hash, candidate manifest hash, migration-rule version, validation report hash, and staged-dataset hash. An operator string alone is not approval.
6. **COMMIT_PREPARED** — acquire an exclusive writer lock; verify the active dataset has not changed since preparation; persist a journal containing the previous active pointer and the exact candidate pointer; ensure the staged dataset and journal are durable.
7. **COMMITTED** — atomically replace the active-dataset pointer or perform an equivalent storage-level atomic switch. Never overwrite individual active records in place and never delete the source snapshot.
8. **POST_COMMIT_VERIFIED** — read back the active pointer, verify the referenced dataset manifest and hashes, and record the committed revision. If verification fails, enter rollback.
9. **ROLLED_BACK** — atomically restore the previous active pointer from the durable journal; preserve both source and candidate datasets and all audit records. A rollback is a new state transition, not deletion of history.

## Mandatory failure behavior

- Any unresolved mapping, duplicate identity, source/target validation error, unapproved normative transformation, hash mismatch, or missing historical baseline blocks commit.
- A staging directory must be new and empty; a failed run must not reuse stale output.
- A retry must either reproduce the same canonical target hashes from the same source snapshot and rule version or report a determinism failure.
- A concurrent update to the active dataset between preparation and commit must invalidate the prepared transaction.
- A crash at any commit boundary must be recoverable from a durable journal and a single authoritative active pointer.
- Rollback restores the previous pointer and never destroys source history or the failed candidate.
- No `commit_allowed=true` state may be inferred merely from successful schema tests, a clean dry-run, or the existence of a staged directory.

## Required evidence before implementation can be enabled

1. The exact historical v1.3 archive and its SHA-256.
2. Passing target-schema and cross-record validation on a representative and then complete source corpus.
3. Repeat-run evidence showing identical RFC 8785 target digests for the same source snapshot and migration-rule version.
4. Failure-injection tests for disk/write errors, concurrent writers, interruption before and after pointer replacement, corrupted journal, failed post-commit verification, and rollback recovery.
5. A documented storage model specifying the active pointer, atomicity guarantees, durability/fsync expectations, lock semantics, and journal retention.
6. An owner-approved commit authorization procedure and audit identity.
7. A separately reviewed operational runbook and a dry-run rehearsal using a disposable dataset.

## Current disposition

Do not implement or enable a commit path in this PR. Keep `commit_allowed=false` hard-coded until the owner separately approves the transaction design and every prerequisite above has been evidenced. The absence of CI is not itself proof of a code defect, but it means the recent target-validation and digest changes remain unverified.
