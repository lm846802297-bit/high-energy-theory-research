# RC-001 — VLL–Higgs–Singlet UV–EFT One-Loop Matching

> **Record type:** baseline consolidation and verification-gap tracking. This record does not assert that the complete matching calculation is finished.
>
> **Work status:** Verification in progress  
> **Overall model-level claim status:** Unresolved  
> **Created:** 2026-10-23  
> **Repository baseline:** main at c992daac633ac9df3d0aad008e104125206cb890

## 1. Scientific question

What can be established, under the explicitly recorded VLL–Higgs–Singlet model assumptions, by matching the UV theory onto an EFT at one loop, and what additional evidence is required before the results can be used as a complete nonredundant Wilson-coefficient set or a physical prediction for scalar mixing?

The record links the existing model definition, analytical derivations, symbolic checks, Mathematica runs, the unexecuted FeynArts/FeynCalc scaffold, and the current scope of the physical conclusions. It is a consolidation of existing work, not a new derivation and not a declaration that any unresolved result has passed verification.

## 2. Immutable baseline and provenance

### Primary research source

- **Document:** higgs_portal_mixing_unified_reviewer_response_and_uv_eft_UPDATED_v2(8)(20261021)(153)_matchete_mapping_version_history.md
- **Source location:** ChatGPT Library, file ID file_00000000b7b48230a2ada1957a9ed4a0, version ID 1
- **Size:** 1,989,214 bytes
- **SHA-256:** f30af8ccc62feafa3923e8356437e4b80b40e518fc9b1188646b4d763e2791f1
- **Relevant sections:** §§248–251 (unbroken-phase four-point and two-point hard matching); §§261–262 (broken-phase algebra and light-field soft functions); §273.9 (FeynArts/FeynCalc scaffold and effective-potential cross-check).
- **Model reference used by the source note:** original paper, version v1, model section: https://arxiv.org/html/2608.27258v1#S2

The primary source is a Library artifact, not a file currently committed to this repository. The filename, Library ID/version, size, and SHA-256 identify the exact source used to seed this record. If a later source revision is adopted, add a new baseline entry rather than silently replacing this one.

### Supporting computational artifacts

| Artifact | SHA-256 | Status and scope |
|---|---|---|
| section273_feyncalc_threshold_workflow.wl | 8e2c7a36c5cacecf35194a92cde50e52ec457cb884684c719e5aafc6b67053ab | 2,577-byte annotated FeynArts/FeynCalc scaffold for the four-point portal threshold. It is not an execution log and has not been run. The custom FeynArts model file and schematic particle-label mapping are still required. |
| section273_feyncalc_audit_log.json | dea8c3ff0a18163d4e1b697a4a44ea44f33a416ab7c85adc3dc71c8bd11e0bfa | Records exact effective-potential algebra checks and explicitly records FeynCalc execution as NOT RUN. |
| uv_eft_audit_suite_output.txt | d8471c9b990671777d957ea1afa5b2c3d5e67ffd6e2e1f6925f7713f68d66a86 | Python audit-suite output for selected numerator, trace, and Wick-sign checks. The log itself explicitly limits what these checks establish; it is not a complete UV–EFT matching result. |

The supporting files above were located in the Library and hashed for provenance. Their existence does not mean that the unexecuted scaffold has been run or that every check in the audit log is independent of the derivation it tests.

## 3. Model, scheme, and scope frozen for this record

The working UV interaction is the flavor-resolved VLL model

\[
\mathcal L_{\mathrm{int}}\supset
-\sum_{\ell=\mu,\tau}
\left[
y_\ell \bar L_\ell H E_{\ell R}
+\lambda_\ell S_\ell \bar E_{\ell L}\ell_R
+M_{E\ell}\bar E_{\ell L}E_{\ell R}
\right]+\mathrm{h.c.},
\qquad S_\mu=S,\quad S_\tau=S^* .
\]

The tree-level dimension-five coefficient convention used in the source record is

\[
C_{5,\ell}=-\frac{y_\ell\lambda_\ell}{M_{E\ell}}.
\]

The scalar invariants and portal term are

\[
X=H^\dagger H,\qquad Y=S^\dagger S,\qquad
V\supset \lambda_{HS}XY .
\]

