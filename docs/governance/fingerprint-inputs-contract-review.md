# FingerprintInputs contract review

**Status:** unresolved design contract; no fields or hashing semantics are approved by this note.

## Evidence

The v1.6.6 candidate design lists `fingerprint_inputs: Record<FingerprintInputs>` in the Run Plan field table, but does not define a `FingerprintInputs` nested object in the fixed-object section. The current candidate schema consequently defines `fingerprint_inputs` as a closed object with no properties, so only `{}` is valid.

The Run Manifest does define a `FingerprintBundle` with input-set, configuration, code-tree, environment, execution-spec, dependency-artifact, composite hashes, and a profile version. Those output digest fields do not, by themselves, define which exact source/artifact/configuration inputs must be included in the input set.

## Questions to settle before enabling non-empty values

1. Does the input declaration identify source/configuration/code/environment/artifact IDs, their content digests, or both?
2. How are absent or unavailable source/artifact digests represented, and may a Run Plan be `ready` while any required fingerprint input is unknown?
3. Is `execution_spec_sha256` part of `FingerprintInputs`, or only part of the resulting `FingerprintBundle`?
4. How are dependency artifact hashes sorted and canonicalized, and which profile/version fixes the composite-hash payload?
5. How does a changed input invalidate downstream Run Plans, Runs, manifests, validation reports, and Claims?

## Recommended candidate contract (proposal only; not implemented)

A reasonable default is for `FingerprintInputs` to declare **which versioned records participate in the fingerprint**, while the Run Manifest's `FingerprintBundle` stores the computed component and composite hashes. This avoids duplicating digest outputs in the input declaration.

Proposed fields for review:

- `source_ids`: unique Source record IDs, sorted by a specified canonical order;
- `configuration_id`, `code_id`, `environment_id`: the exact records used, nullable only when the task contract explicitly permits their absence;
- `input_artifact_ids`: the exact input Artifact IDs, not output artifacts;
- `execution_spec_sha256`: digest of the exact execution specification;
- `fingerprint_profile_version`: identifies the canonicalization and composition rules used to calculate the Run Manifest's `FingerprintBundle`.

Under this proposal, the fingerprinting procedure resolves each referenced record to its declared content/component digest. A required digest that is unavailable must not be silently omitted: the Run Plan should remain blocked or otherwise explicitly non-reproducible under a reviewed status rule. The manifest then records `input_set_sha256`, component digests, `dependency_artifact_sha256`, and `composite_sha256`.

## Decisions still required

1. **Unavailable hashes:** should a missing required digest block a Run Plan from becoming `ready`, or is there an explicitly non-reproducible execution mode?
2. **Input set:** should external Source IDs and input Artifact IDs both feed `input_set_sha256`, with artifact dependencies also summarized separately, or should there be a non-overlapping partition?
3. **Canonicalization:** which exact serialization, sorting, and numeric encoding rules are normative, and how is the profile version advanced?

## Recommended disposition

Adopt the proposed field separation only after review; do not implement it from this note alone. Until the fields and hashing semantics are approved, keep `run_plan.fingerprint_inputs` closed and empty-only. Do not silently reuse the Run Manifest's `FingerprintBundle` as the input declaration; they serve different roles. Once agreed, add the field schema, a canonical test vector, positive/negative fixtures, and dependency-invalidation tests.
