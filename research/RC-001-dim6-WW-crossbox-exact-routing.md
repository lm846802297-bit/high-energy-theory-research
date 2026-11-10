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

These identities settle the operator-level relation between the two charge-conjugate tree orientations. The conjugate orientation matches \(Q_{LD}^\dagger\), which is the same integrated action operator as \(Q_{LD}\) modulo the displayed total derivative. Since the coefficient is proportional to \(|y_\ell|^2\) and the pure-\(WW\) hard sub-block is real, the conjugate orientation fixes the same Wilson coefficient; it is **not** an additional factor of two. The \(1/2!\) in the second-order expansion is already canceled by the two dummy vertex-label orderings. This resolves the operator-level multiplicity, but not the exact graph-label census or every Feynman-rule sign; those remain subject to diagram-level validation.

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
A_{05}=2\left(1-\frac1d\right)J-\frac2dK,\qquad
A_{06}=-J+\frac2dK.
}
\]
The reduction uses
\[
J=\int_k\frac1{(k^2)^2(k^2-M_E^2)},\qquad
K=\int_k\frac1{k^2(k^2-M_E^2)^2}.
\]
In particular, \(A_{02}=A_{06}\) at the retained order: for LD-W-06,
\[
-(2P-k)\cdot k=k^2-2k\cdot P=(k-P)^2+O(P^2),
\]
so the scalar numerator cancels the \((k-P)^2\) propagator denominator and leaves the same vector integral as LD-W-02.

For LD-W-05, define \(F(x)=1/[x(x-M_E^2)]\). The numerator chain reduces to
\[
\frac{(2P-k)^\mu}{k^2}F((k-P)^2).
\]
Expanding \((k-P)^2=k^2-2k\cdot P+O(P^2)\), the coefficient of \(\slashed P\) is
\[
2J+\frac2d\int_k F'(k^2).
\]
Since
\[
F'(x)=-\frac1{x^2(x-M_E^2)}
-\frac1{x(x-M_E^2)^2},
\]
this gives \(A_{05}=2J-2(J+K)/d\). The companion exact-rational script performs this vector-tensor reduction before inserting the scalar master values; it does not assume a common numerator.

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

The exact weighted sum simplifies before integration:
\[
\frac14(-A_{01}+A_{02}+A_{05}-A_{06})
=\frac{d-1}{2d}(J-K).
\]
This is a useful check: the two equal kernels \(A_{02}\) and \(A_{06}\) cancel in the triplet projection, while the \(A_{01}\) and \(A_{05}\) terms combine into \(J-K\).

### Longitudinal \(R_\zeta\)-propagator check

The same four numerator chains can be contracted with the longitudinal projector in
\[
D_{\mu\nu}^{ab}(k)=\frac{-i\delta^{ab}}{k^2+i0}
\left[g_{\mu\nu}-(1-\zeta)\frac{k_\mu k_\nu}{k^2+i0}\right].
\]
Denote the coefficient obtained with \(k_\mu k_\nu/k^2\) by \(A_i^{(L)}\). Direct contraction gives
\[
\boxed{
A_{01}^{(L)}=-\frac2dK,\qquad
A_{02}^{(L)}=-J+\frac2dK,
}
\]
\[
\boxed{
A_{05}^{(L)}=-\frac2dK,\qquad
A_{06}^{(L)}=-J+\frac2dK.
}
\]
For LD-W-01, \(k_\mu\gamma^\mu(-\slashed k)=-k^2\); the two adjacent \((k-P)\)-slash factors then cancel the corresponding denominator. For LD-W-02 and LD-W-06, the longitudinal contraction reproduces the same numerator as the Feynman-gauge contraction. For LD-W-05, the contraction gives
\[
\frac{(2k\cdot P-k^2)\slashed k}{k^2}
\frac{1}{k^2(k-P)^2[(k-P)^2-M_E^2]},
\]
whose local \(\slashed P\) coefficient is \(-2K/d\).

The weak-triplet weighted longitudinal sum therefore vanishes identically:
\[
\boxed{
\frac14\left[-A_{01}^{(L)}+A_{02}^{(L)}
+A_{05}^{(L)}-A_{06}^{(L)}\right]=0.
}
\]
Thus this fixed-routing \(WW\) cross-box triplet sub-block is independent of \(\zeta\). This is a nontrivial gauge-parameter check of the four cross-box diagrams. It is **not** the complete Slavnov–Taylor identity for the full four-point/current amplitude: the same-vertex, external-field, gauge-sector, and one-\(W\) form-factor sectors remain outside this sub-block.

