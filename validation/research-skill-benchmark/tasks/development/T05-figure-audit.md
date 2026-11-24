# Development task T05 — public-source scientific figure integrity and AFH response reproduction

Status: development task; included in protocol v1.1. The two parts are separate source pipelines.

This task uses only public GitHub repositories. It does not access or depend on the private LZ-3-body-for-hdm repository.

## Immutable public input bundle

### Part A — paired paper figure panels

Repository: lm846802297-bit/axial-vector-review-response

Pinned source commit: 80fef16fa73f77b5374e50e076ffaeaf71df3b76

The two single-panel PDFs are the left and right panels of the same existing-constraints figure in the axial-vector model manuscript.

1. Left panel:
   - Path: overleaf-source/axial-vector-model-building-v6/plots/axial_vector_constraint.pdf
   - Git blob SHA-1: 2c99971dd49595946e10cc2c58fc8ed5e7db6000
   - SHA-256: 376b232856af01995abe5b7350bc1ecc357d51c3b93002b23c8946a0b81f5adb
   - Size: 681,479 bytes
2. Right panel:
   - Path: overleaf-source/axial-vector-model-building-v6/plots/axial_vector_constraint_g_vs.pdf
   - Git blob SHA-1: 918ae390bc57c146e4c27637189fe16c33536a1a
   - SHA-256: a523d9e801a4fadf749bef3294fcf5ba3905d68f9077a41d4cea43e095cf1a4d
   - Size: 595,427 bytes
3. Companion manuscript source:
   - Path: overleaf-source/axial-vector-model-building-v6/main-v6.tex
   - Git blob SHA-1: b99f9e26a0b57acd0a4938ea6e03fc691a82becb
   - SHA-256: de9132ba936c6b1f3701d7c5a6398e39b89357903be789953972527753540e9a
   - Size: 71,477 bytes

The companion TeX includes both panels at 0.48\textwidth and gives their shared caption. Use it to establish the intended physical width and the figure's model assumptions. Do not infer figure page numbers from TeX line numbers.

### Part B — native Xe-131 AFH response data and reproducible SVG views

Repository: lm846802297-bit/radiative-dark-matter-nuclear-currents

Pinned source commit: 9ed185aefe29cebbaaf575c5b2ae4b3fc16b0078

1. Native Xe-131 response CSV:
   - Path: nuclear/afh/data/native_v6_2026-11-22/native/afh_v6_xe131_eight_response_native.csv
   - Git blob SHA-1: ea2aca029b6f298f79fc009a17d6fb73d53da36e
   - SHA-256: 585ab0f483be0d8131566cefc4cb420c6db7e07bebbcd2b887da568cda2f4ffb
   - Size: 538,596 bytes
2. Native Wolfram exporter:
   - Path: nuclear/afh/data/native_v6_2026-11-22/source/run_afh_full_response_database.wls
   - Git blob SHA-1: c815500398d7f55de079dffbaaa846bc84de81f5
   - SHA-256: 10b254971a1f9dade783cfdf603f15885b08894e4de54aae2791243bf3369642
   - Size: 2,947 bytes
3. Original run manifest:
   - Path: nuclear/afh/data/native_v6_2026-11-22/run_manifest.json
   - Git blob SHA-1: a7b271f1ecd8eacc0a29d67623a2ae1c31e341a6
   - SHA-256: 5cc300da9d199946a6d9df08c8e448d2ddd426a50f4310a9984ce1c1e06b39f7
   - Size: 10,803 bytes
4. Dataset README:
   - Path: nuclear/afh/data/native_v6_2026-11-22/README.md
   - Git blob SHA-1: b987e3b12f710dad834af7909b367e6caa05e2da
   - SHA-256: f79b51c251b164a4f0e144e06def48e434b408b98538e3e791db87d2bcf43101
   - Size: 2,138 bytes
5. Dataset checksum list:
   - Path: nuclear/afh/data/native_v6_2026-11-22/SHA256SUMS.txt
   - Git blob SHA-1: 20dfa29c8bf3c74be74a0841aea4f0ac66a5f939
   - SHA-256: 3ec08fd0fb76a93b94d21ee12b3f3a06db2fc40ac46d94aa376995629e7b81a9
   - Size: 2,473 bytes

The public repository documents 2,401 momentum points for Xe-131, q_A from 0 to 0.6 GeV, eight response columns, and zero native imaginary residual. The native database was compared against a source-translated Python reference for 16,807 isotope/q rows at rtol=5e-7, atol=2e-12; the maximum combined-tolerance utilization was 0.05879.

