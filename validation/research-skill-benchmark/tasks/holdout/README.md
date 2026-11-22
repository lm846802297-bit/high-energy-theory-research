# Holdout set — sealed evaluation

Status: **reserved; do not use during Skill development.**

Holdout prompts, input snapshots, task manifest, evaluator mappings, and scoring keys must be kept out of model workspaces. A separate evaluator prepares the sealed package only after the final Skill commit, protocol, rubric, evaluator code, and analysis plan are frozen.

## Required package structure

The private evaluator package must contain:

- A task manifest with task ID, dimension, independent task-family ID, immutable input sources, and an explicit \`required_evaluators\` list for every task.
- Exact prompt and input snapshots, each with repository/commit/path, Git blob SHA-1, byte size, and SHA-256.
- Evaluator-only answer keys, golden outputs, and expected numerical results.
- A frozen scoring plan, sample-size plan, bootstrap seed, and hash of the analysis code.
- A mapping from every required evaluator ID to its pinned evaluator implementation and expected result-payload contract.

Every task must declare \`required_evaluators\`, even when it relies entirely on blinded human review (use an empty list). All non-empty evaluator IDs must exist in the pinned evaluator registry. The comparison evaluator rejects missing or failed required checks, mismatched input/output hash bindings, missing result artifacts, and invalid evaluator payloads. For T05-like figure tasks, the required data-to-figure check must run in submission mode and validate the model's actual submitted outputs; a CI baseline-only check is not sufficient.

## Blinding and handling rules

- Do not place gold answers, detailed scoring keys, evaluator registry, or Golden outputs in model-visible workspaces.
- Keep task prompts/input snapshots separate from evaluator keys and required-evaluator result contracts.
- Record SHA-256 hashes for the sealed task package, task manifest, evaluator key, and analysis plan.
- Mount the evaluator key only in the scoring environment.
- The Git repository is not a security boundary. Use a separate private evaluator repository and model workspaces without evaluator history or network access.
- If any holdout content is exposed to Skill authors or used to modify the Skill, invalidate that task and replace it.
- Do not report holdout performance until all paired A/B runs, required deterministic checks, and blinded scoring are complete.

## Minimum Round 2 design

The holdout must contain at least two independently authored task-family clusters per each of the six dimensions, with at least three paired repetitions per task: at least 12 independent task-family clusters, 36 paired task runs, and 72 model runs. A documented power analysis may increase, but not reduce, these minima.

No holdout tasks have been prepared or run yet. This is intentional; the benchmark protocol, Skill version, evaluator code, and analysis plan must be frozen first.
