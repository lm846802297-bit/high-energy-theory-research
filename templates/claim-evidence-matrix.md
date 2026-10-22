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


## Active claim records — RC-001

| Claim ID | Exact claim | Assumptions and valid domain | Derivation evidence | Computational evidence | Independent check | Claim status | Manuscript locations | Remaining action |
|---|---|---|---|---|---|---|---|---|
| CL-001 | The fixed-sector four-point hard difference is \(i|C_{5,\mu}|^2[(L_\mu-2)s+t/6]/(16\pi^2)\) plus the flavor-\(\tau\) \(u\)-channel analogue. | Unbroken phase; fixed complex external legs; stated Yukawa order; light fields retained; source conventions and subtraction scheme. | Baseline document §248. | Exact analytical ledger and symbolic consistency checks in §248; uv_eft_audit_suite_output.txt records only selected numerator/trace/Wick checks. | No full FeynArts/FeynCalc run. | Conditionally supported | Internal matching record; no final manuscript claim authorized by this row alone. | Execute diagram-level workflow and compare UV/EFT graphs and local projection. |
| CL-002 | The heavy–light two-point hard kernel has the stated \(p^0,p^2,p^4/M^2\) terms under the source's \(i\Pi\) convention. | Unbroken phase; massless light fermion; flavor-resolved heavy mass; specified PV normalization and \(\overline{\mathrm{MS}}\) convention. | Baseline document §250. | Exact-arithmetic checks and the recorded \(A_0/B_0\) expansion in the baseline document. | Algebraic checks are documented; external diagram-package reproduction remains open. | Conditionally supported | Internal matching record; physical pole statements remain out of scope. | Run and archive the corresponding model-specific diagram calculation; compare counterterms and finite terms. |
| CL-003 | The zero-momentum effective-potential portal threshold is \(\Delta\lambda_{HS}=-\sum_\ell |y_\ell|^2|\lambda_\ell|^2/(8\pi^2)\) in the stated potential convention. | Background-field potential; specified heavy–light VLL mass matrix; flavor assumptions and scheme from §§248/251/273. | Baseline document §§248.6 and 251. | Exact effective-potential algebra check and two-route potential expansion recorded in the source; audit JSON hash is recorded in RC-001. | FeynArts/FeynCalc scaffold exists but is explicitly unrun. | Conditionally supported | Do not promote to a full-model numerical portal or mixing prediction without the boundary condition. | Execute diagram-level four-point check and confirm sign/convention mapping. |
| CL-004 | The section-261/262 symbolic matrix/EOM and soft-loop identities hold within their explicitly tested algebraic/integral scope. | Only the exact variables, expansions, loop functions, and numerical control cases recorded in those sections. | Baseline document §§261–262. | Section 261: 25 Mathematica symbolic checks plus documented Python checks; section 262: 25 Mathematica symbolic checks, six high-precision \(B_0\) integrals, and documented Python checks. | Mathematica and Python runs check related but overlapping identities; neither is a full diagram-package run. | Conditionally supported | Internal calculation record only. | Finish missing light-field/tadpole/input-scheme pieces before interpreting as a physical pole result. |
| CL-005 | A complete nonredundant Wilson vector and final physical scalar-mixing prediction have been established. | Would require all relevant UV/EFT sectors, fixed parameter boundary, complete basis reduction, and specified on-shell observable. | No complete evidence chain in the baseline. | FeynArts/FeynCalc not run; full model-level vector and on-shell/LSZ closure remain open. | Not established. | Unresolved | No final claim permitted. | Complete gates in research/RC-001-vll-higgs-singlet-uv-eft.md before reassessment. |
