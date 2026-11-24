# High-Energy Theory Research Skill evaluation — 2026-11-22

This is a bounded evaluation record for PR #27 in `lm846802297-bit/high-energy-theory-research`. It evaluates the new Skill modules using a symbolic phase-space derivation, an independent numerical integration, and a PDF figure audit. The Windows follow-up records Skill discovery and reference loading at the tested PR head. The LZ source repository was used as a read-only reference.

## Contract test

- Test file: `tests/unit/test_skill_contract.py` from PR branch `feat/research-skill-optional-tooling-20261122`.
- Test source Git blob SHA-1: `4a2ad1da1c430760f442caa6ae7840f3a197cb8e`.
- Result: 6 passed, 0 failed.
- Environment: Python 3.13.5, Linux x86_64.
- Scope: the exact test file and PowerShell diagnostic were run against a minimal filesystem fixture. The PR's actual Skill/reference files were separately read from GitHub. This was not a full repository checkout or full unit-test suite.
- PowerShell was unavailable in the Linux environment; the Windows diagnostic was statically reviewed but not executed.

## Symbolic calculation

`symbolic/derive_phase_space_jacobian.py` verifies the Källén factorization and the exact Jacobian for `s = Delta*u^2`. It also compares the correct transformed integrand with an explicitly constructed candidate expression that omits the factor 2. That candidate is exactly half the correct absolute integral; the factor cancels after unit-area normalization, so its normalized shape is unchanged. This script does **not** parse or execute the private LZ `reproduce_fig2.py` source file, so the candidate comparison alone is not proof of what that source file contains.

The original-variable and transformed-variable mpmath integrals agree at 50 decimal digits for the stated unit-specified benchmark (`m1 = 1.0 GeV`, `m2 = 0.2 GeV`, `Delta = 0.5 GeV^2`). See `symbolic/result.json`.

## Numerical convergence

`numerical/convergence_phase_space.py` uses the full Jacobian and compares Gauss-Legendre orders 4 through 1024. It also compares six recoil points against SciPy adaptive quadrature in the original integration variable and checks the heavy-particle endpoint limit. The archived CSV is sampled every 25 keV; the internal convergence grid has 701 points plus exact endpoints.

- Exact recoil interval: 106.5912099532–670.7107218078 keV.
- 2-to-3 peak: 328.0152102888 keV.
- 2-to-3 peak height: 3.02546756595e-3 per keV.
- Maximum 8-to-16 normalized-shape relative difference: 4.52e-16.
- Maximum Gauss-Legendre-512 vs original-variable SciPy-quad relative difference: 2.91e-15.
- Exact vs heavy-particle endpoint difference: 0.00798555 keV.

The 2-to-2 step-function area is evaluated analytically; applying trapezoidal integration across its discontinuous endpoints gives a grid-dependent value and is not used as the normalization check.

## Existing source-record consistency findings

