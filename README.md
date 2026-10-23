# High-Energy Theory Research

A research workspace for high-energy theory, with an explicit workflow for tracing changes from scientific questions to derivations, computations, verified claims, and manuscript revisions. It also includes a reusable research Skill and evidence-aware infrastructure for high-energy theoretical physics and phenomenology; peer-review response is one supported workflow, not the overall objective.

## Scientific Diff Workflow

A **scientific diff** is more than a text or code comparison. It records what changed in a research state, why it changed, what evidence supports the change, which checks were performed, and which downstream results or claims may be affected.

The workflow is designed for theoretical particle physics, UV–EFT matching, perturbative calculations, numerical phenomenology, and manuscript/reviewer-response work. It organizes evidence; it does **not** replace scientific judgment or prove a result correct merely because a workflow completed.

### Start here

1. Read [the workflow specification](docs/scientific-diff-workflow.md).
2. Copy [the research-change template](templates/research-change.md) for each substantive research change.
3. Use [the claim–evidence matrix template](templates/claim-evidence-matrix.md) to track the support for important physical statements.
4. Apply [the review checklist](docs/review-checklist.md) before marking a change complete or synchronizing it into a manuscript.
5. Read the [active research records](research/README.md); the first baseline is [RC-001: VLL–Higgs–Singlet UV–EFT matching](research/RC-001-vll-higgs-singlet-uv-eft.md), with its [record-specific claim–evidence matrix](research/RC-001-claim-evidence-matrix.md).
6. For the reusable research Skill, start at [SKILL.md](skills/high-energy-theory-research/SKILL.md), then read its reference guides.
7. Review [repository status](docs/REPOSITORY_STATUS.md), [open issues](docs/OPEN_ISSUES.md), and the [normative decision register](docs/governance/DECISION_REGISTER.md) before changing candidate schemas.
8. Read the [v1.6.5 design baseline](docs/design/high-energy-theory-research-Skill-v1.6.5.md), the [v1.6.7 consolidated design/implementation report](docs/design/high-energy-theory-research-Skill-v1.6.7.md), and the [v1.6.6 Artifact-identity candidate clarification](schema/v1.4.3.7/audit/高能理论物理研究-Skill-详细设计文档-v1.6.6-Artifact身份语义候选修订.md).

### Core chain

Scientific question → baseline and assumptions → derivation → computation → verification → physical claim → manuscript.

Every arrow should be traceable. A change to an upstream assumption or formula must trigger an impact review of dependent calculations, plots, constraints, and manuscript statements.

### Repository layout

