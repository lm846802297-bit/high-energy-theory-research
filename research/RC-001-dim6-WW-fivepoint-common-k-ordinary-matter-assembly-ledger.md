# RC-001 — Common-\(k\) ordinary-matter longitudinal assembly ledger

**Workstream:** RC-001-WW-UV-FF-02, Stage B2c-IVn-g/02  
**Status:** the pairwise ingredients are indexed: cross-vertex and same-vertex fermion WTIs, six scalar-line/seagull endpoint kernels, six graph-specific \(R_{\rm FG}\) current projections, orientation-dependent three-W phases, the local Yukawa-singlet endpoint cancellation with common heavy-channel routing, the 1PI/1PR LSZ boundary, the exact longitudinal inverse-kernel completion target for \(R_{\rm FG}\), the IVn-e audit of momentum-dependent scalar-current routing, the exact three-W internal-leg exchange identity at the vertex/group-factor level, and seven exact scalar/fermion-line versus three-W denominator-factor relations. The IVh arbitrary-current identity was not sufficient by itself to establish graph-specific scalar-current cancellation. IVn-f/01–05 now insert the actual currents, ordered Dirac chains, shifted denominators, and scalar-line/seagull endpoint structures for all six pair classes; the full ordinary-matter longitudinal sum remains open. IVn-f/01 now closes the actual LD-W-01 F-F commutator/three-W sub-block with its explicit Dirac chain, physical weak tensor, relative phase, and complete spectator denominators; it leaves the explicit nonzero R_FG projection. IVn-f/02 now separates LD-W-02 into its A-side fermion/three-W sub-block and B-side scalar-line/seagull kernel, and derives the exact (V_B(k)=V_B(\kappa)+q) rebase with both symmetric and commutator (q^\mu) contacts retained. IVn-f/03 now adds the LD-W-05 A-side scalar split, with the symmetric and commutator q^mu contacts retained. IVn-f/04 completes the pair-specific LD-W-03/04 same-vertex endpoint bridge: V_S^line=V_S^3W-q, the symmetric and commutator q^mu contacts remain separate, and both Dirac-Hermitian R_FG chains and heavy spectators are checked. IVn-f/05 completes the pair-specific LD-W-06 S-S endpoint bridge: A and B currents are rebased separately, with (V_A^{\rm line}=V_A^{3W}-q) and (V_B^{\rm line}=V_B^{3W}+q); their two seagulls and weak tensors remain distinct. IVn-g/01 now audits the secondary shifts of the two LD-W-06 scalar-line \(-\Delta_W\) terms: the scalar/W/current factors align, but the heavy channel shifts to (h-q) on A and (h+q) on B. These terms cannot be identified pointwise with the unshifted (h)-channel three-W integrand. This is not yet a summed Slavnov–Taylor identity. The scalar symmetric and commutator tensors remain distinct; reducible external-leg/LSZ terms and the gauge-fixing/ghost sector remain separate.

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

### 4.2 LD-W-02 graph-specific endpoint split (IVn-f/02)

For \(A=\bar L,\ B=H^\dagger\), the A-side fermion Yukawa-endpoint shift \(k_{\rm old}=k+q\) maps the B scalar current to \(V_B(\kappa)\), exactly the current in the three-W graph. Its single-W denominator is \(\mathscr D_{3W}^{02}/k^2\).

The B-side scalar-line/seagull kernel is a distinct sub-block. It contains \(V_B(k)\), \(\delta_B=\Delta_Y-\Delta_W\), and the seagull contact \(\Delta_Yq^\mu\). Re-expressing it in the three-W current basis gives
\[
\begin{aligned}
\mathcal C_B^\mu=g_2\Big[
&\tfrac12\delta_BV_B^\mu(\kappa)\mathcal S_B^a
+(\tfrac12\delta_B+\Delta_Y)q^\mu\mathcal S_B^a\\
&+\tfrac i2\delta_BV_B^\mu(\kappa)\mathcal G_{AB}^a
+\tfrac i2\delta_Bq^\mu\mathcal G_{AB}^a
\Big].
\end{aligned}
\]
The last two \(q^\mu\) terms are kept separately in the symmetric and commutator weak tensors. At the exact rational diagnostic point \(\delta_B=9/380\), and the commutator \(q^\mu\) contact produces a nonzero 16/16 Dirac matrix. This is not evidence of a physical non-cancellation; its combination with external-field/Yukawa endpoint variations and LSZ terms remains open.

