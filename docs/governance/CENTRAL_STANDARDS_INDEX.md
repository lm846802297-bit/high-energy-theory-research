# Central Research Standards Index

简体中文版：[CENTRAL_STANDARDS_INDEX.zh-CN.md](CENTRAL_STANDARDS_INDEX.zh-CN.md)。

**Status:** normative navigation index  
**Owner:** central research infrastructure repository  
**Scope:** shared minimum standards for research repositories that adopt this framework

This index identifies the single central authority for each shared requirement. It is a navigation and precedence document; the linked standards contain the normative details.

## 1. Shared standards

| Area | Canonical authority | What it governs |
|---|---|---|
| Repository entry and agent instructions | [AGENTS.md](../../AGENTS.md) | Preflight, repository boundaries, task routing, and mandatory entry-point instructions |
| Research governance and source hierarchy | [Research Governance Standard](../RESEARCH_GOVERNANCE_STANDARD.md) | Authority, source hierarchy, conflict resolution, scientific status, and central/project boundaries |
| Compute execution | [Research Compute Policy](../../RESEARCH_COMPUTE_POLICY.md) | Primary execution environment, GitHub archive, Actions independent verification, and run provenance |
| Task handoff | [Research Task Handoff Standard](../RESEARCH_TASK_HANDOFF_STANDARD.md) and [brief template](../../templates/research-task-brief.md) | Pre-execution task specification and return record for substantive work |
| Scientific change lifecycle | [Scientific Diff Workflow](../scientific-diff-workflow.md) | Project/workstream/change/run/claim hierarchy and question-to-evidence traceability |
| Research Quality Gate | [Research Quality Gate](RESEARCH_QUALITY_GATE.md) | Ten shared acceptance areas, task profiles, and PASS/FAIL/BLOCKED/NOT RUN/N/A semantics |
| Research communication | [Scientific Diff §11](../scientific-diff-workflow.md#11-research-reporting-and-communication-standard) | Conclusion/evidence/results/remaining-work reporting and evidence-proportional language |
| Calculation-result archival | [Calculation-result archival policy](../CALCULATION_RESULT_ARCHIVAL_POLICY.md) | Native outputs, extract-before-upload, provenance, hashes, remote verification, and CI boundary |
| Structured numerical records | [RCRPS v1.0.1](../STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.md) and [adoption record](RCRPS_V1.0.1_ADOPTION_RECORD.md) | Run manifests, result summaries, validation reports, source-control provenance, and CSV conventions |
| Scientific review | [Scientific Change Review Checklist](../review-checklist.md) | Baseline, derivation, computation, physical claims, dependencies, and decisions |
| Document review and migration | [Research Document Review Standard](../DOCUMENT_REVIEW_STANDARD.md) | Document identity, authority, scientific content, citations, consistency, reproducibility, links, disposition, and safe migration |
| Referee response and manuscript synchronization | [Referee Response and Manuscript Synchronization Standard](../REFEREE_RESPONSE_AND_MANUSCRIPT_SYNCHRONIZATION_STANDARD.md) | Reviewer-facing argument completeness, separation from internal manuscript tracking, preservation of independent scientific arguments, and review records |
| Git and integration | [Git merge policy](GIT_MERGE_POLICY.md) | PR lifecycle, review, merge strategy, main-branch discoverability, and post-merge verification |
| High-energy-theory methods | [Research Skill](../../skills/high-energy-theory-research/SKILL.md) | Domain-specific literature, derivation, UV–EFT, loop, and phenomenology workflows |
| Project/workstream navigation | [Project registry](../../projects/README.md) | Project identity, parent/workstream hierarchy, and canonical repository entry points |

## 2. Normative status and version rules

- **Adopted:** the document is an approved central authority. Downstream repositories adopt it through a reviewed PR pinned to a full commit SHA or release.
- **Historical compatibility:** the document/schema remains available for validating or interpreting old records, but is not the default for new work.
- **Candidate / draft:** the document or tool is not a normative requirement. Do not promote it because it is present in the repository or a workflow passes.
- **Implemented, not normative:** software exists, but its contract or acceptance meaning has not been approved.

RCRPS v1.0.1 is the adopted central structured-result standard for new substantial numerical runs from 2026-11-23. RCRPS v1.0.0 remains the historical compatibility profile; its schema and historical records are unchanged. Research-record Schema v1.4.3.7 remains a separate candidate and is not the result-data schema.

## 3. Adoption and precedence

1. This central repository owns shared minimum standards, reusable Skills, templates, schemas, validators, and reusable automation.
2. Each project repository owns its models, assumptions, domain conventions, calculations, inputs, native outputs, scientific claims, and domain-specific acceptance criteria.
3. A project may add stricter compatible requirements. It must not silently weaken an adopted central minimum.
4. A downstream repository records the exact central commit, optional release identifier, adopted profiles, local extensions, and any approved deviations in its standards lock file. See the [Downstream Standards Adoption Contract](DOWNSTREAM_STANDARDS_ADOPTION.md) and [lock template](../../templates/research-standards-lock.yaml).
5. Standards updates do not automatically change downstream repositories. Adoption occurs through a separate reviewed PR.

## 4. Recommended reading order

For a new substantive research task:

1. Read the downstream repository's AGENTS.md and project README.
2. Read this index and the [Research Governance Standard](../RESEARCH_GOVERNANCE_STANDARD.md).
3. Complete a [Research Task Brief](../../templates/research-task-brief.md) under the [Task Handoff Standard](../RESEARCH_TASK_HANDOFF_STANDARD.md).
4. Apply the task-appropriate profile in the [Research Quality Gate](RESEARCH_QUALITY_GATE.md).
5. Follow the relevant compute, archival, structured-record, scientific-diff, and Git policies.
6. Read the project's domain-specific profile and primary scientific sources.

## 5. Explicitly project-local material

Do not move the following into the shared minimum merely because a project has documented them:

- LZ three-body kinematics, AFH response conventions, isotope choices, halo models, detector response, and likelihood assumptions;
- UV–EFT diagram completeness, renormalization prescriptions, Ward identities, counterterm bookkeeping, and operator-basis conventions for a particular model;
- Collider-specific UFO, MadGraph, Pythia8, Delphes, event-sample, cutflow, and detector-card rules;
- thermal field theory, dimensional reduction, electroweak phase-transition observables, and project benchmarks;
- model-specific field content, physical assumptions, input datasets, frozen benchmarks, and numerical acceptance thresholds.

A reusable domain profile may be promoted centrally only when its scope, ownership, interface, and independent validation are explicit.
