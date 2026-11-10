# RC-001 research-change record — dimension-six gauge subgraphs

## 1. Identity and baseline

- **Research-change ID:** RC-001-GAUGE-SUBGRAPHS (subrecord of RC-001; not a replacement for the parent record)
- **Title:** Gauge corrections to \(Q_{LD}\), \(Q_{RD}\), and associated current/source operators
- **Created / updated:** 2026-10-23
- **Work status:** Verification in progress
- **Related project:** [RC-001 VLL–Higgs–Singlet UV–EFT matching](RC-001-vll-higgs-singlet-uv-eft.md)
- **Baseline revision:** `main` at merge commit `65edf2256948056c6b15094e5fb7f2ebe1f3b682`
- **Working revision:** `main` after the follow-up Scientific Diff record commit
- **Related records:** [claim–evidence matrix](RC-001-claim-evidence-matrix.md), [gauge attachment atlas](RC-001-dim6-gauge-diagram-atlas.md), [UV–EFT subtraction ledger](RC-001-dim6-uv-eft-subtraction-ledger.md), [master-integral record](RC-001-dim6-heavy-line-vertex-box-integrals.md), [mixed kinetic threshold](RC-001-dim6-mixed-kinetic-threshold.md)

## 2. Scientific question

### Question

What are the complete \(O(g^2/M_E^2)\) corrections to the tree-level \(Q_{LD}\) and \(Q_{RD}\) amplitudes after summing heavy-line self-energies, both conjugate Yukawa vertices, crossed boxes, external-field/parameter counterterms, EFT soft graphs, and covariant-derivative contact vertices in one common scheme?

### Baseline statement

