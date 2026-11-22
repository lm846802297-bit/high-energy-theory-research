# Central Research Standards Audit Matrix

**Audit phase:** Phase I — Existing-standard audit  
**Audit date:** 2026-11-23  
**Canonical repository:** lm846802297-bit/high-energy-theory-research  
**Audited default branch:** main  
**Frozen main baseline:** b713bfdc971d1118406f619fe3a3fb5c9614e2a7  
**Audit branch:** docs/central-research-standards-phase-i-20261123  
**Approved architecture:** docs/superpowers/specs/2026-11-23-central-research-standards-design.md  
**Scope approval:** The project owner approved application to all theoretical-physics, particle-physics, high-energy-physics, numerical-phenomenology, and related research-computation projects on 2026-11-23.

## 1. Purpose and audit boundary

This matrix inventories the existing central policies, research workflows, templates, Skills, schemas, validators, GitHub workflows, and relevant open pull requests. It records what already exists and how it should be reused in the approved central architecture.

This is an audit and disposition document. It does not itself amend any existing normative policy, approve a candidate schema, close or merge an open PR, change a downstream repository, or certify a scientific result.

The audit uses the exact main baseline above. Open PR content is identified separately by PR number and head/base information; it is not treated as part of main.

### 1.1 Status semantics

Git integration state and normative maturity are independent fields:

- **Merged on main:** the source is present in the audited main tree.
- **Open / Draft / Ready for review:** the source exists on a PR branch and is not yet integrated.
- **Mandatory / author-approved / adopted:** the source has an explicit current normative role within its stated scope.
- **Proposed / candidate / draft:** the source has not passed its required approval or release gate.
- **Implemented:** code or a workflow exists; implementation alone does not make its behavior a universal research requirement.

A merged PR does not automatically resolve a stale “proposed” status line inside the merged document. A passing software test does not establish physical correctness.

### 1.2 Disposition vocabulary

| Disposition | Meaning |
|---|---|
| RETAIN_AS_CENTRAL_AUTHORITY | Keep the existing source as the authoritative central document or entry point |
| REUSE_WITHOUT_DUPLICATION | Use the existing source or link to it; do not create a competing copy |
| EXTRACT_GENERAL_RULES | Extract reusable requirements while preserving domain-specific details in their original project |
| RECONCILE_OVERLAP | Resolve inconsistent status, duplicate wording, or competing contracts before release |
| PIN_AS_VERSIONED_DEPENDENCY | Consume the source from a fixed release and full commit SHA |
| KEEP_PROJECT_LOCAL | Retain project-specific physics, benchmarks, inputs, and procedures in the project repository |
| DEFER_PENDING_RELEASE_GATE | Do not promote the item until its explicit review, decision, or validation gate is complete |

## 2. Executive findings

1. The repository already contains most of the substance required for a central research-quality framework: compute provenance, native-output archival, structured run records, scientific change tracking, claim/evidence assessment, and merge governance.
2. The ten-item Research Quality Gate is not yet defined as one versioned, task-profile-aware standard. Its requirements are distributed across several documents. Phase II should consolidate references and acceptance semantics rather than duplicate their full text.
3. The merged RCRPS v1.0.0 documentation contains a status inconsistency: the standard itself still says “Proposed for adoption”, while the merged root instructions and archival policy direct researchers to follow it.
4. Two open PRs, #28 and #29, propose overlapping but non-identical RCRPS v1.0.1 revision-provenance designs. They must be reconciled into one schema contract before v1.0.1 is published.
5. The reusable high-energy-theory Research Skill exists. PR #27 adds cross-repository distribution, task-specific modules, and a benchmark harness. Its latest reported central and Windows validation workflows pass, but the benchmark protocol remains draft and no formal with-Skill/without-Skill A/B runs or sealed holdout have been executed.
6. Schema v1.4.3.7 remains a candidate, not a released central standard. Its four Artifact decisions remain pending; migration and fingerprint-contract gaps remain open.
7. The existing GitHub workflows are standalone repository workflows. The main tree has no reusable workflow declared with workflow_call and no composite action directory. Reusable cross-repository automation is future work, not an existing capability.
8. RESEARCH_COMPUTE_POLICY.md is byte-identical in the current main branches of this repository and research-ai-hub (Git blob SHA 3e6abce6e864b22db65cf9d733eb819958b0c153). The central repository should own the canonical copy; downstream adoption should use a pinned reference rather than long-term independent copies.
9. LZ-3-body-for-hdm already has a merged ten-field Research Task Handoff Standard. Its general task-specification structure is reusable; its three-body momentum examples and AFH conventions must remain project-local.
10. CI is explicitly optional as a research/merge gate under the existing policy. The new Quality Gate must require appropriate verification evidence, but must not make GitHub Actions the only acceptable execution route.

