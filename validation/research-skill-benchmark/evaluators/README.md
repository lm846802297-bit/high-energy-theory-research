# Evaluators and blinded review

The evaluator workspace is separate from model-visible task inputs. The pinned registry is evaluators/manifest.json; it contains evaluator identities, input hashes, evaluator-only golden outputs, and manual-review responsibilities. Do not mount the registry, golden outputs, or development-key.md into A/B model workspaces.

## Deterministic evaluator package

Runtime dependencies are pinned in evaluators/requirements.txt. The lightweight CI/unit-test dependencies are pinned separately in evaluators/requirements-test.txt. The package uses Python 3.12+ and JSON Schema Draft 2020-12. The central schema-validation workflow runs both JSON Schema meta-validation and the 33-test evaluator suite, then executes the pinned T01/T02 symbolic/numerical references and the T05 PDF/data-to-figure checks. T03 remains a blinded human source-review task.

- evaluate.py validate-run: validates a run record, verifies A/B-specific Skill fields, checks budget limits and reviewer consensus/adjudication, verifies every artifact's actual SHA-256 under a required artifact root, and recomputes Q from the five dimension scores.
- evaluate.py validate-pair: verifies exactly one A and one B record, identical common controls, distinct transcript and artifact paths, the locked Skill commit, and the task-specific Skill reference.
- evaluate.py verify-sources: verifies staged input byte size, Git blob SHA-1, and SHA-256 against the development task manifest. The staged input tree preserves the repository slug followed by the original repository path.
- evaluate.py compare: pairs immutable records, rejects missing/duplicate pairs, requires each run's source-file bundle to match the task manifest and verifies staged source bytes, Git blob IDs, sizes, and SHA-256, computes task and task-family effects, performs the preregistered cluster bootstrap for a sufficiently complete Round 2 holdout, and emits the comparison report.
- verify_dirac_trace.py: independent 4x4 Dirac-representation trace and Clifford-algebra check for T04; Python standard library only.
- verify_repro_package.py: independently verifies T06 source/input/output hashes and recomputes the weighted mean from the exact CSV bytes. It deliberately does not execute model-generated source code.
- verify_figure_regeneration.py: verifies the pinned T05-B generator, model-visible CSVs, evaluator-only golden SVGs, runs only the trusted pinned plotting script in a temporary workspace, compares exact plotted path data, SVG structure/labels and coordinates within 0.01 px against historical Golden files, and (for scored runs) compares submitted model SVGs byte-for-byte with fresh trusted-generator outputs.

The T01/T02 symbolic reference and the T02 LZ-specific convergence program are pinned in the registry. The latter is a supporting cross-check, not the numerical oracle for the T02 GeV benchmark. T05-A's PDF text-size scanner is a screening tool; it does not replace visual inspection or establish journal compliance. T05-B uses the historical Golden SVGs for semantic curve/structure checks; exact byte comparison is reserved for model submissions versus fresh trusted-generator output.

All source files are staged once before A/B runs. The preferred policy is offline after staging. The evaluator fails closed on missing files, size/hash mismatches, invalid schemas, control mismatches, over-budget runs, missing scores, and incorrect composite scores. It preserves failed records and does not modify inputs.

## Blinded human scoring

Two reviewers independently score anonymized outputs without seeing the arm label. Preserve both original score sheets. A one-point disagreement requires a documented consensus note. A two-point disagreement, hard-gate disagreement, or disagreement about fabricated evidence requires a third adjudicator. Preserve pre-adjudication scores, consensus notes, adjudication, exact agreement, and quadratic-weighted Cohen's kappa.

## Pair integrity

The run-record Schema enforces A/B-specific Skill availability. The pair checker additionally requires equality of model/settings, runtime/hardware, project instructions/workspace, task prompt/source hashes, tools/versions, network policy, budgets, randomization seed, and pair order. Only Skill availability, Skill commit/manifest, invocation, and B's loaded task-specific references may differ. Any mismatch invalidates the entire pair; rerun both arms with a new pair ID.

## Separation and security

Do not expose evaluator keys, golden outputs, or Holdout prompts to model workspaces. The Git repository is not a security boundary. For sealed Holdout, use a separate private evaluator repository and a model workspace without repository history or external network access. Keep native outputs read-only during scoring.

No benchmark result is valid without run records, source/input hashes, evaluator versions, pair-integrity checks, and blinded review.
