# Schema v1.4.3.7 — Normalization and Migration Boundary Review

**Review type:** static source/document review; no code was changed and no test was run in this review.  
**Observed PR branch:** `fix/schema-governance-20261023`  
**Historical observed PR HEAD:** `c69651858a9c0b6155242c25a4c09c1364284823` (superseded by the 2026-10-24 main synchronization)  
**Status:** candidate-only; PR #6 remains Open/Draft and is not merged.

## 1. Revision and evidence boundary

At the time of the initial static review, the only local test summary available was for code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` (migration rules v5), and the PR HEAD was `c69651858a9c0b6155242c25a4c09c1364284823`. This historical revision comparison is superseded by the owner-reported 8/8 directory-manifest, 36/36 migration, 30/30 integration, 87/87 unit, compilation, and Schema validation pass on pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a`.

The current PR branch contains migration rules v6, including MIG-015 for Task Execution Contract (TEC) registry/hash withholding and a source-root symlink guard. These changes were not validated by the rules-v5 results. The owner later reported successful local verification of them on pre-sync HEAD `9bebbdf`; those results do not validate the subsequent synchronized merge commit `0f65b17` or the final documentation-only HEAD.

The GitHub Actions runs associated with `0799dada7eaa8dcd08b8db2f2311a844335d7198` and `c69651858a9c0b6155242c25a4c09c1364284823` are recorded as failed runs (run IDs `39969213674` and `39976133434`). The connector returned no step summaries or usable job logs for these runs. They are not passing CI evidence; the available records are also insufficient to attribute the conclusion to a code-level test failure.

The checked-in `schema/v1.4.3.7/audit/validation-report.json` correctly labels itself as a historical snapshot, with no reconstructed commit SHA or run ID. Do not overwrite that snapshot with a locally generated report.

## 2. Directory-manifest normalization

### Verified by source inspection

The current `schema/v1.4.3.7/tools/directory_manifest.py`:

- requires the exact `FileEntry` key set and rejects missing/extra keys;
- normalizes `relative_path` to Unicode NFC;
- rejects empty paths, absolute paths, drive-prefixed paths, backslashes, empty path segments, `.` and `..` segments;
- detects duplicate paths after NFC normalization;
- rejects symlinks and rejects `allow_symlinks=True` rather than implying that a manifest-only helper can verify link targets;
- validates file size/hash/null fields by entry type and sorts entries by normalized path;
- emits compact UTF-8 JSON and hashes those bytes with SHA-256.

The helper is deliberately not a filesystem walker: it does not prove that a supplied manifest matches the files and bytes on disk. That boundary must remain explicit.

### Open canonicalization-contract gaps

1. **JCS numeric domain.** The helper uses Python `json.dumps`, not a general RFC 8785 implementation. The `FileEntry.size_bytes` schema allows any non-negative integer (no maximum), and the helper likewise accepts arbitrarily large Python integers. Integers outside the IEEE-754 safe-integer domain can produce different canonical representations across runtimes. Before claiming interoperable RFC 8785 behavior, either define and enforce a safe numeric domain (for non-negative byte sizes, at most `2^53 - 1`) or use a tested RFC 8785 implementation that rejects values outside its supported numeric domain. Any schema-level bound is a candidate-contract change and must be reviewed under DD-ART-008 rather than silently introduced.

2. **Path-array ordering.** `out.sort(key=lambda x: x["relative_path"])` uses Python's Unicode code-point ordering. The contract says to sort by normalized path but does not define the cross-language comparison order. Code-point ordering can differ from UTF-16 code-unit ordering for supplementary-plane characters; for example, U+1F600 and U+E000 can sort differently. Specify the comparison rule and add a golden vector containing such paths.

3. **Directory-manifest golden evidence.** The existing `target-digest-jcs-v1.golden.json` and its unit test validate a migration target-record digest, not the directory-manifest serialization profile. Directory-manifest tests cover stable ordering, NFC collision, path rejection, exact keys and symlink rejection, but do not compare canonical manifest bytes and SHA-256 against a dedicated golden vector. Add this before treating the directory hash as a cross-language contract.

4. **Schema/helper symlink mismatch.** The Artifact Schema permits `entry_type: "symlink"`, while the helper rejects every symlink entry. This is already a known DD-ART-008 mismatch. Keep it open until the owner approves the normative policy; do not change the Schema to make the test suite appear consistent.

These are static contract findings, not observed test failures. The rules-v5 local pass does not cover these untested edge cases.

## 3. Migration safety boundary

The current branch's migration source implements the following conservative controls:

