# Changelog

## 2026-10-21 — Initial repository import

- Imported the extracted contents of the Schema v1.4.3.7 integrated candidate bundle into schema/v1.4.3.7/.
- Added the v1.6.5 design baseline and the four-decision review.
- Added a reusable research Skill scaffold, reference guides, unit checks, pinned validation dependency, and GitHub Actions workflow.
- Corrected the candidate package README's integration-test count from 27 to 29; the bundled test file contains 29 tests.
- Regenerated audit/validation-report.json using the bundled validator. The fresh report records 58 checks, 83 fixture expectations, 16 semantic-case expectations, 25 schema record types, and 125 trace rows.
- No JSON Schema definitions or normative decisions were changed in this import. Four Artifact identity decisions remain pending approval.

## 2026-10-21 — P0 project-record validation and audit reconciliation

- Added `skills/high-energy-theory-research/scripts/validate_project_records.py` for JSON/YAML parsing, candidate JSON Schema checks, bounded cross-record validation, per-project primary-ID uniqueness across record types, status/reason consistency, and local source/artifact path checks.
- Added regression tests for valid JSON/YAML, missing references, cross-type duplicate IDs, missing `not_applicable` reasons, invalid status values, duplicate YAML keys, and local path checks.
- Added the pinned PyYAML dependency and included the Skill script in Python compilation checks.
- Corrected array-reference handling for artifact inputs, validation activity/report evidence, benchmark evidence, and parameter-point artifact lists; added a regression test so empty arrays are not misread as scalar IDs.
- Reconciled the traceability CSV count at 125 data rows (excluding the header) and corrected the stale audit narrative. The schema remains a candidate and scientific acceptance remains out of scope.

## 2026-10-21 — Fixture-index version-field audit

- Recorded the observed mismatch between the candidate bundle manifest (`1.4.3.7-candidate`) and the fixture index (`1.4.3.6-candidate`).
- Confirmed that CI verifies the fixture-index file digest and fixture outcomes but does not interpret the top-level index `schema_version`.
- Preserved the existing index bytes because the source ZIP is not committed and the field's intended semantics are not defined. This is an explicit unresolved release blocker, not a claimed fix.

## 2026-10-21 — Fixture-index audit guard and end-to-end pilot

- Added a regression test that verifies the fixture-index version mismatch, source-lineage record, and current validator behavior remain explicit; the index bytes were not changed.
- Added a synthetic 2x2 mass-squared matrix pilot with exact eigenvalues/masses, trace and determinant checks, eigenvector normalization/orthogonality, eigenpair residuals, and a positivity check.
- Added a synthetic Task-to-Claim record chain and tests for candidate-schema payloads that are currently rejected. The mathematical calculation passes, but full reproducibility acceptance is explicitly blocked until the structured schema envelopes are completed.

## 2026-10-21 — Structured research-record payload remediation

- Added explicit candidate-schema structures for Run Plan `execution_spec`, Run Manifest snapshots/fingerprint bundle/outputs/validation, Claim evidence dimensions and physics assessment, and Artifact Plan completeness rules.
- Allowed `schema_or_structure` to carry an opaque object or null, consistent with its design-document type.
- Updated the two positive Claim fixtures to use `physics_assessment: null` under the object-or-null contract.
- Left `run_plan.fingerprint_inputs` unchanged because the source design references `FingerprintInputs` without defining its fields or hash semantics; documented this as a release blocker rather than inventing a normative contract.

## 2026-10-23 — Multi-project registry foundation (Phase A)

- Added projects/README.md and projects/registry.yaml to register project/workstream hierarchy.
- Registered axial-vector-model-building as the parent project and vll-higgs-singlet-uv-eft as a nested workstream, not a separate top-level project.
- Added templates/project-record.md for future projects and workstreams.
- Updated the repository landing page, research index, and Scientific Diff workflow to distinguish project, workstream, research-change, run, and claim identities.
- No existing research files were moved or renamed. The registry is navigation metadata only; no candidate schema was changed and no scientific result was promoted.

## 2026-10-23 — Multi-project user guide and registry validation

- Added docs/USER_GUIDE.md as the detailed operating manual; the root README remains the short onboarding page.
- Added a dedicated project-registry validator and unit tests for hierarchy consistency, duplicate IDs, missing canonical paths, and path traversal.
- Updated the research Skill and project registry guide to distinguish navigation metadata from candidate-schema structured research records.
- Updated the README validation commands and project hierarchy references.
- No existing research files were moved. The new validator and tests have not been executed in a repository runtime in this change; treat runtime validation as pending until the command/test output is captured.

## 2026-10-23 — Simplified Chinese documentation