The exact source and six local tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-02-common-k-FS-endpoint-split.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_02_common_k_FS_endpoint_split.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-02-common-k-FS-endpoint-split.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-02-common-k-FS-endpoint-split.txt\`

### 4.3 LD-W-05 graph-specific endpoint split (IVn-f/03)

For \(A=H,\ B=L\), the unshifted B-side fermion Yukawa-endpoint term carries \(V_A(k)\), exactly the A-scalar current in the three-W graph. Its denominator is \(\mathscr D_{3W}^{05}/\kappa^2\).

The A-side scalar-line/seagull kernel instead contains \(V_A^{\rm line}=2p_2-\kappa\), while the three-W current is \(V_A^{3W}=2p_2-k\). Since \(V_A^{\rm line}=V_A^{3W}-q\), the exact rebased current is
\[
\begin{aligned}
\mathcal C_A^\mu=g_2\Big[
&-\tfrac12\delta_AV_A^{3W,\mu}\mathcal S_A^a
+(\tfrac12\delta_A+\Delta_Y)q^\mu\mathcal S_A^a\\
&-\tfrac i2\delta_AV_A^{3W,\mu}\mathcal G_{AB}^a
+\tfrac i2\delta_Aq^\mu\mathcal G_{AB}^a
\Big].
\end{aligned}
\]
At the exact rational diagnostic point \(\delta_A=-6/391\); the commutator \(q^\mu\) contact produces a nonzero 16/16 Dirac matrix. It is retained and is not interpreted as a physical non-cancellation.

The exact source and six local tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-05-common-k-SF-endpoint-split.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_05_common_k_SF_endpoint_split.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-05-common-k-SF-endpoint-split.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-05-common-k-SF-endpoint-split.txt\`

The scalar-line/seagull sub-block is now also explicit. Its weak tensors remain
\[
\mathcal S_X^a
\quad\text{and}\quad
\mathcal G_{AB}^a\ \text{or}\ \mathcal G_{FS}^a
\]
as separate structures. The local Yukawa-singlet endpoint variation is now checked separately: \( (R_{\bar L}^a+R_H^a)T_0=0 \) and \( (R_{H^\dagger}^a+R_L^a)T_0=0 \), and the common-​\(k\) shifts show that the two fields at each Yukawa vertex multiply the same heavy-channel spectator. This closes the local charge-sum sub-block. It does not yet provide the complete reducible external-leg/LSZ contribution or the full gauge variation of the amputated Green function. Do not infer a complete scalar-endpoint cancellation merely from the universal arbitrary-current kernel identity.

### 4.4 LD-W-03/04 same-vertex S-to-F endpoint bridge (IVn-f/04)

The same-vertex scalar endpoint has a different current rebase from both cross-vertex scalar cases. With
\[
r_S^Y=p_S-k,\quad r_S^W=p_S-\kappa,\quad
\Delta_{Y,W}=1/(r_S^{Y,W})^2,\quad \delta_S=\Delta_Y-\Delta_W,
\]
the S-to-F scalar WTI gives
\[
q\cdot(r_S^W+r_S^Y)\Delta_W\Delta_Y
=\Delta_W-\Delta_Y=-\delta_S.
\]
The scalar-line current is \(V_S^{\rm line}=2p_S-\kappa\), while the three-W current is \(V_S^{3W}=2p_S-k\), so \(V_S^{\rm line}=V_S^{3W}-q\). The exact rebased scalar-line/seagull current is
\[
\begin{aligned}
\mathcal C_S^\mu=g_2\Big[
&\tfrac12\delta_S V_S^{3W,\mu}\mathcal S_S^a
+\tfrac12(\Delta_Y+\Delta_W)q^\mu\mathcal S_S^a\\
&+\tfrac i2\delta_S V_S^{3W,\mu}\mathcal G_{FS}^a
-\tfrac i2\delta_Sq^\mu\mathcal G_{FS}^a
\Big].
\end{aligned}
\]
Thus the symmetric and commutator contacts have coefficients \((\Delta_Y+\Delta_W)/2\) and \(-i\delta_S/2\), respectively. This is not the LD-W-02 B-side or LD-W-05 A-side formula with a relabelled endpoint.

The common shift \(k_{\rm old}=k+q\) maps the original scalar-line momenta to
\[
r_S^S\to r_S^W,\quad r_S^Y\to r_S^Y,\quad
r_F^W\to r_F^Y,\quad k_S\to\kappa,\quad
V_S\to V_S^{\rm line}.
\]
Moreover,
\[
\Delta_W(k)=\Delta_Y(k+q),\quad
r_F^Y(k)=r_F^W(k+q),\quad
V_S^{\rm line}(k)=V_S^{3W}(k+q).
\]
Therefore the \(-\Delta_W\) part of the scalar WTI maps, after \(k\to k+q\), to the corresponding F-side endpoint routing. The seagull denominator is exactly \(D_{3W}/k^2\); the scalar-line graph retains both scalar propagators and must not be assigned the seagull denominator.

The actual ordered kernels are
\[
\mathcal K_{03,S}=\slashed{\mathcal C}_S\slashed r_F^Y/\kappa^2,\qquad
\mathcal K_{04,S}=\slashed r_F^Y\slashed{\mathcal C}_S/\kappa^2,
\]
and the corresponding three-W remainders retain
\[
\begin{aligned}
\mathcal N_{03}&=(V_S^{3W}\cdot k)\slashed k\slashed r_F^Y
-(V_S^{3W}\cdot\kappa)\slashed\kappa\slashed r_F^Y,\\
\mathcal N_{04}&=(V_S^{3W}\cdot k)\slashed r_F^Y\slashed k
-(V_S^{3W}\cdot\kappa)\slashed r_F^Y\slashed\kappa.
\end{aligned}
\]
The chiral heavy propagator \(P_R(\slashed h_E+M_E)P_L/(h_E^2-M_E^2)\) remains a \(k\)-independent spectator in the original seed order.

The exact source and seven regression tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-03-04-common-k-same-vertex-endpoint-split.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_03_04_common_k_same_vertex_endpoint_split.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-03-04-common-k-same-vertex-endpoint-split.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-03-04-common-k-same-vertex-endpoint-split.txt\`

The exact rational checks use two nonsingular points for both pair orientations. They confirm 64/64 direct-versus-factorized \(R_{\rm FG}\) matrix components and 64/64 raw-versus-rebased scalar-kernel components. The two q-contact matrices remain nonzero. The weak-index checks reproduce the S-to-F group-phase identity, but do not claim the Lorentz-weighted four-attachment cancellation.

### 4.5 LD-W-06 two scalar endpoints (IVn-f/05)

LD-W-06 has two independent scalar-line/seagull sub-blocks. For the A endpoint,
\[
V_A^{\rm line}=V_A^{3W}-q,\qquad
\mathcal C_A^\mu=g_2\left[
-\tfrac12\delta_AV_A^{3W,\mu}\mathcal S_A^a
+(\Delta_{AY}+\tfrac12\delta_A)q^\mu\mathcal S_A^a
-\tfrac i2\delta_AV_A^{3W,\mu}\mathcal G_{AB}^a
+\tfrac i2\delta_Aq^\mu\mathcal G_{AB}^a
\right].
\]
For the B endpoint,
\[
V_B^{\rm line}=V_B^{3W}+q,\qquad
\mathcal C_B^\mu=g_2\left[
\tfrac12\delta_BV_B^{3W,\mu}\mathcal S_B^a
+(\Delta_{BY}+\tfrac12\delta_B)q^\mu\mathcal S_B^a
+\tfrac i2\delta_BV_B^{3W,\mu}\mathcal G_{AB}^a
+\tfrac i2\delta_Bq^\mu\mathcal G_{AB}^a
\right].
\]
The actual contracted kernels are
\[
\mathcal K_{06,A}=\slashed h(V_B^{3W}\cdot\mathcal C_A)/\kappa^2,\qquad
\mathcal K_{06,B}=(V_A^{3W}\cdot\mathcal C_B)\slashed h/k^2.
\]
The A/B seagull tensors remain
\[
\mathcal S_A^a=\tfrac12R_B^aT_0,\qquad
\mathcal S_B^a=\tfrac12R_A^aT_0.
\]
They are not identified, even though both commutators use \(\mathcal G_{AB}^a\).

The seagull denominators satisfy \(D_{A,\rm sg}=D_{3W}/k^2\) and \(D_{B,\rm sg}=D_{3W}/\kappa^2\). The scalar-line denominators retain both propagators on their respective scalar lines. The actual S-S \(R_{\rm FG}\) numerator is
\[
\mathcal N_{06}
=(V_A^{3W}\cdot k)\slashed h(V_B^{3W}\cdot k)
-(V_A^{3W}\cdot\kappa)\slashed h(V_B^{3W}\cdot\kappa).
\]
Two nonsingular rational points verify the direct Lorentz contraction (32/32 matrix components) and the A/B raw-to-rebased endpoint kernels (64/64 matrix components). All four A/B symmetric/commutator \(q^\mu\) contacts remain nonzero.

The exact source and six local tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-06-common-k-SS-two-endpoint-bridge.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_06_common_k_SS_two_endpoint_bridge.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-06-common-k-SS-two-endpoint-bridge.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-06-common-k-SS-two-endpoint-bridge.txt\`

This closes the pair-specific endpoint-current rebase for LD-W-06, not the complete S-S four-attachment Ward sum.

### 4.6 LD-W-06 secondary scalar shifts change the heavy channel (IVn-g/01)

The second loop shifts needed to align the \(-\Delta_W\) terms are not innocuous. For the A-side term, set \(k_A'=k+q\). The scalar and current factors map as
\[
\kappa(k)\to k_A',\quad
r_A^W(k)\to r_A^Y(k_A'),\quad
r_B^Y(k)\to r_B^W(k_A'),
\]
\[
V_A^{\rm line}(k)\to V_A^{3W}(k_A'),\quad
V_B^{3W}(k)\to V_B^{\rm line}(k_A').
\]
But
\[
\boxed{h(k)=h(k_A')-q.}
\]
The shifted heavy denominator is \((h(k_A')-q)^2-M_E^2\), not the original \(h(k_A')^2-M_E^2\).

For the B-side term, set \(k_B'=k-q\). Then
\[
k\to\kappa(k_B'),\quad
r_A^Y(k)\to r_A^W(k_B'),\quad
r_B^W(k)\to r_B^Y(k_B'),
\]
\[
V_A^{3W}(k)\to V_A^{\rm line}(k_B'),\quad
V_B^{\rm line}(k)\to V_B^{3W}(k_B'),
\]
whereas
\[
\boxed{h(k)=h(k_B')+q.}
\]
Its heavy denominator is \((h(k_B')+q)^2-M_E^2\).

The generic identities are
\[
(h-q)^2-M_E^2=(h^2-M_E^2)+q^2-2h\cdot q,
\]
\[
(h+q)^2-M_E^2=(h^2-M_E^2)+q^2+2h\cdot q.
\]
At the exact rational point used in IVn-g/01,
\[
H_0=-377,\qquad H_A=-389,\qquad H_B=-365.
\]
The scalar/W/current factors align under each secondary shift, but the heavy denominators remain distinct. This is not a physical non-cancellation: the shifted terms must be compared with the corresponding Yukawa-endpoint and reducible LSZ contributions. The previous local Yukawa-singlet charge check was performed at the first common-\(k\) routing; its extension to these \(h\pm q\) channels is an explicit remaining check.

The exact source and six local tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-06-secondary-shift-heavy-channel-audit.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_06_secondary_shift_heavy_channel_audit.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-06-secondary-shift-heavy-channel-audit.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-06-secondary-shift-heavy-channel-audit.txt\`

IVn-g/02 extends the local Yukawa-singlet charge check to these shifted channels: the two left-vertex variations share (h-q), and the two right-vertex variations share (h+q), so both local charge sums still vanish. This is a precise routing/denominator result, not a completed Ward identity.

### 4.7 Shifted LD-W-06 Yukawa-singlet charge factors (IVn-g/02)

The secondary shifts change the heavy channel but do not split the two field variations at either Yukawa singlet:
\[
k_A'=k+q:\quad h_{\bar L}=h_H=h(k_A')-q,
\]
\[
k_B'=k-q:\quad h_{H^\dagger}=h_L=h(k_B')+q.
\]
The physical charge sums therefore remain
\[
(R_{\bar L}^a+R_H^a)T_0\,S_E(h-q)X_A=0,\qquad
(R_{H^\dagger}^a+R_L^a)T_0\,S_E(h+q)X_B=0.
\]
The exact check passes 8/8 vector components for each heavy-channel map and 96/96 weak-index components for the shifted singlet charge sums. This is a local endpoint-factor cancellation; it does not sum the scalar-line/three-W Lorentz kernels or the reducible LSZ terms.

The exact source and five local tests are recorded in:
- \`calculations/RC-001-dim6-WW-fivepoint-LD-W-06-shifted-Yukawa-singlet-charge-closure.py\`
- \`calculations/test_RC001_dim6_WW_fivepoint_LD_W_06_shifted_Yukawa_singlet_charge_closure.py\`
- \`research/RC-001-dim6-WW-fivepoint-LD-W-06-shifted-Yukawa-singlet-charge-closure.md\`
- \`validation/RC-001-dim6-WW-fivepoint-LD-W-06-shifted-Yukawa-singlet-charge-closure.txt\`

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

1. **Assemble the ordinary-matter longitudinal integrand for all six pairs.** Insert the four fermion-line WTI endpoint pieces, all six scalar-line/seagull kernels, and all six three-W kernels using the actual common-\(k\) routes. Keep all \(P_L/P_R\) endpoint pieces, the \(S\to F\) and \(A\to B\) weak-index orders, and the distinct \(\mathcal S_A,\mathcal S_B,\mathcal S_S\) tensors.
2. **Perform every secondary loop-variable shift on the complete numerator and denominator.** Keep the two terms in each \(\delta_X=\Delta_Y-\Delta_W\) separate. For LD-W-06, the A and B negative-propagator terms shift \(h\) to \(h-q\) and \(h+q\), respectively.
3. **Extend the shifted-channel audit to the other five pair classes.** For every local Yukawa endpoint pair, verify that the two field variations share the same shifted heavy-channel factor after the full momentum/current map. LD-W-06 passes this local charge-factor test.
4. **Combine the ordinary-matter 1PI terms with the local endpoint variations.** Only after the weak-index, Dirac-order, momentum-shift, and heavy-denominator identities close should the full longitudinal integrand be declared telescoped.
5. **Write the four reducible external-leg/LSZ factors and their lower-point amplitudes explicitly.** Keep them outside the 1PI five-point vertex until the full Ward identity is assembled.
6. **Derive the BRST/ghost Slavnov–Taylor completion** and test the longitudinal inverse-kernel target \(D(\kappa)[L(\kappa)-L(k)]D(k)=-R_{\rm FG}\) in the assembled matter-current chains.
7. **Add counterterms:** \(W\)-field, gauge-coupling, matter-field, Yukawa, heavy-mass, and operator counterterms. Only after the complete off-shell identity closes should the common-regulator UV–EFT subtraction and comparison with the EFT one-\(W\) vertex be performed.

No loop integration, complete STI closure, transverse form factor, UV–EFT matching coefficient, or Wilson coefficient is claimed at this stage.
