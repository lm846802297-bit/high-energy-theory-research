# Development task T03 — source-grounded paper reading

Status: development only; may be used to improve the Skill.

## Input source

Use the immutable source PDF:

- Repository: `lm846802297-bit/LZ-3-body-for-hdm`
- Commit: `8902abdb8bc44cad690059f9985204b4c0737657`
- Path: `paper-source/figures/fixed_speed_recoil_spectra_v2.pdf`
- SHA-256: `9eb61ea4dc77c6a23af29aa1d2887b692488daa9e997d59f0c7aea28c8be9df1`

The PDF is a figure source, not a full paper. Do not describe it as a complete manuscript.

## Prompt

Inspect the exact PDF above and produce a source-grounded figure-reading note.

1. Identify the original PDF page number and the visible panel structure.
2. Transcribe the axis labels, units, legend entries, and visible curve distinctions exactly.
3. Separate direct visual observations from physical interpretation.
4. Identify which information cannot be established from this figure alone.
5. Cite the original PDF page and source path for each claim.

If the source PDF cannot be retrieved byte-for-byte and its SHA-256 verified, stop and report the missing input rather than substituting a web image or another PDF.

## Evaluator notes (not shown to the model)

- Verify the source SHA-256 before scoring.
- Score exact transcription, page provenance, and the distinction between observation and interpretation.
- This task evaluates source-grounded figure reading, not the correctness of the underlying physics model.
