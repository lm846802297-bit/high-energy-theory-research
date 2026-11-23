# Referee Response and Manuscript Synchronization Standard

**Status:** adopted shared standard  
**Effective date:** 2026-11-23  
**Scope:** referee-response writing, review, substantive editing, and synchronization with the manuscript in repositories that adopt the central standards framework.

This standard governs the scientific argument and file-role boundaries of referee responses. It does not prescribe a particular model, journal format, response length, or project-specific manuscript workflow.

## 1. Keep reviewer-facing and internal documents separate

### Referee-facing response

The response letter is written for the referee and editor. It should answer the report directly and support its conclusions with the relevant model definitions, derivations, numerical results, experimental comparisons, and scientific applicability conditions.

Do not include internal task assignments, to-do lists, branch names, PRs, commits, CI status, version-management details, or internal manuscript-synchronization progress.

### Internal manuscript-synchronization record

When a response requires a corresponding manuscript change, track that work in an internal checklist or change record. Identify the manuscript location, current text, intended change, evidence, and actual status.

The internal record is not part of the referee-facing response. If the task is limited to the response letter and no manuscript change is required, do not create an unnecessary synchronization checklist.

Never claim that the manuscript has been revised, added to, removed from, or shortened unless the selected manuscript source was actually changed and checked.

**Separating internal progress from the response does not mean hiding scientific limitations.** State real assumptions, applicability boundaries, missing evidence, and unresolved physics accurately. If the available evidence does not support the intended claim, narrow the claim rather than inserting internal project status into the letter.

## 2. Organize the response around the referee's questions

For a substantive referee comment with multiple subquestions, use two levels:

1. **Overall response:** a concise statement of the central answer, the model or scope boundary, and the issues addressed below.
2. **Point-by-point responses:** a sufficiently detailed answer to each independent subquestion, following the referee's numbering or structure where practical.

Start each response with the direct answer. Then explain the physical reason and provide the evidence needed to assess it. A summary in the overall response does not replace the reasoning required in the individual replies.

Do not create artificial subquestions or numbering. Do not rely on “see above” when the current answer still needs a clear statement of its own conclusion and decisive conditions. Cross-reference a derivation when it has already been fully established, while retaining the relations needed to understand the current answer.

## 3. Argument completeness

The depth of the response should match the scientific complexity of the comment. For substantive physics or phenomenology questions, check the following dimensions as applicable:

1. **Direct answer and physical reason** — identify exactly what was asked and explain which mechanism, symmetry, interaction, or kinematic condition determines the answer.
2. **Formula source and derivation** — identify the Lagrangian, charge assignment, mass matrix, effective operator, amplitude definition, equation, or primary reference from which the relation follows. Show the intermediate steps that carry the argument; do not merely list formulas.
3. **Numerical result and benchmark meaning** — state the inputs, parameter point, normalization, approximation, units, uncertainty, and what the number actually tests. Explain which claim it supports.
4. **Experimental applicability and model mapping** — identify relevant production mechanisms, couplings, spin structures, decay channels, branching fractions, lifetimes, acceptances, and statistical definitions. Explain whether a published limit applies directly, requires reinterpretation, or does not constrain the stated model under the adopted assumptions.
5. **Independent subquestions** — give each distinct physical or experimental question an identifiable answer and its corresponding evidence.

These are reasoning dimensions, not a mandatory five-paragraph template. A simple clarification may be brief. A claim involving a model mechanism, quantitative result, or experimental bound requires enough derivation and evidence to be independently assessed.

## 4. Preserve independent scientific arguments when editing

Do not delete or merge content merely because it appears textually repetitive. Similar wording or shared terminology does not prove that two passages serve the same scientific function.

Before merging or removing material, determine whether it expresses the same physical proposition, applicability conditions, and evidence function. Preserve distinctions such as:

- separate diagrams, topologies, or subsets with different scope;
- UV contributions versus EFT contributions or counterterm sectors;
- what a numerical cross-check actually validates versus what it does not cover;
- a benchmark-specific approximation versus a result valid over a wider parameter range;
- a partial calculation versus a complete matching, observable, or physical prediction.

A merge is acceptable only when the resulting text retains all necessary equations, reasoning steps, numerical values, benchmarks, citations, validation scope, and applicability conditions.

Deleting or substantially compressing an independent physical conclusion, derivation, benchmark, numerical result, validation statement, or applicability condition is a scientific-content change, not routine copy-editing. The change record must identify the original location, the reason, the replacement location, and the impact on the argument. Obtain the author's explicit approval before removing an independent scientific conclusion, calculation evidence, validation result, or applicability condition.

When equivalence cannot be established, preserve both passages or use a cross-reference. Argument completeness takes precedence over superficial brevity.

## 5. Scientific integrity and tone

- Retain necessary scientific qualifications; remove repetitive disclaimers that add no new physical information.
- Distinguish a result that is not excluded by a particular constraint from a result that is positively established or experimentally allowed over a stated parameter space.
- Do not transfer formulas, parameter relations, or experimental bounds between different models without a derivation or explicit matching.
- Do not present a conditional benchmark as a general conclusion.
- Do not use future-tense promises to substitute for an answer supported by current evidence.
- Do not hide an incomplete calculation. State what is established and narrow the claim to that scope.
- Use a formal, direct, evidence-led tone. Avoid defensive essays, unnecessary self-criticism, and generic statements about future work.

## 6. Review and change records

For a PR that materially edits a referee-facing response or its supporting scientific argument:

- identify the exact response-letter and manuscript source revisions;
- inspect the actual diff, not only the PR summary;
- include a before/after preservation audit for affected major comments and subquestions;
- include a deletion/merge ledger, or explicitly state that there are no substantive deletions or merges;
- verify that claims about manuscript edits match the actual manuscript diff;
- distinguish source review, compilation, PDF visual inspection, numerical reproduction, script tests, and CI. Do not claim one type of check establishes another.

Reviewers should compare the ledger with the actual diff and identify any unrecorded removal of scientific content. If a change removes an independent scientific conclusion, calculation evidence, validation result, or applicability condition, verify that the author explicitly approved it.

The [Research Document Review Standard](DOCUMENT_REVIEW_STANDARD.md) governs the review of the response letter, internal checklist, and related research documents. The [Research Quality Gate](governance/RESEARCH_QUALITY_GATE.md) governs the task-level evidence and acceptance status.

See also the [Central Research Standards Index](governance/CENTRAL_STANDARDS_INDEX.md).
