# Repository status

**As of 2026-10-21. Status: development / candidate.**

## Imported assets

| Area | State |
|---|---|
| Research Skill design | v1.6.5 baseline retained; v1.6.6 Artifact-identity clarification is the latest candidate |
| Schema package | 25 schema entry points, 83 indexed fixtures, candidate only |
| Cross-record validation | Prototype available; bounded semantic checks implemented |
| Migration | Dry-run/staging prototype only; no source overwrite or commit operation |
| Requirement/test traceability | CSV traceability data and regenerated validation report included |
| Skill runtime | Initial instruction and reference scaffold added; not yet a complete automated research agent |
| Project-record validator | P0 CLI added for JSON/YAML parsing, candidate-schema validation, mapped references, cross-type ID uniqueness, status/reason checks, and local source/artifact path checks |
| Scientific validation | Not implemented; no physics result is certified by this repository |

## Local verification performed

Environment: Python 3.13, jsonschema 4.26.0.

- Bundle validator: 58 checks passed, 0 failed.
- Schema meta-validation and manifest hashes: 25 record types loaded.
- Fixture expectations: 83/83 matched.
- Bundled semantic cases: 16/16 matched.
- Prototype integration tests: 29/29 passed.
- Python syntax compilation: 7 candidate Python files passed.

These results apply only to the initial import candidate and declared test scope. GitHub Actions passed for the initial import head `2aea74decaa9676d211186610dbafd8a4d638f4b` ([run](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39521772118)). That run does not validate later commits; use the latest workflow run for the exact head SHA.

## Release gates

1. Approve or reject DD-ART-007 through DD-ART-010 explicitly.
2. Resolve fixture-index top-level version-field semantics using the audit in `schema/v1.4.3.7/audit/fixture-index-version-audit.md`; the source ZIP is not committed and the current validator does not interpret that field.
3. Resolve the migration ambiguity around validation_ids without guessing target types.
4. Expand semantic/state-machine coverage and test actual filesystem manifests.
5. Define scientific acceptance tests for real research tasks before claiming end-to-end reproducibility.
