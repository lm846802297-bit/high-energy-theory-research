# Central archive boundary check (opt-in)

The central repository holds shared infrastructure. Put project derivations,
calculation code, inputs, outputs, and scientific evidence in the project
repository. The central project registry may link to verified evidence.
This check is a path-based review aid, not a required CI check.

From a checkout with both commits and their common history available:

```sh
python skills/high-energy-theory-research/scripts/validate_central_archive_boundary.py \
  --base origin/main --head HEAD
```

Use the actual topic head, not a synthetic PR merge commit, to inspect the
topic delta. Pass immutable SHAs for repeatable review. The command inspects
new paths between the unique Git merge base and the head tree. It does not
inspect the working tree. Exit codes: **0** no blocked paths, **1** blocked
additions listed in the JSON report, **2** unable to check (for example,
missing history, an invalid ref, or an ambiguous merge base).

## Path rules

- Block new paths under `artifacts/`, `calculations/`, `research/`, and
  `validation/`. Copies and rename destinations are new paths if the path
  did not exist in the base. Existing historical files can be amended or
  removed in a reviewed correction or transfer; their presence does not
  cause failure.
- Allow shared test and benchmark infrastructure under the explicit
  `validation/skill-benchmark/`, `validation/workflow-tests/`, and
  `validation/infrastructure-tests/` directories. Existing open Skill
  distribution work also uses these compatibility prefixes
  `validation/research-skill-benchmark/` and
  `validation/skill-module-evaluation-2026-11-22/`; this does not certify
  their contents or approval status. Prefer stable generic directories
  for new infrastructure.
- Other paths, including registry metadata, workflows, Skills, schemas,
  and synthetic fixtures under `tests/`, are outside this check. A new
  legitimate infrastructure prefix, if needed, should be an explicit
  policy change with tests rather than an override at invocation time.

Paths alone cannot establish whether a file is infrastructure or project
evidence. A pass is not an approval to add project data under an allowed
prefix, to overwrite an existing path with new project results, or to
retire source files before verifying the destination, provenance, and
downstream references. Changes to the check or its allowlist need review.
