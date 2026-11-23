# Downstream Standards Adoption Contract

简体中文版：[DOWNSTREAM_STANDARDS_ADOPTION.zh-CN.md](DOWNSTREAM_STANDARDS_ADOPTION.zh-CN.md)。

**Status:** adopted central contract  
**Effective date:** 2026-11-23  
**Scope:** project repositories consuming shared standards from high-energy-theory-research

## 1. Purpose

This contract makes downstream adoption explicit and reproducible. A downstream project must identify which central standards it has adopted and the exact immutable central revision that supplied them.

The contract prevents a project from silently following a moving main branch, mixing incompatible standard versions, or treating the presence of a copied document as proof of adoption.

## 2. Required lock record

Each adopting project stores a YAML lock file, normally at research/standards-lock.yaml or another path declared in its README. Use the [lock template](../../templates/research-standards-lock.yaml).

Required fields:

- lock_version: version of this lock-file format.
- central_repository: canonical owner/repository.
- standards_release: central release/tag when one exists; otherwise null.
- source_commit: full 40-character commit SHA that was reviewed and adopted.
- adopted_at: date of the downstream adoption decision.
- adoption_pr: downstream PR that integrated the lock and local references.
- adopted_profiles: stable IDs of the shared standards adopted by this project.
- local_extensions: project-local policy paths and their scope.
- deviations: explicit exceptions to central requirements, each with rationale and approval reference; use an empty list when there are none.

A release tag does not replace source_commit; record both when available. Do not invent a release identifier. Until the central project publishes a standards release, set standards_release to null and pin the full commit SHA.

## 3. Adoption profiles

The initial profile identifiers are:

- core-governance
- research-compute
- task-handoff
- scientific-diff
- research-quality-gate
- calculation-result-archive
- rcrps-v1.0.1
- git-review-and-merge
- document-review
- referee-response-and-manuscript-synchronization

Projects may adopt a subset when appropriate, but the lock must list each adopted profile explicitly. A numerical project adopting rcrps-v1.0.1 must also preserve its domain-specific extensions fields and validation procedures.

## 3A. Machine validation

The central repository provides `docs/schemas/standards-adoption-v1.0.0.schema.json` and `docs/schemas/validate_standards_adoption.py`. Run the validator against the repository's canonical lock file and, when present, the task-provenance record and standards validation report. It checks the record contract, known profile-to-document mappings, local extension paths/fingerprints, and task-to-lock/brief fingerprints. The central commit can additionally be checked against the local Git object database when the exact central object is available.

A passing structural validator establishes only that the declared adoption and evidence records are internally consistent. It does not establish that every requirement was followed during reasoning or that a physical result is correct. Task-level application remains subject to review of the actual work and its scientific evidence.

## 4. Local extensions and deviations

- Project-local physics rules remain in the owning project repository.
- A project may strengthen a central requirement.
- A project must not silently weaken or redefine an adopted central minimum.
- A deviation must name the central profile/requirement, explain why it is inapplicable or unsuitable, identify the project-owner decision/PR, and give a review date or condition for reconsideration.
- N/A under a task profile is not automatically a project-wide deviation.

## 5. Migration and updates

1. Read the central standards index and the exact pinned documents at source_commit.
2. Compare them with existing project instructions and policies.
3. Keep domain-specific rules; remove or redirect only duplicated shared text after reviewing inbound links and operational dependencies.
4. Add/update the lock file and link it from the project README/AGENTS.
5. Open a focused downstream PR. Do not edit a project's main automatically when the central standard changes.
6. Review the exact diff, validate links and tools, and record the downstream acceptance decision.
7. Update the lock only when a new central revision is deliberately adopted.

The central repository is authoritative for shared minimum standards. Downstream repositories remain authoritative for their scientific content, actual runs, inputs, native results, and project-specific acceptance criteria.

## 6. Current release state

RCRPS v1.0.1 is an adopted central result-data standard. The broader central standards set does not yet have a published semantic-versioned release. Until such a release is approved, downstream projects must pin a full commit SHA and use standards_release: null.

See the [Central Research Standards Index](CENTRAL_STANDARDS_INDEX.md).
