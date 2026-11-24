# Protocol v1.3 run artifacts

This directory is exclusively for the GPT-6 / Extra High protocol v1.3 cohort.

- Store A run records under `run-artifacts/records/no-skill/`.
- Store B run records under `run-artifacts/records/with-skill/`.
- Store each run's visible-answer capture, evidence, evaluator payloads, and native outputs beneath `run-artifacts/`, using unique run-specific paths.
- The `records/` directory is the input to `evaluate_v1_3.py compare --records-dir`; the full `run-artifacts/` directory is its `--artifact-root`.
- Keep A and B conversations, workspaces, transcripts, and artifact paths separate.
- Run IDs should identify protocol, task, repetition, and arm (for example `v1.3-T01-r1-A` and `v1.3-T01-r1-B`).
- Record the frozen seed `20261124` and the preassigned pair order from `protocol/v1.3/experimental-design.md`.
- Do not place v1.2 artifacts here or v1.3 artifacts in the legacy v1.2 directories.
- No run record is created until the corresponding fresh independent ChatGPT conversation has actually occurred.