The tree coefficients are
\[
C_{LD,\ell}=\frac{|y_\ell|^2}{M_{E_\ell}^2},\qquad
C_{RD,\ell}=\frac{|\lambda_\ell|^2}{M_{E_\ell}^2}.
\]
The repository now contains a charge-compatible attachment-class census, an exact \(SU(2)_L\) projection for the six \(WW\) line-pair classes, a partial diagonal-gauge parameter-counterterm calculation, a Feynman-gauge heavy-line self-energy subgraph, selected scalar master-integral UV/IR splits, and the additive \(B-A'\) vacuum-polarization threshold. It does **not** contain the complete gauge-corrected amplitudes or a closed dimension-six Wilson vector.

### Target

For each external amplitude and each gauge sector, produce the labeled UV graph sum, matching EFT graph sum under the same IR prescription, the separate UV/IR poles, finite local hard terms, counterterms, and projection into one nonredundant operator basis. Keep the full claim unresolved until all required graph families and basis reductions are closed.

## 3. Scope and assumptions

- **Included:** \(Q_{LD}\), \(Q_{RD}\), one-gauge-boson corrections at \(O(g^2/M_E^2)\), heavy-line self-energy, both conjugate Yukawa vertices, cross-vertex boxes, external fields, parameter/operator counterterms, EFT soft subtractions, derivative-contact graphs, and the \(B-A'\) kinetic matrix.
- **Excluded from closure:** full \(O(M_E^{-4})\) dimension-eight hard matching and physical scalar-mixing/LSZ claims.
- **Phase and fields:** unbroken phase; massless light fields for hard matching; \(H,S,A'\) and light leptons retained in the EFT.
- **Regularization:** \(d=4-2\epsilon\), common \(\overline{\mathrm{MS}}\) convention, and identical nonexceptional off-shell external momenta (or one explicitly shared IR regulator) on UV and EFT sides.
- **Gauge convention:** Feynman gauge for the currently evaluated heavy-line subgraph only. The final summed result must be gauge-parameter independent for the gauge-invariant matching coefficient.
- **Flavor/charges:** \(\eta_\mu=+1\), \(\eta_\tau=-1\), \(Y_E=-1\), \(x_E=\eta_\ell\), \(Y_L=-1/2\), \(Y_{\ell_R}=-1\), \(x_L=\eta_\ell\), \(x_{\ell_R}=-\eta_\ell\), \(x_{S_\ell}=2\eta_\ell\).
- **Kinetic mixing:** the renormalized \(\chi(\mu_R)\) boundary condition is an independent input unless specified; a one-loop threshold must not be silently reinterpreted as a tree-level mixing.

## 4. Current calculation record

### Evaluated sub-blocks

1. Heavy-\(E_\ell\) self-energy at \(p^2=0\) and its insertion into the chirality-preserving propagator, including the subgraph-level pole/counterterm cancellation in the stated Feynman-gauge convention.
2. The zero-momentum scalar kernel \(B_0(0;0,M_E^2)=\Delta_\epsilon+1-\ln(M_E^2/\mu_R^2)\) and representative numerator reductions before full Feynman-rule signs and group factors.
3. A representative crossed-box scalar master with an explicit hard-minus-soft split, retaining separate UV and IR poles.
4. The additive \(B-A'\) vacuum-polarization trace and finite heavy threshold for the stated charge spectrum.
5. Exact-algebra scripts for the displayed parameter integrals, partial fractions, charge traces, and \(SU(2)\) contractions.
6. Signed charge-factor tables for all three pairings at the four conjugate Yukawa vertices, plus a tree-propagator argument showing the complete purely light vertex subfamily cancels from the hard difference at \(O(M_E^{-2})\) when the EFT contact set is included.
7. A conditional (B-A') input-parameter counterterm sub-block, using an explicit signed off-diagonal propagator coefficient; it remains separate from the complete mixed-gauge amplitude.
8. The heavy-containing FF/FS Yukawa-vertex hard sub-block for Q_LD and Q_RD, with oriented -F factors, all six one-vertex pole/log/finite expressions, and the doubled contribution of the two conjugate vertices.
9. The four (Q_{LD}) pure-(WW) cross-vertex attachment classes LD-W-01/02/05/06 with distinct fixed-ordering momentum routings, pairwise Lorentz kernels, and the explicit hard/soft scalar-master split. The unit-multiplicity hard coefficient is ((3Delta_{m UV}/8-3L/8+11/16)/M_E^2); its soft UV pole cancels the hard UV pole, leaving the expected full-amplitude IR pole. The result is recorded in research/RC-001-dim6-WW-crossbox-exact-routing.md and is not a complete LD-W matching coefficient.

### Not established

- No complete vertex or crossed-box graph sum has been evaluated. The (Q_{LD}) pure-(WW) calculation is only the four cross-vertex kernels for one fixed ordered tree contraction and unit multiplicity; the second charge-conjugate/crossed routing, exact diagram count, and full Ward/counterterm sum remain open.
- No complete \(Q_{LD}\) or \(Q_{RD}\) UV amplitude has been subtracted against the full EFT amplitude.
- No finite gauge-correction Wilson coefficient is claimed.
- No full Ward-identity sum, shared counterterm matrix, Fierz/EOM/source reduction, or independent diagram-package validation has been completed.
- Repository CI was explicitly skipped by project decision; this is not a pass and is not a physics criterion for closure.

## 5. Verification plan

| Check | Method / acceptance criterion | Status |
|---|---|---|
| Charge-compatible diagram generation | Generate individual diagrams with a model-aware diagram package; reconcile every generated graph with the hand census and include multiplicities/routings | Not checked; tool availability blocker recorded |
| Heavy-line subgraph | Re-derive numerator, signs, \(O(\epsilon)\) terms, mass/field counterterms in a second convention or implementation | Algebraically checked; independent diagram check open |
| Yukawa vertices | Compute both conjugate vertices with explicit momentum flow, representation generators, charge factors, and common IR prescription | Heavy-containing FF/FS hard sub-block evaluated; full UV–EFT vertex/contact sum remains open |
| Crossed boxes | Enumerate all allowed pairings and crossings; reduce Dirac/weak tensors before summing; UV minus EFT must cancel common IR poles | (Q_{LD}) pure-(WW): four fixed-ordering cross-pair kernels and hard/soft split checked at unit multiplicity; second routing, exact diagram count, full Ward/counterterm sum and other gauge sectors open |
| EFT contact terms | Include all vertices generated by covariant derivatives and all operator insertions required by the external amplitude | Incomplete |
| Mixed \(B-A'\) sector | Specify the renormalized kinetic matrix, its counterterm and threshold convention; keep tree-level \(\chi\) effects separate from one-loop-generated thresholds | Partial two-point threshold only |
| Gauge Ward identities | Sum vertex, self-energy, external-field, contact, and counterterm terms; verify gauge-parameter cancellation in the matched coefficient | Not checked |
| Common-basis reduction | Apply \(SU(2)\), Dirac/Fierz, EOM/source relations once; preserve current-current and four-fermion companions | Partial \(SU(2)\) algebra only |
| Independent validation | Use a diagram-level package or a genuinely independent explicit amplitude derivation; do not count symbolic identity checks as diagram validation | Not checked |
| CI | Explicit project decision is to skip CI for this iteration | Skipped; not passed |

## 6. Claim and downstream impact

- **Claim IDs:** CL-010 (heavy-line/scalar-master subblocks), CL-011 (\(B-A'\) additive pole and threshold), CL-012 (signed conjugate Yukawa-vertex charge factors), CL-013 (light-only vertex hard cancellation), CL-014 (conditional mixed input-parameter poles), CL-015 (heavy-containing vertex hard sub-blocks), CL-005 (complete Wilson vector; remains unresolved).
- The new sub-blocks can support only their narrowly stated integral/charge-trace claims.
- No new finite \(Q_{LD}\) or \(Q_{RD}\) coefficient is authorized for a manuscript, scan, or phenomenological conclusion.
- Existing bosonic field-strength/current-to-gauge and scalar/source terms in master §§254–255 must not be duplicated.
- Downstream impact review remains open for the complete current/source basis and the dimension-eight matching stage.

## 7. Next concrete action

For (Q_{LD}) pure-(WW), explicitly map or calculate the second charge-conjugate/crossed tree routing and validate diagram multiplicities; then include the same-vertex and external-field terms in the Ward bookkeeping. Only after this should the one-(W) form factor and common-basis projection be closed. Next, extend the same per-pair routing/hard-soft method to (Q_{LD}) (BB) and (A'A'), and to the (Q_{RD}) gauge sectors, using the already-evaluated heavy-vertex sub-block without recomputing it. Combine each complete gauge sector with the heavy-line self-energy, parameter/operator counterterms, and EFT soft/contact terms in one UV/IR table before updating any full Wilson coefficient.

## 8. Decision

**Decision:** carry forward as an open research change. The current merge is a version-control integration checkpoint only. The scientific result is a set of evaluated sub-blocks plus an explicit calculation/verification plan, not a complete one-loop matching result.
