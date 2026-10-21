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

## Recommended disposition

Keep `run_plan.fingerprint_inputs` closed and empty-only until these semantics are defined. Do not silently reuse the Run Manifest's `FingerprintBundle` as the input declaration; they serve different roles. Once agreed, add the field schema, a canonical test vector, positive/negative fixtures, and dependency-invalidation tests.

This issue is separate from DD-ART-007 through DD-ART-010. It does not authorize a schema release or migration commit.
