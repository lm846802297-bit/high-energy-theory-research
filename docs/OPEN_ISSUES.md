# Open issues and known limitations

This list deliberately separates confirmed software checks from unresolved design and scientific questions.

## P0 — Must resolve before calling the schema package a release

1. **Four normative decisions remain pending.** DD-ART-007 through DD-ART-010 are recommendations, not approvals. See the decision register and full review.
2. **Migration remains blocked.** The dry-run finds an ambiguous validation_ids mapping. The prototype must not guess the target record type; commit_allowed remains false.
3. **Traceability count mismatch.** The historical audit narrative reports 123 trace rows, while the freshly regenerated validator report reads 125 rows. Reconcile the source CSV, counting convention, and narrative before release.
4. **Fixture-index version label.** manifest.json identifies the package as 1.4.3.7-candidate, while tests/fixture-index.json retains 1.4.3.6-candidate. This may reflect inherited fixtures; do not relabel until the intended meaning of the field is confirmed.
5. **Source lineage.** The v1.4.3.7 audit records derivation from a v1.4.3.6 candidate source bundle. Preserve that lineage; do not describe this as an independently approved v1.4.3.7 release.

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
