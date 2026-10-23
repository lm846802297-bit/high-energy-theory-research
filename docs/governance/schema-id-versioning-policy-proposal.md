# Schema `$id` and Versioning Policy Proposal

**Status: proposal only — owner approval required.** This document does not approve a canonical URI, change any schema `$id`, or authorize a release.

## Decision question

For the integrated Schema bundle, does each schema's `$id` identify (a) the exact versioned schema artifact published by this project, or (b) the upstream/source schema identity from which the artifact was inherited?

The current candidate does not state this consistently. Static inventory found 23 schema files whose `$id` and title carry a v1.4.2 candidate label and two files carrying a v1.4.3.6 integrated-candidate label. All inspected `$id` values use the `schemas.example.invalid` host. The original intent of these values has not been established.

## Recommendation for owner review

Adopt **versioned integrated-artifact identity** for `$id`:

1. A schema `$id` identifies the exact schema document as distributed in a named integrated bundle version; it is not a mutable alias for “latest”.
2. All record schemas in one integrated release use one owner-controlled HTTPS base URI and the same bundle-version segment, with a record-type-specific filename.
3. Candidate and released identifiers must not be conflated. The final URI scheme must explicitly state whether candidate artifacts receive public candidate-specific identifiers or remain local/unpublished until release.
4. Upstream lineage is recorded separately in the manifest/audit metadata (source bundle, source schema identifier, source hash, and integration change record); it must not be encoded by leaving mixed upstream version labels in the integrated artifact's `$id`.
5. The placeholder host `schemas.example.invalid` is not a production URI and must never be represented as an approved release identifier.

This recommendation makes an integrated schema's identity unambiguous while preserving provenance independently. It is not normative until the repository owner approves it.

## URI template (not a real URI)

After approval of a real base URI, the proposed shape is:

`<OWNER-APPROVED-HTTPS-BASE>/high-energy-theory/schema/<VERSION>/<RECORD_TYPE>.schema.json`

The template is intentionally not substituted into the schemas. Do not guess a domain, rewrite the 25 schema files, or regenerate manifest hashes until the owner has approved both the base URI and the candidate-versus-release version naming convention.

## Alternatives

| Option | Advantages | Risks / costs |
|---|---|---|
| Preserve inherited source `$id` values | Keeps source identity visible | Mixed version labels remain; identifiers may not resolve to the integrated artifact; provenance and artifact identity are conflated |
| Use integrated, versioned `$id` values (recommended) | Consistent bundle identity; deterministic versioned references | Requires an approved URI base and explicit source-lineage metadata |
| Use unversioned “latest” identifiers | Convenient for consumers | Mutable identity; cache and reproducibility ambiguity; unsuitable as the sole identifier for archival evidence |

## Required approval record

Before implementation, record:

- approved HTTPS base URI and control of its namespace;
- whether candidate bundles receive candidate-specific URIs or use local identifiers until release;
- exact version-segment syntax;
- whether the source identifier and source hash are preserved in manifest metadata;
- compatibility plan for consumers that may already have cached the inherited `$id` values;
- the test that rejects placeholder hosts and inconsistent bundle-version segments in a release candidate.

## Current gate

Until explicit owner approval is recorded, leave all current `$id` values unchanged and classify the URI policy as **BLOCKED / PENDING APPROVAL**. The current values are not evidence that the source-identity option was intentionally chosen. Schema v1.4.3.7 remains `candidate` / `not_released`.
