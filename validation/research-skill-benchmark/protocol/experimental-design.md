# Experimental design — v1.0 draft

Status: **draft; freeze only after the target Windows Codex model/runtime is recorded.**

## 1. Hypothesis and estimand

Primary hypothesis:

`H1: mean(Q_B - Q_A) > 0`

where A is the same GPT model without the shared Research Skill and B is the same model with the pinned Skill available and explicitly invoked.

The estimand is the paired difference in blinded scientific-quality score for the same task under the two arms. Also report task-level outcomes; do not rely only on a pooled mean.

This benchmark does not claim that a Skill improves the underlying model. It measures the incremental effect of this Skill package under the recorded runtime, tools, tasks, and project context.

## 2. Arms and controls

### A — No Skill

- Shared `high-energy-theory-research` Skill is not installed, mounted, or included in the accessible workspace.
- No Skill manifest or Skill-specific reference files are provided.
- The model receives the common task prompt, project context, and tool access.

### B — With Skill

- Install or mount the exact Skill commit recorded in the environment lock.
- Explicitly invoke `$high-energy-theory-research` for the task.
- Load only the task-specific reference required by the Skill.
- Record the Skill source commit and per-file installation manifest.

### Identical in A and B

- Exact model label/build, reasoning effort, sampling settings, and system/developer configuration where exposed.
- Fresh conversation/session for every run.
- Same task prompt, inputs, source snapshots, workspace files, project-level instructions, tool allowlist, network policy, time/token budget, and stopping rule.
- Same OS, hardware/runtime, Python/compiler/package versions, and available external software.
- Same evaluation scripts and reference answers, which are never exposed to the model.

The common harness must not mention or imply the existence of the Skill in A. It must not contain a project instruction telling A to invoke the Skill. In B, Skill invocation is the only intended treatment difference.

If the host automatically exposes other Skills or changes tool permissions between arms, record the deviation and invalidate the affected pair.

## 3. Randomization and repetitions

Round 1 contains three development tasks: T01 theory/Jacobian derivation, T02 threshold numerical integration, and T03 source-grounded reading of the pinned axial-vector manuscript.

Run each task three times in each arm: 3 tasks × 3 repeats × 2 arms = 18 runs.

- Use fresh sessions and clean working directories.
- Randomize whether A or B is run first for each task/repetition using a recorded random seed.
- Pair runs by task ID and repetition index.
- Do not reuse one arm's conversation, outputs, intermediate files, or discoveries in the other arm.
- If a run fails for an infrastructure reason, preserve its record and rerun both members of the pair under a new pair ID. Never silently discard an unfavorable scientific result.

Three repetitions are a pilot, not enough for a strong population-level statistical claim. Report all individual outcomes, paired differences, mean, median, range, and a bootstrap interval only as exploratory uncertainty. Do not claim statistical significance from this pilot.

## 4. Task roster

The six development tasks are indexed in `tasks/development/manifest.json`.

| Task | Dimension | Skill reference for B arm |
|---|---|---|
| T01 | Theoretical derivation / Jacobian | `symbolic-calculation.md` |
| T02 | Numerical integration / convergence | `numerical-scans-and-uncertainty.md` |
| T03 | Source-grounded paper reading | `paper-reading.md` |
| T04 | Symbolic Dirac trace | `symbolic-calculation.md` |
| T05 | PDF figure audit | `scientific-figure-audit.md` |
| T06 | Reproducibility package | `source-and-version-audit.md` |

Round 1 runs T01–T03 (18 paired-arm runs). Round 2 runs all six development dimensions and adds a separately prepared sealed holdout set. The development tasks and their evaluator key may be used to refine the Skill; they cannot establish generalization on their own.

T03 uses the complete pinned axial-vector manuscript PDF, not the earlier single-figure PDF. Its Git commit, blob SHA-1, file size, and companion TeX source are recorded in the task prompt and task manifest. The evaluator must calculate and record the PDF SHA-256 from the exact staged bytes before the task is scored. The PDF page number and rendered equation number must be read from the PDF, not inferred from TeX line numbers.

## 5. Development and holdout separation

- Development tasks may be inspected and used to improve Skill instructions.
- Holdout task prompts, inputs, expected results, and scoring keys are sealed from the model and from Skill authors during development.
- A holdout task may be opened only after the Skill commit and scoring rubric have been frozen and hashed.
- Any use of holdout content to modify the Skill invalidates that holdout task; replace it with a new task and record the invalidation.
- Keep task prompts and evaluator keys in separate directories. The evaluator key is mounted only in the evaluator environment, never in the model workspace.

A Git repository is not a security boundary. For a genuinely blind holdout, run the model in a workspace that does not contain `tasks/holdout`, evaluator keys, or the benchmark repository history. For stronger blinding, keep holdout keys in a separate private evaluator repository.

## 5. Scoring and non-compensatory gates

Use [scoring-rubric.yaml](scoring-rubric.yaml). Two independent reviewers should score outputs without seeing the arm label. Deterministic evaluators should run before human review.

Hard gates:
- A critical physics/math error cannot be compensated by writing quality or speed.
- Fabricated citations, fabricated tool execution, or fabricated validation evidence fail the affected run.
- Destructive changes to source data or project records fail the run.
- A required validation reported as PASS without an artifact fails the run.
- Materially incorrect conventions, dimensions, signs, normalization, or units fail the relevant correctness gate.

Report the five weighted dimensions separately and the autonomy guardrail separately. Do not hide a regression in one dimension behind the composite score.

## 6. Outcomes and adoption decisions

A Skill module is retained only if the evidence shows at least one meaningful benefit:
- improved physical/mathematical correctness;
- improved independent validation or uncertainty analysis;
- improved provenance/reproducibility;
- improved evidence traceability or figure integrity.

A module must also avoid a material regression in reasoning autonomy or a material increase in unnecessary work.

If the confidence interval is wide or results are mixed, classify the result as **inconclusive**, not PASS.

No minimum score or adoption threshold may be changed after inspecting holdout outcomes. Any threshold revision requires a new protocol version and a fresh holdout set.

## 7. Required run artifacts

For every run, retain:
- run ID, pair ID, task ID, arm, repetition, timestamp;
- exact model/build/runtime and reasoning settings;
- Skill commit and file manifest for B; explicit `not_available` for A;
- exact task/input hashes and project/source commit;
- prompt/transcript or a privacy-reviewed reproducible transcript reference;
- tool calls, commands, logs, resource/time budget;
- native output files and SHA-256;
- deterministic evaluator outputs;
- reviewer scores and adjudication;
- deviations, failed checks, and unresolved issues.

Do not store secrets, API keys, private tokens, or personal data in benchmark records.

## 8. Freeze checklist

Before Round 1:
1. Complete [environment-lock.json](environment-lock.json) using the actual Windows Codex environment.
2. Pin the Skill commit and hash the Skill files.
3. Freeze task prompts, input files, scoring rubric, and evaluator versions.
4. Create isolated A/B workspaces and confirm A cannot access the Skill.
5. Confirm B can explicitly invoke the pinned Skill and read its task references.
6. Confirm identical tools, project context, and resource budgets.
7. Record the randomization seed and freeze the protocol commit.
8. Only then execute the 18 pilot runs.
