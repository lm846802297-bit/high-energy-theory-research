# Schema v1.4.3.7 candidate

This directory contains an unapproved candidate schema bundle. It is not a released normative version.

## Versioned fixture sets

- `tests/fixture-index.json` is the inherited `1.4.3.6-candidate` fixture index. Its bytes and version label are preserved as provenance; it is not silently relabeled.
- `tests/fixture-index-v1.4.3.7.json` is the candidate-specific fixture index used for acceptance against the current schemas. The four Run Plan/Run Manifest valid/conditional fixture records are regenerated in `tests/v1.4.3.7/` with non-empty structured payloads that meet the candidate contracts.
- The validator reports mismatches between the inherited fixture expectations and current candidate schemas separately as compatibility drift. Those mismatches do not replace or weaken the version-matched candidate test suite.

## FingerprintInputs

`run_plan.fingerprint_inputs` uses the candidate-only `fingerprint-inputs-v1` contract described in `docs/governance/fingerprint-inputs-contract-review.md`. The RFC 8785 deterministic hashing implementation, golden vector and negative tests are in the research Skill scripts and `tests/unit/test_fingerprint_inputs.py`.

## Validation-report provenance

The workflow regenerates `audit/validation-report.json` in the runner and uploads it as the `candidate-schema-validation-report` Actions artifact. The checked-in report file is an imported repository snapshot and is not by itself evidence of the latest CI run. Use the report artifact attached to the specific workflow run when auditing current counts and fixture outcomes.

## Release constraints

- DD-ART-007 through DD-ART-010 remain unapproved.
- `validation_ids` migration remains staging-only and blocked while ambiguous.
- Schema/CI success is not a physics correctness certificate. A real research task must independently verify provenance → configuration → run → artifact → validation → evidence → Claim before any release decision.
