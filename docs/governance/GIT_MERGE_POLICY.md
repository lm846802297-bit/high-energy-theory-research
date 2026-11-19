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
