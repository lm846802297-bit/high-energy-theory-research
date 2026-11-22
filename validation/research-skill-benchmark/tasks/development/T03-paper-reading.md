# Development task T03 — source-grounded paper reading

Status: development only; may be used to improve the Skill.

## Immutable source

Use the complete manuscript PDF:

- Repository: `lm846802297-bit/axial-vector-review-response`
- Source commit: `a7ac6456dafb27492183912fe4abbaa73a9455f7`
- PDF path: `archive/manuscript-baselines/axial_vector_model_building-v6.pdf`
- Git blob SHA-1: `be8f472a8cc3c35975dcb5970c9be996fde2d985`
- File size: 2,759,986 bytes
- Companion TeX source: `overleaf-source/axial-vector-model-building-v6/main-v6.tex`
- Companion TeX blob SHA-1: `b99f9e26a0b57acd0a4938ea6e03fc691a82becb`

Before starting, verify the downloaded PDF's Git blob identity against the pinned source commit and calculate its SHA-256 locally. Record both identifiers in the run manifest. Do not substitute a newer manuscript, a web-rendered image, or another PDF.

## Prompt

Read the manuscript and prepare a source-grounded research note focused on the paper's pure-axial benchmark and its main existing-constraints figure.

1. State the paper's model setup and the assumptions that define the pure-axial effective-current benchmark. Distinguish the full UV model from the reduced phenomenological limit.
2. Locate the equation that defines the reduced (A') interactions with charged leptons and neutrinos. Give its original equation number, PDF page, conventions, and the sign/chirality structure of each current.
3. Locate the two-panel existing-constraints plot labelled `fig:allconstraints` in the companion TeX source. Identify its original figure number and PDF page.
4. Explain what each panel plots, the meanings of the contours and dashed line, and the assumptions attached to the scalar-decoupling benchmark.
5. Identify which displayed curves are described in the manuscript as indicative recasts or rate-level estimates rather than official experimental limits.
6. Trace the figure's main physical claims to the relevant equations and nearby manuscript discussion. Separate what the authors calculate, reinterpret, assume, and explicitly leave for future detector-level work.
7. Report any information that cannot be established from the PDF or its companion source. Do not invent page numbers, equation numbers, experimental interpretations, or numerical values.

Cite the original equation/figure numbering and PDF page for every source-dependent claim. Preserve the manuscript's terminology and distinguish direct source statements from your own reconstruction.

## Required output

- Source identity and verified hashes.
- Short model/benchmark summary.
- Equation and Figure locator table with original numbering and PDF pages.
- Panel-by-panel figure interpretation.
- A claim/evidence/assumption table.
- Explicit unresolved or not-reported items.