The original AFH package is not redistributed. The WLS file is the retained Native exporter and the run manifest records the original package version and source hash. Do not claim that running this exporter from the public bundle regenerates the native CSV, and do not execute or invent the unavailable package.

6. Deterministic plotting adapter supplied with this benchmark:
   - Repository: lm846802297-bit/high-energy-theory-research
   - Source commit: b540b0cb5ef030147b0ceb2357506b02e5f218ea
   - Path: validation/research-skill-benchmark/tools/plot_afh_xe131_responses.py
   - Git blob SHA-1: f68c3beb0c02048a566d7454a9232ff2041af032
   - Size: 12,692 bytes

This adapter uses only the Python standard library. It creates two deterministic SVG views from the pinned CSV: six positive diagonal responses on a logarithmic axis, and the two signed interference responses on separate symmetric-log panels. It is a presentation transformation, not a new AFH calculation.

## Prompt

### Part A — audit the paper figure

1. Verify the Git blob SHA-1, byte size, and SHA-256 of both PDF panels and the companion TeX source.
2. Read the TeX around the two includegraphics commands and the shared caption. Explain which physical variables each panel displays and how the right panel is mapped from the left panel.
3. Render both PDFs at the intended width implied by 0.48\textwidth, at a recorded resolution of at least 300 dpi. Preserve the rendered PNGs as native run artifacts.
4. Run the deterministic PDF text-size screen on both panels with --min-pt 5.0. Report the minimum effective text size, text-run count, below-threshold count, spacing-issue count, and warnings separately for each panel.
5. Inspect the rendered panels at intended physical size. Check axis labels and units, tick readability, legend placement, contour identities, dashed perturbativity boundary, line styles, clipping, overlap, and color/line distinguishability.
6. Explain the figure caption's assumptions: pure-axial effective-current benchmark, scalar-decoupling choice, the meaning of the dashed perturbativity boundary, and the fact that the right panel contains no additional likelihood information.
7. Distinguish the PDF text-size screening result from the actual visual inspection. Five points is a screening threshold in this task, not an independently established journal requirement.

### Part B — audit data provenance and reproduce the separate AFH response views

1. Verify Git blob SHA-1, byte size, and SHA-256 for the CSV, Native WLS exporter, run manifest, README, checksum list, and benchmark plotting adapter.
2. Cross-check the CSV SHA-256 against the repository's SHA256SUMS.txt entry. Read the README and run manifest to report the original AFH version, Native Wolfram version, source-package hash, isotope, q-grid, response columns, normalization convention, and recorded independent comparison status/tolerances.
3. Confirm the CSV contains exactly 2,401 Xe-131 rows with strictly increasing q_GeV from 0 to 0.6 GeV, all eight real response columns, and the documented imaginary-residual behavior.
4. Run the unmodified plotting adapter:
   python high-energy-theory-research/validation/research-skill-benchmark/tools/plot_afh_xe131_responses.py --csv radiative-dark-matter-nuclear-currents/nuclear/afh/data/native_v6_2026-11-22/native/afh_v6_xe131_eight_response_native.csv --out-dir results/plots
5. Preserve both generated SVGs and their SHA-256 values. Render both SVGs for visual inspection.
6. Explain why the diagonal responses use a logarithmic axis and why the interference plot must preserve signs. Check the plotted endpoint values and at least three interior q points against the raw CSV.
7. Do not apply the factor-four equal-proton/equal-neutron conversion to the raw AFH columns. Do not replace signed interference terms by absolute values.
8. State explicitly that the native response dataset's recorded Python comparison does not validate the complete P3-C particle-nuclear current contraction.

## Required output

- Source identity and a machine-readable SHA-256/Git-blob manifest for every input.
- Part A: two rendered panel PNGs, two PDF screening JSON results, a concise visual audit, and explicit PASS/FAIL/NOT AUDITABLE for each check.
- Part B: input provenance audit, native generator/source interpretation, both SVGs, SVG hashes, rendered previews, and independent CSV-coordinate spot checks.
- Exact command, Python version, operating system, environment, stdout/stderr, and runtime.
- An explicit statement that Part A is a paper-PDF audit and Part B is a separate native-CSV-to-SVG presentation pipeline.
- Do not claim that the plotting adapter recalculates AFH responses or that the original WLS exporter can run without the unbundled AFH package.
