# RC-001 — \(Q_{LD}\) pure-\(WW\) cross-box exact routing and hard/soft split

**Status:** exact Lorentz reductions and the scalar-master UV–EFT split are checked for the four cross-vertex \(WW\) attachment classes in one fixed ordered external amplitude. The result is a **unit-multiplicity, fixed-routing sub-block**, not the complete \(WW\) Wilson coefficient. The full charge-conjugate/crossed-routing census, diagram-generator validation, common Ward sum, and common-basis matching remain open.

## 1. Frozen amplitude and conventions

Use the ordered Green function
\[
\bar L_i(p_1),\qquad H_j(p_2),\qquad H_k^\dagger(p_3),\qquad L_l(p_4),
\]
with all momenta incoming. For the local derivative projection choose
\[
p_1=p_3=0,\qquad p_2=P,\qquad p_4=-P.
\]
The left Yukawa vertex is \(-iy_\ell\bar L H E_R\), and the right conjugate vertex is \(-iy_\ell^\ast\bar E_R H^\dagger L\). The heavy momentum is \(q_E=k-P\), where the \(W\) momentum \(k\) flows from the left Yukawa vertex to the right.

Use Feynman gauge, \(d=4-2\epsilon\), and the common \(\overline{\rm MS}\) convention
\[
\Delta_{\rm UV,IR}=\frac1{\epsilon_{\rm UV,IR}}-\gamma_E+\ln4\pi,
\qquad L=\ln\frac{M_E^2}{\mu_R^2}.
\]
The loop-integral normalization and the scalar master UV/IR split are those in research/RC-001-dim6-heavy-line-vertex-box-integrals.md.

The chosen momentum point is an **exceptional local projection** because two external momenta are set to zero. The calculation keeps \(\Delta_{\rm UV}\) and \(\Delta_{\rm IR}\) distinct using the explicit hard/soft master split. It is not a substitute for a complete nonexceptional off-shell Green-function calculation of all six attachment classes.

## 2. Tree orientation and multiplicity boundary

The fixed external field content selects one \(y_\ell\) vertex and one \(y_\ell^\ast\) vertex:
\[
(\bar L,H)\quad\text{and}\quad(H^\dagger,L).
\]
At second order in the interaction, the two dummy-label orderings of these distinct vertices cancel the \(1/2!\) in the perturbative expansion:
\[
\frac1{2!}\left[
\mathcal L_y(x)\mathcal L_{y^\ast}(y)
+\mathcal L_{y^\ast}(x)\mathcal L_y(y)
\right]
\longrightarrow
\mathcal L_y(x)\mathcal L_{y^\ast}(y)
\]
after relabelling \(x\leftrightarrow y\). This is one ordered tree contraction, not an extra factor of two.

There is also a useful operator identity. With the gauge-singlet composite spinor
\[
\Psi=H^\dagger L,\qquad \bar\Psi=\bar L H,
\]
the derivative operator is \(Q_{LD}=\bar\Psi i\slashed D\Psi\), and
\[
Q_{LD}^\dagger
=-i(D_\mu\bar\Psi)\gamma^\mu\Psi
=Q_{LD}-i\partial_\mu(\bar\Psi\gamma^\mu\Psi).
\]
Thus \(Q_{LD}\) is Hermitian modulo a total derivative in the action.

These identities settle the dummy vertex-label factor for the displayed ordered contraction. They do **not** by themselves certify that every additional charge-conjugate/crossed external routing in the atlas maps to the same off-shell Green function. No extra multiplicity is assigned here. The other routing must be explicitly mapped or generated before the result is promoted.

## 3. \(SU(2)_L\) attachment classes

The heavy \(E\) is an \(SU(2)_L\) singlet, so there is no \(WEE\) attachment. The six unordered pairs among the four external doublet lines are the six atlas classes:
\[
\binom{4}{2}=6.
\]
The independently checked weak tensors are
\[
\begin{array}{c|rrrrrr}
\text{pair}&01&02&03&04&05&06\\ \hline
\text{line pair}
&\bar L-L&\bar L-H^\dagger&\bar L-H&L-H^\dagger&L-H&H^\dagger-H\\
T_0,T_3\text{ projection}
&-\frac14T_3&+\frac14T_3&-\frac34T_0&
-\frac34T_0&+\frac14T_3&-\frac14T_3
\end{array}
\]
where \(T_0=\delta_{ij}\delta_{kl}\) and \(T_3=2\delta_{il}\delta_{kj}-\delta_{ij}\delta_{kl}\). These factors are imported from the exact generator-contraction audit research/RC-001-dim6-SU2-attachment-projection.md; they are not inferred from the loop numerators.

