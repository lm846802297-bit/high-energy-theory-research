# Phase I: Central Research Standards Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an evidence-backed audit matrix of the existing central research standards, Skills, templates, schemas, workflows, and dependent open PRs in `high-energy-theory-research`, without changing their normative meaning or project records.

**Architecture:** Keep the approved central design in `docs/superpowers/specs/2026-11-23-central-research-standards-design.md`. Add one governance audit matrix under `docs/governance/`, linking each audited source to its exact path, frozen baseline, status, scope, overlap, gaps, and recommended disposition. This phase is documentation-only; it does not consolidate or rewrite standards, add Skills, modify validators, change downstream repositories, or alter branch protection.

**Tech Stack:** Markdown; GitHub repository contents; Git SHA/blob identity; existing repository link conventions. No new runtime dependencies.

**Spec:** `docs/superpowers/specs/2026-11-23-central-research-standards-design.md`

## Global Constraints

- Baseline is `b713bfdc971d1118406f619fe3a3fb5c9614e2a7`.
- Work only on `docs/central-research-standards-phase-i-20261123`; do not write to `main`.
- Preserve existing normative files and historical records byte-for-byte.
- Do not promote candidate or draft material to approved status.
- Distinguish merged status from normative approval status; a merged file can still contain a proposed/candidate standard.
- Treat PR #27, #28, and #29 as open dependencies; do not merge, retarget, close, or rewrite them.
- Keep project-specific physics procedures in their project repositories unless demonstrably reusable.
- CI is not a mandatory research gate; do not change repository protection settings.
- Every audit conclusion must point to an inspected source path, commit, PR, or other evidence.
- The approved design document is already committed on this branch at commit `c6f14bce307f5129bd6879ae1e59f9510c2d472c`.

## Review Focus

1. **Status mismatch:** a file may be merged but still say “proposed”; record both Git integration status and normative maturity separately.
2. **Overlapping authority:** compute, archival, structured-result, task-handoff, and reporting rules overlap; identify exact authority boundaries instead of merging prose prematurely.
3. **Candidate leakage:** Schema v1.4.3.7 and RCRPS v1.0.1 must not be presented as released standards.
4. **Project-specific leakage:** UV–EFT, three-body scattering, and other physics checks must not become universal requirements without a generalizable contract.
5. **Workflow mismatch:** the current repository says CI is optional; the Quality Gate must require relevant verification evidence without making Actions the sole way to obtain it.

---

## File Structure

- Create: `docs/governance/CENTRAL_STANDARDS_AUDIT_MATRIX.md` — the Phase I inventory and disposition matrix.
- Modify: `README.md` — add a short link to the approved central design and Phase I audit matrix, without changing existing research instructions.
- Modify: `README.zh-CN.md` — add the corresponding Chinese navigation entry.
- Modify: `CHANGELOG.md` — record this Phase I audit deliverable and its exact status.
- Do not modify: `AGENTS.md`, `RESEARCH_COMPUTE_POLICY.md`, archival policy, structured-result schema, existing Skills, candidate schema package, active research records, or open PR branches.

## Task 1: Build the source inventory and disposition matrix

**Files:**
- Create: `docs/governance/CENTRAL_STANDARDS_AUDIT_MATRIX.md`

**Interfaces:**
- Consumes: approved architecture spec at `docs/superpowers/specs/2026-11-23-central-research-standards-design.md`.
- Produces: a source-of-truth audit with columns for source/path, frozen-baseline identity, integration state, normative maturity, scope, overlap/dependency, gap/conflict, disposition, and follow-up owner/phase.

- [ ] **Step 1: Record repository baseline and audit method**

Record repository, branch, baseline SHA, audit date, and scope. State that the audit covers central normative docs, Skills, references, templates, schemas, scripts, workflows, and open PRs.

- [ ] **Step 2: Inventory core policy sources**

Include at minimum:
  - `AGENTS.md`
  - `RESEARCH_COMPUTE_POLICY.md`
  - `docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md`
  - `docs/STRUCTURED_RESULT_DATA_STANDARD.md`
  - `docs/scientific-diff-workflow.md`
  - `docs/review-checklist.md`
  - `docs/governance/GIT_MERGE_POLICY.md`
  - `docs/governance/DECISION_REGISTER.md`

For each, record what it governs, whether it is approved/adopted/proposed/candidate, and which parts of the ten-item gate it already covers.

- [ ] **Step 3: Inventory task handoff and claim/evidence sources**

