# Experimental design — v1.0 draft

Status: **draft; freeze only after the target Windows Codex model/runtime is recorded. No formal A/B run has been performed.**

## 1. Hypothesis and estimand

The primary hypothesis is:

    H1: mean(Q_B - Q_A) > 0

A is the fixed GPT model without the shared Research Skill; B is the same model with the pinned Skill available and explicitly invoked.

The estimand is the paired difference in blinded scientific-quality score for the same task. Report task-level and task-family outcomes; a pooled run mean alone is not the primary result. This benchmark measures the incremental effect of the Skill package under the recorded runtime, tools, tasks, and project context. It does not claim to improve the underlying model.

## 2. Arms and controls

### A — No Skill

- The shared high-energy-theory-research Skill is not installed, mounted, or present in the accessible workspace.
- No Skill manifest or Skill-specific reference files are provided.
- The model receives the common task prompt, project context, and tool access.

### B — With Skill

- Install or mount the exact Skill commit recorded in the protocol lock.
- Explicitly invoke the shared Skill for the task.
- Load only the task-specific reference required by the Skill.
- Record the Skill source commit, installation manifest SHA-256, and loaded references.

### Identical in A and B

- Exact model label/build, reasoning effort, sampling settings, and system/developer configuration where exposed.
- Fresh conversation/session and clean working directory for every run.
- Same task prompt, input bytes, source snapshots, project instructions, tool allowlist, network policy, time/token budget, and stopping rule.
- Same OS, hardware/runtime, Python/compiler/package versions, and available external software.
- Same evaluator versions and reference answers; neither is exposed to the model.
- Remove the shared-Skill routing paragraph from the common AGENTS.md snapshot used by both arms, preserving all other project instructions byte-for-byte. Record the transformed snapshot hash. A must not be told that the Skill exists.
- Other project-specific Skills and tools remain identical in both arms; do not weaken the baseline by removing unrelated tools.

Stage all source inputs before a run. The preferred network policy is **offline after staging**: no external search or network retrieval during a scored task. If the actual host cannot enforce this, record the exact policy and invalidate any pair with asymmetric network access. The common harness must not mention the Skill in A. Skill availability/invocation is the only intended treatment difference.

If the host automatically exposes other Skills or changes tool permissions between arms, preserve the records and invalidate the entire pair. Do not repair only one arm.

## 3. Randomization and repetitions

Round 1 uses T01 theoretical derivation, T02 reduced threshold phase-space integration, and T03 source-grounded manuscript reading. Each task is run three times in each arm: 3 tasks × 3 repeats × 2 arms = **18 model runs**.

- Use fresh sessions and clean working directories.
- Randomize whether A or B runs first for each task/repetition using a recorded seed.
- Pair runs by task ID and repetition index.
- Do not reuse one arm's conversation, outputs, intermediate files, or discoveries in the other arm.
- If an infrastructure failure prevents a run, preserve its record and rerun both members under a new pair ID. Never silently discard an unfavorable scientific result.

Round 1 is an exploratory pilot. Report every run and paired difference; do not use pilot means or intervals to claim statistical significance or accept/reject a Skill module.

## 4. Task roster and task-family dependence

The development tasks are indexed in tasks/development/manifest.json.

| Task | Dimension | Task family | Skill reference |
|---|---|---|---|
| T01 | Theoretical derivation / Jacobian | threshold_kinematics | references/symbolic-calculation.md |
| T02 | Reduced threshold phase-space integration | threshold_kinematics | references/numerical-scans-and-uncertainty.md |
| T03 | Source-grounded paper reading | source_grounded_reading | references/paper-reading.md |
| T04 | Symbolic Dirac trace | symbolic_trace | references/symbolic-calculation.md |
| T05 | PDF figure audit + separate data-to-figure reproduction | figure_integrity | references/scientific-figure-audit.md |
| T06 | Reproducibility package | reproducibility | references/source-and-version-audit.md |

T01 and T02 deliberately share threshold kinematics. They test complementary symbolic and numerical skills, but they count as **one independent task-family cluster** for generalization claims.

T02 is a reduced one-dimensional threshold phase-space kernel in a constant-amplitude benchmark. It tests the threshold measure, Jacobian, convergence, and independent integration route. It is not a complete process-specific three-body rate: no full matrix element, angular dependence, nuclear response, halo folding, detector acceptance, or event-rate normalization is included.