## 3. Core policy inventory

| Source and baseline identity | Integration state | Normative maturity and scope | Existing coverage / overlap / gap | Recommended disposition |
|---|---|---|---|---|
| **AGENTS.md** — blob 0b5df9eb46f079f31e0284fcf8bd662c6f6720ee | Merged on main | Mandatory instructions for agents and contributors in this repository | Covers source conventions, analytical completeness, independent checks, numerical reporting, provenance, archival, claim discipline, PR review, and the CI boundary. It is the main operational entry point but is not yet a downstream version-lock contract. | RETAIN_AS_CENTRAL_AUTHORITY |
| **RESEARCH_COMPUTE_POLICY.md** — blob 3e6abce6e864b22db65cf9d733eb819958b0c153 | Merged on main | Author-approved normative policy; effective 2026-11-20; current text scopes it to this research project | Defines primary execution by actual environment, GitHub as canonical archive, Actions as independent verification, and required run provenance. The exact same blob is present in research-ai-hub main, creating two maintained copies. | RETAIN_AS_CENTRAL_AUTHORITY; RECONCILE_OVERLAP |
| **docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md** — blob c8755f2890fded6c187486791d4b3eb0abb5e6fe | Merged on main | Mandatory repository-wide policy for numerical and computational research | Covers native/uncompressed outputs, large/restricted files, run provenance, hashes, remote verification, and optional CI. It complements rather than replaces scientific validation. Its scope text is repository-oriented and must be connected to downstream adoption. | RETAIN_AS_CENTRAL_AUTHORITY |
| **docs/STRUCTURED_RESULT_DATA_STANDARD.md** — blob 6cb56872c3da8528b41a9d96a21aae3f83f8306d | Merged by PR #25, merge commit b713bfdc971d1118406f619fe3a3fb5c9614e2a7 | PR #25 is merged and root policies treat v1.0.0 as adopted; the document's own status line still says “Proposed for adoption” | Defines run_manifest, result_summary, validation_report, native tabular outputs, status separation, domain extensions, and validation. The status line conflicts with the merged PR title and mandatory references in AGENTS.md and the archival policy. | RECONCILE_OVERLAP |
| **docs/STRUCTURED_RESULT_DATA_STANDARD.zh-CN.md** — blob 89873b08e8e1b25f765e3ecc861c5a0c96b1107c | Merged on main | Chinese counterpart of v1.0.0; carries the same proposed/adoption wording ambiguity | Must remain semantically aligned with the English standard and any future v1.0.1 decision. | RECONCILE_OVERLAP |
| **docs/schemas/research-result-record-v1.0.0.schema.json** — blob 8c072cf088e1cab39b0a18411d81682c0cc8ab44 | Merged on main | Adopted v1.0.0 data-record schema baseline | Validates run_manifest, result_summary, and validation_report structure and selected file/hash/CSV properties. It validates record structure, not physical correctness. Keep it distinct from the unreleased rich research-record Schema v1.4.3.7. | RETAIN_AS_CENTRAL_AUTHORITY |
| **docs/schemas/validate_result_records.py** — blob aee7bdf00ea14f6b562f8a18a9d195d9df9ba7bf | Merged on main | Implemented validator for the v1.0.0 result-record profile | Validates schema and referenced output metadata. Its missing-dependency error currently points to research/schemas/requirements-result-validation.txt, while the actual requirements file is under docs/schemas/. This is a small implementation/documentation mismatch to correct in a later focused change. | REUSE_WITHOUT_DUPLICATION |
| **docs/scientific-diff-workflow.md** — blob 0f8ad1257c73cd82decd0560c2c95e3cc859bbda | Merged on main | Repository research workflow; applies to theoretical and phenomenological research | Defines project → workstream → research change → run → claim, evidence dependencies, and the scientific question-to-manuscript chain. It is broader than a numerical quality checklist and should remain the research-change framework. | RETAIN_AS_CENTRAL_AUTHORITY |
| **docs/review-checklist.md** — blob 54b539cc3ab53de8e8d6df7b8539d19feb8367db | Merged on main | Existing scientific-change review checklist | Covers baseline, scope, derivation, computation, claims, dependencies, and decisions. It overlaps with Quality Gate items 6–9 but does not define one machine-readable gate or a uniform independent-review contract. | REUSE_WITHOUT_DUPLICATION |
| **docs/governance/GIT_MERGE_POLICY.md** — blob 8954183a6d1440518b534c4f30137dfa25ba9642 | Merged on main | Normative repository policy | Establishes merge-commit default, pre-merge review, main as canonical research archive, and PR lifecycle. It is the existing authority for Quality Gate item 10 within this repository. | RETAIN_AS_CENTRAL_AUTHORITY |
| **docs/governance/DECISION_REGISTER.md** — blob a8b2f55753d10e3f0fd5fab8a3758b8e880647cd | Merged on main | Normative register of candidate-schema decisions; four entries remain pending | DD-ART-007 through DD-ART-010 are recommendations, not approvals. The register prevents candidate rules from being promoted merely because they appear in the package. | DEFER_PENDING_RELEASE_GATE |
| **docs/REPOSITORY_STATUS.md** — blob 30684a31694ee7d0f3ab31dde9a42fe5fbe61b4b | Merged on main | Status report, not a normative standard; header says “As of 2026-10-21” | Records candidate-schema and Skill implementation maturity. Its date predates the later PR #25 merge and current PR #27/#29 activity; refresh it when the candidate/Skill governance work is next reconciled. | RECONCILE_OVERLAP |
| **docs/OPEN_ISSUES.md** — blob fe0b095e7d82bdd55f57e83d61cf52f2359c6752 | Merged on main | Open-issue and release-blocker register | Records pending Artifact decisions, migration ambiguity, fixture-index version discrepancy, undefined FingerprintInputs contract, and missing real-task scientific acceptance. Keep these blockers visible. | DEFER_PENDING_RELEASE_GATE |

