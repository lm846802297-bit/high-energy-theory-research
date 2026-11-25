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

## Static comparison of the two checked-in indexes

A source-level comparison of the current candidate and legacy index JSON found:

- 83 fixture entries in each index; all 83 fixture IDs are unique within each index.
- The sets of fixture IDs are identical; no ID exists only in one index.
- Four entries differ in the `file` path only: the valid and conditional fixtures for `run_plan` and `run_manifest` point to versioned `tests/v1.4.3.7/...` paths in the candidate index and the older `tests/valid` / `tests/conditional` paths in the legacy index.
- The compared entries' record type, fixture kind, expected schema result, expected semantic result, requirement IDs, and expected error codes are unchanged for those four entries.

This is a comparison of the two files currently checked into the branch, not proof that the legacy index is byte-identical to the unavailable v1.4.3.6 source archive. The owner subsequently ran the candidate validator locally on code HEAD `1bb852c85594a6ef0e930e934cd28a438bc28a7c`; the report showed 68/68 checks, 83/83 candidate fixture outcomes, 16/16 semantic cases, and 125 trace rows passing. The original archive is still required for byte-for-byte source-lineage verification.

## Validator and regression behavior

The candidate validator checks:
1. the canonical candidate index digest;
2. the legacy index digest;
3. candidate index schema_version equality with the bundle schema_version;
4. legacy index schema_version equality with the explicitly declared legacy baseline version;
5. candidate fixture IDs and expected schema/semantic outcomes; and
6. historical fixture expectations against the candidate schemas, reported separately as compatibility drift.

The historical index is not relabeled. Candidate acceptance uses the canonical version-matched index. The owner-reported local validator run passed all 83 candidate fixture outcomes and separately recorded four legacy expectation mismatches against the candidate schemas. A mismatch in historical expectations is not silently converted into a candidate pass.

## Release boundary

This resolves the meaning of the metadata field, not the missing source archive. Schema v1.4.3.7 remains an unreleased candidate. DD-ART-007 through DD-ART-010 remain pending explicit owner approval, and historical v1.3 migration compatibility remains unverified.
