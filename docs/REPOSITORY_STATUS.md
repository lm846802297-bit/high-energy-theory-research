# Repository status

**As of 2026-10-23. Status: development / candidate; no formal Schema release.**

## Current state

| Area | State |
|---|---|
| Research Skill design | v1.6.5 baseline retained; v1.6.6 Artifact-identity clarification remains a candidate |
| Schema package | v1.4.3.7 candidate; 25 schema entry points and 83 indexed fixture IDs |
| Normative decisions | DD-ART-007 through DD-ART-010 pending explicit owner approval |
| Fixture index | Canonical index is version-matched to v1.4.3.7 candidate; inherited v1.4.3.6 expectations remain separately preserved |
| Cross-record validation | Prototype available; bounded semantic checks implemented |
| Migration | Rules-v6 source-aware prototype; full Draft 2020-12 target validation, RFC 8785 JCS target digests, MIG-014 dependent-reference withholding, MIG-015 Task Execution Contract hash/registry withholding, explicit input-root symlink rejection, and fail-closed staging for incomplete source snapshots. Rules-v5 validation was owner-reported passing on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` (7/7 directory-manifest, 33/33 migration, 30/30 integration, 83/83 unit tests, compilation, Schema validator 68/68, fixtures 83/83, semantic cases 16/16, trace rows 125); rules-v6 changes/tests not yet run; GitHub Actions unverified; staging-only, `commit_allowed=false` |
| Historical v1.3 compatibility | Unverified; original v1.3 source bundle/corpus unavailable |
| Requirement/test traceability | CSV traceability data and imported audit reports included; report snapshots are SHA/time scoped |
| Skill runtime | Initial instruction and reference scaffold added; not yet a complete automated research agent |
| Scientific validation | Not implemented; no physics result is certified by this repository |

## Validation evidence and remaining gates

The owner reports that the following rules-v5 checks ran locally on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` (Python version for this run not separately recorded). These results predate the rules-v6 MIG-015 code change:

- Directory-manifest tests: 7/7 passed.
- Migration regression tests: 33/33 passed.
- Integration tests: 30/30 passed.
- Full `tests/unit` suite: 83/83 passed.
- Python compilation: passed.
- Full Schema validator: 68/68 checks, 83/83 candidate fixture outcomes, 16/16 semantic cases, and 125 trace rows passed.

The new MIG-014 regression test `test_valid_claim_is_withheld_when_referenced_plan_fails_target_schema` passed. The Schema report was saved in a temporary directory rather than replacing the checked-in historical `schema/v1.4.3.7/audit/validation-report.json`. See `schema/v1.4.3.7/audit/current-head-test-execution-2026-10-23.md`.

**Current acceptance wording:** The rules-v5 candidate implementation passed the owner-reported local validation on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. The subsequent rules-v6 MIG-015 and source-root symlink changes have not yet been execution-verified. GitHub Actions is unverified for this phase; this is not a claim that GitHub Actions has passed.

These results verify the available local candidate test scope. They do **not** establish compatibility with the absent historical v1.3 source corpus, byte-for-byte lineage of the unavailable v1.4.3.6 archive, complete cross-record/state-machine semantics, scientific correctness, or transaction safety. Four legacy Fixture Index expectations remain separately recorded as compatibility drift. `commit_allowed=false` remains mandatory.

## Latest static review follow-up

A static review found that `directory_manifest.py` could discard extra FileEntry keys before hashing and accepted an `allow_symlinks=True` argument despite lacking filesystem-root verification. The helper now rejects non-exact FileEntry key sets and explicitly rejects `allow_symlinks=True`. The owner reports that the new directory-manifest tests passed 7/7, and the full local suites passed on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. These results are local evidence only, not a passing GitHub Actions run. DD-ART-008 remains pending approval; filesystem traversal and byte-for-byte directory verification are still unimplemented.

## Current rules-v6 verification boundary

The migration code and mapping contract have since advanced to `v1.4.3.7-migration-rules-6`, with MIG-015 blocking Task Execution Contract migration when the alternative-identity registry is missing or the source contract hash has not been revalidated under an owner-approved payload rule. Two Task Execution Contract tests, one source-root symlink test, and the contract-rule assertion were added. **The rules-v6 code and tests have not yet been run locally.** Do not carry forward the rules-v5 passing counts as proof of rules-v6 behavior. The Artifact Schema/helper symlink mismatch is also recorded for DD-ART-008 review; no normative Schema change was made.

## Release gates

1. Obtain explicit owner decisions on DD-ART-007 through DD-ART-010.
2. Supply and hash the exact historical v1.3 source bundle and representative/complete source records; run the compatibility procedure in schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. Keep migration staging-only until all references and target records validate, unresolved items are zero, and transactional commit/rollback safeguards exist. Do not change commit_allowed=false to bypass these gates.
4. Re-run the local verification suites after any subsequent code or schema changes; retain the report outside the repository's historical snapshot and record the exact tested commit.
5. Expand semantic/state-machine coverage and test actual filesystem manifests.
6. Complete normative schema coverage and define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.
