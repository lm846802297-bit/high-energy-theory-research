# High-Energy Theory Research Skill evaluation — 2026-11-22

This is a bounded evaluation record for PR #27 in `lm846802297-bit/high-energy-theory-research`. It evaluates the new Skill modules using a symbolic phase-space derivation, an independent numerical integration, and a PDF figure audit. It does not modify the original LZ research repository or claim Windows Codex runtime discovery.

## Contract test

- Test file: `tests/unit/test_skill_contract.py` from PR branch `feat/research-skill-optional-tooling-20261122`.
- Test source Git blob SHA-1: `4a2ad1da1c430760f442caa6ae7840f3a197cb8e`.
- Result: 6 passed, 0 failed.
- Environment: Python 3.13.5, Linux x86_64.
- Scope: the exact test file and PowerShell diagnostic were run against a minimal filesystem fixture. The PR's actual Skill/reference files were separately read from GitHub. This was not a full repository checkout or full unit-test suite.
- PowerShell was unavailable in the Linux environment; the Windows diagnostic was statically reviewed but not executed.

## Symbolic calculation

`symbolic/derive_phase_space_jacobian.py` verifies the Kallen factorization and the exact Jacobian for `s = Delta*u^2`. It finds that the existing LZ Fig. 2 phase-space shape kernel is half the unnormalized integral because it omits an overall factor of 2. This factor cancels after unit-area normalization, so the normalized shape is unchanged. It must be restored before using the kernel for an absolute phase-space factor, cross section, or rate.

The original-variable and transformed-variable mpmath integrals agree at 50 decimal digits for the stated dimensionless benchmark. See `symbolic/result.json`.

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

These are findings about the existing LZ reproduction record, not changes made by this Skill PR. The original LZ repository was not modified.

## PDF figure audit

The audited input is `paper-source/figures/fixed_speed_recoil_spectra_v2.pdf` from the LZ repository at the same source commit. Its SHA-256 is recorded in `pdf/figure_audit.json`.

The local content-stream audit found 37 text runs, a minimum effective size of 6.48 pt, zero runs below the 5 pt screening threshold, zero character/word-spacing issues, and no parser warnings. The one-page figure was rendered at 180 dpi and visually inspected. The 5 pt value is a screening threshold only; no journal-specific compliance claim is made.

The local audit implementation was reconstructed from the method of the pinned Nature Skills script, but its byte identity with the upstream Git blob was not established. The local script hash and upstream reference blob hash are both recorded in `pdf/figure_audit.json`.

## Windows Codex discovery

The read-only PowerShell diagnostic checks the repository source, project scope, user scope, required references, and CLI availability. It does not install or copy the Skill and cannot establish runtime discovery. The current Codex documentation lists `.agents/skills/` and `~/.agents/skills/`; openai/codex issue #40458 reports a Windows Desktop project-local discovery problem. The exact Windows host must still be tested in a fresh session. This remains the blocker before converting PR #27 from Draft to Ready for review.

## Reproduction commands

From the evaluation root:

```bash
python symbolic/derive_phase_space_jacobian.py
python numerical/convergence_phase_space.py
python pdf/audit_pdf_text_reconstructed.py /path/to/fixed_speed_recoil_spectra_v2.pdf --min-pt 5.0 --json
```

The PDF is not duplicated in this evaluation folder; its repository path, source commit, Git blob SHA-1, and SHA-256 are recorded in `pdf/figure_audit.json`.