Using the scalar masters gives
\[
(J-K)_{\rm hard}
=\frac{\Delta_{\rm UV}+2-L}{M_E^2},\qquad
(J-K)_{\rm soft}
=\frac{-\Delta_{\rm UV}+\Delta_{\rm IR}}{M_E^2},
\]
\[
(J-K)_{\rm full}
=\frac{\Delta_{\rm IR}+2-L}{M_E^2}.
\]
Therefore
\[
A_{WW}^{\rm hard}
=\frac{d-1}{2d}\frac{\Delta_{\rm UV}+2-L}{M_E^2},
\qquad
A_{WW}^{\rm soft}
=\frac{d-1}{2d}\frac{-\Delta_{\rm UV}+\Delta_{\rm IR}}{M_E^2}.
\]
Expanding \(d=4-2\epsilon\) and retaining the \(O(\epsilon)\) coefficient multiplying the pole,
\[
\frac{d-1}{2d}
=\frac38-\frac{\epsilon}{16}+O(\epsilon^2),
\]
yields
\[
\boxed{
A_{WW}^{\rm hard}
=\frac1{M_E^2}\left(
\frac38\Delta_{\rm UV}-\frac38L+\frac{11}{16}
\right).
}
\]
An independent direct evaluation of the combined full integral is also available. The weighted integrand is
\[
-\frac{d-1}{2d}\frac{M_E^2}{(k^2)^2(k^2-M_E^2)^2}.
\]
Using the standard two-denominator gamma-function formula with the same pole normalization,
\[
-M_E^2\int_k\frac1{(k^2)^2(k^2-M_E^2)^2}
=-\frac1{M_E^2}
\left(\frac{4\pi\mu_R^2}{M_E^2}\right)^\epsilon
\frac{\Gamma(2+\epsilon)\Gamma(-\epsilon)}
{\Gamma(2-\epsilon)}.
\]
Its expansion is
\[
\frac1{M_E^2}\left(
\Delta_{\rm IR}+2-L+O(\epsilon)
\right),
\]
which independently reproduces \((J-K)_{\rm full}\) and, after multiplication by \((d-1)/(2d)\), the full finite \(11/16\). This gamma-function check is independent of the separate \(J\) and \(K\) master decomposition, though it uses the same stated \(\overline{\rm MS}\) pole convention.

At the master-integral level the soft term is
\[
\boxed{
A_{WW}^{\rm soft}
=\frac1{M_E^2}\frac38(-\Delta_{\rm UV}+\Delta_{\rm IR}),
}
\]
and the un-subtracted full master sum is
\[
\boxed{
A_{WW}^{\rm full}
=\frac1{M_E^2}\left(
\frac38\Delta_{\rm IR}-\frac38L+\frac{11}{16}
\right).
}
\]
The hard UV pole cancels the soft/EFT UV pole in the matching difference, leaving the common IR pole. This is a scalar-master expansion-by-regions check, not yet a complete nonexceptional off-shell UV-minus-EFT Green-function calculation.

### \(O(\epsilon)\) finite term

The finite \(11/16\) has a different decomposition from the earlier draft. At \(d=4\), the \(J-K\) combination gives the finite constant \(3/4\), because \(J_{\rm hard}\) contributes \(+1\) and \(-K_{\rm hard}\) contributes another \(+1\). The dimensional prefactor contributes
\[
-\frac{\epsilon}{16}\Delta_{\rm UV}\longrightarrow-\frac1{16}.
\]
Consequently,
\[
\frac34-\frac1{16}=\frac{11}{16}.
\]
The previous per-pair expressions \(A_{05}=(1+2/d)J\) and \(A_{06}=-4J/d\), and the associated \(+3/16\) explanation, are superseded. Although they happened to reproduce the same final weighted finite number, they did not represent the individual numerator reductions correctly.

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

1. The operator-level charge-conjugate orientation is mapped by Hermitian conjugation and IBP to the same action operator; no extra factor of two is allowed. Reconcile the diagram generator's labeled orientations against this operator-level identity and verify that no topologically distinct contraction is omitted.
2. Validate the diagram multiplicities, orientations, and Feynman-rule signs with FeynArts/QGRAF or an independent explicit Wick-contraction derivation. The existing attachment atlas is not an exact diagram count.
3. Include LD-W-03/04 and the external \(L,H\) LSZ terms in the complete gauge Ward bookkeeping, even though their common light-only matching pieces cancel at \(O(M_E^{-2})\).
4. Combine the hard UV pole with the EFT operator counterterm and the \(C_{LD}\), \(g_2\), and field-renormalization conventions exactly once.
5. Check the one-\(W\) form factor/longitudinal Ward identity and only then apply the EOM/current projection.
6. Repeat the complete sum at common nonexceptional off-shell external momenta (or with one explicitly shared IR regulator) before promoting a finite Wilson coefficient.

The companion exact-rational script and seven regression tests verify the local scalar-master split, all four pair kernels, the weak-tensor-weighted hard/soft/full sums, the retained \(O(\epsilon)\) finite term, and the Hermiticity/combinatoric identities. These are local symbolic checks, not a diagram-package calculation.