## 4. Task handoff, templates, and claim/evidence records

| Source and baseline identity | Integration state | Normative maturity and scope | Existing coverage / overlap / gap | Recommended disposition |
|---|---|---|---|---|
| LZ **research/RESEARCH_TASK_HANDOFF_STANDARD.md** — blob 5e09d78a6020af78562ed208da82a02feb278ee1; PR #72 merge commit 2d116d973f0e9ac48b6cb189f576d2104b77dd6a | Merged in LZ-3-body-for-hdm, not in this central repository | Mandatory for substantive tasks in the LZ repository | Contains ten fields: research question; source papers/files/repositories; Git commit/version; conventions; assumptions/approximations; known validated results; required independent derivation; numerical checks; expected output; unresolved questions. This is the best existing source for a reusable task handoff. It also contains three-body-specific momentum labels and examples. | EXTRACT_GENERAL_RULES; KEEP_PROJECT_LOCAL |
| LZ **research/_template/RESEARCH_TASK_BRIEF.md** — blob dbbb4be31e6046dde5dfe99ea75a8f358256c0bf | Merged in LZ-3-body-for-hdm | Project template; used with the LZ handoff standard | Provides a fillable ten-section brief and return record. The general fields can become a central template; LZ-specific examples and references must not be copied as universal physics rules. | EXTRACT_GENERAL_RULES |
| **templates/research-change.md** — blob 4ad7db0598ac687bf2c6abb9fb9ceebd73ce2f3d | Merged on main | Existing central template | Captures research-change identity, question, scope, conventions, derivation, provenance, verification, claim assessment, impact, and final decision. It is a change/result record, not a substitute for a pre-execution task handoff. | REUSE_WITHOUT_DUPLICATION |
| **templates/claim-evidence-matrix.md** — blob 40911b8edcc862c9c8242f4a7a752d615a5fac14 | Merged on main | Existing central template | Captures each claim, valid domain, derivation/computational/independent evidence, status, manuscript location, and remaining action. It is the correct claim-level evidence ledger. | REUSE_WITHOUT_DUPLICATION |
| **templates/project-record.md** — blob db1d12c7612756c68cc76e813de2d333ef1e3cd5 | Merged on main | Existing project/workstream template | Defines project identity, scope, workstreams, evidence, and next actions. It is a project-navigation and planning template, not a run manifest. | REUSE_WITHOUT_DUPLICATION |

