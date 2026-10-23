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
| Migration | Rules-v4 source-aware prototype; JSON/YAML inventory, duplicate-key rejection, manifest/schema SHA checks, typed-ID collision checks, target-enum/time validation, full Draft 2020-12 target validation, RFC 8785 JCS target digests, mapping provenance, and fail-closed staging that blocks all target writes for incomplete source snapshots; owner-reported rules-v4 local validation passed on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`; rules-v5 dependent-reference fix is awaiting rerun; dry-run/staging only, `commit_allowed=false` |
| Historical v1.3 compatibility | Unverified; original v1.3 source bundle/corpus unavailable |
| Requirement/test traceability | CSV traceability data and imported audit reports included; report snapshots are SHA/time scoped |
| Skill runtime | Initial instruction and reference scaffold added; not yet a complete automated research agent |
| Scientific validation | Not implemented; no physics result is certified by this repository |

## Validation evidence and remaining gates

The owner reports that the following checks ran locally under Python 3.12.14 on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`:

- Migration regression tests: 32/32 passed.
- Integration tests: 30/30 passed, including `test_30_validation_ids_resolve_but_invalid_targets_are_withheld`.
- Full `tests/unit` suite: 75/75 passed.
- Python compilation: passed.
- Full Schema validator: 68/68 checks, 83/83 candidate fixture outcomes, 16/16 semantic cases, and 125 trace rows passed.

The validator initially encountered a Windows default-GBK decoding error; it passed when rerun in UTF-8 mode. The resulting report was saved in a temporary directory rather than replacing the checked-in historical `schema/v1.4.3.7/audit/validation-report.json`. The historical report is intentionally not presented as evidence from this local run. See `schema/v1.4.3.7/audit/current-head-test-execution-2026-10-23.md`.

The local results verify the rules-v4 candidate test scope. A later rules-v5 change now withholds migrated records that reference a Validation Plan/Activity that fails target validation; that new code and regression test still require local execution. The previous results do **not** establish compatibility with the absent historical v1.3 source corpus, byte-for-byte lineage of the unavailable v1.4.3.6 archive, complete cross-record/state-machine semantics, scientific correctness, or transaction safety. Four legacy Fixture Index expectations remain separately recorded as compatibility drift.

## Release gates

1. Obtain explicit owner decisions on DD-ART-007 through DD-ART-010.
2. Supply and hash the exact historical v1.3 source bundle and representative/complete source records; run the compatibility procedure in schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. Keep migration staging-only until all references and target records validate, unresolved items are zero, and transactional commit/rollback safeguards exist. Do not change commit_allowed=false to bypass these gates.
4. Re-run the local verification suites after any subsequent code or schema changes; retain the report outside the repository's historical snapshot and record the exact tested commit.
5. Expand semantic/state-machine coverage and test actual filesystem manifests.
6. Complete normative schema coverage and define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.
