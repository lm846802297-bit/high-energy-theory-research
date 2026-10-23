# Repository status

**As of 2026-10-24. Status: development / candidate; no formal Schema release.**

## Current state

| Area | State |
|---|---|
| Research Skill design | v1.6.5 baseline retained; v1.6.6 Artifact-identity clarification remains a candidate |
| Schema package | v1.4.3.7 candidate; 25 schema entry points and 83 indexed fixture IDs |
| Normative decisions | DD-ART-007 through DD-ART-010 pending explicit owner approval |
| Fixture index | Canonical index is version-matched to v1.4.3.7 candidate; inherited v1.4.3.6 expectations remain separately preserved |
| Cross-record validation | Prototype available; bounded semantic checks implemented |
| Migration | Rules-v6 source-aware prototype; MIG-012–015 target/reference/hash guards; staging-only with `commit_allowed=false`. Owner-reported local verification passed on pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a` (directory-manifest 8/8, migration 36/36, integration 30/30, unit 87/87, Python compilation, Schema 68/68, candidate Fixtures 83/83, semantic cases 16/16, trace rows 125). GitHub Actions runner allocation remains unresolved; the post-sync merge commit still requires full local revalidation. |
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

**Current acceptance wording:** The owner reports that the pre-sync PR HEAD `9bebbdf279fefba098fa237915ff71361103201a` passed the complete local candidate scope: directory-manifest 8/8, migration 36/36, integration 30/30, unit 87/87, Python compilation, Schema validator 68/68, candidate fixtures 83/83, semantic cases 16/16, and trace rows 125. This is owner-reported local evidence, not GitHub Actions evidence. The synchronized merge commit has not yet been locally validated.

These results verify the available local candidate test scope. They do **not** establish compatibility with the absent historical v1.3 source corpus, byte-for-byte lineage of the unavailable v1.4.3.6 archive, complete cross-record/state-machine semantics, scientific correctness, or transaction safety. Four legacy Fixture Index expectations remain separately recorded as compatibility drift. `commit_allowed=false` remains mandatory.

## Latest static review follow-up

A static review found that `directory_manifest.py` could discard extra FileEntry keys before hashing and accepted an `allow_symlinks=True` argument despite lacking filesystem-root verification. The helper now rejects non-exact FileEntry key sets and explicitly rejects `allow_symlinks=True`. The owner reports that the new directory-manifest tests passed 7/7, and the full local suites passed on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. These results are local evidence only, not a passing GitHub Actions run. DD-ART-008 remains pending approval; filesystem traversal and byte-for-byte directory verification are still unimplemented.

## Historical rules-v6 verification boundary (superseded by 2026-10-24 evidence)

The migration code and mapping contract have since advanced to `v1.4.3.7-migration-rules-6`, with MIG-015 blocking Task Execution Contract migration when the alternative-identity registry is missing or the source contract hash has not been revalidated under an owner-approved payload rule. Two Task Execution Contract tests, one source-root symlink test, and the contract-rule assertion were added. This paragraph records the earlier pre-validation state and is superseded by the owner-reported full local verification on pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a` below. The Artifact Schema/helper symlink mismatch is also recorded for DD-ART-008 review; no normative Schema change was made.

## Release gates

1. Obtain explicit owner decisions on DD-ART-007 through DD-ART-010.
2. Supply and hash the exact historical v1.3 source bundle and representative/complete source records; run the compatibility procedure in schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. Keep migration staging-only until all references and target records validate, unresolved items are zero, and transactional commit/rollback safeguards exist. Do not change commit_allowed=false to bypass these gates.
4. Re-run the local verification suites after any subsequent code or schema changes; retain the report outside the repository's historical snapshot and record the exact tested commit.
5. Expand semantic/state-machine coverage and test actual filesystem manifests.
6. Complete normative schema coverage and define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.

## Historical PR branch reconciliation — 2026-10-23 (superseded by 2026-10-24 synchronization)

At review time, GitHub PR #6 reports code-bearing HEAD `c69651858a9c0b6155242c25a4c09c1364284823`; the owner-reported local pass is for `0799dada7eaa8dcd08b8db2f2311a844335d7198`. GitHub's compare endpoint reports the tested SHA as an ancestor 41 commits behind the current PR HEAD. The current code-bearing branch includes rules-v6/MIG-015 and source-root-symlink changes, so the rules-v5 test counts do not validate the current branch.

Actions runs `39969213674` (tested SHA `0799...`) and `39976133434` (current code-bearing SHA `c696...`) both have a `failure` conclusion; the connector returned no usable step summaries or job logs. Neither is a passing CI record, and the available records do not establish a code-level test failure. See the [normalization and migration boundary review](schema/v1.4.3.7/audit/normalization-and-migration-boundary-review-2026-10-23.md) for the exact scope and remaining canonicalization gaps.

This review adds audit documentation only; it does not modify migration code or Schema semantics. PR #6 remains Open/Draft, DD-ART-007 through DD-ART-010 remain pending, and `commit_allowed=false` remains mandatory.


## Current HEAD verification and main synchronization — 2026-10-24

### Owner-reported local results (pre-sync HEAD)

