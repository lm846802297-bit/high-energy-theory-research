# Open issues and known limitations

This list separates verified software behavior from unresolved design, provenance, and scientific questions.

## P0 — Must resolve before calling the schema package a release

1. **Four normative decisions remain pending.** DD-ART-007 through DD-ART-010 are recommendations, not approvals. No normative Schema change or formal release may treat them as approved until the repository owner explicitly decides each one. See docs/governance/DECISION_REGISTER.md and docs/governance/schema-v1.4.3.7-four-decisions-review.md.
2. **Historical v1.3 compatibility is unverified.** The exact v1.3 machine-readable source bundle and historical record corpus are unavailable in the repository/inspected Library inventory. The migration prototype's synthetic tests do not replace that baseline. See schema/v1.4.3.7/audit/v1.3-compatibility-gate.md.
3. **Migration cannot commit.** The source-aware validation_ids resolver has positive and negative regression cases, but unresolved/missing source targets still block migration. Transactional commit and pointer-based rollback are not implemented, so commit_allowed=false is an intentional safety invariant.
4. **The integrated candidate is not released.** Schema v1.4.3.7 remains candidate-only. The last main-branch run explicitly inspected for this note, #39896401710 on SHA `35d854699b652d69a1e51335dfaff1fe27dda0cd`, failed before a runner/step was assigned; main has since advanced through documentation-only changes, and this note does not assert a CI result for the newer HEAD. Separately, manual dispatch of PR #6 HEAD `531497c0e6e45ce4316e77266530856fe9544f26` ([run #39898913319](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39898913319)) was blocked by GitHub account billing/payment or spending-limit status before any step ran. Neither run provides a test result. Historical green runs apply only to their recorded SHAs.

## Resolved in the candidate metadata contract

- **Fixture-index version semantics.** The canonical manifest.fixture_index now points to the version-matched v1.4.3.7 candidate index. manifest.legacy_fixture_index preserves the 1.4.3.6 expectation baseline. The validator checks both file digests and both version relationships. The original source ZIP is not committed, so byte-for-byte equality with that archive is not claimed. See schema/v1.4.3.7/audit/fixture-index-version-audit.md.

## P1 — Coverage and implementation gaps

- The schemas are candidate envelopes, not a complete transcription of every normative field and condition in the design document.
- FingerprintInputs has a candidate contract and deterministic tests, but its normative status still requires review. The fingerprint contract does not establish scientific correctness.
- Cross-record validation does not cover every polymorphic reference or every state-machine namespace.
- Event payload hashes are not comprehensively recomputed.
- The directory-manifest helper validates a restricted FileEntry representation; it does not walk the filesystem or prove that the manifest matches disk contents. Symlinks are rejected by default.
- The Skill instruction scaffold is not yet a complete executable workflow for all research tasks.

## Scientific acceptance — Not yet implemented

- No physical calculation, phenomenological scan, experimental recast, or manuscript claim is certified merely because software tests pass.
- The synthetic 2x2 matrix pilot exercises exact results and independent algebraic checks, but is not a real phenomenology task. A later acceptance suite must test a real research task, including source provenance, conventions, independent symbolic/numerical checks, software versions, and result-to-claim traceability.
- Parameter-space reports must distinguish theoretically realizable, experimentally allowed, excluded, not assessed, and EFT-inapplicable regions; benchmark-dependent results must label their benchmark assumptions.