- Added `README.zh-CN.md` for the repository landing page and `docs/USER_GUIDE.zh-CN.md` as a full Chinese user manual.
- Added Chinese counterparts for all seven existing README files: design documents, project registry, research records, candidate Schema v1.4.3.7, and both evaluation-pilot directories.
- Added language-switch links from the corresponding English README files and the English user guide.
- Preserved source identifiers, paths, commands, equations, schema-field names, and validation caveats; no English original was replaced.
- Verified that each translated document has the same number of Markdown headings as its English source, and checked relative links plus Markdown code-fence pairing in both language versions. No scientific calculation or CI run was performed by this documentation-only change.

## 2026-11-22 — Optional tooling and task-specific physics references

- Added task-specific references for symbolic calculations, numerical integration/scans/convergence, scientific figure auditing, and source-grounded paper reading.
- Added a pinned optional-tooling map for selected third-party Skills, including source commits, licenses, dependencies, and use boundaries.
- Kept the existing root AGENTS.md as the sole repository-wide authority; no duplicate AGENTS.md or competing project-wide policy was created.
- Preserved the existing high-energy-theory-research Skill name and entry point; no existing research records, source calculations, schemas, or open PRs were changed.
- Added Skill-contract regression coverage for the new reference files and optional-tooling route.
- Validation and Windows Codex discovery remain pending until run in the target Windows Codex environment.

## 2026-11-22 — Skill module evaluation and Codex discovery diagnostics

- Added a read-only PowerShell diagnostic for the current project/user Codex Skill paths; no local installation or runtime discovery is claimed.
- Updated the optional-tooling map to distinguish current `.agents/skills` paths from older `.codex/skills` examples.
- Strengthened numerical guidance on full Jacobians, normalized shapes versus absolute rates, and output/manifest consistency.
- Strengthened figure guidance so PDF text-size thresholds come from the target journal rather than a universal default.
- Added a bounded evaluation case using an existing 2→3 phase-space integration and an existing paper figure PDF. The evaluation scripts, environment, inputs, outputs, and audit reports are recorded separately from the original LZ project.
- Linux contract tests and numerical/PDF checks are recorded; Windows Codex runtime discovery remains pending.


## 2026-11-22 — Windows Desktop discovery caveat

- Distinguished filesystem path checks from runtime Skill discovery.
- Recorded openai/codex issue #40458, which reports repository-local Skill discovery failures in Windows Codex Desktop.
- Updated the diagnostic output and contract tests to preserve read-only behavior and require host-specific runtime confirmation.
- A user-scope copy remains a global diagnostic comparison, not a project-isolated workaround.

## 2026-11-22 — Installer rollback and cross-repository scope review

- Fixed scratch cleanup so a previous Skill backup is preserved whenever installation/rollback has not safely completed; destination existence alone no longer authorizes deleting a remaining backup.
- Extracted the cleanup decision into a small helper and added six Windows PowerShell regression cases, including a rollback failure with a concurrently occupied destination. Windows execution of this new regression file is pending.
- Clarified that candidate-schema and project-registry validators require a pinned central source checkout; the standalone user-level Skill export does not include the central schema bundle/helper module.
- Added a Skill contract assertion for the central-only validator boundary.
- The central PR remains Draft pending Windows PowerShell 5.1 execution of the new rollback regression test and final review.

## 2026-11-22 — Installer manifest integrity hardening

- Existing installation manifests now require the expected source repository, a 40-character lowercase Git commit SHA, every required Skill file, valid 64-character lowercase SHA-256 entries, and an exact match between recorded and actual installed file inventories.
- Added seven Windows PowerShell manifest-integrity cases covering valid inventory, wrong repository, malformed source commit, missing required file, modified hash, empty inventory, and unrecorded extra file.
- Extended the Python Skill contract test to assert the installer helper and Windows regression test are included in the repository.
- Windows PowerShell 5.1 execution of the expanded 13-case installer regression remains pending.

## 2026-11-22 — Research Skill A/B benchmark scaffold

- Added a preregistered A/B protocol comparing the same GPT/Codex runtime with and without the shared Research Skill.
- Added a weighted scoring rubric with non-compensatory physics/evidence gates and a separate reasoning-autonomy guardrail.
- Added an environment lock, run-record schema, comparison-report schema, and separate run directories for both arms.
- Added six development tasks covering theoretical derivation, numerical integration, source-grounded manuscript reading, symbolic Dirac traces, PDF figure audit, and reproducibility.
- Separated development evaluator keys from model-visible task prompts.
- Reserved a holdout area but did not create or expose holdout prompts/keys; a genuinely blind holdout must be prepared after protocol and Skill versions are frozen.
- No A/B model runs have been executed. The benchmark protocol remains draft pending exact model/build capture and Windows workspace-isolation checks.
