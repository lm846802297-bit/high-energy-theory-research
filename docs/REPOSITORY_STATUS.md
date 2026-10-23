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
| Migration | Source-aware validation_ids resolver has positive/negative synthetic tests; dry-run/staging only, commit_allowed=false |
| Historical v1.3 compatibility | Unverified; original v1.3 source bundle/corpus unavailable |
| Requirement/test traceability | CSV traceability data and imported audit reports included; report snapshots are SHA/time scoped |
| Skill runtime | Initial instruction and reference scaffold added; not yet a complete automated research agent |
| Scientific validation | Not implemented; no physics result is certified by this repository |

## Validation evidence and CI boundary

The repository has historical green software-test results for pre-integration SHAs, including the candidate schema suite and migration unit tests. Those results remain valid only for their recorded commits.

The latest main HEAD inspected after the project-registry updates was d30734fa078a49262c043eb817479dc680d23ee5. Its latest workflow run, https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39895811558, failed before any workflow step was recorded; the job had no assigned runner name. This is not evidence of a code-test failure, but it also is not a passing CI result for current main. The governance-fix branch requires its own validation when a runner is available.

## Release gates

1. Obtain explicit owner decisions on DD-ART-007 through DD-ART-010.
2. Supply and hash the exact historical v1.3 source bundle and representative/complete source records; run the compatibility procedure in schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. Keep migration staging-only until all references and target records validate, unresolved items are zero, and transactional commit/rollback safeguards exist. Do not change commit_allowed=false to bypass these gates.
4. Run the full workflow on the final candidate HEAD and inspect its artifacts; a historical green run cannot substitute for current CI.
5. Expand semantic/state-machine coverage and test actual filesystem manifests.
6. Complete normative schema coverage and define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.
