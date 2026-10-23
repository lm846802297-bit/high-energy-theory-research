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
| Migration | Rules-v5 source-aware prototype; full Draft 2020-12 target validation, RFC 8785 JCS target digests, MIG-014 dependent-reference withholding, and fail-closed staging for incomplete source snapshots; owner-reported local validation passed on code HEAD `587587ae0b114d9624bfb7b270c8754b7e9cbef0` (33/33 migration, 30/30 integration, 76/76 unit tests; Schema validator 68/68, 83/83 candidate fixtures, 16/16 semantic cases, 125 trace rows); GitHub Actions temporarily excluded from this phase's acceptance and to be supplemented when runners are available; dry-run/staging only, `commit_allowed=false` |
| Historical v1.3 compatibility | Unverified; original v1.3 source bundle/corpus unavailable |
| Requirement/test traceability | CSV traceability data and imported audit reports included; report snapshots are SHA/time scoped |
| Skill runtime | Initial instruction and reference scaffold added; not yet a complete automated research agent |
| Scientific validation | Not implemented; no physics result is certified by this repository |

## Validation evidence and remaining gates

The owner reports that the following checks ran locally under Python 3.12.14 on code HEAD `587587ae0b114d9624bfb7b270c8754b7e9cbef0`:

- Migration regression tests: 33/33 passed.
- Integration tests: 30/30 passed.
- Full `tests/unit` suite: 76/76 passed.
- Python compilation: passed.
- Full Schema validator: 68/68 checks, 83/83 candidate fixture outcomes, 16/16 semantic cases, and 125 trace rows passed.

The new MIG-014 regression test `test_valid_claim_is_withheld_when_referenced_plan_fails_target_schema` passed. The Schema report was saved in a temporary directory rather than replacing the checked-in historical `schema/v1.4.3.7/audit/validation-report.json`. See `schema/v1.4.3.7/audit/current-head-test-execution-2026-10-23.md`.

**Current acceptance wording:** The current candidate implementation's local validation has passed. GitHub Actions is temporarily excluded from this phase's acceptance and will be supplemented when runners are available. This is not a claim that GitHub Actions has passed.

These results verify the available local candidate test scope. They do **not** establish compatibility with the absent historical v1.3 source corpus, byte-for-byte lineage of the unavailable v1.4.3.6 archive, complete cross-record/state-machine semantics, scientific correctness, or transaction safety. Four legacy Fixture Index expectations remain separately recorded as compatibility drift. `commit_allowed=false` remains mandatory.

## Latest static review follow-up

A static review found that `directory_manifest.py` could discard extra FileEntry keys before hashing and accepted an `allow_symlinks=True` argument despite lacking filesystem-root verification. The helper now rejects non-exact FileEntry key sets and explicitly rejects `allow_symlinks=True`; `tests/unit/test_directory_manifest.py` was added. These latest helper changes and tests have not yet been executed locally. The previous rules-v5 passing results apply to code HEAD `587587ae0b114d9624bfb7b270c8754b7e9cbef0`, before this helper patch. Re-run the new directory-manifest tests and full local validation against the latest branch HEAD before treating the current tree as locally verified. DD-ART-008 remains pending approval; filesystem traversal and byte-for-byte directory verification are still unimplemented.

## Release gates

1. Obtain explicit owner decisions on DD-ART-007 through DD-ART-010.
2. Supply and hash the exact historical v1.3 source bundle and representative/complete source records; run the compatibility procedure in schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. Keep migration staging-only until all references and target records validate, unresolved items are zero, and transactional commit/rollback safeguards exist. Do not change commit_allowed=false to bypass these gates.
4. Re-run the local verification suites after any subsequent code or schema changes; retain the report outside the repository's historical snapshot and record the exact tested commit.
5. Expand semantic/state-machine coverage and test actual filesystem manifests.
6. Complete normative schema coverage and define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.
