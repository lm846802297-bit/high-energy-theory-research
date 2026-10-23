# Current-HEAD test execution record — 2026-10-23

## Scope

Requested checks:
- migration regression tests, including the incomplete-source-snapshot staging guard;
- candidate Schema validator;
- Fixture Index digest/version/baseline-linkage checks;
- broader unit tests and Python compilation through the Schema-only workflow.

## Exact revision and execution attempt

- Repository: `lm846802297-bit/high-energy-theory-research`
- Branch: `fix/schema-governance-20261023`
- Tested HEAD: `7fee92c046f2ae0e70dd3d25de74e1bad0924d4d`
- Workflow: Candidate schema validation
- Workflow run: [#39947829988](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39947829988)
- Attempt: 2 (failed-job rerun)
- Job: `validate-candidate`, job ID `120398881938` on attempt 2
- Observed conclusion: `failure`
- Runner assignment: `runner_id=0`, empty `runner_name`, labels only `ubuntu-latest`
- Recorded job steps: none (`steps=[]`)
- Artifacts: none
- Job logs: unavailable; GitHub's log endpoint returned BlobNotFound.

The run completed within seconds without a runner assignment or any recorded step. Therefore this is **an execution-infrastructure failure, not a code-level test failure**. No conclusion about pass/fail of the requested Python tests or Schema validation can be drawn from this run.

## Local execution attempt

A local checkout was attempted with:

```text
git clone --depth 1 --branch fix/schema-governance-20261023 https://github.com/lm846802297-bit/high-energy-theory-research.git
```

The execution environment could not resolve `github.com` (`Could not resolve host: github.com`), so the private repository could not be checked out into the local runtime. This prevented a local Python run as well.

## Code and test changes present at this HEAD

The source tree contains the following candidate changes, which are **not execution-verified**:

1. Migration contract MIG-012 requires full Draft 2020-12 target-schema validation with format checking.
2. Migration contract MIG-013 requires target digests to use RFC 8785 JCS canonical UTF-8 bytes, while source hashes remain raw-byte SHA-256.
3. Migration staging blocks all target writes if the source snapshot is empty, contains source symlinks, or has skipped/unreadable source files. The report records `staging_blocked`, `staging_blockers`, and `staging_written_record_count`.
4. Unit tests include an incomplete-snapshot regression and exact MIG-012/MIG-013 contract checks.
5. The evidence unit test's undefined `BUNDLE` references were changed to the declared `SCHEMA_ROOT`.
6. The Schema validator checks candidate-index baseline path/version against the Manifest legacy-index path/version.

These statements describe the committed source, not passing tests.

## Required commands once an executable runner is available

Use Python 3.12 and install the repository-pinned dependencies:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests/unit -p "test_migration_reference_resolution.py" -v
python schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py schema/v1.4.3.7
python schema/v1.4.3.7/tests/integration/test_v1_4_3_7.py
python -m unittest discover -s tests/unit -v
python -m compileall -q schema/v1.4.3.7/tools skills/high-energy-theory-research/scripts
```

For a local validation run, the generated report should identify the exact tested commit and execution environment, have zero failed checks, and show all candidate fixtures and semantic cases matching their expected outcomes. The migration regression suite must explicitly pass the incomplete-snapshot test and the JCS golden-vector test. Workflow-specific run identifiers are not required to classify a result as locally validated.

## Disposition at the time of the initial runner failure (historical)

- No code changes were made in response to that runner failure because no code test executed and no test failure was observed.
- At that time, the current HEAD was not execution-verified.
- This historical disposition is superseded by the later owner-reported local verification entries below; it does not imply that GitHub Actions passed.


## Follow-up: integration test fixture mismatch (2026-10-23)

### User-provided local results for the pre-fix HEAD

For `52ad314861a9009e19be75475a630854b6537fc4`, the user reports:
- migration regression tests: 32/32 passed;
- full Schema validator: 68/68 checks, 83/83 candidate fixture outcomes, 16/16 semantic cases, and 125 trace rows passed;
- integration tests: 29/30 passed, with only `test_30_validation_ids_resolve_but_invalid_targets_are_withheld` failing;
- `tests/unit`: 75/75 passed;
- Python compilation passed.

These are the user's reported local results. They were not reproduced in this execution environment. The local report used environment marker `local`, with no GitHub Actions run ID, so it is not CI provenance evidence.

### Root-cause assessment from source review

The failing test's assertions expected schema-invalid targets, but all three source fixtures were target-schema-complete:
- `claim.json` contained the required `statement`;
- `validation-activity.json` contained the required `tool_id`;
- `validation-plan.json` contained the required `method`.

The migration's observed zero schema failures and zero unresolved items were therefore consistent with those fixtures. The defect was in the test fixture setup, not evidence of a migration implementation defect.

### Minimal corrective change

The three fixture records now each omit exactly one required target property, while retaining the IDs and fields needed to test legacy `validation_ids` resolution:
- Claim: omit `statement`;
- validation activity: omit `tool_id`;
- validation plan: omit `method`.

The integration test now requires exactly three `TARGET_SCHEMA_VALIDATION_FAILED` diagnostics covering those three record types, `migratable_record_count == 0`, and no mapped `target_record_type` for any invalid target. It also preserves the separate assertion that `migrate_record` successfully resolves the Claim's activity and plan references without reference-resolution errors. Thus the test distinguishes successful reference typing from complete target-schema validity.

### New HEAD and verification status

- New HEAD after the fixture/test correction: `b478482f6d94902d239531ce1b0dfcad6599b1d0`.
- Static reinspection confirms the three fixture fields are absent, each is required by its corresponding target Schema, and the strengthened assertions are present.
- Workflow [#39961892933](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39961892933) still failed before runner assignment (`runner_id=0`, no runner name, no steps). No Python tests ran on the new HEAD.
- Therefore the fix is **source-reviewed but not execution-verified**. The user should rerun the integration test and relevant regression suites against this exact new HEAD in the local checkout. Do not claim the previous 29/30 result applies to the modified HEAD.

### Historical Fixture Index mismatch remains separate

The four v1.4.3.6 index entries differ from the candidate index only in paths for valid/conditional `run_plan` and `run_manifest` fixtures. The index audit records that these entries retain their expected schema/semantic outcomes and requirement/error metadata. This historical expectation drift is reported separately by the candidate validator and does not explain the integration failure above, which uses a dedicated three-record migration source directory. The original v1.4.3.6 source archive remains unavailable, so byte-for-byte archive lineage is still unverified.

### Disposition

This was the disposition before the corrected integration test was rerun. It is superseded by the local-verification addendum above: the owner reports 30/30 integration tests and all listed regression/Schema checks passed on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`. PR #6 remains Open and Draft; `commit_allowed=false` remains mandatory while historical compatibility, owner approvals, cross-record validation, and transaction safety are unresolved.

## Follow-up: owner-reported local verification on corrected HEAD

**Verification target:** `1bb852c85594a6ef0e930e934cd28a438bc28a7c`  
**Environment:** Python 3.12.14 on the owner's Windows desktop checkout  
**Working tree:** reported clean; no repository files were modified during the test run.

The owner reports the following actual local execution results for the exact HEAD above:

| Check | Result |
|---|---:|
| Migration regression unit tests | 32/32 passed |
| Integration tests | 30/30 passed |
| Full `tests/unit` suite | 75/75 passed |
| Python compilation | Passed |
| Full Schema validator | 68/68 checks passed |
| Candidate fixture outcomes | 83/83 matched |
| Semantic cases | 16/16 matched |
| Requirement traceability | 125 rows matched |

The previously failing integration test `test_30_validation_ids_resolve_but_invalid_targets_are_withheld` now passes. The corrected fixture/test behavior therefore has local execution evidence on `1bb852c85594a6ef0e930e934cd28a438bc28a7c`; the earlier 29/30 result applies only to the pre-fix HEAD and is superseded for the current code.

The validator initially encountered a Windows default-GBK decoding error. Re-running in UTF-8 mode passed. The generated report was written to a temporary directory and did not overwrite the checked-in historical report:
`C:\\Users\\84680\\AppData\\Local\\Temp\\schema-validation-final-0a81973c-0aa1-4c35-9869-4dbd55fbe07d\\v1.4.3.7\\audit\\validation-report.json`.

The four legacy `1.4.3.6-candidate` fixture expectation mismatches remain separately reported. They did not cause candidate-index fixture failures. The original `1.4.3.6` archive is still unavailable, so byte-for-byte lineage of the legacy index remains unverified.

### Current evidence classification

- **Locally execution-verified (owner-reported):** the test and validator results in the table above, against the exact HEAD stated above.
- **Statically reviewed:** migration source-inventory guard, full target-schema validation path, RFC 8785 target digest contract, Fixture Index digest/version/baseline links, and test-to-contract assertions.
- **Still unverified due to missing historical inputs:** full v1.3 migration compatibility and byte-for-byte lineage to the original v1.4.3.6 archive.
- **Still pending owner approval:** DD-ART-007 through DD-ART-010 and the Schema `$id`/version identity policy.
- **Still not implemented / disabled:** full cross-record/state-machine validation and transactional commit, active-pointer switching, and rollback. `commit_allowed=false` remains mandatory.

This follow-up supersedes earlier statements in this record that the corrected integration test had not yet been run. The checked-in `audit/validation-report.json` remains a historical snapshot; the temporary local report is the report from this local run.

## Rules-v5 local verification — owner-reported result

The owner reports that the desktop checkout matched GitHub branch HEAD `587587ae0b114d9624bfb7b270c8754b7e9cbef0`, with a clean working tree, when the following checks were executed under Python 3.12.14:

| Check | Result |
|---|---:|
| Migration regression tests | 33/33 passed |
| Integration tests | 30/30 passed |
| Full repository unit tests | 76/76 passed |
| Python compilation | Passed |
| Full Schema validator | 68/68 checks passed |
| Candidate Fixture outcomes | 83/83 matched |
| Semantic cases | 16/16 matched |
| Requirement traceability | 125 rows passed |

The new regression test `test_valid_claim_is_withheld_when_referenced_plan_fails_target_schema` passed. It covers a Schema-valid Claim that references a Plan which fails target Schema validation; the dependent Claim is withheld to avoid emitting a dangling typed reference.

The Schema report was generated in a temporary copy at `C:\\Users\\84680\\AppData\\Local\\Temp\\schema-validation-rules-v5-de84e1b1-e212-4ac9-b012-44c3bf829fc4\\v1.4.3.7\\audit\\validation-report.json`. The checked-in `audit/validation-report.json` remains a historical snapshot and was not overwritten. Four historical `1.4.3.6-candidate` Fixture expectation differences remain separately recorded; they did not fail the candidate Fixture checks.

**Current acceptance wording:** The current candidate implementation's local validation has passed. GitHub Actions is temporarily excluded from this phase's acceptance and will be supplemented when runners are available. This wording does not assert that a GitHub Actions run has passed.

These results verify the available local candidate test scope only. Historical v1.3 compatibility, byte-for-byte lineage of the unavailable v1.4.3.6 archive, pending normative decisions, complete cross-record/state-machine semantics, scientific correctness, and transaction safety remain separate unresolved matters. `commit_allowed=false` remains unchanged.

## Follow-up local validation after directory-manifest safety fix

**Owner-reported result; exact tested code/test HEAD:** `0799dada7eaa8dcd08b8db2f2311a844335d7198`. The desktop checkout reportedly matched GitHub branch HEAD and had a clean working tree when the checks ran.

- Directory-manifest regression tests: **7/7 passed**.
- Migration regression tests: **33/33 passed**.
- Integration tests: **30/30 passed**.
- Full unit-test suite: **83/83 passed**.
- Python compilation: **passed**.
- Full Schema validation: **68/68 checks**, **83/83 candidate Fixture outcomes**, **16/16 semantic cases**, and **125 trace rows** passed.

The new directory-manifest tests cover missing/extra FileEntry keys, NFC-equivalent path collisions, traversal/absolute/backslash paths, deterministic sorting, and symlink rejection. The validation report was generated in a temporary directory outside the repository; the checked-in historical `audit/validation-report.json` was not overwritten. Four historical `1.4.3.6-candidate` Fixture expectation differences remain recorded separately and did not fail the candidate Fixture checks.

These are local results reported by the repository owner. They are not evidence of a passing GitHub Actions run. The tested code/test HEAD is recorded explicitly. The later PR branch did not advance only through documentation: the current code-bearing HEAD includes rules-v6/MIG-015 and source-root-symlink changes, which are not covered by the rules-v5 results recorded above.

The result verifies the available candidate test scope only. It does not establish historical v1.3 compatibility, byte-for-byte lineage of the unavailable v1.4.3.6 archive, approval of DD-ART-007 through DD-ART-010, complete cross-record/state-machine semantics, scientific correctness, or transaction safety. `commit_allowed=false` remains unchanged.

## Follow-up static review — Task Execution Contract hash gate

A subsequent static review found that the migration could emit a Task Execution Contract after mapping `contract_hash` to `contract_sha256` without revalidating the hash against the candidate payload, and could accept a missing `alternative_identity_methods` registry because that property is optional in the candidate Schema. This conflicts with the pending DD-ART-010 recommendation and its compatibility matrix, which prohibits silently defaulting a missing registry and requires unresolved treatment when the original hash payload cannot be validated.

The migration prototype has been updated to rules version `v1.4.3.7-migration-rules-6` with rule MIG-015. It now withholds a Task Execution Contract when the registry is absent or its source hash cannot be revalidated under an owner-approved payload rule. Two Task Execution Contract tests, one symlinked-source-root test, and the migration-contract assertion were added. **These rules-v6 changes and tests have not yet been executed locally.** The previous 7/7, 33/33, 30/30, 83/83, and Schema 68/68 results apply to rules-v5 code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`, not the current rules-v6 code.

The same static pass identified a source-inventory gap: the migrator checked symlinks inside the input tree but not the input root path itself. The code now includes the source root in the symlink check, and a regression test was added; it is not yet execution-verified. It also identified a remaining DD-ART-008 contract mismatch: the Artifact Schema permits `entry_type: "symlink"`, while the directory-manifest helper rejects all symlink entries. Do not resolve this by silently changing the Schema before the owner approves the symlink policy. Actual filesystem traversal and byte verification remain unimplemented. `commit_allowed=false` remains unchanged.

## Follow-up — current PR branch reconciliation

The GitHub PR metadata was rechecked after the owner-reported local run:

- Current code-bearing PR HEAD at review: `c69651858a9c0b6155242c25a4c09c1364284823`.
- Owner-reported tested HEAD: `0799dada7eaa8dcd08b8db2f2311a844335d7198` (rules v5).
- GitHub compare reports the tested SHA as an ancestor 41 commits behind the current code-bearing HEAD.
- The current branch contains rules v6/MIG-015 and a source-root-symlink guard with new regression tests. The 7/7, 33/33, 30/30, 83/83 and Schema 68/68 results belong to the earlier rules-v5 revision and do not validate those later code changes.
- Actions runs [`39969213674`](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39969213674) and [`39976133434`](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39976133434) both report `failure`. The available job records contain no usable step summaries or logs, so neither run is a pass and neither establishes a code-level test failure.

Static normalization findings and required follow-up tests are recorded in the [Normalization and migration boundary review](schema/v1.4.3.7/audit/normalization-and-migration-boundary-review-2026-10-23.md). No migration or Schema code was changed by this audit-document update.
