# Schema v1.4.3.6 integrated candidate

Status: CANDIDATE / NOT RELEASED. Derived from v1.4.2 candidate bundle plus DD-ART-006 proposal.

This bundle changes the Artifact contract and is not backward-compatible without migration. `artifact_storage_kind` and `alternative_identity` are required. A hashless external file remains `needs_review` under the strict candidate interpretation even if an alternative identity is verified; that status means method verification only, not byte-level integrity. Directory artifacts use FileEntry objects and `directory_manifest_sha256`.

The source design document remains v1.6.5; an aligned draft is provided outside the bundle as v1.6.6 candidate. The normative choices are not approved.
