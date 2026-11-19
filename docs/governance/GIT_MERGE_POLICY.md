# Research PR merge strategy and commit-history policy

This policy applies to all contributors and agents working in this repository. It complements the Scientific Diff workflow, the User Guide, and the repository's evidence and validation rules.

## 1. Default: Create a merge commit

Use GitHub **Create a merge commit** by default for substantive research and repository changes, including:

- UV–EFT matching, loop calculations, renormalization, operator-basis reduction, and Ward-identity work;
- derivations, symbolic calculations, numerical integrations, convergence studies, and independent checks;
- schema, migration, and research-Skill changes that alter behavior or governance;
- research records, claim–evidence matrices, and manuscript-supporting evidence.

A merge commit preserves the topic branch's meaningful individual commits and their parent/child relationships, while making the PR integration boundary explicit on main. This is important for tracing scientific assumptions, equations, code changes, numerical corrections, tests, and evidence, and for using Git bisect when a downstream claim changes.

## 2. Exceptions

### Squash and merge

Use only for a genuinely trivial, indivisible maintenance/documentation batch whose intermediate commits carry no useful independent research or review provenance (for example, spelling, formatting-only, or tiny mechanical cleanup). Do not squash a PR containing distinct scientific decisions, derivations, implementation stages, tests, or validation evidence merely to shorten the main log.

### Rebase and merge

Use only when a linear history is explicitly desired and the topic commits are already meaningful, ordered, and independently reviewable. Rebase-and-merge rewrites commit identities; it does not preserve the original branch's exact commit graph.

## 3. Pre-merge procedure

1. Inspect the PR's full commit list and actual diff; do not choose a strategy based only on commit count.
2. Remove or consolidate temporary, duplicate, or misleading commits before final review when appropriate.
3. Confirm that the PR is one coherent research change, with its frozen baseline, scientific delta, evidence, impact review, and validation status recorded.
4. Select **Create a merge commit** unless a documented exception applies. State the reason in the PR description when using Squash or Rebase.
5. Do not rewrite or force-push reviewed/shared history merely for cosmetic cleanup.

## 4. Post-merge verification

Verify the merge commit and integrated main state. Check the research-change record, claim–evidence matrix, source, tests, run records, inputs/outputs, and hashes as applicable. Update the relevant research record with the integrated revision. Report repository archival and scientific validation as separate statuses.

## 5. Historical PRs

This policy applies prospectively. Do not rewrite already merged PRs to change their historical merge method. Existing squash/rebase merges remain valid historical records, with their PR discussions and original branch history available where retained.

**Rule of thumb:** substantive research defaults to Merge Commit; Squash is for trivial changes with no independent research-history value; Rebase is for an intentional linear history with already curated commits.

## 6. Main is the canonical research archive

The default branch `main` is the canonical, searchable, durable archive of completed and accepted research records. A pull request is a review and integration mechanism; it is not a substitute for archiving completed work on `main`.

### Research-work lifecycle

| State of work | Required location and action |
|---|---|
| Active or incomplete research | Keep on a topic branch; use a Draft PR when an early review or handoff is useful. State what is incomplete and what evidence is still required. |
| Ready for review | Open a focused PR to `main`; include the actual research record, code, inputs or immutable provenance, outputs, run manifest, tests, and claim/evidence status as applicable. |
| Completed and accepted research | Merge the PR into `main` after review and scope-appropriate checks. Do not leave accepted results available only on a branch or in an open PR. |
| Superseded or historical research | Keep the record on `main`, clearly label its status, and link the successor; do not erase provenance. |

### Main-branch discoverability

- Every substantive completed study must have a stable entry point in the relevant project/workstream README and, where appropriate, the research registry and claim–evidence matrix.
- Index entries must identify the question, source/equation provenance, assumptions and inputs, calculation method, result paths, validation actually performed, scientific status, relation to the adopted baseline, and next research entry point.
- The root README and project registry should link to the relevant study indexes; do not rely on PR search, branch names, chat history, or temporary Actions artifacts to discover completed work.
- Update indexes in the same PR as the result whenever practical. After merge, verify that the entry point and its linked files are present on `main`.

### Merge and closure discipline

- Once a PR is reviewed, its acceptance criteria are met, and the required evidence is archived, merge it using the repository's merge strategy in §§1–2 and close the PR as completed.
- Keep Draft PRs for genuinely unfinished work. A failed or missing check must be described accurately; distinguish a scientific failure from an optional or infrastructure-only CI issue under the archival policy.
- Do not bulk-merge stacked or dependent PRs without checking their baselines, dependency order, diffs, and acceptance status. Do not merge a PR whose own description says required calculations, tests, or independent checks remain unexecuted.
- After merge, verify the merge commit on `main`, update the research record with the integrated revision, and remove a topic branch only when it contains no unique unmerged work.

This section governs discoverability and lifecycle; it does not change the repository's existing default of **Create a merge commit** for substantive research.
