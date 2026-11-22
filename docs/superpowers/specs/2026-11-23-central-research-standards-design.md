# Central Research Standards Architecture

**Status:** Approved design; implementation is staged through reviewable phases  
**Approval date:** 2026-11-23  
**Canonical repository:** `lm846802297-bit/high-energy-theory-research`  
**Approved baseline:** `b713bfdc971d1118406f619fe3a3fb5c9614e2a7`

## 1. Purpose

Establish this repository as the single central source of general research standards, reusable Research Skills, templates, schemas, and validation tooling for the user's theoretical-physics, particle-physics, high-energy-physics, and numerical-phenomenology projects.

The central repository governs shared research process and evidence requirements. Each downstream research repository remains the canonical home for its own scientific model, derivations, project-specific code, input data, benchmarks, native calculation outputs, domain-specific validation, and accepted research records.

## 2. Goals

1. Maintain one authoritative version of shared research standards.
2. Make standards consumable by downstream repositories through pinned releases and full commit SHAs.
3. Define a common Research Quality Gate with explicit evidence and status semantics.
4. Integrate Superpowers' general software-engineering workflows without copying or forking its upstream implementation.
5. Provide reusable Research Skills, templates, schemas, scripts, and GitHub workflows where their contracts are stable.
6. Preserve existing research records, paths, historical outputs, and approved decisions.
7. Pilot adoption in `LZ-3-body-for-hdm` and the electroweak-phase-transition research repository before broader rollout.

## 3. Non-goals

- Do not create another central standards repository.
- Do not turn `research-ai-hub` into a second standards authority; it remains the multi-model orchestration project.
- Do not move or rewrite historical research results.
- Do not change frozen physics benchmarks or project-specific theoretical decisions.
- Do not promote candidate schemas or draft PRs to approved standards without their own review and release gates.
- Do not duplicate or modify Superpowers' upstream skills.
- Do not make GitHub Actions the default primary scientific-computation environment.
- Do not change branch-protection or repository-administration settings without separate explicit authorization.

## 4. Responsibilities and boundaries

### 4.1 Central repository

The central repository owns:
- shared research-quality and reproducibility standards;
- task handoff and evidence-reporting standards;
- general Research Skills and their distribution contract;
- generic templates and machine-readable schemas;
- reusable provenance, integrity, and report validators;
- reusable GitHub workflows/actions when their interfaces are stable;
- release tags, compatibility policy, and downstream adoption guidance.

### 4.2 Downstream project repositories

Each project repository owns:
- its scientific questions, models, assumptions, conventions, and derivations;
- project-specific calculation code and inputs;
- frozen benchmarks and reference data;
- actual run manifests, native outputs, logs, figures, and checksums;
- domain-specific numerical and physical validation;
- project-specific claims, research records, PRs, and accepted results.

A downstream project may add stricter requirements. It may not silently weaken the central minimum requirements. Where a central check is not scientifically applicable, the project must record N/A with a reason.

### 4.3 Research AI Hub

`research-ai-hub` remains responsible for provider access, model routing, independent model comparisons, and orchestration. It consumes the central standards at a pinned version and does not independently redefine them.

## 5. Two-layer standards model

### Layer 1 — shared minimum standards

The shared layer covers:
- exact source revision and Git provenance;
- input provenance and SHA-256;
- software/runtime/dependency and hardware capture;
- physical and numerical execution parameters;
- native output preservation and integrity;
- numerical convergence and uncertainty/error analysis where applicable;
- independent physical/scientific validation where applicable;
- relevant regression testing;
- independent code/research review;
- PR review and approved integration into the canonical branch.

The ten-item Research Quality Gate applies according to task class. Numerical-computation tasks must satisfy all applicable computation and validation items. Purely analytical or editorial tasks use a task-appropriate profile; non-applicable checks are N/A with an explicit reason, never silently omitted or marked PASS.

### Layer 2 — domain-specific profiles

Examples include:
- three-body dark-matter scattering: phase-space integration, recoil kinematics, AFH response matching, nuclear-response validation;
- electroweak phase transitions: thermal field theory, dimensional reduction, effective-potential and perturbative-order checks;
- UV–EFT matching: diagram completeness, counterterms, UV/IR separation, Ward identities, operator-basis reduction;
- gauge theory: Ward/Slavnov–Taylor identities, propagator poles, polarization completeness, gauge-parameter checks;
- numerical phenomenology: scan coverage, likelihood assumptions, experimental recasts, and uncertainty propagation.

Domain profiles remain in the relevant project repositories unless they are genuinely reusable across projects in that domain.

## 6. Existing material and migration rules

Reuse and reconcile existing material before adding new normative documents. Preserve established paths where practical.