The same-vertex pairs LD-W-03 and LD-W-04 are light-only Yukawa-vertex subgraphs: the heavy propagator carries fixed external momentum and is not part of the loop integration. Their \(O(M_E^{-2})\) UV contribution is reproduced by the gauge-covariant EFT insertion under a common regulator, as in the light-only cancellation record. They remain in the Ward/contact bookkeeping but do not supply a new hard coefficient in this subfamily.

The four cross-vertex pairs LD-W-01, 02, 05, and 06 are the hard box sub-block evaluated below. External \(L,H\) self-energy/LSZ factors are common to the UV and EFT tree amplitudes at this order and cancel in the matching difference when the same field convention is used. The differentiated composite \(H^\dagger L\) is an \(SU(2)\) singlet, so the \(Q_{LD}\) insertion has no direct \(W\) contact vertex.

## 4. Exact per-pair routing

For the fixed external ordering, momentum conservation gives
\[
q_{\bar L}=-k,\qquad q_{H^\dagger}=k,\qquad
q_H=P-k,\qquad q_L=q_E=k-P.
\]
The scalar-gauge vertex follows from
\[
\mathcal L\supset ig_2W_\mu^aH^\dagger t^a
\overleftrightarrow{\partial^\mu}H.
\]
With the stated all-incoming convention, the \(H\) endpoint contributes \(2P-k\), and the \(H^\dagger\) endpoint contributes \(-k\).

The four denominators and numerator chains are distinct:

| Pair | Denominator | Numerator chain |
|---|---|---|
| LD-W-01: \(\bar L-L\) | \(k^4(k-P)^2[(k-P)^2-M_E^2]\) | \(\gamma^\mu(-\slashed k)\slashed{(k-P)}\slashed{(k-P)}\gamma_\mu\) |
| LD-W-02: \(\bar L-H^\dagger\) | \(k^6[(k-P)^2-M_E^2]\) | \(\gamma^\mu(-\slashed k)\slashed{(k-P)}(-k_\mu)\) |
| LD-W-05: \(L-H\) | \(k^2(k-P)^4[(k-P)^2-M_E^2]\) | \((2P-k)_\mu\slashed{(k-P)}\slashed{(k-P)}\gamma^\mu\) |
| LD-W-06: \(H^\dagger-H\) | \(k^4(k-P)^2[(k-P)^2-M_E^2]\) | \(-(2P-k)\cdot k\,\slashed{(k-P)}\) |

After the chirality projection and extraction of the local \(\slashed P\) term, the scalar kernels are
\[
\boxed{
A_{01}=\frac{2(d-2)}dK,\qquad
A_{02}=-J+\frac2dK,
}
\]
\[
\boxed{
A_{05}=\left(1+\frac2d\right)J,\qquad
A_{06}=-\frac4dJ.
}
\]
The reduction uses
\[
J=\int_k\frac1{(k^2)^2(k^2-M_E^2)},\qquad
K=\int_k\frac1{k^2(k^2-M_E^2)^2}.
\]
No common-numerator approximation is used.

## 5. Explicit UV–EFT scalar-master split

The common crossed-box master split recorded in the subtraction ledger is
\[
J_{\rm full}=\frac{\Delta_{\rm IR}+1-L}{M_E^2},
\qquad
J_{\rm soft}=\frac{-\Delta_{\rm UV}+\Delta_{\rm IR}}{M_E^2},
\]
hence
\[
J_{\rm hard}=J_{\rm full}-J_{\rm soft}
=\frac{\Delta_{\rm UV}+1-L}{M_E^2}.
\]
For \(K\), the hard/full contribution is \(-1/M_E^2\); its \(O(M_E^{-2})\) soft expansion is the scaleless power integral \(\int d^dk/k^2\), which vanishes in dimensional regularization and has no logarithmic pole at this order.

