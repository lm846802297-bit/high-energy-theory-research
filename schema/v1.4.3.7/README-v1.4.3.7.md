# Schema v1.4.3.7 Integrated Candidate

Status: candidate / not approved.

Source design SHA-256: `49b113fe790b413851dbafafc0728426d6de74af05503a728dd687ebcbde2269`
Source bundle SHA-256: `aefb34e68af65daf8277b9553d232cab29ffb5df9c4f18c1cfe126474a06adf1`

## Contents
- 25 JSON Schema entry points and inherited 83 fixture set
- `tools/cross_record_validate.py`: bounded cross-record validator
- `tools/migrate_v1_3_to_v1_4.py`: safe staging-only migration prototype
- `tools/directory_manifest.py`: restricted FileEntry manifest canonicalization proposal
- `tests/integration/test_v1_4_3_7.py`: 30 executable tests
- `tests/integration/dataset/`: five-record cross-record smoke dataset
- `tests/integration/migration-source-v1.3/`: negative migration fixture with a missing validation target
- `tests/integration/migration-source-v1.3-resolvable/`: positive synthetic source graph with a unique started activity and a unique plan
- `audit/`: decision review, reports, staging output, traceability and test map

## Re-run
From this directory:
```bash
python tools/schema-v1.4.3.6-validate.py .
python tests/integration/test_v1_4_3_7.py
python tools/cross_record_validate.py tests/integration/dataset --output audit/cross-record-smoke-report.json
python tools/migrate_v1_3_to_v1_4.py tests/integration/migration-source-v1.3 --schemas-dir schemas
```

Migration defaults to dry-run. `--write-staging --output PATH` writes a staging result only. The output directory must be outside the input tree and empty or new; non-empty output directories are rejected to avoid stale files. Source records are never overwritten, and no commit operation is implemented.

All four normative decisions remain pending approval. See `audit/v1.6.6-four-decisions-review.csv` and `audit/审计报告-v1.4.3.7.md`.

The migration contract is now rules v6. MIG-015 withholds Task Execution Contract records when `alternative_identity_methods` is missing or the source `contract_hash` has not been revalidated under an owner-approved DD-ART-010 payload. The code and two Task Execution Contract regression tests were added after the rules-v5 local validation on code/test HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198`. The source-root symlink guard and a third migration test were also added; rules-v6/source-inventory validation is still pending. The Artifact Schema's symlink enum and the helper's symlink rejection remain a DD-ART-008 contract mismatch.

## Fixture-index version-field audit

The metadata contract is now explicit: `manifest.fixture_index` is the canonical, version-matched v1.4.3.7 candidate index; `manifest.legacy_fixture_index` preserves the v1.4.3.6 expectation baseline. The validator checks both digests and version relationships. The unavailable source archive is not claimed to match the preserved index byte-for-byte. See `audit/fixture-index-version-audit.md`.

## End-to-end Skill pilot

The repository includes a synthetic algebraic pilot under `tests/eval-cases/analytic-mass-matrix-pilot/`. Its mathematical checks pass within the stated pilot scope. The candidate-only `FingerprintInputs` contract, deterministic hashing implementation, golden vector, and negative tests are documented in `docs/governance/fingerprint-inputs-contract-review.md` and `tests/unit/test_fingerprint_inputs.py`; that contract's normative status and the end-to-end execution/evidence workflow remain separate release gates. The pilot is not a physical calculation and does not establish complete research reproducibility.


## Historical v1.3 compatibility gate

The full historical v1.3 machine-readable source bundle is not available in the repository or the inspected Library inventory. The migration tool is a tested prototype, not proof of compatibility with all historical records. `commit_allowed=false` remains mandatory. Required source artifacts and acceptance criteria are listed in `audit/v1.3-compatibility-gate.md`.