The numerical test was based on the already merged LZ Fig. 2 reproduction record at commit `8902abdb8bc44cad690059f9985204b4c0737657` (PR #77). Static inspection of its pinned source, manifest, README, tests, and archived outputs finds several reproducibility mismatches:

1. `run_manifest.json` passes `--source-pdf`, but `reproduce_fig2.py` does not define that CLI argument.
2. The README describes vector-path extraction and output figure files that the committed script does not create; the script saves `fig2_reproduction.svg` only.
3. The archived CSV header differs from the field names emitted by the committed script.
4. The manifest records five tests, while the only test file in the directory contains four test methods.
5. The README lists `paper_fig2_vector_digitized.csv` and two SVG files that are not present in the committed directory tree.

These are historical observations from a prior read-only inspection, not changes made by this Skill PR. The referenced LZ repository is private and its source bytes are not included in this public evaluation bundle. They are therefore not independently revalidated by the current public CI and must not be presented as CI-verified findings. The original LZ repository was not modified.

## PDF figure audit

The audited input is `paper-source/figures/fixed_speed_recoil_spectra_v2.pdf` from the LZ repository at the same source commit. Its SHA-256 is recorded in [`pdf/audit_result.json`](pdf/audit_result.json).

The local content-stream audit found 37 text runs, a minimum effective size of 6.48 pt, zero runs below the 5 pt screening threshold, zero character/word-spacing issues, and no parser warnings. The one-page figure was rendered at 180 dpi and visually inspected. The 5 pt value is a screening threshold only; no journal-specific compliance claim is made.

The local audit implementation was reconstructed from the method of the pinned Nature Skills script, but its byte identity with the upstream Git blob was not established. The reconstructed script is included alongside the audit result.

## Latest installer hardening status

At the later installer review, two additional safeguards were added:

- Rollback cleanup preserves the previous installation backup unless the new installation is confirmed present or no backup remains.
- Existing installation manifests are now checked for the expected source repository, a 40-character lowercase commit SHA, all required Skill files, valid 64-character SHA-256 entries, and an exact match with the installed file inventory.

The Windows PowerShell regression script now contains six rollback-cleanup cases and seven manifest-integrity cases (13 total). The Python Skill contract suite now contains seven tests, including a check that the installer helper and Windows regression script are included.

**Superseded by current-head CI:** Windows PowerShell 5.1 installer run #46 passed all 6 rollback-cleanup and 7 manifest-integrity cases. Candidate validation run #1310 passed the Skill contract suite, the full central unit suite (51 tests), and the Benchmark evaluator suite (46 tests). These results apply to PR HEAD `653c2a16c44482cea77ae11ee0459516c0c1adff`. The workflow tests the installer helpers and script parsing; it does not perform a full user-level installation on the user's Windows host.

## Windows Codex discovery

The Windows follow-up used PR head `92e57041218bae574b2acfbd2c8eda5a61a89648`, Windows build 26300, Codex Desktop 26.1117.4957.0, and bundled codex-cli 0.171.0-alpha.13.

| Check | Result |
| --- | --- |
| PowerShell diagnostic | Exit 0 after copying the complete Skill to the isolated worktree's `.agents/skills/high-energy-theory-research/`. All eight references were present. |
| Desktop discovery and invocation | The native picker showed the Skill as project-scoped. A fresh turn selected it and read `SKILL.md` and `references/symbolic-calculation.md` with PowerShell. |
| CLI discovery | The app-server `skills/list` returned the Skill enabled with `scope: repo`. |
| CLI reference loading | Two fresh read-only invocations reached Skill selection but failed to start the PowerShell subprocess because the Windows runtime provisioning service was unavailable. Reference loading in that CLI mode remains unverified. |

The local Windows Python 3.12.14 checks passed 60 schema checks, 83 candidate fixture expectations, 16 semantic expectations, 29 integration tests, and 45 unit tests, including the six Skill contract tests. The schema validator used `PYTHONUTF8=1` on the GBK-default host. This follow-up uses local acceptance evidence.

## Reproduction commands

From the evaluation root:

```bash
python symbolic/derive_phase_space_jacobian.py
python numerical/convergence_phase_space.py
python pdf/audit_pdf_text_reconstructed.py /path/to/fixed_speed_recoil_spectra_v2.pdf --min-pt 5.0 --json
```

The PDF is not duplicated in this evaluation folder; its repository path, source commit, and SHA-256 are recorded in [`pdf/audit_result.json`](pdf/audit_result.json).


## Current review boundary — 2026-11-24

- The current PR head is `653c2a16c44482cea77ae11ee0459516c0c1adff`.
- Current-head CI: Candidate validation Run 1310 succeeded; Windows PowerShell 5.1 installer Run 46 succeeded.
- The symbolic Jacobian script's factor-2 comparison is an analytic candidate-kernel diagnostic. It does not fetch or execute the private LZ source; the separate historical LZ source-audit observations above are not revalidated by public CI.
- Formal ChatGPT Web A/B runs have not started. Benchmark protocol v1.1 requires backend wall time, per-call tool counts, and tool logs that the current Web UI does not expose. Upgrade to a Web-observable v1.2 protocol and re-freeze the environment before any formal run.
