# Deletion reference preflight (opt-in)

Before deleting research materials after a cross-repository move, pin the
source baseline and destination commit. Verify the destination paths and bytes,
and confirm that a reader with the intended access can follow the new links.
Then review an exact candidate deletion commit, including navigation updates:

```sh
# In the repository's development environment (optional parser).
# Set BASE_SHA and CANDIDATE_SHA to the reviewed commits first.
python -m pip install "markdown-it-py==4.3.0"
python skills/high-energy-theory-research/scripts/check_deleted_markdown_targets.py \
  --base "$BASE_SHA" --head "$CANDIDATE_SHA"
```

Choose the intended pre-deletion baseline explicitly; the checker does not
calculate a merge base or inspect dirty/untracked files. It reports Markdown
links and images (including reference-style links) in the candidate's tracked
`.md` files whose repository-relative destination existed at the baseline
and is now gone. Query strings and fragment identifiers are removed for the
path comparison. A renamed target or a directory that disappeared counts as
deleted at its old path. The line number identifies the containing Markdown
block. Exit codes: **0** no such links, **1** findings, **2** unable to check.

The scan does not look up external URLs, verify section anchors, find links
already broken at the baseline, or parse raw HTML, scripts, workflow paths,
notebooks, or other file types. Review those consumers separately. Run the
existing registry validator from a clean checkout of the candidate with its
normal development dependencies, if a project registry is present:

```sh
python skills/high-energy-theory-research/scripts/validate_project_registry.py
```

This is a local review aid, not a policy change, CI requirement, or replacement
for checking destination access and fingerprints. Do not copy project data to
the central repository to silence a stale link; update its navigation instead.
