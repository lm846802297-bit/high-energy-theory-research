# Research Document Review Standard

**Status:** adopted shared standard  
**Effective date:** 2026-11-23  
**Scope:** substantive review, editing, migration, archival classification, and cross-document consistency work in repositories that adopt the central standards framework.

This standard defines how to review human-readable research documents. It complements the [Research Quality Gate](governance/RESEARCH_QUALITY_GATE.md); it does not replace scientific derivation, numerical validation, or domain-specific review.

## 1. Proportionality and review scope

Apply the checks below to the parts of a document materially affected by a substantive edit. Apply them to the complete document when the task claims a full-document review, changes its scientific authority or lifecycle, or migrates/archives it.

A trivial spelling, punctuation, or formatting correction may use a focused check. It does not require a full scientific re-review when the meaning, evidence, and authority are unchanged.

A bulk inventory is not a content review. When a task claims a document-by-document audit, every in-scope document must have its own review disposition. Do not infer that uninspected files passed because their directory or register was checked.

## 2. Review dimensions

For each in-scope document, assess the following as applicable:

1. **Identity and role** — title, purpose, intended audience, project/workstream, and document type.
2. **Authority and lifecycle** — current authority, working draft, historical snapshot, superseded note, generated output, or deliverable. Identify the canonical replacement where one exists.
3. **Scientific content** — equations, definitions, conventions, dimensions, units, approximations, parameter values, limiting cases, and whether the stated conclusion follows from the cited derivation or data.
4. **Evidence and citations** — references resolve and support the attached claim. Distinguish literature statements, adopted assumptions, numerical observations, and conclusions.
5. **Consistency** — compare model assumptions, benchmarks, numerical values, notation, and status statements with the current authoritative research record.
6. **Reproducibility** — where relevant, identify source revision, input provenance, configuration, command, software environment, output location, checksums, and validation criteria.
7. **Links and assets** — validate relative Markdown links, anchors, images, PDFs, data paths, scripts, and cross-document references.
8. **Language and structure** — clear title, scope, definitions, reasoning, results, applicability conditions, and next steps. Remove stale or contradictory instructions without erasing historical facts.
9. **Disposition** — retain, revise, mark historical/superseded, merge into a canonical document, relocate, or propose removal. Removal requires provenance and inbound-reference checks.

A check that does not apply should be recorded as N/A when a formal audit record is required. Do not claim a check was completed merely because the document is readable or well formatted.

## 3. Review disposition and lifecycle are separate

Use the following review dispositions when a document-level register is maintained:

- **PASS** — all applicable checks were completed and no actionable issue was found.
- **PASS_WITH_NOTES** — usable within the reviewed scope; non-blocking findings are recorded.
- **REVISION_REQUIRED** — at least one actionable content, evidence, consistency, or presentation issue remains.
- **BLOCKED** — review cannot be completed because a specific source, dataset, permission, or required context is unavailable.
- **PENDING** — inventory only; no content-level review has been completed.

Record lifecycle/authority separately, for example: current authoritative, working draft, historical, superseded, generated, archival, or duplicate candidate. **HISTORICAL is a lifecycle classification, not a review disposition.** A historical document may still contain a formatting issue; a PASS disposition does not make an old document current authority.

## 4. Scientific-claim integrity

A document review must preserve distinctions that affect the claim:

- analytic derivation versus numerical implementation;
- pointwise agreement versus global convergence;
- software/CI success versus numerical or physical validation;
- a conditional benchmark versus a general result or final exclusion;
- an adopted model assumption versus an independently established physical fact;
- a local or partial calculation versus the complete observable or physical process.

Do not silently change a result, uncertainty, benchmark, model assumption, applicability condition, or physical conclusion during editorial cleanup. Record a scientific discrepancy and route it for a separate decision when it cannot be resolved from the cited evidence.

## 5. Review record

When a formal document audit or migration register is required, record at least:

- repository and exact reviewed commit SHA;
- file path, title, role, project/workstream, and lifecycle/authority;
- review disposition;
- findings and required action;
- reviewer and review date;
- relevant source, evidence, or replacement-document links.

For code, data, schemas, and generated numerical artifacts, use the corresponding technical validation procedure. Do not treat a prose-review disposition as proof that a script, dataset, or scientific calculation is correct.

## 6. Migration, archival, and removal

Before moving, merging, archiving, or removing a document:

1. Identify its role, authority, lifecycle, and any unique scientific content.
2. Search inbound references, including Markdown links, code imports, workflow paths, LaTeX inputs, scripts, manifests, and external handoff instructions.
3. Preserve the old-to-new path mapping and update references in the same change where practical.
4. Preserve historical source bytes and fingerprints when they have provenance value. If a review register records both a previously reviewed version and the current file, keep those fingerprints in separate fields; do not overwrite the historical fingerprint merely to make it match the current tree.
5. Verify the resulting links and files on the canonical branch after integration.

Do not infer that two documents are duplicates from similar titles or wording. Confirm that their scientific proposition, assumptions, evidence, applicability, and document role are genuinely equivalent before merging them.

## 7. Coverage tracking for bulk audits

For a full repository-document audit:

- define the in-scope file types and baseline commit before counting;
- maintain a unique path inventory with one disposition per document;
- distinguish inventory coverage from completed content review;
- record the reviewed commit/blob identity and current-tree identity separately when historical fingerprints must be preserved;
- update the inventory when files are added, renamed, relocated, or removed;
- retain dated audit snapshots so that later changes do not rewrite the historical review record.

A bulk audit is complete only when its declared scope, file inventory, per-document dispositions, and path/link checks reconcile. This requirement applies to tasks that claim a bulk audit; it does not make a full repository-wide audit mandatory for ordinary research work.

See also the [Central Research Standards Index](governance/CENTRAL_STANDARDS_INDEX.md) and [Research Quality Gate](governance/RESEARCH_QUALITY_GATE.md).