- checks all 25 candidate schema files against the manifest and validates each schema under Draft 2020-12;
- validates each provisional target with a full Draft 2020-12 validator and format checker before target emission;
- uses the pinned `rfc8785` implementation for target-record canonical digests, separate from the directory-manifest helper;
- quarantines unknown fields and records unresolved mappings instead of silently preserving or discarding them;
- resolves legacy `validation_ids` only with same-project, unique source evidence, and withholds a dependent Claim if its referenced Validation Plan/Activity does not produce a valid target;
- blocks target staging for empty, incomplete/skipped or symlink-containing source snapshots, and rejects staging inside the source tree or into a non-empty output directory;
- reports `commit_allowed: false` and keeps migration staging-only.

Rules v6 adds MIG-015. A TEC with a missing `alternative_identity_methods` registry is withheld; a source `contract_hash` mapped to `contract_sha256` is not treated as a verified target digest while the owner-approved DD-ART-010 payload rule is unresolved. The added TEC and source-root-symlink regression tests are present in the current branch, but have not been execution-verified on the current branch HEAD.

The migration remains a prototype. It does not implement an atomic transaction, active-dataset pointer switch, transaction journal, writer lock or rollback. The authentic historical v1.3 source bundle and corpus are unavailable, so historical compatibility remains unverified. `commit_allowed=false` must not be relaxed.

## 4. Governance and documentation state

- Schema v1.4.3.7 remains a candidate; the manifest is not a release approval.
- DD-ART-007 through DD-ART-010 remain recommendations pending explicit owner decisions.
- The four inherited v1.4.3.6 Fixture expectation differences remain compatibility drift; the unavailable source archive prevents byte-for-byte lineage verification.
- Schema identifier/version questions, incomplete normative field coverage, the `completed_at`/`finished_at` relationship, and bounded cross-record/state-machine coverage remain release gates.
- Local results reported for `0799dada7eaa8dcd08b8db2f2311a844335d7198` are: directory-manifest tests 7/7, migration tests 33/33, integration tests 30/30, full unit tests 83/83, Python compilation passed, Schema validator 68/68, candidate fixtures 83/83, semantic cases 16/16 and 125 trace rows. These are owner-reported local results for rules v5 only, not GitHub Actions results and not evidence for rules v6.

## 5. Required next steps

1. Synchronize the desktop checkout to the actual current PR HEAD and confirm `git rev-parse HEAD` before running or recording tests.
2. Run the migration regression suite (including the new MIG-015 and source-root-symlink tests), directory-manifest tests, integration tests, full unit suite, Python compilation and full Schema validator on that exact SHA.
3. Add a directory-manifest canonical-byte/hash golden vector, a numeric-boundary case, and a Unicode path-ordering case; define the serialization/sort contract before changing historical digests.
4. Reconcile the Schema/helper symlink policy only after DD-ART-008 is approved.
5. Keep PR #6 open and Draft until current-HEAD evidence and owner decisions are complete. Do not merge or release; retain `commit_allowed=false`.


## Addendum — owner-reported validation and provisional vector follow-up (2026-10-24)

### Exact local evidence boundary

The owner reports that local checks ran on PR HEAD `d4424f2012f6ec95e089019c10afb1fa95b6d619` and passed: directory-manifest tests 7/7, migration regression tests 36/36, integration tests 30/30, full unit tests 86/86, Python compilation, and the full Schema validator (68/68 checks, 83/83 candidate Fixture outcomes, 16/16 semantic cases, 125 trace rows). These results are owner-reported and apply only to that SHA.