T03 uses the complete pinned axial-vector manuscript PDF and its companion TeX source from the same repository commit. The evaluator stages both files once, verifies each Git blob SHA-1 and byte size, computes SHA-256 for both, and distributes byte-identical read-only copies to A and B. The TeX is a locator/cross-check aid. Original equation/Figure numbering and every reported PDF page number must be verified against the rendered PDF; never infer PDF pages from TeX line numbers.

T05 has two separate source pipelines. **T05-A** audits the pinned PDF. **T05-B** regenerates two SVG figures from a separately pinned plotting script and two raw CSV inputs. The CSV-to-SVG generator is not claimed to have produced the PDF in T05-A. Golden SVGs and their hashes are evaluator-only; they are never placed in model workspaces.

## 5. Development and holdout separation

- Development tasks and development evaluator keys may be used to improve Skill instructions.
- Holdout prompts, input snapshots, expected results, and scoring keys remain sealed from the model and Skill authors during development.
- A holdout package may be opened only after the final Skill commit, protocol, rubric, evaluator versions, and analysis plan are frozen and hashed.
- Any holdout exposure or use to modify the Skill invalidates the affected task; replace it and record the invalidation.
- Keep model prompts/inputs separate from evaluator keys and golden outputs. The evaluator key is mounted only in the evaluator environment.

A Git repository is not a security boundary. For a genuinely blind holdout, run models in workspaces that do not contain evaluator keys, golden outputs, holdout prompts, or benchmark repository history. Keep the sealed holdout and keys in a separate private evaluator repository. The evaluator workspace is read-only with respect to native run outputs.

## 6. Scoring and non-compensatory gates

Use protocol/scoring-rubric.yaml. The evaluator recomputes the weighted score from the five final dimension scores; a model-reported composite is not authoritative.

    Q = 25 × Σ_i (w_i S_i)

where w_i are normalized weights (0.35, 0.25, 0.20, 0.10, 0.10) and each S_i is in [0,4]. Thus Q is on a 0–100 scale.

Two reviewers independently score anonymized outputs without seeing the arm label. Preserve both original score sheets. A one-point score disagreement requires a documented consensus note. A difference of two or more points, a hard-gate disagreement, or a disagreement about fabricated evidence requires a third adjudicator. Preserve adjudication and pre-adjudication scores. Report exact agreement and quadratic-weighted Cohen's kappa.

A critical physics/math error, fabricated evidence, unauthorized destructive change, false PASS claim, or material convention/unit error fails the affected run regardless of weighted score. A B-arm hard-gate failure prevents a Positive decision.

## 7. Statistical analysis and decisions

The minimum practically meaningful improvement is **+5 Q points** on the 0–100 scale. Smaller positive effects may be reported but do not satisfy the Positive criterion.

For Round 2, the sealed holdout must contain:

- at least two independently authored task-family clusters in each of the six dimensions;
- at least three paired repetitions per task;
- at least 12 independent task-family clusters and 36 paired task runs, i.e. **72 model runs minimum**.

A documented power analysis may increase the number of families or repetitions before unsealing; it may not reduce these minima. Freeze the final sample size, analysis code, bootstrap seed, and analysis-plan hash before the evaluator opens the holdout.

The primary endpoint is the equal-weight macro-average of per-task-family mean paired differences. First average repetitions within each task, then task IDs within each family, then weight independent families equally. The 95% uncertainty interval uses 10,000 cluster-bootstrap resamples over task-family clusters, preserving all tasks and repetitions inside each sampled family. Report task-level and family-level results. Do not treat T01 and T02 as independent clusters.

Decision rules for the sealed Round 2 holdout:

- **Positive:** family macro-average ΔQ ≥ +5; 95% cluster-bootstrap lower bound > 0; mean autonomy difference ≥ −0.5; no B-arm hard-gate failure; no dimension mean regression ≤ −0.5 points; no family mean regression ≤ −5 Q points; and no unresolved pair-integrity/protocol deviation.
- **Negative:** 95% interval upper bound < 0, or B-arm hard-gate failures occur in at least two distinct paired runs.
- **Mixed:** one B-arm hard-gate failure, or overall improvement accompanied by a material dimension/task-family regression.
- **Inconclusive:** interval includes zero, practical-effect threshold is not met, study is underpowered, or required evidence is missing.

