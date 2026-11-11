# RC-001 — Common-\(k\) ordinary-matter longitudinal assembly ledger

**Workstream:** RC-001-WW-UV-FF-02, Stage B2c-IVn-f/01  
**Status:** the pairwise ingredients are indexed: cross-vertex and same-vertex fermion WTIs, six scalar-line/seagull endpoint kernels, six graph-specific \(R_{\rm FG}\) current projections, orientation-dependent three-W phases, the local Yukawa-singlet endpoint cancellation with common heavy-channel routing, the 1PI/1PR LSZ boundary, the exact longitudinal inverse-kernel completion target for \(R_{\rm FG}\), the IVn-e audit of momentum-dependent scalar-current routing, the exact three-W internal-leg exchange identity at the vertex/group-factor level, and seven exact scalar/fermion-line versus three-W denominator-factor relations. The current-routing audit shows that IVh's arbitrary-current identity has not yet been matched to the actual IVl/IVm scalar currents for the scalar-containing pairs. IVn-f/01 now closes the actual LD-W-01 F-F commutator/three-W sub-block with its explicit Dirac chain, physical weak tensor, relative phase, and complete spectator denominators; it leaves the explicit nonzero R_FG projection. This is not yet a summed Slavnov–Taylor identity. The scalar symmetric and commutator tensors remain distinct; reducible external-leg/LSZ terms and the gauge-fixing/ghost sector remain separate.

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
The IVl source inserts the six graph-specific currents into the residual tensor. However, IVn-e finds that the scalar derivative currents used in IVl and IVm are evaluated at different shifted momenta: \(V_A(k)-V_A(\kappa)=q\), \(V_B(k)-V_B(\kappa)=q\), and \(V_S(k)-V_S(\kappa)=q\). The IVh arbitrary-current test uses independent momentum-independent symbols for its endpoint currents, so it proves the tensor identity but does not yet prove the graph-specific cancellation after these scalar-current shifts. The exact six-endpoint diagnostic is recorded in `research/RC-001-dim6-WW-fivepoint-momentum-dependent-scalar-current-audit.md`. IVn-e also checks seven exact denominator-factor relations. In the cross A/B and same-vertex F/S line insertions, an adjacent matter propagator replaces the second W propagator in the corresponding three-W denominator; the seagull denominators are the three-W denominator divided by the relevant W virtuality. These relations are recorded in the IVn-e audit. No physical non-cancellation is claimed; the loop-variable/routing bridge remains to be derived. IVn-d separately identifies \(R_{\rm FG}\) as the negative of the propagator-sandwiched longitudinal inverse-kernel difference: with \(L_{\mu\nu}(p)=p_\mu p_\nu\), \(D(\kappa)[L(\kappa)-L(k)]D(k)=-R_{\rm FG}\). Thus \(K+L=p^2g\) closes the inverse-kernel algebra. This is the tensor target for the BRST/ghost STI, not proof that a ghost graph by itself cancels the matter-chain remainder.

### 4.1 LD-W-01 graph-specific control result (IVn-f/01)

For \(A=\bar L,\ B=L\), the actual chain
\[
\mathcal X_{01}=-\slashed r_A\slashed h\slashed r_B^Y P_L
\]
has been inserted into the Feynman-gauge inverse-kernel identity. The A-side Yukawa-endpoint shift \(k_{\rm old}=k+q\) and the unshifted B-side map align the two single-W denominator terms with the three-W reference. The physical A/B commutator tensors both give \(-ig_2\mathcal G_{AB}^a\), and the actual matrix contraction gives
\[
\mathcal M_{01,\mathrm{comm}+3W}
=\frac{-ig_2\mathcal G_{AB}^a}
{r_A^2(r_B^Y)^2(h^2-M_E^2)}
\frac{\mathcal N_{01}}{k^2\kappa^2}.
\]
This is precisely the retained \(R_{\rm FG}\) projection in the isolated commutator/three-W sub-block. It is not the full LD-W-01 five-point Ward identity: Yukawa-endpoint gauge variations, external legs, ghosts, counterterms, and UV–EFT subtraction remain outside this calculation.

The exact source and six local tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-01-common-k-numerator-denominator.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_01_common_k_numerator_denominator.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-01-common-k-numerator-denominator.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-01-common-k-numerator-denominator.txt\`

The scalar-line/seagull sub-block is now also explicit. Its weak tensors remain
\[
\mathcal S_X^a
\quad\text{and}\quad
\mathcal G_{AB}^a\ \text{or}\ \mathcal G_{FS}^a
\]
as separate structures. The local Yukawa-singlet endpoint variation is now checked separately: \( (R_{\bar L}^a+R_H^a)T_0=0 \) and \( (R_{H^\dagger}^a+R_L^a)T_0=0 \), and the common-​\(k\) shifts show that the two fields at each Yukawa vertex multiply the same heavy-channel spectator. This closes the local charge-sum sub-block. It does not yet provide the complete reducible external-leg/LSZ contribution or the full gauge variation of the amputated Green function. Do not infer a complete scalar-endpoint cancellation merely from the universal arbitrary-current kernel identity.

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
for LD-W-01…06. No new topology is introduced in IVl/IVm/IVn-a…IVn-e.

## 6. Remaining assembly gates

1. **LD-W-02 (F–S) is next.** Keep the A-side fermion endpoint and the B-side scalar-line/seagull endpoint as separate sub-blocks. In the A-side Yukawa-endpoint map, the B scalar current is \(V_B(\kappa)\), exactly as in the three-W graph. The B scalar-line kernel instead contains \(V_B(k)\), \(\Delta_Y-\Delta_W\), and the seagull contact \(\Delta_Yq^\mu\). Do not identify these currents by inspection; derive the complete numerator/denominator relation and keep \(\mathcal S_B^a\) and \(\mathcal G_{AB}^a\) separate.
2. **LD-W-05 (S–F):** repeat the endpoint-level construction for the A-side scalar, retaining \(V_A(\kappa)\), its opposite scalar-WTI orientation, the B-side fermion current, and the A seagull.
3. **LD-W-03/04 (same-vertex):** assemble each ordered Dirac-Hermitian chain separately, preserving the \(S\to F\) phase and the heavy spectator \(S_E(h_E)\).
4. **LD-W-06 (S–S):** keep the A and B scalar-line terms and their two seagulls separate until both full Lorentz-weighted weak tensors have been inserted.
5. After the six pair-specific sub-blocks are explicit, assemble the complete ordinary-matter longitudinal integrand. Retain all \(P_L/P_R\) endpoint pieces and the raw weak-index order.
6. Combine the Yukawa-endpoint terms with the local Yukawa-singlet charge cancellation; do not absorb the four external-leg emissions into the 1PI five-point vertex.
7. Write the four external-leg/LSZ factors and their lower-point amplitudes explicitly, then derive the BRST/ghost Slavnov–Taylor completion and test the longitudinal inverse-kernel target \(D(\kappa)[L(\kappa)-L(k)]D(k)=-R_{\rm FG}\) in the assembled matter-current chains.
8. Add the \(W\)-field, gauge-coupling, matter-field, Yukawa, heavy-mass, and operator counterterms. Only after the complete off-shell identity closes should the common-regulator UV–EFT subtraction and comparison with the EFT one-\(W\) vertex be performed.

No loop integration, complete STI closure, transverse form factor, UV–EFT matching coefficient, or Wilson coefficient is claimed at this stage.
