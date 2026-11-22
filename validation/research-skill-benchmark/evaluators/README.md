# Evaluators and blinded review

Evaluators are separate from model-visible task inputs.

## Deterministic evaluators

Use exact/symbolic checks, high-precision numerical references, input/output hashes, schema validation, and source-page/figure verification where possible.

A deterministic evaluator must:
- declare its inputs and versions;
- fail closed when required inputs are missing or hashes mismatch;
- distinguish a numerical tolerance check from a proof of physical correctness;
- emit machine-readable JSON and a human-readable summary;
- preserve failed cases and warnings.

## Human scoring

Two reviewers independently score each output using `protocol/scoring-rubric.yaml`. Reviewers receive anonymized outputs with arm labels removed. They should not see prompts indicating whether a Skill was used.

Resolve disagreements using a third adjudicator or a documented consensus process. Preserve both initial scores and the adjudication.

## Separation

Do not mount evaluator keys, gold answers, or holdout prompts into A/B model workspaces. Keep the evaluator environment read-only with respect to native run outputs.

No benchmark result is considered valid without task/input hashes, run records, and evaluator versions.