- **docs/scientific-diff-workflow.md** — workflow, definitions, status model, and physics-specific guidance.
- **docs/review-checklist.md** — checks for scientific changes and manuscript synchronization.
- **docs/design/** — retained design baseline and consolidated implementation report.
- **docs/governance/** — normative decisions and fingerprint-contract review.
- **templates/research-change.md** — record for an individual research change.
- **templates/claim-evidence-matrix.md** — generic template for a new claim–evidence ledger.
- **research/** — active research-change records and their current claim status.
- **calculations/** — reproducible symbolic/algebraic calculation scripts; each script states what it does and does not validate.
- **validation/** — captured calculation outputs and validation logs, kept distinct from planned or unexecuted checks.
- **schema/v1.4.3.7/** — candidate JSON Schemas, fixtures, validators, migration prototype, audit reports, and requirement/test traceability.
- **skills/high-energy-theory-research/** — reusable Skill entry point, reference guides, fingerprinting, and project-record validation tools.
- **tests/eval-cases/** — bounded analytic-matrix and UV–EFT hard-derivative pilot cases.
- **tests/unit/** — regression tests for the Skill scaffold, record validator, fingerprints, migration reference resolution, and pilots.

## Research Skill and schema candidate

**Status: development / candidate stage. No formal schema release is declared.**

- Research design baseline: v1.6.5.
- Artifact-identity clarification: v1.6.6 candidate; its normative decisions remain pending approval.
- Consolidated design/implementation report: v1.6.7.
- Schema package: `schema/v1.4.3.7/`, imported as a candidate bundle.
- The candidate contains 25 JSON Schema entry points, 83 indexed fixtures, cross-record validation, a conservative migration prototype, a directory-manifest helper, audit reports, and traceability data.
- The canonical `manifest.fixture_index` is version-matched to `1.4.3.7-candidate`; `manifest.legacy_fixture_index` preserves the `1.4.3.6-candidate` expectation baseline. Both digests and version relationships are checked.
- The project-record validator is `skills/high-energy-theory-research/scripts/validate_project_records.py`. It supports JSON/YAML parsing, candidate-schema checks, bounded reference and ID validation, status/reason consistency, and local source/artifact path checks.
- The end-to-end UV–EFT pilot checks a bounded hard-kernel derivative and small-`r` expansion against independent Feynman-parameter quadrature. It does not establish completeness of the full UV diagram set, full dimension-six basis reduction, or scientific acceptance of a final Wilson coefficient.

## Operating principles

- Preserve the baseline; do not silently overwrite prior results.
- Separate assumptions, derivations, code, numerical outputs, evidence, and claims.
- Record the exact scope and conditions under which a result holds.
- Distinguish calculation completion from independent verification and claim confirmation.
- Mark checks as not applicable only with a reason; mark missing evidence as unresolved, not passed.
- Keep manuscript wording no stronger than the verified evidence.
- Use Git diffs for versioned text/code, and record hashes or metadata for notebooks, datasets, generated figures, and other artifacts that ordinary text diffs cannot meaningfully compare.

## Local validation

A historical pre-integration CI run for PR HEAD `5c5b10b6889c2e4146d0a696fde16f2b3ca847bf` passed the candidate validation workflow on 2026-10-21 ([GitHub Actions run](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39542332657)). Its results included 25/25 schema entry points, 83/83 fixture expectations, 16/16 semantic cases, 29/29 integration tests, and 36/36 repository unit tests. These results apply only to that SHA.

The current `main` HEAD inspected after the project-registry updates is `d30734fa078a49262c043eb817479dc680d23ee5`. Its latest workflow run, [#39895811558](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39895811558), failed before any workflow step was recorded because no runner was assigned. This is not evidence of a code-test failure, but it also provides no passing CI result for current `main`. Do not use the historical green run as a substitute for validating the current candidate.

The separate Mathematica verification script is included in the provenance bundle but was **not run in CI** and is not marked passed. Rerun the complete workflow for the final HEAD when a runner is available.

### Validation commands

```bash
python -m pip install -r requirements-dev.txt
python schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py schema/v1.4.3.7
python schema/v1.4.3.7/tests/integration/test_v1_4_3_7.py
python -m unittest discover -s tests/unit -v
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
```

## Governance and release limits

Do not treat the candidate as an approved release until all release gates have been addressed:

1. DD-ART-007 through DD-ART-010 are recommendations, not approvals; obtain explicit normative decisions.
2. Resolve the fixture-index version-field mismatch: the inherited index says `1.4.3.6-candidate` while the bundle manifest says `1.4.3.7-candidate`. The source archive needed for byte-for-byte lineage verification is unavailable.
3. Resolve ambiguous legacy `validation_ids` mappings without guessing target record types. Migration remains staging-only with `commit_allowed=false`; no source overwrite or migration commit is authorized.
4. Expand semantic/state-machine coverage and verify directory manifests against actual filesystem contents.
5. Define and review the `FingerprintInputs` field and hashing contract, then complete the structured record coverage needed for full reproducibility acceptance.
6. Implement scientific acceptance tests for real research tasks before claiming end-to-end scientific reproducibility.

## Scientific integrity boundary

Passing software tests is not proof of a correct physical derivation. A correct derivation is not, by itself, proof that a numerical implementation or an experimental constraint has been applied correctly. The relevant checks depend on the model, approximation, renormalization scheme, data, and observable.

This workflow makes those dependencies explicit; it does not certify physics automatically. A candidate schema or completed merge must not be described as scientific approval of the UV–EFT matching, a Wilson coefficient, or an experimental-acceptance claim.
