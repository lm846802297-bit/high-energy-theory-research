# Scientific figure design and audit

Load this reference when producing, revising, or reviewing a figure that supports a physical statement.

## Figure starts from the physics

Before plotting, identify:

- the exact claim and parameter region the figure is intended to support;
- plotted variables, definitions, units, normalization, and coordinate transformations;
- theoretical curves, experimental constraints, benchmark assumptions, and validity domains;
- uncertainties, confidence levels, nuisance assumptions, and whether a band is statistical, systematic, theoretical, or combined;
- raw data/source files, transformations, interpolation, smoothing, binning, exclusions, and the plotting code.

Do not infer the physics from a template or a visual style.

## Particle-physics-specific checks

- Label axes with the physical quantity and unit, including powers and normalization conventions.
- For logarithmic axes, state the base/meaning where ambiguity exists and handle zero/negative values explicitly.
- Preserve disconnected allowed/excluded regions; do not join them for visual convenience.
- Distinguish theoretical consistency, perturbativity, vacuum stability, EFT validity, and experimental exclusion.
- Identify the experiment, analysis/release, observable, confidence level, luminosity/dataset, and assumptions for every experimental contour.
- For exclusion curves, do not imply that a displayed region is excluded beyond the actual analysis domain or stated assumptions.
- For theory curves, identify benchmark parameters, perturbative order, approximation, and numerical status.
- State the meaning of shaded bands and error bars in the legend or caption. Do not use one symbol for incompatible uncertainty definitions.
- Do not silently extrapolate, interpolate across failed points, clip inconvenient data, or conceal numerical instabilities.

## Multi-panel figures

Plan panels from the scientific argument. Each panel should contribute a distinct necessary piece of evidence. Align comparable axes and scales; document intentional asymmetry, insets, or exceptions. Keep source data and a panel-to-source mapping.

## Export and automated QA

Retain the plotting source, raw/processed data, environment and dependency versions, and editable native outputs (PDF/SVG where suitable) alongside publication formats.

Optional local audits include:

- PDF effective text size;
- multi-panel alignment from rendered geometry;
- text/line/image collision checks;
- SVG structural checks;
- image/PDF metadata and effective raster resolution.

Run audits on the final exported artifact, not only on an intermediate preview. Inspect the figure at its final physical size. Automated geometry checks cannot establish that a physical contour, axis transformation, error band, or claim is scientifically correct.

Use third-party figure Skills only as optional guidance. Do not copy protected assets or code unless the applicable license permits it. Never upload unpublished figures or data to an external image service without explicit authorization.
