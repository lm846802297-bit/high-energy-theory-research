# Open issues and known limitations

This list deliberately separates confirmed software checks from unresolved design and scientific questions.

## P0 — Must resolve before calling the schema package a release

1. **Four normative decisions remain pending.** DD-ART-007 through DD-ART-010 are recommendations, not approvals. See the decision register and full review.
2. **Migration remains blocked.** The dry-run finds an ambiguous validation_ids mapping. The prototype must not guess the target record type; commit_allowed remains false.
3. **Fixture-index version field is unresolved.** The imported index says 1.4.3.6-candidate while the bundle manifest says 1.4.3.7-candidate. The source lineage points to a v1.4.3.6 archive, but that archive is not committed, and the current validator does not define or enforce the top-level field's meaning. Preserve the current value until source bytes or a metadata contract resolve it. See [fixture-index version audit](../schema/v1.4.3.7/audit/fixture-index-version-audit.md).
4. **Source lineage.** The v1.4.3.7 audit records derivation from a v1.4.3.6 candidate source bundle. Preserve that lineage; do not describe this as an independently approved v1.4.3.7 release.

## Reconciled in this branch

- **Traceability row count.** The CSV contains 125 non-empty data rows excluding the header, matching the regenerated validation report. The stale audit narrative count of 123 has been corrected. This reconciles the count only; it does not establish full requirement coverage.

## P1 — Coverage and implementation gaps

- The schemas are candidate envelopes, not a complete transcription of every normative field and condition in the design document.
- Cross-record validation does not cover every polymorphic reference or every state-machine namespace.
- Event payload hashes are not comprehensively recomputed.
- The directory-manifest helper validates a restricted FileEntry representation; it does not walk the filesystem or prove that the manifest matches disk contents. Symlinks are rejected by default.
- Migration is staging-only and historical v1.3 compatibility has not been established.
- The Skill instruction scaffold is not yet a complete executable workflow for all research tasks.

## Scientific acceptance — Not yet implemented

- No physical calculation, phenomenological scan, experimental recast, or manuscript claim is certified merely because software tests pass.
- A future end-to-end acceptance suite must test a real research task, including source provenance, conventions, independent symbolic/numerical checks, software versions, and result-to-claim traceability.
- Parameter-space reports must distinguish theoretically realizable, experimentally allowed, excluded, not assessed, and EFT-inapplicable regions; benchmark-dependent results must label their benchmark assumptions.
