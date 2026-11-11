# RC-001 — Common-\(k\) ordinary-matter longitudinal assembly ledger

**Workstream:** RC-001-WW-UV-FF-02, Stage B2c-IVn-b  
**Status:** the pairwise ingredients are indexed: cross-vertex and same-vertex fermion WTIs, six scalar-line/seagull endpoint kernels, six graph-specific \(R_{\rm FG}\) current projections, orientation-dependent three-W phases, and the local Yukawa-singlet endpoint cancellation with common heavy-channel routing. This is not yet a summed Slavnov–Taylor identity. The scalar symmetric and commutator tensors remain distinct; reducible external-leg/LSZ terms and the gauge-fixing/ghost sector remain separate.

## 1. Frozen common-\(k\) definitions

Write
\[
\kappa=k+q,\qquad p_4=-p_1-p_2-p_3-q.
\]
For cross-vertex \(A\to B\) pairs,
\[
r_A=k-p_A,\qquad r_B^Y=k+p_B+q,\qquad h=k-p_1-p_2.
\]
For same-vertex \(S\to F\) pairs,
\[
r_F^W=k+p_F,\qquad r_F^Y=k+p_F+q,\qquad
r_S^Y=p_S-k,\qquad h_E=p_F+p_S+q.
\]
The same-vertex \(h_E\) is independent of \(k\) and its heavy propagator remains a spectator.

The already validated shifts are:
- cross A-side Yukawa endpoint and A scalar seagull: \(k_{\rm old}=k+q\), with internal-W momentum \(\kappa\);
- cross B-side Yukawa endpoint and B scalar seagull: no shift, with internal-W momentum \(k\);
- same-vertex F-side Yukawa endpoint: no shift;
- same-vertex S-side Yukawa endpoint and S seagull: \(k_{\rm old}=k+q\), with internal-W momentum \(\kappa\).

## 2. Pair-by-pair ingredient map

| Pair | Fermion-line WTI | Scalar line + seagull | Three-W orientation and phase-weighted group tensor | Explicit RFG chain |
|---|---|---|---|---|
| LD-W-01 (F–F) | A-oriented and B-oriented WTIs | none | \(A\to B:\ -ig_2\mathcal G_{AB}\) | \(\mathcal N_{01}\), with \(-\slashed r_A\,\slashed h\,\slashed r_B^Y\) |
| LD-W-02 (F–S) | A-oriented WTI | B scalar: \(\mathcal C_B\), one seagull | \(A\to B:\ -ig_2\mathcal G_{AB}\) | \(\mathcal N_{02}\), with \(-\slashed r_A\,\slashed h\,V_B\) |
| LD-W-03 (F–S) | same-vertex LD-W-03 WTI | S scalar: \(\mathcal C_S\), one seagull | \(S\to F:\ +ig_2\mathcal G_{FS}\) | \(\mathcal N_{03}\), order \(\slashed k\slashed r_F^Y\) |
| LD-W-04 (S–F) | same-vertex LD-W-04 conjugate WTI | S scalar: \(\mathcal C_S\), one seagull | \(S\to F:\ +ig_2\mathcal G_{FS}\) | \(\mathcal N_{04}\), order \(\slashed r_F^Y\slashed k\) |
| LD-W-05 (S–F) | B-oriented WTI | A scalar: \(\mathcal C_A\), one seagull | \(A\to B:\ -ig_2\mathcal G_{AB}\) | \(\mathcal N_{05}\), with \(V_A\,\slashed h\,\slashed r_B^Y\) |
| LD-W-06 (S–S) | none | A scalar \(\mathcal C_A\) and B scalar \(\mathcal C_B\), two separate seagulls | \(A\to B:\ -ig_2\mathcal G_{AB}\) | \(\mathcal N_{06}\), with \(V_A\,\slashed h\,V_B\) |

