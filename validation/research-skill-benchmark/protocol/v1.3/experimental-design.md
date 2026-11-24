# Experimental design — v1.3

Status: **FROZEN CANDIDATE PROTOCOL v1.3 — pending PR review and merge. Round 1 remains the 18-run T01/T02/T03 pilot; no model runs have started.**

## 1. Hypothesis and estimand

The primary hypothesis is:

    H1: mean(Q_B - Q_A) > 0

A is GPT-6 with Extra High reasoning effort and the Particle Physics Research plugin not selected or invoked; B uses the same GPT-6 / Extra High configuration with the pinned plugin explicitly selected and invoked.

The estimand is the paired difference in blinded scientific-quality score for the same task. Report task-level and task-family outcomes; a pooled run mean alone is not the primary result. This benchmark measures the incremental effect of the Skill package under the recorded runtime, tools, tasks, and project context. It does not claim to improve the underlying model.

## 2. Arms and controls

### A — No Skill

- The installed Particle Physics Research plugin is not selected or invoked in the A conversation.
- No Skill manifest or Skill-specific reference files are supplied to the A conversation.
- Record evidence that no Skill reference was loaded. If the plugin is automatically invoked or any Skill reference appears in A, invalidate the pair.
- The model receives the common task prompt and identical built-in tool access.

### B — With Skill

- Select the already-installed Particle Physics Research plugin, version 0.2.0, pinned to the exact Skill commit recorded in the protocol lock.
- Explicitly invoke `@Particle Physics Research` for the task.
- Load only the task-specific reference required by the Skill.
- Record the Skill source commit, installation manifest SHA-256, and loaded references.

### Identical in A and B

- Exact ChatGPT model label **GPT-6** and **Extra High** reasoning effort, as fixed by the user; record any additional UI-exposed settings.
- Fresh ChatGPT Web conversation for every run; one task per conversation.
- Same task prompt, input bytes, source snapshots, user/project instructions, built-in tool allowlist, network policy, 30-minute visible-turnaround limit, and stopping rule. No tool-call cap is imposed because ChatGPT Web does not expose a verifiable per-invocation event log.
- Same browser, OS, client/runtime, Python/data-analysis availability, and file-upload path.
- Same evaluator versions and reference answers; neither is exposed to the model.
- Use identical user-provided task context and instructions in both arms; do not add a project-specific Skill-routing paragraph to either arm. A must not be told that the Skill exists.
- No other plugins, connected apps, external APIs, or web search are used in either arm. Stage identical inputs before the run.

Stage all source inputs before a run. The preferred network policy is **offline after staging**: no external search or network retrieval during a scored task. If the actual host cannot enforce this, record the exact policy and invalidate any pair with asymmetric network access. The common harness must not mention the Skill in A. Skill availability/invocation is the only intended treatment difference.

If ChatGPT automatically exposes Skill instructions in A, or changes built-in tool permissions between arms, preserve the records and invalidate the entire pair. Do not repair only one arm.

## 3. Randomization and repetitions

Round 1 uses T01 theoretical derivation, T02 reduced threshold phase-space integration, and T03 source-grounded manuscript reading. Each task is run three times in each arm: 3 tasks × 3 repeats × 2 arms = **18 model runs**.

- Use fresh sessions and clean working directories.
- Randomize whether A or B runs first for each task/repetition using a recorded seed.
- **v1.3 Round 1 randomization is frozen:** seed = `20261124`; generate a balanced list containing five `A_then_B` and four `B_then_A` orders, shuffle it with Python 3.13.5 `random.Random(20261124).shuffle`, and assign it to the nine pairs in the order T01-r1, T01-r2, T01-r3, T02-r1, T02-r2, T02-r3, T03-r1, T03-r2, T03-r3. The resulting pair-order map is: T01-r1 B_then_A; T01-r2 B_then_A; T01-r3 A_then_B; T02-r1 A_then_B; T02-r2 A_then_B; T02-r3 B_then_A; T03-r1 B_then_A; T03-r2 A_then_B; T03-r3 A_then_B. Record the same seed and pair order in both run records of each pair.
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

T05 has two separate public-source pipelines. **T05-A** audits both paired axial-vector constraint-panel PDFs from axial-vector-review-response, with the companion TeX used to establish the shared caption and intended panel width. **T05-B** verifies the Native AFH Xe-131 CSV and its WLS exporter/run-manifest provenance from radiative-dark-matter-nuclear-currents, then reproduces two SVG views using the pinned standard-library plotting adapter in this benchmark. The adapter is a presentation transformation of existing native data; it does not rerun the unavailable AFH package or calculate new nuclear responses. T05-A and T05-B are independent pipelines.

