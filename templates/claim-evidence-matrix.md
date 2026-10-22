# Claim–Evidence Matrix

Use this ledger for important physical claims that appear in calculations, figures, papers, abstracts, conclusions, or reviewer responses. One row should represent one assessable claim, not an entire section of prose.

## Claim ledger

| Claim ID | Exact claim | Assumptions and valid domain | Derivation evidence | Computational evidence | Independent check | Claim status | Manuscript locations | Remaining action |
|---|---|---|---|---|---|---|---|---|
| CL-001 | [One precise statement] | [Parameter range, approximation, benchmark, scheme, confidence level] | [File / section / artifact] | [Run / output / hash] | [Method and result, or not performed] | [Proposed / Supported / Conditionally supported / Unresolved / Contradicted / Superseded] | [File, section, equation, figure] | [Action or none] |

## Rules for using the matrix

1. Quote or precisely formulate the claim. Avoid vague labels such as “the model works.”
2. Record assumptions and the domain where the statement is intended to hold.
3. Link evidence to the exact derivation, run, data version, or figure; filenames alone may be insufficient if they are overwritten.
4. Separate a numerical output from the interpretation of that output.
5. Record independent verification explicitly. If it has not occurred, say so.
6. If the evidence supports only a benchmark or restricted region, use “Conditionally supported” and state the restriction.
7. If evidence is missing or contradictory, use “Unresolved” or “Contradicted”; do not silently retain a stronger manuscript claim.
8. When a claim changes, preserve the earlier wording in the change history or linked research-change record.
9. Synchronize abstracts, conclusions, captions, appendices, and reviewer replies with the same assessed claim.
10. A status label is a summary, not evidence. The linked artifacts and rationale are the evidence.

## Example of scope discipline

These statements are not equivalent:

- “The constraint is absent.”
- “The constraint has not been evaluated.”
- “The constraint is subdominant within the stated benchmark and assumptions.”
- “The constraint does not change the exclusion in the tested parameter region.”

Use only the statement supported by the actual analysis. In particular, “not evaluated” must not be converted into “irrelevant.”
