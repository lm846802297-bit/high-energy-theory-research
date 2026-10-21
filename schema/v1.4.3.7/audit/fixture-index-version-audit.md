# Fixture index version-field audit

**Status:** audited, unresolved; no version label changed.
**Scope:** `schema/v1.4.3.7/tests/fixture-index.json` and its relationship to the candidate bundle metadata.

## Observed evidence

| Location | Observed value or behavior | Interpretation limit |
|---|---|---|
| `manifest.json` | `schema_version = 1.4.3.7-candidate` | Labels the integrated candidate bundle. |
| `tests/fixture-index.json` | Top-level `schema_version = 1.4.3.6-candidate` | The repository contains no schema/document defining the meaning of this top-level index field. |
| `IMPORT_PROVENANCE.json` | Records lineage from `schema-v1.4.3.6-integrated-candidate-bundle.zip`, SHA-256 `aefb34e68af65daf8277b9553d232cab29ffb5df9c4f18c1cfe126474a06adf1` | The source ZIP itself is not committed in this repository, so its exact fixture-index bytes cannot currently be compared with the imported file. |
| `manifest.json` | Records `fixture_index_sha256 = fa1047d096208c81e2798af0276cfe0aeccca37dba599e3ef837664c44cc6133` | The bundle validator verifies that the current index file matches this digest. This proves internal digest consistency, not the meaning or original provenance of the version field. |
| `tools/schema-v1.4.3.6-validate.py` | Checks the fixture-index file hash, fixture IDs, fixture outcomes, and trace links; it does not interpret the top-level `idx["schema_version"]`. | Current CI passing does not resolve the version-field semantics. |
| Individual fixture entries | Use `schema_version = 1.4` | This is the record-format version; it does not define the top-level fixture-index metadata field. |

## Finding

The mismatch is **consistent with an inherited source-package label**, because the documented source lineage points to a v1.4.3.6 candidate bundle. However, the source archive is not present for byte-level comparison, and no normative contract defines whether the index's top-level `schema_version` means:

1. the bundle version to which the index belongs;
2. the version of the index metadata format; or
3. the source bundle version from which the index was inherited.

Therefore, it is not yet justified to replace `1.4.3.6-candidate` with `1.4.3.7-candidate`. Nor is it justified to assert that the old value is a deliberately preserved provenance field.

## Validator behavior

The current validator confirms the file digest recorded in `manifest.json` and checks fixture contents. It does not enforce equality between the manifest's `schema_version` and the fixture index's top-level `schema_version`. The passing CI result is consequently compatible with this metadata mismatch.

## Safe disposition

- Preserve the current index bytes and manifest digest while the field's meaning is unresolved.
- Keep this issue as a release blocker for metadata clarity; do not interpret it as evidence that the fixture payloads themselves failed.
- If the original source ZIP becomes available, compare the extracted `tests/fixture-index.json` bytes and digest directly.
- Then define the field contract explicitly. If it denotes the current bundle, update it to the candidate bundle version and regenerate the manifest digest. If it denotes source lineage or index-format version, rename/document it explicitly in a reviewed metadata change and preserve source provenance.
- Add a validator regression test for the chosen contract before removing this issue.

## Release boundary

This audit does not approve DD-ART-007 through DD-ART-010, unblock `validation_ids` migration, establish full schema coverage, or certify any physical result.
