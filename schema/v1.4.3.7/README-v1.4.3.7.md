# Schema v1.4.3.7 Integrated Candidate

Status: candidate / not approved.

Source design SHA-256: `49b113fe790b413851dbafafc0728426d6de74af05503a728dd687ebcbde2269`
Source bundle SHA-256: `aefb34e68af65daf8277b9553d232cab29ffb5df9c4f18c1cfe126474a06adf1`

## Contents
- 25 JSON Schema entry points and inherited 83 fixture set
- `tools/cross_record_validate.py`: bounded cross-record validator
- `tools/migrate_v1_3_to_v1_4.py`: safe staging-only migration prototype
- `tools/directory_manifest.py`: restricted FileEntry manifest canonicalization proposal
- `tests/integration/test_v1_4_3_7.py`: 29 executable tests
- `tests/integration/dataset/`: five-record cross-record smoke dataset
- `tests/integration/migration-source-v1.3/`: intentionally ambiguous migration source fixture
- `audit/`: decision review, reports, staging output, traceability and test map

## Re-run
From this directory:
```bash
python tools/schema-v1.4.3.6-validate.py .
python tests/integration/test_v1_4_3_7.py
python tools/cross_record_validate.py tests/integration/dataset --output audit/cross-record-smoke-report.json
python tools/migrate_v1_3_to_v1_4.py tests/integration/migration-source-v1.3 --schemas-dir schemas
```

Migration defaults to dry-run. `--write-staging --output PATH` writes a staging result only. No commit or overwrite is implemented.

All four normative decisions remain pending approval. See `audit/v1.6.6-four-decisions-review.csv` and `audit/审计报告-v1.4.3.7.md`.

## Fixture-index version-field audit

The fixture index retains the observed top-level label `1.4.3.6-candidate`, while this integrated bundle is labeled `1.4.3.7-candidate`. The source lineage points to a v1.4.3.6 archive, but the archive is not committed and the current validator does not interpret the index field. The value is intentionally left unchanged pending source-byte comparison or an explicit metadata contract. See `audit/fixture-index-version-audit.md`.