The repository owner reports a clean desktop working tree before and after verification on exact pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a`:

- Directory-manifest tests: **8/8 passed**, including the provisional golden-vector test.
- Migration-reference regression tests: **36/36 passed**.
- Integration tests: **30/30 passed**.
- Full unit tests: **87/87 passed**.
- Python compilation: **passed**.
- Full Schema validator: **68/68 checks**, **83/83 candidate Fixture outcomes**, **16/16 semantic cases**, **125 trace rows**.

Four historical `1.4.3.6-candidate` Fixture expectation differences remain; no historical expectation or hash was rewritten. The golden vector remains `provisional_not_normative`.

The validator report was written outside the repository under the desktop environment's `%TEMP%\schema-validation-pr6-*` temporary directories. Two such directories remain because recursive deletion was denied. No repository files were deleted. The exact path for the `9bebbdf` report was not supplied in the handoff, so it is not reconstructed here.

### GitHub Actions diagnosis

Run [#40013524904](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40013524904) corresponds to `9bebbdf`; [#40016709849](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40016709849) corresponds to the synchronized merge commit `0f65b17`. Both report `failure` with `runner_id=0`, an empty runner name, no recorded steps, and no artifacts. The log endpoints return no stored log. The main-branch commit [`d6143c2`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/d6143c2aa15191ac8521e062d90860ba86713f00) independently records that Actions could not allocate a runner. The workflow YAML declares `runs-on: ubuntu-latest` and ordinary test steps; available evidence supports a runner-allocation/execution-infrastructure failure, but does not distinguish account billing/quota, repository/organization policy, or a GitHub-side incident. The connector could not read the Actions permission/settings endpoint, so the underlying cause remains unresolved. No workflow steps were skipped or weakened to manufacture a pass.

### Main-branch delta and sync method

At the start of this synchronization, current `main` was `d6143c2aa15191ac8521e062d90860ba86713f00`, with 12 main-only commits after common ancestor `2c4b443173f58a577cda7d3eb88d32c93fdf0643`. Those commits add the historical Higgs-portal v66 archive, update the RC-001 research record and project registry, and add the `artifacts/` navigation line to `README.md`. Tree comparison found only one shared changed leaf file: `README.md`; the artifact navigation line was merged with the PR's candidate-governance text.

The branch was synchronized by a two-parent merge commit rather than a rebase, preserving the PR history and avoiding a force-push. The candidate workflow retains its provenance checks and restores the main-branch UV–EFT pilot compile/build/artifact steps. The merge commit `0f65b17d066126b5a5174230856df05e276c2a05` has not yet been locally validated. The current follow-up changes only audit documents; run the complete validation suite on the final branch HEAD.

### DD-ART-008 decision status

The new [DD-ART-008 decision-options comparison](../governance/schema-v1.4.3.7-dd-art-008-decision-options-2026-10-24.md) compares numeric-domain, path-ordering, serialization-scope and symlink-policy alternatives. It is a review proposal only. No Schema semantics, historical hashes, or owner decisions were changed. DD-ART-007 through DD-ART-010 remain pending; `commit_allowed=false` remains mandatory.


### Follow-up after merge commit — 2026-10-24

Current branch head at the time of this audit update is a documentation-only follow-up on top of merge commit `0f65b17d066126b5a5174230856df05e276c2a05`. The schema/migration implementation and restored workflow steps are unchanged by this documentation follow-up. Nevertheless, the exact final branch HEAD should be used for the next full local validation run.

Actions Run [#40016709849](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40016709849) corresponds to merge commit `0f65b17`; the job again has `runner_id=0`, an empty runner name, an empty step list, and no artifact. This repeats the same pre-step runner-allocation failure after synchronizing main. The exact underlying account, repository/organization-policy, or GitHub-side cause remains unconfirmed.


## Follow-up — UV–EFT workflow contract test committed (2026-10-24)

- Test-contract commit: [`11d5637`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/11d56378f152f0db12f3b1758b1659decf7f2760).
- The remote test is now named `test_schema_ci_builds_and_uploads_uv_eft_bundle`. It checks PR-head checkout, validation-report provenance (run ID, attempt, validator hash and traceability CSV hash), the UV–EFT `run_record_chain.py` build step, artifact upload action/name/path, `if-no-files-found: error`, retention, and continued exclusion of `verify_pv_derivative_mathematica.wl`.
- The owner reports the targeted test, full unit suite (87/87), and `git diff --check` passed in the desktop worktree before the remote commit. The owner also reports directory-manifest 8/8, migration regression 36/36, integration 30/30, Python compilation, UV–EFT bundle 22 records/0 errors/0 warnings (human review pending), and Schema validation 68/68 checks, 83/83 candidate Fixture outcomes, 16/16 semantic cases and 125 trace rows. These are owner-reported local results, not independently reproduced here.
- The local run preceded commit `11d5637`; the exact committed tree has not yet received a fresh local run. The remote assertion contract was reconstructed from the owner's description because the desktop diff was not directly accessible. Synchronize the desktop branch and inspect the local-vs-remote diff before considering the test-fix handoff complete.
- Four historical v1.4.3.6 Fixture differences remain; no historical expectation or hash was rewritten. Four temporary directories remain outside the repository because deletion was blocked: `schema-validation-pr6-d442-*`, `schema-validation-pr6-9bebbdf-*`, `schema-validation-pr6-cb736-*`, and `uv-eFT-hard-derivative-bundle-cb736-*`.
- Actions Run [#40020290127](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40020290127) for `11d5637` failed before any step: `runner_id=0`, empty runner name, no steps, and no artifact. This is not evidence of a code-level test failure or a passing CI run.
- PR #6 remains Open / Draft / unmerged; Schema v1.4.3.7 remains `candidate` / `not_released`; `commit_allowed=false` remains mandatory.
