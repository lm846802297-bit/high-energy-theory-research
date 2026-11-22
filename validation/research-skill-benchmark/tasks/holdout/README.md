# Holdout set — sealed evaluation

Status: **reserved; do not use during Skill development.**

Holdout prompts, input snapshots, and scoring keys must be kept out of model workspaces. The task IDs and input hashes should be registered here only after a separate evaluator has prepared the sealed package.

Rules:
- Do not place gold answers or detailed scoring keys in the model-visible workspace.
- Keep task prompts/input snapshots separate from evaluator keys.
- Record SHA-256 hashes for the sealed task package and evaluator key.
- Mount the evaluator key only in the scoring environment.
- If any holdout content is exposed to Skill authors or used to modify the Skill, invalidate that task and replace it.
- Do not report holdout performance until all paired A/B runs and blinded scoring are complete.

No holdout tasks have been prepared or run yet. This is intentional; the benchmark protocol must be frozen first.