Round 1 is descriptive only and cannot establish Positive or Negative. Round 3 project-level results require a separate project-stratified analysis plan. A positive whole-package result does not automatically validate every Skill module; use a later ablation (no Skill / core Skill only / core plus selected module) when module-level causality is needed.

No threshold, scoring rule, or analysis choice may change after holdout outcomes are inspected. A substantive change requires a new protocol version and a fresh holdout.

## 8. Required run artifacts

For every run, retain:

- run ID, pair ID, task ID, arm, repetition, timestamps, randomization seed, and A/B execution order;
- protocol commit, Skill source commit, environment-lock/rubric/evaluator/task-manifest hashes;
- exact model/build/runtime/reasoning settings and host hardware where exposed;
- common project instruction/workspace hashes, including proof that shared-Skill routing was removed;
- exact task prompt/input hashes and every source file's repository, commit, path, Git blob SHA-1, byte size, and SHA-256;
- tool allowlist/versions, network policy, resource budgets, actual wall time, tokens if exposed, tool-call count, commands, exit status, and logs;
- Skill availability evidence, install manifest hash, invocation, and references loaded (B); explicit absence evidence (A);
- native output files and SHA-256, the task's required_evaluators list, deterministic evaluator versions/results, evaluator result IDs/statuses/input-output hash bindings, hash-verified evaluator result artifacts, both blinded reviewer sheets, consensus/adjudication, deviations, failed checks, and unresolved issues.

Do not store secrets, API keys, private tokens, or personal data in benchmark records.

## 9. Pair-integrity rules

Before scoring, validate each pair with both the JSON Schema and the deterministic pair checker. The following must match exactly between A and B: protocol lock, model/settings, runtime/hardware, project instruction/workspace snapshots, task prompt/input/source hashes, tool allowlist/versions, network policy, budgets, randomization seed, and pair execution order.

Permitted treatment differences are limited to Skill availability, Skill source/manifest, invocation, and task-specific references loaded by B. A must prove no Skill was available; B must prove the pinned Skill was available, invoked, and the task-specific reference was loaded. The transcript/output workspaces must be separate. Any control mismatch invalidates the entire pair; preserve both records and rerun both arms under a new pair ID.

The run-record Schema enforces arm-specific Skill fields and adjudicated hard-gate consistency. The comparison evaluator requires every task manifest entry to declare `required_evaluators`, requires every A/B run to contain each listed evaluator exactly once with PASS status, binds evaluator input hashes to the task input manifest, binds evaluator output hashes to registered result artifacts, and inspects the actual evaluator JSON payloads under the explicit artifact root. T05-B must use submission mode and prove that the model-submitted SVGs match a fresh trusted-generator run; the CI baseline-only check cannot satisfy a scored T05 task. The comparison evaluator also requires each run's source-file bundle to match the pinned task manifest and verifies staged source bytes, Git blob IDs, sizes, and SHA-256 values. The pair checker enforces equality of shared controls, budget adherence, pinned Skill commit, task-specific reference loading, and separate per-run artifact paths. A hash written in a record without matching bytes is not evidence. Neither check alone is sufficient.

## 10. Freeze checklist

Before Round 1:

1. Capture the actual Windows Codex model/runtime and hardware in environment-lock.json.
2. Pin the final Skill commit and hash all Skill files.
3. Freeze task prompts, input bytes, task manifest (including every task's `required_evaluators`), rubric, evaluator manifest, evaluator code/dependencies, evaluator-result payload contracts, and analysis plan.
4. Run the evaluator unit suite and validate both JSON Schemas with Draft 2020-12; verify that each task's required evaluators are registered and have tested PASS/failure fixtures.
5. Verify all staged source files by Git blob SHA-1, byte size, and SHA-256.
6. Create isolated A/B workspaces; prove A cannot access the Skill and B can invoke the exact pinned Skill.
7. Confirm identical tools, project context, network policy, and budgets.
8. Record the randomization seed and freeze the protocol commit.
9. Only then execute the 18 pilot runs. Do not create or expose Holdout until the final Skill and protocol are frozen.