The initial audit must distinguish:
- adopted/approved normative documents;
- merged documents whose internal status text may be stale;
- draft or candidate documents;
- implemented tools that are not yet normative;
- project-specific methods that should not be generalized;
- duplicated copies that should become pinned references or compatibility stubs.

Known source material includes the root `AGENTS.md`, `RESEARCH_COMPUTE_POLICY.md`, calculation archival policy, structured result data standard v1.0.0, Scientific Diff workflow, review checklist, Git merge policy, existing Research Skill, schemas, templates, LZ Research Task Handoff Standard, and the open Skill/RCRPS PRs.

The Schema v1.4.3.7 package remains candidate until its independent governance decisions and release gates are completed. RCRPS v1.0.0 is the currently merged structured result-record baseline. RCRPS v1.0.1 remains pending until its PR review and merge are completed.

## 7. Superpowers integration

Use Superpowers for general engineering process:
- brainstorming and planning;
- test-driven development;
- systematic debugging;
- verification before completion;
- independent code review;
- branch completion.

The central Research Skills add scientific requirements around source verification, conventions, physical derivations, provenance, numerical convergence, independent physical validation, and scientific claim status. They must not impose a fixed mathematical method where the model/researcher must choose a method based on the problem.

## 8. Cross-repository distribution and versioning

Downstream projects consume:
1. Research Skills through the supported agent skill mechanism;
2. reusable GitHub workflows/actions pinned to a reviewed full commit SHA;
3. templates, schemas, and validators from a pinned release or immutable commit.

Each downstream repository records the central repository, release identifier, full commit SHA, adopted profiles, and any project-specific extensions in a lock/configuration file.

Never make historical results depend on a moving `main` reference. Standards updates are adopted by downstream PRs; they do not automatically modify project main branches.

Use semantic versioning for central standards releases. A compatibility-preserving addition increments the minor version; an incompatible normative change increments the major version. Patch releases correct non-semantic errors without silently changing the acceptance meaning of historical runs.

## 9. Automation and human review boundaries

Automation may validate:
- file hashes and source identities;
- environment and run-manifest structure;
- required metadata and native-output inventories;
- schema validity, paths, byte counts, row counts, and checksum consistency;
- relevant software regression tests.

Project-specific scientific workflows must validate:
- analytic identities and limiting cases;
- conservation laws and symmetry/gauge constraints;
- numerical convergence, error estimates, and uncertainty;
- independent implementations or derivations appropriate to the claim.

Human review remains responsible for scientific interpretation, independent code review, acceptance of the PR, and merge approval. A green CI result, valid schema, checksum match, or successful execution cannot independently certify a physical claim.

The existing compute policy remains in force: primary computation runs in the actual selected execution environment; GitHub is the durable archive; GitHub Actions is for CI and independent verification, not the default primary calculation engine. Required research tests must run in an appropriate available environment; Actions availability is not a prerequisite for continuing research.

## 10. Phased implementation

- **Phase I — Existing-standard audit:** inventory normative sources, status, scope, overlap, conflicts, gaps, open PR dependencies, and recommended disposition. Deliver a central standards audit matrix.
- **Phase II — Standards consolidation:** publish the central standards index and reconcile the ten-item Quality Gate with existing adopted policies, without duplicating or weakening them.
- **Phase III — Research Skills:** add generic quality-gate, provenance, and physical-validation Skills while retaining the high-energy-theory-specific Skill.
- **Phase IV — Automation:** add validated manifest/environment/hash/output checks and reusable workflows/actions with tests.
- **Phase V — Downstream pilots:** adopt the pinned standards in LZ three-body and electroweak phase-transition repositories through separate PRs.
- **Phase VI — Release:** complete independent review, regression tests, documentation checks, and release gates; merge by PR using the repository's substantive-change merge policy and publish the first approved central standards release.

Each phase has its own plan, deliverables, validation, and review. Later phases do not begin merely because earlier documentation exists; their acceptance evidence must be recorded.

## 11. Phase I acceptance

Phase I is complete when:
1. every relevant existing policy, Skill, template, schema, workflow, and open PR has an identified source path and baseline revision;
2. each source is classified by approval/maturity status and scope;
3. duplicated, overlapping, stale, contradictory, and project-specific material is identified with evidence;
4. all material gaps are listed without prematurely implementing them;
5. each source has a recommended disposition: retain, reuse, extract, reconcile, pin/reference, keep project-local, or defer;
6. links and source references in the audit matrix are checked against the frozen baseline;
7. the audit is submitted in a focused PR and reviewed before merge.

## 12. Approval and change control

This design was approved by the project owner on 2026-11-23. Implementation proceeds phase by phase through reviewable branches and PRs. Changes to the approved architecture or scope must be documented as design revisions rather than silently introduced during implementation.