The exact \(R_{\rm FG}\) numerators and denominators are recorded in
\`research/RC-001-dim6-WW-fivepoint-explicit-RFG-six-pair-currents.md\`.
The actual scalar-line/seagull kernels and their \(\mathcal S_X/\mathcal G_{\rm orient}\) tensors are recorded in
\`research/RC-001-dim6-WW-fivepoint-explicit-scalar-line-seagull-six-pair.md\`.
The same-vertex fermion WTI orientations are recorded in
\`research/RC-001-dim6-WW-fivepoint-same-vertex-fermion-WTI.md\`.

## 3. Fermion-line Ward identities

The cross-vertex identities remain the B2c-I/II conventions:
\[
S_F(-r_A^W)\slashed qP_LS_F(-r_A^Y)
=S_F(-r_A^W)P_R-P_LS_F(-r_A^Y),
\]
\[
S_F(r_B^Y)\slashed qP_LS_F(r_B^W)
=P_LS_F(r_B^W)-S_F(r_B^Y)P_R.
\]
For the same-vertex pairs, the explicit newly derived identities are
\[
\boxed{
S_F(r_F^W)\slashed qP_LS_F(r_F^Y)
=S_F(r_F^W)P_R-P_LS_F(r_F^Y)
\quad(\mathrm{LD\!-\!W\!-\!03}),
}
\]
\[
\boxed{
S_F(r_F^Y)\slashed qP_LS_F(r_F^W)
=P_LS_F(r_F^W)-S_F(r_F^Y)P_R
\quad(\mathrm{LD\!-\!W\!-\!04}).
}
\]
The two same-vertex identities are related by Dirac-Hermitian conjugation but retain opposite open-line order. The heavy channel \(S_E(h_E)\) is a spectator and is not differentiated with respect to \(k\).

## 4. What the common-\(k\) kernel cancellation does establish

For the cross-vertex group phase \(-ig_2\mathcal G_{AB}\), and the same-vertex phase \(+ig_2\mathcal G_{FS}\), the universal matter-line commutator kernel and the contracted three-W transverse inverse-kernel difference have already been aligned at common \(k\). Their \(D(k)-D(\kappa)\) pieces cancel in the universal arbitrary-current sub-block, leaving
\[
R_{\rm FG}^{\mu\nu}
=\frac{k^\mu k^\nu-\kappa^\mu\kappa^\nu}{k^2\kappa^2}.
\]
The present IVl calculation inserts the actual endpoint numerators into this residual tensor for all six pairs. It does **not** set \(R_{\rm FG}\) to zero.

The scalar-line/seagull sub-block is now also explicit. Its weak tensors remain
\[
\mathcal S_X^a
\quad\text{and}\quad
\mathcal G_{AB}^a\ \text{or}\ \mathcal G_{FS}^a
\]
as separate structures. The local Yukawa-singlet endpoint variation is now checked separately: \\( (R_{\\bar L}^a+R_H^a)T_0=0 \\) and \\( (R_{H^\\dagger}^a+R_L^a)T_0=0 \\), and the common-​\\(k\\) shifts show that the two fields at each Yukawa vertex multiply the same heavy-channel spectator. This closes the local charge-sum sub-block. It does not yet provide the complete reducible external-leg/LSZ contribution or the full gauge variation of the amputated Green function. Do not infer a complete scalar-endpoint cancellation merely from the universal arbitrary-current kernel identity.

## 5. Direct-attachment census

The ordinary internal attachments remain
\[
12\ {\rm matter\!-\!line}
+6\ {\rm scalar\ seagull}
+6\ {\rm three\!-\!W}
=24.
\]
By pair:
\[
(3,4,4,4,4,5)
\]
for LD-W-01…06. No new topology is introduced in IVl/IVm/IVn-a.

## 6. Remaining assembly gates

1. Write the reducible external-field W emissions explicitly and separate them from the 1PI five-point vertex used for Wilson matching; keep the common heavy-channel factors and external propagators visible.
2. Combine the fermion WTI endpoint terms with the local Yukawa-singlet charge cancellation, retaining the \(P_L/P_R\) endpoint pieces and raw weak-index order.
3. Sum the scalar \(\mathcal S_X\) terms with the corresponding endpoint/LSZ terms; keep \(\mathcal G_{AB}\) and \(\mathcal G_{FS}\) separate until their orientation-specific phases are applied.
4. Combine the ordinary-matter integrand with the explicit RFG kernels and the three-W terms.
5. Only then add the gauge-fixing/ghost Slavnov–Taylor sector and the \(W\)-field, gauge-coupling, matter-field, Yukawa, heavy-mass, and operator counterterms.
6. After the complete off-shell identity closes, perform the common-regulator UV–EFT subtraction and compare the local longitudinal contact to the existing EFT one-\(W\) vertex.

No loop integration, complete STI closure, transverse form factor, UV–EFT matching coefficient, or Wilson coefficient is claimed at this stage.