## 5. Development and holdout separation

- Development tasks and development evaluator keys may be used to improve Skill instructions.
- Holdout prompts, input snapshots, expected results, and scoring keys remain sealed from the model and Skill authors during development.
- A holdout package may be opened only after the final Skill commit, protocol, rubric, evaluator versions, and analysis plan are frozen and hashed.
- Any holdout exposure or use to modify the Skill invalidates the affected task; replace it and record the invalidation.
- Keep model prompts/inputs separate from evaluator keys and golden outputs. The evaluator key is mounted only in the evaluator environment.

A Git repository is not a security boundary. For a genuinely blind holdout, run models in workspaces that do not contain evaluator keys, golden outputs, holdout prompts, or benchmark repository history. Keep the sealed holdout and keys in a separate private evaluator repository. The evaluator workspace is read-only with respect to native run outputs.

## 6. Scoring, secondary metrics, and non-compensatory gates

Use protocol/scoring-rubric.yaml. The evaluator recomputes the weighted score from the five final dimension scores; a model-reported composite is not authoritative. Preserve the original five weights. Report unnecessary computations, method-selection autonomy, reproducibility evidence items, and observable resource overhead separately; do not fold them into Q.

    Q = 25 × Σ_i (w_i S_i)

where w_i are normalized weights (0.35, 0.25, 0.20, 0.10, 0.10) and each S_i is in [0,4]. Thus Q is on a 0–100 scale.

Two reviewers independently score anonymized outputs without seeing the arm label. Preserve both original score sheets. A one-point score disagreement requires a documented consensus note. A difference of two or more points, a hard-gate disagreement, or a disagreement about fabricated evidence requires a third adjudicator. Preserve adjudication and pre-adjudication scores. Report exact agreement and quadratic-weighted Cohen's kappa.

A critical physics/math error, fabricated evidence, unauthorized destructive change, false PASS claim, or material convention/unit error fails the affected run regardless of weighted score. A B-arm hard-gate failure prevents a Positive decision.

## 7. Secondary behavioral/resource metrics

- **Unnecessary computation count:** reviewers count discrete visible calculations, searches, tool steps, or workflow artifacts that were not needed and added no decision-relevant evidence. Do not count ordinary algebraic steps or useful checks. Record each event and rationale; report A/B differences separately from Q.
- **Method-selection autonomy:** retain the existing 0–4 autonomy score and record whether the model selected the least-complex sufficient method, rejected inapplicable Skill guidance, and stopped when acceptance criteria were met.
- **Reproducibility evidence:** retain the existing reproducibility and evidence-quality scores; list source/input identity, code/command, environment/parameters, native outputs, convergence/error analysis, and independent checks as present, absent, or not applicable.
- **Resource overhead:** compare UTC send-to-first-observation visible-turnaround upper bounds. Record a UI Worked label separately. Backend wall time, token count, and tool-call count are null unless exposed by the host. Missing logs never mean zero tool calls.

These are descriptive secondary metrics and do not change the five weighted dimensions or decision thresholds.

## 8. Statistical analysis and decisions

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

## 9. Required run artifacts and Web observability

For every run, retain:

- run ID, pair ID, task ID, arm, repetition, UTC send time, first observation of complete answer, randomization seed, and A/B execution order;
- protocol commit, Skill source commit, environment-lock/rubric/evaluator/task-manifest/analysis-plan hashes;
- exact model/build/runtime/reasoning settings and host hardware where exposed;
- visible turnaround upper bound and optional UI Worked label; backend wall time and tokens only if exposed;
- per-invocation tool-call count/log only if the host exposes verifiable events; otherwise record null and set `tool_call_count_observable=false`;
- label exported Markdown as a visible-answer capture, not a backend raw transcript, when no backend transcript is available;
- common task-context and staged-workspace hashes, including proof that no Skill-routing instructions were supplied;
- exact task prompt/input hashes and every source file's repository, commit, path, Git blob SHA-1, byte size, and SHA-256;
- tool allowlist/versions, network policy, visible-turnaround limit, visible timing observations, and explicit observability notes; backend/tool telemetry remains null when unavailable;
- Skill availability evidence, install manifest hash, invocation, and references loaded (B); explicit absence evidence (A);
- native output files and SHA-256, the task's required_evaluators list, deterministic evaluator versions/results, evaluator result IDs/statuses/input-output hash bindings, hash-verified evaluator result artifacts, both blinded reviewer sheets, consensus/adjudication, deviations, failed checks, and unresolved issues.

