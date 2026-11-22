# Development task T05 — scientific PDF figure audit

Status: development only; intended for Round 2.

## Immutable input

- Repository: `lm846802297-bit/LZ-3-body-for-hdm`
- Commit: `8902abdb8bc44cad690059f9985204b4c0737657`
- Path: `paper-source/figures/fixed_speed_recoil_spectra_v2.pdf`
- Git blob SHA-1: `5f2d7a7192c0b3d78fa057ea8a004305f0ae13e8`
- SHA-256: `9eb61ea4dc77c6a23af29aa1d2887b692488daa9e997d59f0c7aea28c8be9df1`

## Prompt

Verify the PDF identity, render the final page at a recorded resolution, and audit the figure.

Check:
1. Effective text sizes and the exact threshold used. Treat 5 pt only as a screening value unless a target-journal rule is independently established.
2. Axis labels, units, legends, line styles, and visible panel layout.
3. Text/curve/legend collisions and clipping.
4. Vector/raster content and effective raster resolution where applicable.
5. Whether the figure's visual encoding preserves the original data and physical meaning.

Retain the audit script/version, exact command, environment, machine-readable report, rendered page, and hashes. State the scope and limitations of every automated check. Do not claim journal compliance from a generic threshold.

## Required output

An audit report, native rendered image, machine-readable JSON, and explicit PASS/FAIL/NOT AUDITABLE outcomes for each check.
