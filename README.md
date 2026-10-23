# High-Energy Theory Research

简体中文版本：[README.zh-CN.md](README.zh-CN.md)。

A research workspace for high-energy theory, with an explicit workflow for tracing changes from scientific questions to derivations, computations, verified claims, and manuscript revisions. It also includes a reusable research Skill and evidence-aware infrastructure for high-energy theoretical physics and phenomenology; peer-review response is one supported workflow, not the overall objective.

## Scientific Diff Workflow

A **scientific diff** is more than a text or code comparison. It records what changed in a research state, why it changed, what evidence supports the change, which checks were performed, and which downstream results or claims may be affected.

The workflow is designed for theoretical particle physics, UV–EFT matching, perturbative calculations, numerical phenomenology, and manuscript/reviewer-response work. It organizes evidence; it does **not** replace scientific judgment or prove a result correct merely because a workflow completed.

### Start here

1. Read the [detailed User Guide](docs/USER_GUIDE.md) for project setup, workstreams, research changes, evidence, validation, and review.
2. Read [the workflow specification](docs/scientific-diff-workflow.md).
3. Copy [the research-change template](templates/research-change.md) for each substantive research change.
4. Use [the claim–evidence matrix template](templates/claim-evidence-matrix.md) to track the support for important physical statements.
5. Apply [the review checklist](docs/review-checklist.md) before marking a change complete or synchronizing it into a manuscript.
6. Read the [active research records](research/README.md); the first baseline is [RC-001: VLL–Higgs–Singlet UV–EFT matching](research/RC-001-vll-higgs-singlet-uv-eft.md), with its [record-specific claim–evidence matrix](research/RC-001-claim-evidence-matrix.md).
7. Use the [project registry](projects/README.md) to distinguish top-level research projects from workstreams and research-change records. The VLL–Higgs–Singlet UV–EFT workstream belongs to the parent project axial-vector-model-building; it is not a separate top-level project.
8. For the reusable research Skill, start at [SKILL.md](skills/high-energy-theory-research/SKILL.md), then read its reference guides.
9. Review [repository status](docs/REPOSITORY_STATUS.md), [open issues](docs/OPEN_ISSUES.md), and the [normative decision register](docs/governance/DECISION_REGISTER.md) before changing candidate schemas.
10. Read the [v1.6.5 design baseline](docs/design/high-energy-theory-research-Skill-v1.6.5.md), the [v1.6.7 consolidated design/implementation report](docs/design/high-energy-theory-research-Skill-v1.6.7.md), and the [v1.6.6 Artifact-identity candidate clarification](schema/v1.4.3.7/audit/高能理论物理研究-Skill-详细设计文档-v1.6.6-Artifact身份语义候选修订.md).

### Core chain

Scientific question → baseline and assumptions → derivation → computation → verification → physical claim → manuscript.

Every arrow should be traceable. A change to an upstream assumption or formula must trigger an impact review of dependent calculations, plots, constraints, and manuscript statements.

### Repository layout

- **docs/scientific-diff-workflow.md** — workflow, definitions, status model, and physics-specific guidance.
- **projects/** — top-level project registry and project/workstream hierarchy; navigation metadata only at this stage.
- **docs/USER_GUIDE.md** — detailed operating manual for project setup, research changes, calculation evidence, validation, and migration discipline.
- **docs/PROJECT_REGISTRY_AUDIT.md** — scope and evidence of the Phase A registry/path pre-audit, including explicit limits on unrun tests and future file migration.
- **docs/review-checklist.md** — checks for scientific changes and manuscript synchronization.
- **docs/design/** — retained design baseline and consolidated implementation report.
- **docs/governance/** — normative decisions and fingerprint-contract review.
- **templates/research-change.md** — record for an individual research change.
- **templates/project-record.md** — template for registering a top-level research project or a nested workstream.
- **templates/claim-evidence-matrix.md** — generic template for a new claim–evidence ledger.
- **research/** — active research-change records and their current claim status.
- **calculations/** — reproducible symbolic/algebraic calculation scripts; each script states what it does and does not validate.
- **validation/** — captured calculation outputs and validation logs, kept distinct from planned or unexecuted checks.
- **schema/v1.4.3.7/** — candidate JSON Schemas, fixtures, validators, migration prototype, audit reports, and requirement/test traceability.
- **skills/high-energy-theory-research/** — reusable Skill entry point, reference guides, fingerprinting, structured-record validation, and project-registry validation tools.
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

A historical pre-integration CI run for PR HEAD `5c5b10b6889c2e4146d0a696fde16f2b3ca847bf` passed the candidate validation workflow on 2026-10-21 ([GitHub Actions run](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39542332657)). Its bounded results included 25/25 schema entry points, 83/83 fixture expectations, 16/16 semantic cases, 29/29 integration tests, and 36/36 repository unit tests. These results apply only to that SHA; they do not establish full schema completeness, historical migration compatibility, or scientific correctness. The Mathematica verification script was not run in CI.

Recent workflow runs for later main commits have repeatedly failed before any workflow step was recorded because no runner was assigned. The latest completed main run checked during this update is [#39896401710](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39896401710) for SHA `35d854699b652d69a1e51335dfaff1fe27dda0cd`. It failed before any workflow step was recorded because no runner was assigned. This is an infrastructure block, not evidence of a code-test failure, but it is not a passing result for the latest candidate. Recheck the exact HEAD's run before release.

### Validation commands

```bash
python -m pip install -r requirements-dev.txt
python schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py schema/v1.4.3.7
python schema/v1.4.3.7/tests/integration/test_v1_4_3_7.py
python -m unittest discover -s tests/unit -v
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
```

## Governance and release limits

Do not treat the candidate as an approved release until all release gates have been addressed:

1. DD-ART-007 through DD-ART-010 are recommendations, not approvals; obtain explicit normative decisions.
2. Fixture-index semantics are now explicit: the canonical index matches `1.4.3.7-candidate`, and the legacy `1.4.3.6-candidate` index is preserved separately. The unavailable source archive means byte-for-byte source-archive equality remains unverified.
3. The source-aware `validation_ids` resolver has positive and negative synthetic regression cases. Missing or ambiguous targets remain unresolved; migration stays staging-only with `commit_allowed=false`. Full historical v1.3 compatibility and transactional commit/rollback remain blocked.
4. Expand semantic/state-machine coverage and verify directory manifests against actual filesystem contents.
5. Define and review the `FingerprintInputs` field and hashing contract, then complete the structured record coverage needed for full reproducibility acceptance.
6. Implement scientific acceptance tests for real research tasks before claiming end-to-end scientific reproducibility.

## Scientific integrity boundary

Passing software tests is not proof of a correct physical derivation. A correct derivation is not, by itself, proof that a numerical implementation or an experimental constraint has been applied correctly. The relevant checks depend on the model, approximation, renormalization scheme, data, and observable.

This workflow makes those dependencies explicit; it does not certify physics automatically. A candidate schema or completed merge must not be described as scientific approval of the UV–EFT matching, a Wilson coefficient, or an experimental-acceptance claim.
