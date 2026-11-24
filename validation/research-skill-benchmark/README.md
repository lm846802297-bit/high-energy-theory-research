# Particle Physics Research Skill Benchmark

Status: **Protocol v1.2 is in draft; Round 1 remains 18 T01/T02/T03 A/B model runs. No model runs have started.**

This benchmark tests whether the shared high-energy-theory-research Skill improves scientific work relative to the same GPT model without that Skill.

## Research question

Does the Skill improve scientific quality, independent validation, reproducibility, and evidence quality without materially reducing method-selection autonomy?

- **A — No Skill:** GPT-6 Pro (Astra Pro), Pro-default reasoning; the installed plugin is not selected or invoked.
- **B — With Skill:** identical controls; Particle Physics Research v0.2.0 is selected and explicitly invoked.

Only Skill availability/invocation and task-tier routing behavior are intentionally changed.

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

T01 and T02 share the threshold_kinematics family and count as one independent task-family cluster. T05-A audits two public axial-vector paper figure panels; T05-B separately reproduces SVG views from public Native AFH Xe-131 response data. The two source pipelines are not conflated.

## Evaluator commands

From the benchmark root, install the lightweight pinned test dependencies and run:

    python -m pip install -r evaluators/requirements-test.txt
    python -m unittest discover -s evaluators -v

The CI workflow also validates both JSON Schemas with Draft 2020-12, parses the JSON manifests and scoring YAML, runs the evaluator unit suite, executes the pinned T01/T02 symbolic and numerical references, screens both public T05 PDF panels and self-tests the Native AFH Xe-131 CSV-to-SVG pipeline.
    python evaluators/evaluate.py validate-run path/to/run-record.json --artifact-root path/to/run-artifacts
    python evaluators/evaluate.py validate-pair path/to/A.json path/to/B.json --artifact-root path/to/run-artifacts
    python evaluators/evaluate.py verify-sources --input-root path/to/staged-inputs
    python evaluators/verify_dirac_trace.py --json-out path/to/dirac-check.json
    python evaluators/verify_repro_package.py --source path/to/solution.py --input path/to/input.csv --output path/to/result.json --manifest path/to/manifest.json
    python evaluators/verify_public_t05.py --part pdf --task-manifest tasks/development/manifest.json --evaluator-manifest evaluators/manifest.json --input-root path/to/staged-inputs --pdf-audit-script path/to/audit_pdf_text_reconstructed.py --output path/to/t05-pdf-audit.json

For a scored T05 run, pass the model's submitted SVG directory to the public T05 evaluator:

    python evaluators/verify_public_t05.py --part figures --task-manifest tasks/development/manifest.json --evaluator-manifest evaluators/manifest.json --input-root path/to/staged-inputs --submitted-output-root path/to/run-artifacts/results/plots --output path/to/t05-afh-figure-check.json

For Round 1, use the development task manifest. For Round 2, pass the sealed evaluator's combined holdout task manifest explicitly:

    python evaluators/evaluate.py compare --records-dir path/to/run-artifacts/records --task-manifest path/to/evaluator-only/holdout-manifest.json --evaluator-manifest path/to/evaluator-only/evaluators/manifest.json --analysis-plan path/to/evaluator-only/experimental-design.md --environment-lock path/to/evaluator-only/environment-lock.json --rubric path/to/evaluator-only/scoring-rubric.yaml --round round_2_full --seed 12345 --protocol-commit COMMIT_SHA --artifact-root path/to/run-artifacts --input-root path/to/staged-inputs --output reports/comparison.json

The compare command consumes immutable A/B run records and a task manifest, verifies every artifact's actual bytes, requires each task's declared deterministic evaluators, checks each ID against the pinned registry and task association, validates evaluator JSON payloads against registry JSON Schemas, binds the exact protocol commit and the exact bytes of the task manifest, scoring rubric, environment lock, analysis plan, and evaluator registry to each run record, recomputes the canonical input-manifest hash, verifies prompt_sha256 against the exact task prompt file, checks result status and input/output hash bindings, recomputes scores, validates pairs, calculates task-family summaries, and writes a comparison report. Round 1 is never classified as confirmatory. The evaluator never executes model-generated source code.

## Current status

- Benchmark and development tasks are in central PR #27.
- Protocol v1.2 adapts run records to ChatGPT Web observability. The Environment Lock remains draft until a fresh conversation confirms the v0.2.0 Skill runtime.
- T05 uses public pinned inputs from axial-vector-review-response and radiative-dark-matter-nuclear-currents; no private LZ repository access or token is required.
- Web run records distinguish visible-turnaround upper bounds from backend wall time, and permit tool-call counts to remain null when per-invocation logs are unavailable.
- The original five weighted dimensions are unchanged. Unnecessary-computation count/events, method-selection autonomy, reproducibility evidence items, and observable resource measures are reported separately.
- No formal model A/B run has started; no Skill module has been accepted or rejected.
- The evaluator manifest, reference outputs, and development key are evaluator-only and must not be mounted into model workspaces.
- Holdout prompts/keys have intentionally not been created; an independent evaluator prepares them only after protocol and Skill freeze.
- No formal A/B runs have been executed.

See the experimental design, scoring rubric, environment lock, and evaluator guide in this directory.


## ChatGPT Web observability — protocol v1.2

- `visible_turnaround_upper_bound_seconds` is UTC send time to first observation of the complete visible answer. It is not backend latency.
- `visible_ui_worked_label` is recorded separately and must not be substituted for the visible-turnaround measure.
- `backend_wall_time_seconds`, `tool_call_count`, and `token_count` are null when the host does not expose them. Missing logs do not mean zero tool calls.
- `tool_call_limit` is null for the current Web host. The evaluator rejects a hard tool-call cap when the count cannot be certified.
- The visible-answer Markdown file is the transcript artifact; it is not a backend raw transcript unless `backend_transcript_available` is true.
- The 30-minute Round 1 limit applies to the visible-turnaround upper bound in both arms.