For the hard matching sections, the baseline is the unbroken phase, massless light fermions, and integration of the heavy Dirac leptons \(E_\mu,E_\tau\), while \(H,S,A'\) and the light fields are retained in the EFT. Light-flavor off-diagonal Yukawa couplings are set to zero. Flavor-resolved expressions keep \(M_{E\ell}\) general; the equal-heavy-mass choice is a benchmark, not a necessary identity for every formula.

The two-point derivation fixes the Minkowski metric \((+---)\), \(D=4-2\epsilon\), the definition of the 1PI insertion \(i\Pi(p^2)\), the Passarino–Veltman \(A_0/B_0\) normalization, and the stated \(\overline{\mathrm{MS}}\) subtraction convention. The potential coefficient is defined in \(V\), while the Lagrangian contains \(-V\). These conventions must not be mixed when comparing signs.

### Included in RC-001

- The fixed four-Yukawa one-loop four-point hard-matching sector and its EFT soft subtraction.
- The heavy–light two-point hard functions, their \(p^0\), \(p^2\), and \(p^4/M_{E\ell}^2\) terms, and the related field/EOM matching recorded in the source.
- The zero-momentum effective-potential portal threshold, tracked separately from the \(p^2\) derivative coefficients.
- The existing broken-phase algebra and light-field soft-loop calculations, with their limited scope stated explicitly.
- The verification gap between analytical/symbolic checks and external diagram-level execution.

### Explicitly not claimed by this record

- A complete nonredundant Wilson vector for every operator and every UV-model sector.
- A unique numerical value for \(\lambda_{HS}\) or a unique physical scalar-mixing prediction; the required renormalized portal boundary is not fully specified in the baseline.
- A completed nonzero kinetic-mixing \(\epsilon_{BX}\) analysis or simultaneous integration of \(A'\).
- A completed full on-shell amplitude, external-leg/LSZ normalization, physical pole equation, or phenomenological exclusion.
- A completed FeynArts/FeynCalc diagram census or an independently reproduced full loop amplitude.
- Any conclusion about the separate Matchete/Warsaw-coefficient discrepancy (for example \(c_{ud1}\) or \(c_{lq1}\)); that is a distinct research question and must not be conflated with the scalar/two-point matching record.

## 4. Existing derivations and what they establish

### 4.1 Four-point derivative hard matching — source §248

For the fixed complex external legs \(H,S,H^\dagger,S^\dagger\), the source derives one connected 1PI UV box for each flavor and the corresponding EFT bubble with two \(C_{5,\ell}\) insertions. The local hard differences are recorded as

\[
i\Delta\Gamma_\mu^{(2)}
=i\,\frac{|C_{5,\mu}|^2}{16\pi^2}
\left[(L_\mu-2)s+\frac{t}{6}\right],
\]

\[
i\Delta\Gamma_\tau^{(2)}
=i\,\frac{|C_{5,\tau}|^2}{16\pi^2}
\left[(L_\tau-2)u+\frac{t}{6}\right],
\qquad
L_\ell=\ln\frac{M_{E\ell}^2}{\mu_R^2}.
\]

The source separates UV and IR poles, the EFT nonlocal logarithms, and the local polynomial. It also records the portal \(p^0\) projection of the same heavy/light fermion box separately from the \(p^2\) derivative projection. This prevents counting the same box as two different diagrams or placing the quartic threshold inside a dimension-six derivative coefficient.

**Evidence boundary:** this is an analytical fixed-sector matching ledger with symbolic consistency checks. The source explicitly states that FeynArts/FeynCalc was not run, that the full set of model sectors and nonzero kinetic mixing are outside this calculation, and that the full nonredundant Wilson vector and on-shell observables remain incomplete.

### 4.2 Two-point hard matching — source §250

With the source's \(i\Pi\) convention, the flavor-resolved heavy–light scalar two-point function is recorded as

\[
\Pi_{\phi\ell}^{\mathrm{bare}}(p^2)
=\frac{|g_{\phi\ell}|^2}{16\pi^2}
\left[
-2M_{E\ell}^2(\Delta_{\mathrm{UV}}-L_\ell+1)
+p^2(\Delta_{\mathrm{UV}}-L_\ell+\tfrac12)
+\frac{p^4}{3M_{E\ell}^2}
\right]
+O(p^6/M_{E\ell}^4),
\]

where \(g_{H\ell}=y_\ell\), \(g_{S\ell}=\lambda_\ell\), and \(L_\ell=\ln(M_{E\ell}^2/\mu_R^2)\). The source derives the common integral through \(A_0(M_{E\ell}^2)\) and \(B_0(p^2;0,M_{E\ell}^2)\), fixes the closed-fermion-loop sign, separates UV poles from finite pieces, and records the mass and wave-function counterterms. The \(p^4/M^2\) term is a finite hard coefficient in this sector; it is not a new UV pole at this order.

**Evidence boundary:** the derivation and exact-arithmetic checks are present in the baseline document. They validate the recorded algebra and conventions under the stated assumptions; they do not replace an external diagram-level implementation or establish the full model's physical pole spectrum.

### 4.3 Zero-momentum portal threshold — sources §§248.6, 251, 273.9

The source records the effective-potential threshold

\[
\Delta V\big|_{XY}
=-\sum_{\ell=\mu,\tau}
\frac{|y_\ell|^2|\lambda_\ell|^2}{8\pi^2}XY,
\]

and therefore, under the stated potential convention,

\[
\lambda_{HS}^{\mathrm{EFT}}(\mu_R)
=\lambda_{HS}^{\mathrm{UV}}(\mu_R)
-\sum_\ell\frac{|y_\ell|^2|\lambda_\ell|^2}{8\pi^2}
+\cdots .
\]

The source reports agreement between two effective-potential expansion routes for the stated background-field coefficients, along with exact-polynomial and high-precision checks. The small standalone Mathematica file in §273.9 is a **scaffold** for the separate FeynArts/FeynCalc four-point calculation; the companion audit log says FeynCalc was not executed. Thus the effective-potential algebra is checked, but the diagram-level UV amplitude minus EFT amplitude has not yet been independently run end to end.

### 4.4 Broken-phase transformations and soft functions — sources §§261–262

The source records a local Mathematica 14.2.0 execution for the section-261 symbolic matrix/EOM checks: 25 Mathematica symbolic checks passed. The associated Python audit reports 59 exact broken-phase checks, three independent diagonalization cases, and three truncation-scaling cases. These are algebraic and matrix-consistency checks, not a loop-diagram calculation.

For section 262, the source reports 62 exact light-fermion checks, eight \(B_0\) integrals, three derivative integrals, and three massless-limit checks in Python; the local Mathematica check reports 25 symbolic checks and six high-precision \(B_0\) integrals. The source explicitly says FeynArts/FeynCalc, Matchete, and matchmakereft were not run for these sections, and that the complete physical spectrum still requires additional light-field contributions and a consistent input/tadpole scheme.

These results can support the corresponding algebraic subclaims within their recorded scope. They must not be described as full external loop-package validation or as a final physical mixing angle.

## 5. Evidence ledger

| Evidence ID | Artifact / location | What it checks | What it does not establish |
|---|---|---|---|
| EV-001 | Baseline document §§248.1–248.9 | Fixed four-Yukawa Wick pairing, UV/EFT local subtraction, scale/log and pole bookkeeping | Full-model diagram census, all operators, external package reproduction, on-shell observables |
| EV-002 | Baseline document §§250.1–250.13 | \(i\Pi\) convention, loop phase, PV combination, hard \(p^0,p^2,p^4/M^2\) terms, counterterms and field/EOM bookkeeping | Full model counterterm matrix or physical pole/LSZ result |
| EV-003 | Baseline document §251 | Effective-potential threshold and higher scalar-potential coefficients from two analytical routes | General off-shell derivative operators, gauge/fermion external-leg matching, physical mixing angle |
| EV-004 | Baseline document §261 and embedded Mathematica log | 25 Mathematica symbolic checks of matrix/EOM/VEV transformations; related Python matrix checks | FeynArts/FeynCalc execution or direct verification of every hard loop coefficient |
| EV-005 | Baseline document §262 and embedded logs | Soft-loop functions, \(B_0\) integrals, massless limits and associated symbolic identities | Complete physical spectrum or full-model pole matching |
| EV-006 | section273_feyncalc_threshold_workflow.wl and section273_feyncalc_audit_log.json | Reproducible scaffold and exact Coleman–Weinberg algebra statement | Actual FeynArts diagram generation or FeynCalc reduction; the scaffold remains unrun |
| EV-007 | uv_eft_audit_suite_output.txt | Selected numerator, trace, Wick-sign, and algebraic kernel checks | External diagram census, full external-leg permutations, all counterterms, or a final Wilson vector |

## 6. Claim–evidence decisions at baseline

The corresponding rows are recorded in templates/claim-evidence-matrix.md.

- **CL-001 — Four-point derivative hard difference:** Conditionally supported for the fixed external legs, Yukawa order, massless-light-field setup, and scheme specified in §248. Full-model matching remains unresolved.
- **CL-002 — Two-point hard kernel:** Conditionally supported for the stated heavy–light Yukawa sector and \(i\Pi\)/PV conventions in §250. External diagram-package reproduction remains open.
- **CL-003 — Portal threshold:** Conditionally supported as the effective-potential coefficient under the stated potential convention. The FeynArts/FeynCalc cross-check remains open; do not claim it has run.
- **CL-004 — Broken-phase symbolic/soft-function subclaims:** Supported only within the explicit algebraic and integral checks recorded in §§261–262. These checks are not a complete physical pole calculation.
- **CL-005 — Complete Wilson vector and physical scalar mixing:** Unresolved. The current evidence does not establish a unique complete vector or a final physical mixing prediction.

## 7. Verification plan and acceptance gates

The next actions are ordered by dependency.

1. **Freeze inputs and conventions.** Record the exact UV Lagrangian, field charges, \(C_5\) sign, mass basis, \(i\Pi\) definition, \(A_0/B_0\) normalization, regularization/subtraction scheme, retained EFT fields, and any benchmark choices. Do not silently promote \(M_{E\mu}=M_{E\tau}\) or \(\epsilon_{BX}=0\) from a benchmark to a general theorem.
2. **Make the loop-package input executable.** Create and version the custom FeynArts model file for the actual VLL model; replace all schematic particle labels and confirm the generated graph list against the hand-derived graph ledger.
3. **Run and archive the diagram-level calculations.** Execute the relevant FeynArts/FeynCalc workflow with recorded Mathematica/FeynArts/FeynCalc versions, exact commands, warnings, diagram counts, intermediate expressions, and output hashes. Keep the portal \(p^0\) projection distinct from the derivative \(p^2\) projection.
4. **Compare by layer.** Compare the direct UV loop, the EFT soft graphs, UV/IR poles, counterterms, finite terms, and local operator projections separately. A match of the final simplified expression alone is not sufficient if conventions or IR subtraction differ.
5. **Perform a genuinely independent check.** Use a separately constructed derivation or implementation for the high-impact coefficients. Do not count the same code path run twice as independent verification. Check known limits, dimensions, scale dependence, and the expected cancellation of nonlocal EFT logarithms and IR poles.
6. **Close the EFT basis and parameter boundary.** Include the required field redefinitions/EOM terms and any additional sectors retained by the model. Specify the renormalized \(\lambda_{HS}\) boundary and decide whether \(A'\) remains in the EFT or is also integrated out.
7. **Only then evaluate physical observables.** Combine the matched coefficients with the broken-phase mass matrix, light-field/tadpole contributions, external-leg normalization, and a stated on-shell process. Record the input scheme and uncertainties before making a numerical scalar-mixing or phenomenological claim.

### Acceptance criteria

- [ ] Exact baseline and model assumptions are identifiable.
- [ ] Every reported result is linked to its derivation and actual computational artifact.
- [ ] Mathematica symbolic algebra, Python exact checks, and FeynArts/FeynCalc diagram execution are reported as separate evidence types.
- [ ] UV and IR poles, finite terms, counterterms, and matching conventions are consistently separated.
- [ ] Required independent checks have actual outputs and are not merely planned.
- [ ] The claim–evidence matrix reflects the valid parameter domain and remaining gaps.
- [ ] No complete Wilson vector or physical mixing prediction is declared before all required sectors and observable-level matching are closed.

## 8. Current physical conclusion

At this baseline, the defensible conclusion is **partial and conditional**:

- The source contains analytical results for the specified four-point hard difference and heavy–light two-point hard functions.
- The zero-momentum portal threshold has an effective-potential algebra cross-check; selected broken-phase matrix/EOM and light-loop functions have documented symbolic and numerical checks.
- The actual FeynArts/FeynCalc diagram-level workflow is not yet executed.
- The complete nonredundant model-level Wilson vector, the required portal boundary, and the physical on-shell scalar-mixing prediction remain unresolved.

This record therefore does not change or certify the physics result. It makes the baseline and evidence chain explicit and defines what must be completed before the final physical claim can be upgraded.

## 9. Change history

| Date | Revision | Change | Reason |
|---|---|---|---|
| 2026-10-23 | RC-001 initial record | Consolidated the v153 source baseline, analytical subresults, Mathematica/Python evidence, unrun FeynArts/FeynCalc scaffold, and claim status | Establish the first end-to-end Scientific Diff record without overstating the completed calculation |
