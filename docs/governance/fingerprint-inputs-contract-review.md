# FingerprintInputs contract review

**Status:** implemented in the v1.4.3.7 candidate branch for review; not a released or approved normative schema.

## Candidate data contract

`run_plan.fingerprint_inputs` is a closed object with these required fields:

- `contract_version`: fixed to `fingerprint-inputs-v1`.
- `canonicalization`: fixed to `RFC8785` (RFC 8785 JSON Canonicalization Scheme).
- `source_inputs`: array of `{source_id, content_sha256}`. Each source is an actual input to the run, not merely a citation. A byte digest is mandatory.
- `input_artifacts`: array of `{artifact_id, digest_kind, digest_sha256}`. `digest_kind` is `content_sha256` for a file or `directory_manifest_sha256` for a directory. Hashless artifacts cannot be treated as reproducible run inputs.
- `configuration`: `{record_id, configuration_sha256, not_applicable_reason}`.
- `code`: `{record_id, code_tree_sha256, not_applicable_reason}`.
- `environment`: `{record_id, environment_sha256, not_applicable_reason}`.
- `execution_spec_sha256`: the RFC 8785 SHA-256 digest of the exact Run Plan `execution_spec`.
- `fingerprint_profile_version`: non-empty version string for the component/composite fingerprint profile.

For each of configuration, code and environment, a referenced record ID requires a valid component digest and a null not-applicable reason. A null record ID requires a null digest and a non-empty not-applicable reason. A missing digest for a referenced record is not equivalent to not-applicable.

## Deterministic hashing algorithm

1. Canonicalize each JSON payload with RFC 8785, encode the canonical text as UTF-8, and calculate lowercase hexadecimal SHA-256.
2. Sort `source_inputs` by `source_id` and `input_artifacts` by `artifact_id` before hashing. Their original array order therefore does not change the fingerprint. Duplicate IDs are rejected even if duplicate entries carry different hashes.
3. `execution_spec_sha256 = SHA256(JCS(execution_spec))`.
4. `input_set_sha256 = SHA256(JCS({contract_version, canonicalization, source_inputs, input_artifacts}))`, with the sorted arrays and exact values from the Run Plan.
5. `dependency_artifact_sha256 = SHA256(JCS(sorted input_artifacts))`.
6. The composite payload is the FingerprintBundle without `composite_sha256`: `algorithm`, `input_set_sha256`, `configuration_sha256`, `code_tree_sha256`, `environment_sha256`, `execution_spec_sha256`, `dependency_artifact_sha256`, and `fingerprint_profile_version`. Null component hashes are allowed only when the corresponding input component is explicitly not applicable.
7. `composite_sha256 = SHA256(JCS(composite payload))`.

The Run Plan top-level IDs must match the IDs inside FingerprintInputs. The top-level `execution_spec_sha256` must match the digest of `execution_spec`. Its input-artifact IDs must exactly match the artifact IDs declared in FingerprintInputs. Where a contract or Run Manifest is supplied, source/artifact references and component hashes are checked against those records.

## Golden vector and acceptance tests

The machine-readable vector at `tests/fixtures/fingerprint-inputs-v1/golden-vector.json` stores the complete input, expected canonical byte strings, and expected digests for the execution spec, input set, dependency-artifact set, and composite bundle. Tests also reverse input arrays, duplicate IDs, alter the execution spec and mismatch linked record IDs to prove deterministic behavior and failure handling.

## Deliberate boundaries

- The contract fingerprints the exact declared input byte/content identities; it does not prove a source's scientific reliability or a claim's correctness.
- Source records used only as citations need not be included in `source_inputs`; the array represents inputs that affect the run result. The Run Manifest may cite additional sources.
- A source/artifact digest that cannot be obtained is not silently omitted from a reproducible run. The run should remain blocked or explicitly outside the reproducibility claim under reviewed status rules.
- RFC 8785 canonicalization does not normalize Unicode strings. Record IDs are expected to be stable identifiers; file/directory path normalization remains governed by the separate artifact-directory contract.
- The golden vector is a deterministic software test, not scientific evidence.

## Review questions before release

1. Approve or revise the field names and exact component separation above.
2. Confirm the rule that a referenced but hashless input blocks reproducible execution rather than being silently omitted.
3. Confirm the fingerprint profile versioning and downstream invalidation policy when source, configuration, code, environment, execution specification, or input artifacts change.

Until these decisions are reviewed, the implementation remains candidate-only. This note does not approve DD-ART-007 through DD-ART-010, authorize migration commits, or release schema v1.4.3.7.