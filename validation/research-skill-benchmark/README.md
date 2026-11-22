# Particle Physics Research Skill Benchmark

Status: **protocol draft — not yet frozen; no formal A/B runs have been executed.**

This benchmark tests whether the shared `high-energy-theory-research` Skill improves scientific work relative to the same GPT model working without that Skill.

## Research question

Does access to the shared Skill improve scientific quality, reproducibility, and evidence quality without materially reducing the model's ability to choose appropriate methods?

The primary comparison is:

- **A — No Skill:** the fixed model, tools, project instructions, and inputs; the shared Skill is unavailable.
- **B — With Skill:** the same model, tools, project instructions, and inputs; the pinned shared Skill is available and explicitly invoked for the task.

Only Skill availability/invocation is intentionally changed.

## Benchmark structure

- `protocol/`: pre-registered design, rubric, and environment record.
- `tasks/development/`: tasks that may be used while improving the Skill.
- `tasks/holdout/`: tasks reserved for final evaluation; do not use them to edit Skill instructions.
- `runs/no-skill/` and `runs/with-skill/`: immutable run records and native outputs.
- `evaluators/`: independent, deterministic checks and blinded-review guidance.
- `reports/`: generated comparisons. No report is a PASS until its required run records and checks exist.

## Three-round evaluation

1. **Round 1 — pilot A/B:** T01 theory/Jacobian derivation, T02 threshold numerical integration, and T03 source-grounded reading of the pinned axial-vector manuscript; three independent runs per arm per task (18 runs total).
2. **Round 2 — six dimensions:** add T04 symbolic Dirac trace, T05 PDF figure audit, and T06 reproducibility package. Use a separately prepared holdout set and blinded scoring.
3. **Round 3 — real projects:** evaluate in LZ, axial-vector, and ColliderAgent using read-only tasks first.

## Current status

- Benchmark directory and protocol are being added to central PR #27.
- No model A/B result exists yet.
- Model/build/runtime lock must be completed on the Windows Codex host before the protocol is frozen.
- Holdout prompts and scoring keys must remain unavailable to the model during scored runs.
- No Skill module is accepted or rejected by this benchmark yet.

See [experimental design](protocol/experimental-design.md), [scoring rubric](protocol/scoring-rubric.yaml), and [environment lock](protocol/environment-lock.json).
