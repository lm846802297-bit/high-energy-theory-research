# Particle Physics Research Skill Benchmark

Status: **protocol draft — not frozen; no formal A/B runs have been executed.**

This benchmark tests whether the shared high-energy-theory-research Skill improves scientific work relative to the same GPT model without that Skill.

## Research question

Does the Skill improve scientific quality, independent validation, reproducibility, and evidence quality without materially reducing method-selection autonomy?

- **A — No Skill:** fixed model, tools, project instructions, inputs, and budget; shared Skill is unavailable.
- **B — With Skill:** identical controls; the pinned shared Skill is available and explicitly invoked.

Only Skill availability/invocation is intentionally changed.

## Structure

- protocol/: pre-registered design, scoring rubric, environment lock, and JSON Schemas.
- tasks/development/: tasks that may be used to improve Skill instructions.
- tasks/holdout/: sealed final-evaluation area; do not use during development.
- runs/no-skill/ and runs/with-skill/: immutable run records and native outputs.
- evaluators/: deterministic validators, pinned evaluator registry, and blinded-review guidance.
- reports/: generated comparisons; no report is PASS until all run records and checks exist.

## Evaluation rounds

1. **Round 1 — Pilot:** T01, T02, T03; three repetitions per arm per task; 18 model runs. Descriptive only.
2. **Round 2 — Full:** all six dimensions plus sealed Holdout. Minimum 12 independent task-family clusters, 36 paired task runs, 72 model runs. Apply frozen statistical decision rules.
3. **Round 3 — Real projects:** read-only tasks in LZ, axial-vector, and ColliderAgent under a separate project-stratified plan.

T01 and T02 share the threshold_kinematics family and count as one independent task-family cluster. T05 contains a PDF audit and a separate CSV-to-SVG regeneration pipeline; the generator is not claimed to have produced the PDF.

## Evaluator commands

From the benchmark root, install the lightweight pinned test dependencies and run:

    python -m pip install -r evaluators/requirements-test.txt
    python -m unittest discover -s evaluators -v

The CI workflow also validates both JSON Schemas with Draft 2020-12, parses the JSON manifests and scoring YAML, and runs the same evaluator unit suite.
    python evaluators/evaluate.py validate-run path/to/run-record.json --artifact-root path/to/run-artifacts
    python evaluators/evaluate.py validate-pair path/to/A.json path/to/B.json --artifact-root path/to/run-artifacts
    python evaluators/evaluate.py verify-sources --input-root path/to/staged-inputs
    python evaluators/verify_dirac_trace.py --json-out path/to/dirac-check.json
    python evaluators/verify_repro_package.py --source path/to/solution.py --input path/to/input.csv --output path/to/result.json --manifest path/to/manifest.json
    python evaluators/verify_figure_regeneration.py --manifest evaluators/manifest.json --model-input-root path/to/staged-inputs --golden-root path/to/evaluator-goldens

For Round 1, use the development task manifest. For Round 2, pass the sealed evaluator's combined holdout task manifest explicitly:

    python evaluators/evaluate.py compare --records-dir path/to/run-artifacts/records --task-manifest path/to/evaluator-only/holdout-manifest.json --round round_2_full --seed 12345 --protocol-commit COMMIT_SHA --analysis-plan-sha256 ANALYSIS_PLAN_SHA256 --environment-lock-sha256 ENVIRONMENT_LOCK_SHA256 --artifact-root path/to/run-artifacts --input-root path/to/staged-inputs --output reports/comparison.json

The compare command consumes immutable A/B run records and a task manifest, verifies every artifact's actual bytes, recomputes scores, validates pairs, calculates task-family summaries, and writes a comparison report. Round 1 is never classified as confirmatory. The evaluator never executes model-generated source code.

## Current status

- Benchmark and development tasks are in central PR #27.
- Protocol remains draft pending Windows host capture and independent review.
- No model A/B result exists; no Skill module has been accepted or rejected.
- The evaluator manifest, reference outputs, and development key are evaluator-only and must not be mounted into model workspaces.
- Holdout prompts/keys have intentionally not been created; an independent evaluator prepares them only after protocol and Skill freeze.
- No formal A/B runs have been executed.

See the experimental design, scoring rubric, environment lock, and evaluator guide in this directory.
