# High-Energy Theory Research

A research workspace for high-energy theory, with an explicit workflow for tracing changes from scientific questions to derivations, computations, verified claims, and manuscript revisions.

## Scientific Diff Workflow

A **scientific diff** is more than a text or code comparison. It records what changed in a research state, why it changed, what evidence supports the change, which checks were performed, and which downstream results or claims may be affected.

The workflow is designed for theoretical particle physics, UV–EFT matching, perturbative calculations, numerical phenomenology, and manuscript/reviewer-response work. It organizes evidence; it does **not** replace scientific judgment or prove a result correct merely because a workflow completed.

### Start here

1. Read [the workflow specification](docs/scientific-diff-workflow.md).
2. Copy [the research-change template](templates/research-change.md) for each substantive research change.
3. Use [the claim–evidence matrix](templates/claim-evidence-matrix.md) to track the support for important physical statements.
4. Apply [the review checklist](docs/review-checklist.md) before marking a change complete or synchronizing it into a manuscript.
5. Read the [active research records](research/README.md); the first baseline is [RC-001: VLL–Higgs–Singlet UV–EFT matching](research/RC-001-vll-higgs-singlet-uv-eft.md).

### Core chain

Scientific question → baseline and assumptions → derivation → computation → verification → physical claim → manuscript.

Every arrow should be traceable. A change to an upstream assumption or formula must trigger an impact review of dependent calculations, plots, constraints, and manuscript statements.

### Repository layout

- **docs/scientific-diff-workflow.md** — workflow, definitions, status model, and physics-specific guidance.
- **docs/review-checklist.md** — checks for scientific changes and manuscript synchronization.
- **templates/research-change.md** — record for an individual research change.
- **templates/claim-evidence-matrix.md** — ledger connecting physical claims to evidence and verification.
- **research/** — active research-change records and their current claim status.

## Operating principles

- Preserve the baseline; do not silently overwrite prior results.
- Separate assumptions, derivations, code, numerical outputs, evidence, and claims.
- Record the exact scope and conditions under which a result holds.
- Distinguish calculation completion from independent verification and claim confirmation.
- Mark checks as not applicable only with a reason; mark missing evidence as unresolved, not passed.
- Keep manuscript wording no stronger than the verified evidence.
- Use Git diffs for versioned text/code, and record hashes or metadata for notebooks, datasets, generated figures, and other artifacts that ordinary text diffs cannot meaningfully compare.

## Scientific integrity boundary

Passing software tests is not proof of a correct physical derivation. A correct derivation is not, by itself, proof that a numerical implementation or an experimental constraint has been applied correctly. The relevant checks depend on the model, approximation, renormalization scheme, data, and observable.

This workflow makes those dependencies explicit; it does not certify physics automatically.
