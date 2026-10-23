# Artifacts

Versioned snapshots of research sources and computational artifacts that are too large, too binary, or too numerous to review line-by-line in ordinary text diffs. Per §8 of the [workflow specification](../docs/scientific-diff-workflow.md), each bundle records provenance, content hashes, and a human-readable summary rather than relying on the diff alone.

Bundles are **immutable**. Adopting a later source revision means adding a new bundle directory, not editing an existing one.

## Bundles

| Bundle | Source version | Linked record | Size | Files |
|---|---|---|---|---|
| [higgs-portal-v66-20261019](higgs-portal-v66-20261019/) | Historical main document v66, dated 2026-10-19 (not the latest research version) | [RC-001](../research/RC-001-vll-higgs-singlet-uv-eft.md) (earlier source generation) | 12,445,122 bytes (12.45 MB) | 138 |

---

## higgs-portal-v66-20261019

A historical snapshot of the local working tree that produced the v66 main document on 2026-10-19. It is committed to provide a stable, hashable provenance trail for the derivations, scripts, audit records, and intermediate outputs associated with that historical state.

> **Historical status and scope caveat.** v66 is **not the latest research version** and must not be treated as the current source of truth. The current research baseline remains v153 as identified in [RC-001](../research/RC-001-vll-higgs-singlet-uv-eft.md); this bundle does not supersede it. This is a working archive, not a validated result set. The v66 document's own opening "unified conclusion status table" governs only the claims it records: any claim marked unresolved, in progress, or not yet verified remains so. Committing a script does not mean its output was independently confirmed, and committing an output does not establish the physical claim built on it.

### Contents

| Path | Contents |
|---|---|
| `higgs_portal_mixing_unified_reviewer_response_and_uv_eft_UPDATED_v2(8)(20261019)(66).md` | Main document, v66: reviewer-response route, one-loop \(s\)–\(h\) mixing, UV–EFT matching record, original-paper cross-check, execution plan |
| `work/` | Version-lineage workspace: correction, enhancement, reconstruction, polish, and validation scripts plus the intermediate drafts they produced |
| `work/latex-build/` | Pandoc + LaTeX typesetting attempt: `main.tex`, `main.pdf`, per-page render checks |
| `计算脚本/` | Computational index; see its [README](higgs-portal-v66-20261019/计算脚本/README.md) for the full inventory and the old-to-new path mapping |
| `计算脚本/section261/`, `计算脚本/section262/` | Per-section working sources, Mathematica sources, logs, manuscript fragments |
| `计算脚本/计算输出/` | Reproduction scripts and check logs for §§250–262 |
| `计算脚本/审计结果/DeepSeek66/` | Independent v66 audit report, recomputation sources, evidence |
| `计算脚本/整理记录/` | Pre/post-relocation SHA-256 manifest and path correspondence |

### Script families in `计算脚本/`

| Family | Role |
|---|---|
| `01`–`05` | Main HiggsPortal verification (pure Mathematica), third-party package run, FeynRules and SARAH model files, HiggsTools constraint scan |
| `audit_*` | Independent checks: Dirac traces per chirality path, Wick rotation signs, six-route geometry coefficients, denominator consistency |
| `build_*` | Pathwise matching integrands, six-cycle weight ledgers, six-labeled orderings |
| `derive_*` | Raw Minkowski numerator derivation and the Minkowski-to-Euclidean \(B\) kernel map |
| `verify_*` | Numerator-to-kernel checks and §245 matching verification |
| `*_verification.json`, `*_output.txt`, `*.csv` | Numerical and symbolic verification outputs retained as evidence |

### Verification status

| Item | Status |
|---|---|
| Document size and SHA-256 | 1,611,984 UTF-8 bytes; `082b9add00b2aecbba9e708cda834033b6c8391679d68ed4b86761ed0d464332` — independently recomputed on 2026-10-23 and matched |
| `计算脚本/section273_feyncalc_threshold_workflow.wl` | `8e2c7a36c5cacecf35194a92cde50e52ec457cb884684c719e5aafc6b67053ab` — annotated FeynArts/FeynCalc scaffold, **not executed** |
| `计算脚本/higgs_portal_threshold_key_result_audit.wl` | `f6a015c87ed01579703ffe1f4d5b5f1b546b670224fbe46e2571d744369473ed` — added after the v66 snapshot's audit chain |
| `计算脚本/run_uv_eft_audit_suite.py` | `ab4967866318d139706ee2fd42d1d2122808fa49687d39825f01196b3434ebb5` — orchestration only; see the B1/B3 sign warning in RC-001 |
| `计算脚本/计算输出/section262_reproduce.py` | `07ca907b58cad437e9bc1dca5fb3e97a1bb909dcc73ff3ca8ac46d8af0813f5c` |
| LaTeX intermediate files | Pruned before commit (`.aux`, `.log`, `.toc`, `.out`, `.fls`, `.fdb_latexmk`, `missfont.log`); `main.pdf` and render checks retained |

The 50 `sha256_after` entries in the relocation manifest and the four smaller-file hashes listed above were independently recomputed against the committed contents and matched. In a follow-up audit on 2026-10-23, the full v66 Markdown blob (Git blob `03b094c34177af4b8e864237290e15f7918f5f5d`) was also independently rehashed: its UTF-8 size is 1,611,984 bytes and its SHA-256 is `082b9add00b2aecbba9e708cda834033b6c8391679d68ed4b86761ed0d464332`, matching the recorded digest. The in-bundle manifest is retained as the original snapshot audit record; this later verification is recorded here and in PR #5. No physics calculation was rerun.

Python reproduction is self-contained per section:

```bash
python 计算脚本/计算输出/section262_reproduce.py
```

Mathematica entries (`01_HiggsPortal_主验算_纯MMA.m`, `section273_feyncalc_threshold_workflow.wl`) require a local Wolfram Engine. The FeynCalc scaffold additionally requires a custom FeynArts model file and a particle-label mapping that are **not** included.

### Known gaps

- `work/latex-build/` is a partial build; the PDF was produced to check pagination and is not a distribution-quality manuscript.
- The historical `prepare.py`, `markdown_qa.cjs`, and `section261/build_v65.py` now use explicit input/dependency paths. Their original source/input directories are not bundled, so those scripts are not self-contained reproduction commands.
- Historical intermediate drafts in `work/` (`v57_*.md`) are retained for traceability only and do not reflect current conclusions.
- `计算脚本/README.md` records one external reference (`work/tsk2_b0.m`) that was already unlocatable at relocation time and was not reconstructed.