Do not store secrets, API keys, private tokens, or personal data in benchmark records.

## 10. Pair-integrity rules

Before scoring, validate each pair with both the JSON Schema and the deterministic pair checker. The following must match exactly between A and B: protocol lock, model/settings, runtime/hardware, project instruction/workspace snapshots, task prompt/input/source hashes, tool allowlist/versions, network policy, budgets, randomization seed, and pair execution order.

Permitted treatment differences are limited to Skill availability, Skill source/manifest, invocation, and task-specific references loaded by B. A must prove the plugin was not selected, no Skill reference was loaded, and no Skill-specific context was supplied; B must prove the pinned plugin was selected, invoked, and the task-specific reference was loaded. The transcript/output workspaces must be separate. Any control mismatch invalidates the entire pair; preserve both records and rerun both arms under a new pair ID.

The run-record Schema enforces arm-specific Skill fields and adjudicated hard-gate consistency. The comparison evaluator requires every task manifest entry to declare `required_evaluators`, requires every A/B run to contain each listed evaluator exactly once with PASS status, binds evaluator input hashes to the task input manifest, binds evaluator output hashes to registered result artifacts, and inspects the actual evaluator JSON payloads under the explicit artifact root. T05-B must use submission mode and prove that the model-submitted SVGs match a fresh trusted-generator run; the CI baseline-only check cannot satisfy a scored T05 task. The comparison evaluator binds the exact protocol commit and exact bytes of the environment lock, scoring rubric, task manifest, analysis plan, and evaluator registry to each run record. It also requires each run's source-file bundle to match the pinned task manifest and verifies staged source bytes, Git blob IDs, sizes, and SHA-256 values. The pair checker enforces equality of shared controls, visible-turnaround budget adherence, matching observability capabilities, pinned Skill commit, task-specific reference loading, and separate per-run artifact paths. A hash written in a record without matching bytes is not evidence. Neither check alone is sufficient.

## 11. Freeze checklist

Before Round 1:

1. Record the fixed GPT-6 / Extra High configuration and all available ChatGPT Web client/host fields in environment-lock.json; retain null for unexposed fields.
2. Pin the installed Skill commit and hash all Skill files; verify the installed plugin manifest against that commit.
3. Freeze task prompts, input bytes, task manifest (including every task's `required_evaluators`), rubric, evaluator manifest (including task-to-evaluator associations and payload JSON Schemas), evaluator code/dependencies, evaluator-result payload contracts, and analysis plan.
4. Run the evaluator unit suite and validate both JSON Schemas with Draft 2020-12; verify that each task's required evaluators are registered and have tested PASS/failure fixtures, including both T05 PDF panels and exact SVG submission comparison.
5. Verify all staged source files by Git blob SHA-1, byte size, and SHA-256. For T05, stage the two public axial-vector PDFs/TeX and the public Native AFH Xe-131 CSV, WLS exporter, run manifest, README, checksum list, and pinned plotting adapter.
6. Create isolated A/B ChatGPT Web conversations; prove A has no plugin/Skill context and B can invoke the exact pinned plugin.
7. Confirm identical tools, project context, network policy, and budgets.
8. Record the randomization seed and freeze the protocol commit.
9. Only then execute the 18 pilot runs. Do not create or expose Holdout until the final Skill and protocol are frozen.


The canonical input-manifest SHA-256 is computed from UTF-8 JSON with sorted keys and compact separators over schema version, task ID, prompt SHA-256, source commit, and source-file identities sorted by repository/path. The scoring evaluator independently hashes the exact prompt file named by each task manifest entry and checks the run-record prompt SHA-256.


## v1.3 cohort boundary

Protocol v1.2 remains immutable and records the GPT-6 Pro (Astra Pro) / Pro-default cohort. Its observations must not be pooled with, or treated as direct model comparisons to, v1.3. Version 1.3 reuses the Particle Physics Research v0.2.0 package, T01/T02/T03 prompts and source inputs, five weighted dimensions, scoring weights, three repetitions per task per arm, 18-run total, stopping rules, and secondary metrics. The intended treatment contrast remains Skill absent versus the same Skill present; the model/reasoning configuration and versioned protocol bindings are distinct.
