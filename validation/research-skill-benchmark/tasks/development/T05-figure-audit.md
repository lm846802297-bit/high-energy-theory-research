# Development task T05 — scientific figure integrity audit

Status: development only; intended for Round 2.

This task contains two separate pipelines. Do not claim that the CSV-to-SVG generator in Part B produced the PDF in Part A.

## Immutable input bundle

All files below are pinned to commit `8902abdb8bc44cad690059f9985204b4c0737657` in `lm846802297-bit/LZ-3-body-for-hdm`.

### Part A — PDF audit target

- Path: `paper-source/figures/fixed_speed_recoil_spectra_v2.pdf`
- Git blob SHA-1: `5f2d7a7192c0b3d78fa057ea8a004305f0ae13e8`
- SHA-256: `9eb61ea4dc77c6a23af29aa1d2887b692488daa9e997d59f0c7aea28c8be9df1`
- Size: 30,288 bytes

### Part B — separate CSV-to-SVG source pipeline

Model-visible inputs:

- Generator: `research/three_body_calculation_and_validation/plot_user_dsigma_curve.py`
  - Git blob SHA-1: `1a1fd7ccca9961d10d4eea83df66ecaaf8377baa`
  - Size: 8,378 bytes
- Data: `research/three_body_calculation_and_validation/results/fixed_speed_xe131_dsigma_450kev.csv`
  - Git blob SHA-1: `a3b590d1705d1478a293eb9e37f6587f2040d57c`
  - Size: 9,348 bytes
- Minima: `research/three_body_calculation_and_validation/results/local_minima_refinement_1keV.csv`
  - Git blob SHA-1: `423bce6526ae931f6d0b95262e3a405872e44d48`
  - Size: 3,949 bytes

Golden SVG outputs are evaluator-only and must not be placed in either model workspace.

## Prompt

### Part A — audit the PDF

1. Verify PDF Git blob identity and SHA-256.
2. Render the final page at a recorded resolution and inspect at intended physical size.
3. Audit effective text sizes and exact threshold. Treat 5 pt only as a screening value unless a target-journal rule is independently established.
4. Check labels, units, legends, line styles, panel layout, collisions, clipping, vector/raster content, and effective raster resolution.
5. Assess visual encoding using evidence available in the PDF. Do not claim source-data fidelity where source data are unavailable.

### Part B — reproduce the separate CSV-to-SVG pipeline

1. Verify Git blob identities and byte sizes of the generator and both CSVs; compute SHA-256 for each staged input.
2. Inspect plotted fields, transformations, axis scales, labels, units, and derived ratios.
3. Run the unmodified generator in an isolated copy of the pinned input tree:

```bash
python plot_user_dsigma_curve.py --csv results/fixed_speed_xe131_dsigma_450kev.csv --minima results/local_minima_refinement_1keV.csv --out-dir results/plots
```

4. Confirm both SVGs are generated; record their SHA-256 values and inspect the rendered figures.
5. Independently spot-check plotted coordinates against the raw CSV and verify the response ratio uses the stated GCN/JJ55 columns.
6. Do not modify source or raw CSVs to force a match.

## Required output

- Part A audit report, native rendered page, and machine-readable JSON.
- Part B input hash manifest, exact command, environment, stdout/stderr, both SVGs, and output hashes.
- Visual inspection notes and explicit PASS/FAIL/NOT AUDITABLE per check.
- Explicit statement that Part A and Part B are separate source pipelines.

The evaluator compares Part B outputs with sealed reference SVGs; their paths and hashes are not model-visible.