Applying the exact kernels pair by pair gives
\[
A_{WW}^{\rm hard}
=\frac14(-A_{01}^{\rm hard}+A_{02}^{\rm hard}
+A_{05}^{\rm hard}-A_{06}^{\rm hard})
\]
\[
\boxed{
A_{WW}^{\rm hard}
=\frac1{M_E^2}\left(
\frac38\Delta_{\rm UV}-\frac38L+\frac{11}{16}
\right).
}
\]
The soft/EFT contribution is
\[
\boxed{
A_{WW}^{\rm soft}
=\frac1{M_E^2}\frac38(-\Delta_{\rm UV}+\Delta_{\rm IR}).
}
\]
The sum is
\[
\boxed{
A_{WW}^{\rm full}
=\frac1{M_E^2}\left(
\frac38\Delta_{\rm IR}-\frac38L+\frac{11}{16}
\right).
}
\]
Thus the hard UV pole cancels the EFT-soft UV pole, and the full amplitude retains only the IR pole. The pairwise identities \(A_i^{\rm full}=A_i^{\rm hard}+A_i^{\rm soft}\) are checked exactly.

### \(O(\epsilon)\) finite term

The coefficient multiplying \(J\) in the weighted sum is \(6/d\):
\[
\frac6d=\frac32+\frac34\epsilon+O(\epsilon^2).
\]
Since \(J_{\rm hard}\) contains \(\Delta_{\rm UV}\), the \(+\frac34\epsilon\) term contributes \(+3/16\) to the finite coefficient after the overall \(1/4\) weak-tensor weight. Setting \(d=4\) before multiplying the pole would give \(1/2\), rather than
\[
\frac12+\frac3{16}=\frac{11}{16}.
\]
The same \(O(\epsilon)\) term is retained in the soft split; its UV and IR finite pieces cancel against one another, leaving no additional soft finite constant.

## 6. Wilson-coefficient interpretation and boundary

For \(C_{LD}=|y_\ell|^2/M_E^2\), the raw triplet-derivative coefficient of this fixed-routing unit-multiplicity sub-block is
\[
C_{3}^{WW,\rm box}
=\left(\frac38\Delta_{\rm UV}-\frac38L+\frac{11}{16}\right)
\frac{g_2^2}{16\pi^2}C_{LD}.
\]
At \(\mu_R=M_E\), its finite hard subset is
\[
\left.C_3^{WW,\rm box}\right|_{\rm finite}
=\frac{11}{16}\frac{g_2^2}{16\pi^2}C_{LD}.
\]
This is **not** yet a complete \(C_{HL}^{(1,3)}\) matching coefficient. EOM/current projection must be applied only after all routings and the full common-basis amplitude are summed.

The previous common-numerator candidate \(+3/(4M_E^2)\) is superseded. The current exact-routing result \(11/(16M_E^2)\) differs because the four pairs have distinct shifted denominators/numerators and the \(O(\epsilon)\) angular term is retained.

## 7. Remaining acceptance gates

1. Explicitly map the second charge-conjugate/crossed tree routing in the atlas to this ordered amplitude, or evaluate it as a separate Green function. Do not insert a factor of two by assumption.
2. Validate the diagram multiplicities, orientations, and Feynman-rule signs with FeynArts/QGRAF or an independent explicit Wick-contraction derivation. The existing attachment atlas is not an exact diagram count.
3. Include LD-W-03/04 and the external \(L,H\) LSZ terms in the complete gauge Ward bookkeeping, even though their common light-only matching pieces cancel at \(O(M_E^{-2})\).
4. Combine the hard UV pole with the EFT operator counterterm and the \(C_{LD}\), \(g_2\), and field-renormalization conventions exactly once.
5. Check the one-\(W\) form factor/longitudinal Ward identity and only then apply the EOM/current projection.
6. Repeat the complete sum at common nonexceptional off-shell external momenta (or with one explicitly shared IR regulator) before promoting a finite Wilson coefficient.

The companion exact-rational script and seven regression tests verify the local scalar-master split, all four pair kernels, the weak-tensor-weighted hard/soft/full sums, the retained \(O(\epsilon)\) finite term, and the Hermiticity/combinatoric identities. These are local symbolic checks, not a diagram-package calculation.
