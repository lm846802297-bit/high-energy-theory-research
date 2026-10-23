# Fixture index version-field audit

**Status:** Resolved at metadata-contract level. Historical source-archive byte comparison remains unavailable and is not represented as verified.

## Normative metadata contract for this candidate

- manifest.schema_version identifies the schema bundle version.
- manifest.fixture_index points to the canonical fixture index used to validate the current bundle. Its top-level schema_version must equal manifest.schema_version.
- manifest.legacy_fixture_index points to a retained historical fixture index. Its top-level schema_version must equal manifest.legacy_fixture_index_schema_version.
- A fixture index's top-level schema_version identifies the target bundle whose fixture expectations it declares. It is not the index metadata format version and does not, by itself, prove the source archive from which the file was imported.
- Source archive lineage is recorded separately in IMPORT_PROVENANCE.json.

## Repository values

| Item | Value | Meaning |
|---|---|---|
| Candidate bundle | 1.4.3.7-candidate | Current, unreleased candidate |
| Canonical fixture index | tests/fixture-index-v1.4.3.7.json | Version-matched candidate acceptance suite |
| Legacy fixture index | tests/fixture-index.json | Preserved 1.4.3.6-candidate expectation baseline |
| Legacy source archive named in provenance | schema-v1.4.3.6-integrated-candidate-bundle.zip | Lineage record only; archive is not committed in the repository |
| Candidate index digest | 720a2f450991ecf8518e1fae86c0e17bfa0765aae1d0c7ff684bb71e32de4fc4 | SHA-256 of the canonical candidate index |
| Legacy index digest | fa1047d096208c81e2798af0276cfe0aeccca37dba599e3ef837664c44cc6133 | SHA-256 of the preserved legacy index |

The repository does not claim byte-for-byte equality between the checked-in legacy index and the unavailable source archive. The current file bytes are identified by the manifest digest; source-archive equality remains unverified.

## Validator and regression behavior

The candidate validator checks:
1. the canonical candidate index digest;
2. the legacy index digest;
3. candidate index schema_version equality with the bundle schema_version;
4. legacy index schema_version equality with the explicitly declared legacy baseline version;
5. candidate fixture IDs and expected schema/semantic outcomes; and
6. historical fixture expectations against the candidate schemas, reported separately as compatibility drift.

The historical index is not relabeled. Candidate acceptance uses the canonical version-matched index. A mismatch in historical expectations is not silently converted into a candidate pass.

## Release boundary

This resolves the meaning of the metadata field, not the missing source archive. Schema v1.4.3.7 remains an unreleased candidate. DD-ART-007 through DD-ART-010 remain pending explicit owner approval, and historical v1.3 migration compatibility remains unverified.