GitHub Actions Run [#39978741584](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39978741584) has conclusion `failure`; its job record has no steps and the run has no artifacts. This is not a passing CI result and does not establish a code-level test failure.

### Provisional directory-manifest vector

A separate vector, `schema/v1.4.3.7/migrations/directory-manifest-candidate-v0.golden.json`, and a unit test now capture the current helper's exact UTF-8 bytes and SHA-256 for NFC normalization and a Unicode-ordering-discriminating input. This is intentionally labelled `provisional_not_normative`. The vector and test have not been executed on the new commit that adds them; the prior results above do not validate this follow-up patch.

The helper's runtime behavior and historical hashes are unchanged by the comment-only clarification. No Schema constraint, symlink policy, or owner decision was changed. The vector does not claim RFC 8785/JCS interoperability and does not settle the safe-integer domain or cross-language path-ordering contract. The Artifact Schema still allows `entry_type: "symlink"` while the helper rejects symlink entries; leave this mismatch open until DD-ART-008 is explicitly approved.


## Follow-up — exact pre-sync HEAD and decision comparison (2026-10-24)

The repository owner reports local validation on exact pre-sync HEAD `9bebbdf279fefba098fa237915ff71361103201a`: directory-manifest 8/8, migration regression 36/36, integration 30/30, full unit tests 87/87, Python compilation, Schema validator 68/68, candidate Fixtures 83/83, semantic cases 16/16, and 125 trace rows. The new provisional golden-vector test is included in the 8/8 result. The working tree was clean before and after validation.

The Schema report was written outside the repository under the desktop environment's `%TEMP%\schema-validation-pr6-*` temporary directories. Two directories remain because recursive deletion was denied; no repository files were deleted. The exact `9bebbdf` path was not supplied and is not guessed.

Actions Run [#40013524904](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40013524904) for pre-sync HEAD `9bebbdf` and Run [#40016709849](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40016709849) for merge commit `0f65b17` both have `failure`, `runner_id=0`, empty runner name, no recorded steps, and no artifact. The log endpoints returned no stored log. Main commit [`d6143c2`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/d6143c2aa15191ac8521e062d90860ba86713f00) also records that Actions could not allocate a runner. The exact account/organization/GitHub-side cause is not visible through the available API. This is runner-allocation evidence, not a code-test failure or a passing CI run.

The branch was synchronized by a two-parent merge commit, not a rebase. Only `README.md` was changed on both sides since the common ancestor; the main branch's `artifacts/` navigation line is retained alongside the PR's candidate-governance changes. The PR workflow's main-branch UV–EFT pilot compile/build/artifact steps are restored while retaining the candidate provenance checks. The post-sync merge commit has not yet been locally validated.

For owner review, see [DD-ART-008 decision options](../../../docs/governance/schema-v1.4.3.7-dd-art-008-decision-options-2026-10-24.md). No normative choice is made. The numeric domain, cross-language path comparator, digest payload scope and symlink policy remain open under DD-ART-008; `commit_allowed=false` remains mandatory.


## Current synchronized-branch status — 2026-10-24

- Current main at synchronization: `d6143c2aa15191ac8521e062d90860ba86713f00`.
- Merge commit: `0f65b17d066126b5a5174230856df05e276c2a05`; compare against current main reported 225 commits ahead and 0 behind, with 37 PR-specific changed files.
- The only shared changed leaf path from the old common ancestor was `README.md`; the `artifacts/` navigation line was reconciled manually. The PR workflow's main-branch UV–EFT pilot compile/build/artifact steps were restored without removing the candidate provenance gate.
- The owner-reported local test pass remains scoped to pre-sync HEAD `9bebbdf`. No local full-suite result is yet available for merge commit `0f65b17` or the current documentation-only follow-up HEAD.
- Actions Run [#40016709849](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40016709849) failed before any runner or test step was recorded. The same runner-allocation failure appears on main Run [#40014204997](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40014204997). The exact infrastructure/account-policy cause remains unresolved.
- DD-ART-008 options are compared in [the decision-options document](../../../docs/governance/schema-v1.4.3.7-dd-art-008-decision-options-2026-10-24.md). No normative decision is implied; `commit_allowed=false` remains mandatory.


## Test-contract follow-up — 2026-10-24

The workflow-contract unit test was updated and committed as [`11d5637`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/11d56378f152f0db12f3b1758b1659decf7f2760). Its remote implementation checks the PR-head checkout, evidence provenance including traceability CSV hash, UV–EFT build command, upload action/name/path, `if-no-files-found: error`, retention, and exclusion of the independent Mathematica script.

The owner reports a targeted-test pass, full unit suite 87/87, and `git diff --check` pass before the remote commit. The associated local run also reports directory-manifest 8/8, migration regression 36/36, integration 30/30, Python compilation, UV–EFT bundle 22 records/0 errors/0 warnings with human review pending, and Schema validation 68/68 checks, 83/83 candidate Fixture outcomes, 16/16 semantic cases, 125 trace rows. These results are owner-reported and are not CI evidence. Since the local run preceded `11d5637` and the desktop diff was not independently available, repeat the targeted and full unit tests against the exact committed branch tree after desktop synchronization.

Actions Run [#40020290127](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/40020290127) failed before runner allocation/steps, with `runner_id=0`, empty runner name, and no artifact. The runner-allocation root cause remains unresolved. Four temporary directories remain outside the repository because cleanup was blocked; no historical Fixture expectations or hashes were rewritten. DD-ART-008 and the other owner decisions remain pending; `commit_allowed=false` remains mandatory.

## Exact-head workflow-test review — 2026-10-24

The desktop branch is synchronized through `46c4cf2e65ce902e4f39a933a3284a6d9553636d`. A local test-only commit [`e1ef2da`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/e1ef2da44c77e3ebb0e04d1f4fbb78abd2f0f517) preserves the remote workflow contract checks and adds explicit assertions for the GitHub Actions execution environment and full UV–EFT build command. At that exact commit, the targeted test passed 1/1, the full unit suite passed 87/87, and `git diff --check` passed locally. This does not establish GitHub Actions success; the runner-allocation failure remains separate and unresolved. No Schema, migration, or historical hash behavior changed. Four historical Fixture differences remain, and `commit_allowed=false` is unchanged.
