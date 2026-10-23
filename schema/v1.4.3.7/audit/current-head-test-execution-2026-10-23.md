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

The Schema validator should be considered successful only if its generated report has zero failed checks, all candidate fixtures match their expected outcomes, and the evidence-provenance workflow step confirms the report was generated for this exact HEAD and run attempt. The migration regression must explicitly pass the incomplete-snapshot test and the JCS golden-vector test.

## Disposition

- No code changes were made in response to the runner failure because no code test executed and no test failure was observed.
- Do not relabel the current HEAD as tested or passing.
- Keep PR #6 Open and Draft, keep `commit_allowed=false`, and do not merge or release.
- Resume code-level diagnosis only after a runner actually starts and reports failing steps, or after the repository is available in an executable local environment.