The LZ handoff standard and central research-change template serve different lifecycle purposes. The central standard should specify the task before execution; the research-change record should preserve the scientific delta and its evidence. They should be linked, not collapsed into one oversized form.

## 5. Skills, validators, and automation inventory

| Source and baseline identity | Integration state | Normative maturity and scope | Existing coverage / overlap / gap | Recommended disposition |
|---|---|---|---|---|
| **skills/high-energy-theory-research/SKILL.md** — blob 7321d6dd7ce4afed1e1d374f9ff4569d74e7d256 | Merged on main | Reusable Skill for high-energy theory and phenomenology; domain-specific rather than universal across every research field | Already defines conventions, evidence classes, independent checks, claim traceability, archival, and a research workflow. Preserve its UV–EFT and phenomenology-specific instructions. A separate generic Quality Gate Skill can call it when the task is in this domain. | RETAIN_AS_CENTRAL_AUTHORITY; KEEP_PROJECT_LOCAL for domain-specific material |
| **references/evidence-and-claim-gates.md** — blob d2477d93d1d030479803ab9997b8d68fe605f806 | Merged on main | Skill reference | Provides explicit claim statuses and minimum claim evidence. It overlaps with the claim/evidence matrix and AGENTS.md but supplies the Skill-facing operational form. | REUSE_WITHOUT_DUPLICATION |
| **references/source-and-version-audit.md** — blob 275d47bc4844dc212854123e351ec5d841ebd097 | Merged on main | Skill reference | Covers literature versions, code/data provenance, run identity, and experimental constraints. Reuse as a Skill reference rather than copy its paragraphs into every standard. | REUSE_WITHOUT_DUPLICATION |
| **references/task-router.md** — blob de8c410f649ca89eff07eafd2993871d01d844cb | Merged on main | Skill task router | Routes literature, derivation, symbolic, model-consistency, phenomenology, experimental-reinterpretation, and manuscript tasks to appropriate checks. It already expresses task profiles conceptually. | REUSE_WITHOUT_DUPLICATION |
| **skills/high-energy-theory-research/scripts/fingerprint_inputs.py** — blob e2bc1032a889cad194b7039a5033dcea27b5a619 | Merged on main | Candidate implementation; its module explicitly says the contract remains candidate-only | Uses RFC 8785 canonicalization and SHA-256, but the central open-issues register says the FingerprintInputs field/hash contract is not fully defined. Do not make it a mandatory cross-project interface until its contract is approved. | DEFER_PENDING_RELEASE_GATE |
| **validate_project_records.py / validate_project_registry.py** | Merged on main | Central-checkout validators for the candidate research-record schema and project registry | Useful in this repository when run with their schema/helper dependencies. PR #27 explicitly clarifies that the standalone user-level Skill export does not contain those dependencies; downstream projects must not assume these validators are independently available. | REUSE_WITHOUT_DUPLICATION; PIN_AS_VERSIONED_DEPENDENCY only if the required schema/tool bundle is explicitly adopted |
| **schema/v1.4.3.7/** | Merged on main as a candidate bundle | Candidate / not released | Includes 25 schema entry points and 83 indexed fixtures. Open issues record four pending Artifact decisions, migration blocked by ambiguous validation_ids, fixture-index version mismatch, and incomplete FingerprintInputs semantics. The synthetic pilot is not a real scientific-acceptance suite. | DEFER_PENDING_RELEASE_GATE |
| **.github/workflows/schema-validation.yml** — blob 292c5d5d0d71b4d0bfc6fa0cf178f517550abd3a | Merged on main | Repository-specific candidate-schema and Skill/benchmark validation workflow | Runs candidate schema, fixture, integration, Skill, and selected pilot checks. It is a standalone workflow, not a reusable workflow. | REUSE_WITHOUT_DUPLICATION; later extract stable interfaces |
| **.github/workflows/structured-result-validation.yml** — blob ccb0c10cf9d70c3f737d74c2f3801a0b9675c90f | Merged on main | Repository-specific RCRPS v1.0.0 validation workflow | Runs the structured result validator and its regression suite. It is a standalone workflow, not a reusable workflow. | REUSE_WITHOUT_DUPLICATION; later extract stable interfaces |
| **.github/workflows/rc001-*.yml** | Merged on main | Project/workstream-specific workflows | Three workflows target RC-001 UV–EFT/QLD calculations. Their source paths, dependencies, and assertions are not generic research-quality actions. | KEEP_PROJECT_LOCAL |
| **.github/actions/** | No directory in audited main tree | No composite action currently present | The audited main tree contains five standalone workflow files, none declaring workflow_call; no reusable workflow or composite action was found. | Defer reusable automation to Phase IV |

## 6. Relevant PR and downstream dependency audit

The following PRs were inspected because they affect shared standards, schemas, Skills, or downstream adoption.

| PR / source | Current state at audit | Evidence and dependency | Audit disposition |
|---|---|---|---|
| Central PR #6 — Schema v1.4.3.7 governance | Open / Draft / unmerged | Candidate-schema governance and migration safety. The PR body preserves candidate/not_released status and commit_allowed=false. It remains 41 commits behind current main by the GitHub compare endpoint; do not treat its candidate rules as approved central standards. | DEFER_PENDING_RELEASE_GATE |
| Central PR #25 — RCRPS v1.0.0 | Merged | Merge commit b713bfdc971d1118406f619fe3a3fb5c9614e2a7. Establishes the v1.0.0 structured result-record baseline. The document status line still needs reconciliation. | RETAIN_AS_CENTRAL_AUTHORITY; RECONCILE_OVERLAP |
| Central PR #27 — Research Skill modules and distribution | Open / Draft / unmerged | Current head 6f5194ff688879466ea0fd995de78a9f089fd708; 130 commits ahead and 41 behind main. Latest Candidate schema validation run 45055223059 and Windows Skill installer validation run 45055223056 both completed successfully on that exact head. The Windows workflow includes PowerShell 5.1 installer/helper regression execution. The benchmark protocol remains draft; no formal A/B model runs or sealed holdout have been executed. | REUSE_WITHOUT_DUPLICATION; PIN_AS_VERSIONED_DEPENDENCY only after review and release |
| Central PR #28 — RCRPS v1.0.1 revision_context proposal | Open / Draft / unmerged | Stacked on the former v1.0.0 candidate branch, not directly on current main; five commits behind main by compare. Uses source.revision_context with checked_out_sha, pr_head_sha, base_sha, and tested_merge_sha semantics. Its two reported workflow checks currently conclude failure on its branch head; do not infer a schema defect without inspecting executed steps. | RECONCILE_OVERLAP |
| Central PR #29 — RCRPS v1.0.1 source_control proposal | Open / Ready for review / unmerged | Directly based on current main at b713bfdc971d1118406f619fe3a3fb5c9614e2a7; current head 518f23008d84d20daa3e9f68a01b374daaf75fb3, 11 commits ahead and 0 behind. Structured result validation run 45053725175 and candidate-schema validation run 45053725188 succeeded. Uses execution.source_control with PR head/base/tested-merge SHAs. | RECONCILE_OVERLAP; review one canonical v1.0.1 contract before release |
| LZ PR #72 — Research Task Handoff Standard | Merged in LZ-3-body-for-hdm | Merge commit 2d116d973f0e9ac48b6cb189f576d2104b77dd6a. Provides the ten-field task handoff and template inspected above. | EXTRACT_GENERAL_RULES; KEEP_PROJECT_LOCAL |
| research-ai-hub PR #1 | Open / unmerged | research-ai-hub remains the model/provider orchestration repository. Its main branch currently contains the same RESEARCH_COMPUTE_POLICY.md blob as this repository. | PIN_AS_VERSIONED_DEPENDENCY; RECONCILE_OVERLAP |

### 6.1 RCRPS v1.0.1 conflict requiring a single decision

PR #28 and PR #29 address the same underlying ambiguity—distinguishing the PR source head, target base, and actual checked-out/tested merge revision—but they do not define the same field layout:

- PR #28 proposes source.revision_context, including checked_out_sha and explicit checkout semantics.
- PR #29 proposes execution.source_control, with pr_head_sha, base_sha, tested_merge_sha, and workflow metadata.

These should not be merged as two independent standards. Review the semantics and downstream compatibility, select one canonical contract, and preserve the unselected design as a superseded proposal if useful. Until then, v1.0.0 remains the merged baseline and v1.0.1 remains unadopted.

### 6.2 Research Skill release boundary

PR #27's latest reported central validation and Windows installer workflow passed on its current head. This is meaningful software evidence for the implemented checks. It does not mean the Research Skill benchmark has established an A/B performance improvement: the protocol and environment lock remain draft, and formal model runs/holdout evaluation have not occurred. Keep software-installation validation and scientific/agent-performance evaluation as separate statuses.

## 7. Ten-item Research Quality Gate coverage map

The labels below describe whether the current central sources cover the subject. They do not claim that every downstream project already enforces the requirement.

| # | Proposed Quality Gate item | Existing evidence and source coverage | Coverage | Gap / Phase II action |
|---:|---|---|---|---|
| 1 | Exact source version and Git commit SHA | RESEARCH_COMPUTE_POLICY.md §§3, 5; archival policy §4; RCRPS v1.0.0 run_manifest; source-and-version-audit reference; LZ task brief §3 | covered | Define one central minimum field contract and downstream lock interaction. |
| 2 | Input provenance and SHA-256 | Archival policy §§3–5; RCRPS v1.0.0 inputs/output records; source-and-version-audit; fingerprint_inputs.py candidate | covered | Keep byte-level SHA-256 mandatory where bytes are available; do not promote the incomplete FingerprintInputs candidate prematurely. |
| 3 | Runtime, dependencies, and execution environment | Compute policy §§1–2; archival policy §4; RCRPS v1.0.0 environment record; source-and-version-audit | covered | Publish a task-profile-aware common manifest mapping without assuming every runtime exposes identical hardware fields. |
| 4 | CPU/GPU, hardware, and physical/numerical parameters | Compute policy §2; archival policy §4; RCRPS configuration/environment records; structured-result standard | covered | Define which hardware fields are required, optional, or N/A for analytical and non-compute tasks. |
| 5 | Native numerical outputs and integrity | Archival policy §§2–5; structured-result standard §§1–3 and validator; AGENTS.md §7 | covered | Preserve the existing extract-before-upload rule and clarify large/restricted data handling in the central index. |
| 6 | Numerical precision, convergence, and error analysis | AGENTS.md §4; review checklist §C; structured-result check categories; LZ task brief §8; domain-specific numerical Skill references | partially_covered | Establish a generic requirement to predefine method/tolerance and report actual convergence/error evidence, while leaving the numerical method and thresholds to each project profile. |
| 7 | Independent physical/scientific validation and analytic limits | AGENTS.md §§4–5; high-energy-theory Skill; evidence-and-claim-gates; review checklist §§B and D; LZ task brief §7–8 | partially_covered | Define task-class-specific physical-validation profiles. A software test, schema check, or checksum must never substitute for a physical check. |
| 8 | Relevant regression tests | AGENTS.md, review checklist, existing schema/result workflows, Skill unit tests, PR #27 test suite | partially_covered | Require relevant regression tests for code/validator changes, but allow them to run in the actual available primary or approved verification environment; Actions remains optional under current policy. |
| 9 | Independent code review | GIT_MERGE_POLICY.md §3; AGENTS.md §7; review checklist §F; PR-based change control | partially_covered | Specify what counts as independent review, reviewer scope, finding severity, disposition, and evidence. Current policy requires review discipline but does not provide one shared reviewer contract for every downstream project. |
| 10 | PR review and approval before merging into main | GIT_MERGE_POLICY.md §§1, 3, 4, 6; AGENTS.md §7–8; root README | covered | Generalize the existing merge/archival lifecycle through a downstream adoption profile; preserve each repository's actual branch permissions and owner approval. |

**Overall result:** all ten topics have existing source coverage, but the ten-item gate is not yet a single adopted, versioned, task-profile-aware standard. Items 6–9 need clearer common acceptance semantics. Items 1–5 and 10 are substantially covered by existing central policies and should be referenced rather than rewritten.

## 8. Conflict and gap register

| ID | Finding | Evidence | Consequence | Recommended resolution phase |
|---|---|---|---|---|
| AUD-01 | RCRPS v1.0.0 integration status conflicts with its “Proposed for adoption” status line | PR #25 merged; AGENTS.md and archival policy require v1.0.0; English/Chinese standard still says proposed | Users cannot tell whether v1.0.0 is adopted or merely proposed | Phase II |
| AUD-02 | Two competing v1.0.1 provenance contracts are open | PR #28 source.revision_context versus PR #29 execution.source_control | Downstream validators and manifests could diverge | Resolve through PR review before v1.0.1 release |
| AUD-03 | Compute policy has an identical maintained copy in research-ai-hub | Same Git blob SHA in both main branches | Future edits can drift and create competing authority | Phase II downstream reference/lock migration |
| AUD-04 | Existing policies are scoped to this repository, while the approved architecture covers multiple repositories | Scope statements in AGENTS.md, compute policy, archival policy, and merge policy | Central approval alone does not automatically make every downstream repository compliant | Phase II versioned adoption contract and downstream PRs |
| AUD-05 | Task handoff and research-change records are complementary but can be mistaken for duplicates | LZ ten-field handoff standard versus central research-change template | A single oversized form would mix pre-execution specification with post-change evidence | Phase II extract general handoff standard; keep the two lifecycle records linked |
| AUD-06 | The Quality Gate is distributed across multiple documents | Ten-item coverage map in §7 | No single source defines task profiles, PASS/FAIL/BLOCKED/NOT RUN/N/A semantics, or evidence thresholds | Phase II |
| AUD-07 | Numerical and physical validation need task profiles | AGENTS.md and Skill give domain-dependent checks; no universal numeric tolerance is appropriate | A rigid universal checklist could require meaningless tests or accept weak evidence | Phase II profiles; Phase V pilot |
| AUD-08 | Independent code review is not yet a uniform cross-project contract | Git merge policy and review checklist provide general review discipline but not a shared independent reviewer specification | Review quality and evidence may vary by project | Phase II / III |
| AUD-09 | Current workflows are not reusable across repositories | Five main workflows; none declares workflow_call; no composite action directory | Downstream projects cannot yet invoke a central Quality Gate as a pinned reusable workflow | Phase IV |
| AUD-10 | FingerprintInputs implementation is still candidate-only | fingerprint_inputs.py says candidate; OPEN_ISSUES.md says field/hash contract incomplete | Do not make its output a mandatory central lock or provenance interface yet | Defer until explicit contract approval |
| AUD-11 | Repository status report is dated 2026-10-21 | docs/REPOSITORY_STATUS.md header | It predates the later v1.0.0 merge and subsequent PR work | Refresh with the next schema/Skill governance update |
| AUD-12 | RCRPS validator dependency error text names a stale path | docs/schemas/validate_result_records.py refers to research/schemas while requirements live in docs/schemas | Installation failure guidance can send users to a nonexistent path | Focused maintenance fix |
| AUD-13 | Candidate Schema v1.4.3.7 has unresolved release blockers | DECISION_REGISTER.md and OPEN_ISSUES.md | The candidate must not be presented as the central released research-record schema | Keep candidate status until its own gates close |
| AUD-14 | PR #6 and PR #27 have diverged from current main | GitHub compare: each is 41 commits behind main | Integration requires careful synchronization and conflict review, not blind merge | Resolve within each PR's own review process |

## 9. Recommended central disposition

### Retain as central authorities

- AGENTS.md
- RESEARCH_COMPUTE_POLICY.md
- docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md
- docs/scientific-diff-workflow.md
- docs/governance/GIT_MERGE_POLICY.md
- the adopted RCRPS v1.0.0 schema baseline, after its status wording is reconciled

### Reuse without duplicating

- docs/review-checklist.md
- templates/research-change.md
- templates/claim-evidence-matrix.md
- templates/project-record.md
- existing claim/evidence, source/version, and task-router Skill references
- the existing v1.0.0 schema and validator

### Extract general rules

- LZ's ten-field Research Task Handoff Standard and task brief template. Extract general task specification fields; do not import LZ-specific momentum conventions, nuclear response procedures, or three-body benchmarks as universal rules.

### Keep project-local

- UV–EFT, QLD, Ward-identity, and operator-basis procedures in their relevant high-energy-theory workstreams.
- Three-body scattering, AFH matching, nuclear responses, and LZ benchmarks in LZ-3-body-for-hdm.
- Thermal field theory, dimensional reduction, electroweak phase-transition observables, and their benchmarks in the electroweak-phase-transition project.
- Any other project's physical model, data, frozen benchmarks, and domain-specific acceptance criteria.

### Defer pending release gates

- Schema v1.4.3.7 and its four pending Artifact decisions.
- FingerprintInputs as a normative contract.
- RCRPS v1.0.1 until the competing PR #28/#29 designs are reconciled and one is reviewed/merged.
- Cross-repository Skill distribution until PR #27 is reviewed and merged.
- Reusable workflows/actions until their inputs, permissions, versioning, and failure semantics are designed and tested.

## 10. Phase II recommendations

Phase II should be a consolidation, not a rewrite:

1. Add a central standards index that maps each requirement to its one authoritative source.
2. Reconcile RCRPS v1.0.0 status wording with the merged PR #25 and existing mandatory references.
3. Define the Quality Gate's task profiles and status vocabulary, then map each item back to existing standards.
4. Extract the general Research Task Handoff Standard from LZ PR #72 while preserving the original LZ standard and its provenance.
5. Define a downstream adoption/lock contract containing central repository, release, full commit SHA, and adopted profiles.
6. Decide one canonical RCRPS v1.0.1 design through review; do not merge competing field contracts.
7. Keep the Schema v1.4.3.7 candidate and its pending decisions separate from the adopted RCRPS v1.0.0 baseline.
8. Plan the research-ai-hub policy-copy migration as a downstream PR, not as an unreviewed edit.
9. Define independent code-review requirements and generic validation evidence semantics without making Actions the only allowed execution route.
10. Leave reusable workflow/action implementation to Phase IV after the manifest and profile interfaces stabilize.

## 11. Audit limitations and evidence discipline

- This audit inspects the audited main tree and the identified PR metadata, PR descriptions/comments, file lists, and workflow-run records. It does not claim that every file in every downstream repository has been exhaustively audited.
- A workflow result is attributed only to the exact PR head for which GitHub reports it. The latest PR #27 checks cited above are the Candidate schema validation and Windows Skill installer validation runs on head 6f5194ff688879466ea0fd995de78a9f089fd708.
- PR #29's reported successful runs apply to head 518f23008d84d20daa3e9f68a01b374daaf75fb3. PR #28's branch checks are recorded as failed at its current reported head; this audit does not infer the underlying cause without executed-step evidence.
- No scientific calculation was run for this documentation/governance audit. No physics result is validated by this matrix.
- No existing policy, schema, Skill, calculation, input, historical result, or open PR was modified as part of preparing this audit matrix.
