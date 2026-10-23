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
| Migration | Rules-v4 source-aware prototype; JSON/YAML inventory, duplicate-key rejection, manifest/schema SHA checks, typed-ID collision checks, target-enum/time validation, full Draft 2020-12 target validation, RFC 8785 JCS target digests, mapping provenance, and fail-closed staging that blocks all target writes for incomplete source snapshots; unresolved/schema-invalid records are withheld; implementation and tests unexecuted; dry-run/staging only, commit_allowed=false |
| Historical v1.3 compatibility | Unverified; original v1.3 source bundle/corpus unavailable |
| Requirement/test traceability | CSV traceability data and imported audit reports included; report snapshots are SHA/time scoped |
| Skill runtime | Initial instruction and reference scaffold added; not yet a complete automated research agent |
| Scientific validation | Not implemented; no physics result is certified by this repository |

## Validation evidence and CI boundary

The static review in `schema/v1.4.3.7/audit/static-schema-migration-review-2026-10-23.md` records the rules-v4 target-validation and JCS changes, incomplete-snapshot staging guard, the proposed `$id` policy, and unresolved schema-contract questions. The migration contract binds target validation and JCS semantics as MIG-012/MIG-013. The compatibility/test matrix is in `docs/governance/schema-v1.4.3.7-decision-compatibility-test-matrix.md`. Regression tests were added but not executed; this review did not run a migration or CI.

The repository has historical green software-test results for pre-integration SHAs, including the candidate schema suite and migration unit tests. Those results remain valid only for their recorded commits.

The latest inspected PR #6 workflow run is [#39943181897](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39943181897) for candidate HEAD `a180a224a7b1d7bf53bc457e44f36baf5fe48b72`. It failed before any workflow step was recorded: the job had no assigned runner and zero steps, so it produced no test result or artifact. The earlier manual dispatch [#39898913319](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39898913319) was blocked by account-level billing/payment or spending-limit status. The governance-fix branch remains unvalidated; no current-HEAD test pass is claimed.

## Release gates

1. Obtain explicit owner decisions on DD-ART-007 through DD-ART-010.
2. Supply and hash the exact historical v1.3 source bundle and representative/complete source records; run the compatibility procedure in schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. Keep migration staging-only until all references and target records validate, unresolved items are zero, and transactional commit/rollback safeguards exist. Do not change commit_allowed=false to bypass these gates.
4. Run the full workflow on the final candidate HEAD and inspect its artifacts; a historical green run cannot substitute for current CI.
5. Expand semantic/state-machine coverage and test actual filesystem manifests.
6. Complete normative schema coverage and define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.