Inspect and record:
  - LZ project's merged `research/RESEARCH_TASK_HANDOFF_STANDARD.md` and `research/_template/RESEARCH_TASK_BRIEF.md` from PR #72, as external project-specific source material;
  - central `templates/research-change.md`, `templates/project-record.md`, and `templates/claim-evidence-matrix.md`;
  - Skill references `evidence-and-claim-gates.md`, `source-and-version-audit.md`, and `task-router.md`.

Identify which concepts are reusable centrally and which remain domain/project-specific.

- [ ] **Step 4: Inventory Skills, schemas, validators, and workflows**

Record:
  - `skills/high-energy-theory-research/SKILL.md` and its references/scripts;
  - `docs/schemas/research-result-record-v1.0.0.schema.json` and validator/tests;
  - candidate `schema/v1.4.3.7/` and its release gates;
  - existing `.github/workflows/` files and any shared automation interfaces.

Separate existing executable checks from proposed future automation. Do not claim a validator proves physical correctness.

- [ ] **Step 5: Record open PR dependencies**

Record PR #27 (cross-repository Research Skill and benchmark work), PR #28 and #29 (RCRPS v1.0.1 work), their base/head relationship, review/test status, and whether they block or merely inform Phase I. Do not alter them.

- [ ] **Step 6: Write the disposition matrix**

Use exactly these dispositions:
  - `RETAIN_AS_CENTRAL_AUTHORITY`
  - `REUSE_WITHOUT_DUPLICATION`
  - `EXTRACT_GENERAL_RULES`
  - `RECONCILE_OVERLAP`
  - `PIN_AS_VERSIONED_DEPENDENCY`
  - `KEEP_PROJECT_LOCAL`
  - `DEFER_PENDING_RELEASE_GATE`

Add a separate status field; never infer approval from a merged commit alone.

- [ ] **Step 7: Add the ten-item coverage map**

For each Quality Gate item, cite existing source coverage and classify the state as `covered`, `partially_covered`, `not_covered`, or `not_applicable_by_task_profile`. Do not yet create new policy text.

- [ ] **Step 8: Review the matrix against the source inventory**

Check every row against the exact source. Ensure each conflict, gap, and recommendation is evidence-linked. Mark unknown items explicitly rather than guessing.

## Task 2: Add navigation and changelog entries

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1 audit matrix and approved design document.
- Produces: discoverable links; no new normative content.

- [ ] **Step 1: Add the central-standards architecture link to both READMEs**

Place it in the existing governance/starting-point section. Preserve the existing numbered instructions and all project-specific links.

- [ ] **Step 2: Add a dated changelog entry**

State that the approved architecture design and Phase I audit matrix are added on the topic branch. Do not claim Phase I complete until Task 1 validation and PR review are finished.

- [ ] **Step 3: Check relative links**

Verify both READMEs link to the exact spec and matrix paths. Confirm no existing links were removed or redirected.

## Task 3: Verify the Phase I deliverable

**Files:**
- Test/read: `docs/governance/CENTRAL_STANDARDS_AUDIT_MATRIX.md`
- Test/read: `README.md`
- Test/read: `README.zh-CN.md`
- Test/read: `CHANGELOG.md`

- [ ] **Step 1: Verify source references**

For each cited file, confirm the path exists at the frozen baseline or label it explicitly as an external/downstream source or open PR.

- [ ] **Step 2: Verify status semantics**

Check that adopted, proposed, candidate, draft, merged, and pending-review states are not conflated.

- [ ] **Step 3: Verify ten-item coverage**

Confirm every gate item has an evidence-backed coverage classification and that project-specific tests are not falsely generalized.

- [ ] **Step 4: Verify preservation**

Compare the branch diff and ensure only the four planned documentation files are changed (the already committed approved design document is included as the fifth tracked deliverable). No calculation source, data, schema, or historical record should be changed.

- [ ] **Step 5: Report actual verification**

Record commands and exact outputs. Do not claim link checks, tests, or review passed unless they were actually run.

- [ ] **Step 6: Open a focused Draft PR**

Target `main`, use a merge commit as the expected integration strategy, and state that Phase I is an audit/documentation deliverable only. Do not merge without review.

---

## Acceptance Criteria

Phase I is ready for review when:
1. The audit matrix covers every required source category and relevant open PR.
2. Each source has integration state and normative maturity recorded separately.
3. Every overlap/conflict/gap has an evidence-linked disposition.
4. The ten-item Quality Gate has a complete coverage map.
5. Candidate and draft material remain explicitly unreleased.
6. Project-specific physics procedures remain project-local unless a reusable general rule is extracted.
7. Both READMEs link to the design and matrix; the changelog reports the correct status.
8. The branch diff contains only approved design/audit/navigation documentation.
9. The PR description lists actual verification and remaining work.
10. No changes are made to `main` before PR review and approval.
