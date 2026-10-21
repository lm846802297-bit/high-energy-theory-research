# High-Energy Theory Research

A reusable research Skill and evidence-aware workflow for high-energy theoretical physics and phenomenology. The system is intended for general research work; peer-review response is one supported workflow, not the overall objective.

## Current state

**Development / candidate stage. No formal schema release is declared.**

- Research design baseline: v1.6.5.
- Latest Artifact-identity clarification: v1.6.6 candidate, still awaiting normative approval.
- Schema package: schema/v1.4.3.7, imported as a candidate bundle.
- The current candidate includes 25 JSON Schema entry points, 83 indexed fixtures, a cross-record validator, a conservative migration prototype, a directory-manifest helper, audit reports, and traceability data.
- The reusable Skill entry point is in skills/high-energy-theory-research/SKILL.md.

## Local validation

The candidate package was checked locally on 2026-10-21:

- 58/58 bundle checks passed.
- 25/25 schema meta-validation and manifest hash checks passed.
- 83/83 fixture expectations matched.
- 16/16 bundled semantic-case expectations matched.
- 29/29 prototype integration tests passed.
- Python syntax compilation passed for the 7 candidate Python files.

These are bounded software-validation results. They do **not** establish full schema completeness, historical migration compatibility, or correctness of any physics result. GitHub Actions has not yet been verified for this import.

## Start here

1. Read docs/REPOSITORY_STATUS.md and docs/OPEN_ISSUES.md.
2. Read the Skill entry point and its three reference guides.
3. Review the v1.6.5 design baseline and the v1.6.6 candidate clarification.
4. Run the candidate checks before proposing schema changes.

## Validation commands

~~~bash
python -m pip install -r requirements-dev.txt
python schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py schema/v1.4.3.7
python schema/v1.4.3.7/tests/integration/test_v1_4_3_7.py
python -m unittest discover -s tests/unit -v
~~~

## Governance gates

Do not treat a candidate as an approved release until the four Artifact identity decisions are explicitly approved, migration blockers are resolved, schema/fixture/traceability consistency is reconciled, and the scientific acceptance layer is implemented and tested. See docs/governance/DECISION_REGISTER.md and docs/OPEN_ISSUES.md.

## Key documents

- Research design baseline: docs/design/high-energy-theory-research-Skill-v1.6.5.md
- Latest candidate clarification: schema/v1.4.3.7/audit/高能理论物理研究-Skill-详细设计文档-v1.6.6-Artifact身份语义候选修订.md
- Schema candidate audit: schema/v1.4.3.7/audit/审计报告-v1.4.3.7.md
- Decision review: docs/governance/schema-v1.4.3.7-four-decisions-review.md
- Repository status: docs/REPOSITORY_STATUS.md
- Open issues: docs/OPEN_ISSUES.md
