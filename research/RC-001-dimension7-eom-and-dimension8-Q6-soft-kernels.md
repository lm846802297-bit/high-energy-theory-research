# RC-001 — Tree-level dimension-seven EOM reduction and dimension-eight Q6-squared soft bubbles

**Status:** analytic operator identities and the universal one-Weyl current-correlator kernel are derived below. The scalar-current bubble integral is reduced to its exact Feynman-parameter pole/log/constant. The overall sign and full weak-index projection in the UV-matched amplitude, and all corresponding hard-region diagrams, remain to be checked against the frozen vertex convention. This note corrects one topology entry in the earlier census: \(Q_{LD}Q_{RD}\) is not a connected one-loop pure-scalar graph in the unbroken massless EFT.

## 1. Frozen conventions and tree-level nonlocal operator

For one flavor \(\ell\),
\[
\mathcal L_{\rm int}\supset-
\left[y_\ell\bar L_\ell H E_{\ell R}
+\lambda_\ell S_\ell\bar E_{\ell L}\ell_R
+M_{E\ell}\bar E_{\ell L}E_{\ell R}\right]+\mathrm{h.c.},
\qquad S_\mu=S,\quad S_\tau=S^*,
\]
\[
C_{5,\ell}=-\frac{y_\ell\lambda_\ell}{M_{E\ell}},
\qquad
Q_{LD,\ell}=(\bar L_\ell H)i\slashed D(H^\dagger L_\ell),
\qquad
Q_{RD,\ell}=S_\ell^\dagger\bar\ell_R i\slashed D(S_\ell\ell_R).
\]
Use \(D_\mu=\partial_\mu+i g_X q X_\mu+\cdots\), \([D_\mu,D_\nu]=i g_XqF_{\mu\nu}+\cdots\), \(\sigma^{\mu\nu}=i[\gamma^\mu,\gamma^\nu]/2\), and metric \(+---\). Then
\[
(i\slashed D)^2=-D^2-\frac{g_Xq}{2}\sigma^{\mu\nu}F_{\mu\nu}+\text{other gauge factors}.
\]

The cross-chirality heavy propagator gives the nonlocal tree-level kernel
\[
\frac{M_E}{(i\slashed D)^2-M_E^2}
=-\frac1{M_E}\left[1+\frac{(i\slashed D)^2}{M_E^2}
+\frac{(i\slashed D)^4}{M_E^4}+\cdots\right].
\]
The first term reproduces the frozen \(C_5\) convention. The next term is the dimension-seven representative
\[
\mathcal O_{7,\ell}^{\rm rep}
=(\bar L_\ell H)(i\slashed D)^2(S_\ell\ell_R),
\qquad
\Delta\mathcal L^{(7)}
\supset \frac{C_{5,\ell}}{M_{E\ell}^2}\mathcal O_{7,\ell}^{\rm rep}
+\mathrm{h.c.}
\]
The coefficient relation is a tree-level propagator expansion, not yet an independent nonredundant Wilson coefficient.

## 2. Exact light-EOM reduction of the derivative square

In the unbroken matching EFT, the renormalizable charged-lepton Yukawa source is absent. Thus, at leading order in the light-field EOM,
\[
i\slashed D\,\ell_R=0,\qquad
(i\slashed D)^2\ell_R=0.
\]
The covariant product rule gives
\[
(i\slashed D)^2(S_\ell\ell_R)
=-(D^2S_\ell)\ell_R
-2(D_\mu S_\ell)D^\mu\ell_R
-\frac{g_Xq_{S_\ell}}2\sigma^{\mu\nu}F^X_{\mu\nu}S_\ell\ell_R.
\]
The last term is the field-strength contribution acting on the scalar factor; the field-strength term acting on \(\ell_R\) cancels against its squared Dirac EOM. For the charge convention \(q_S=+2\), \(q_{S_\mu}=+2\) and \(q_{S_\tau}=-2\).

Define the scalar EOM source \(\mathcal J_{S_\ell}\) by
\[
D^2S_\ell+\frac{\partial V}{\partial S_\ell^\dagger}
+\mathcal J_{S_\ell}=0.
\]
At the tree-level EFT order relevant here,
\[
\mathcal J_{S_\ell}=C_{5,\ell}^*\,\bar\ell_R H^\dagger L_\ell
\]
with the flavor-conjugate orientation understood for \(S_\tau=S^*\). For
\[
V=-\mu_H^2X-\mu_S^2Y+\lambda_HX^2+\lambda_SY^2+\lambda_{HS}XY,
\quad X=H^\dagger H,\quad Y=S^\dagger S,
\]
\[
\frac{\partial V}{\partial S_\ell^\dagger}
=S_\ell(-\mu_S^2+2\lambda_SY+\lambda_{HS}X).
\]
Consequently,
\[
\begin{aligned}
\mathcal O_{7,\ell}^{\rm rep}\doteq{}&
(\bar L_\ell H)
\left[
S_\ell(-\mu_S^2+2\lambda_SY+\lambda_{HS}X)
+C_{5,\ell}^*(\bar\ell_RH^\dagger L_\ell)
\right]\ell_R\\
&-2(\bar L_\ell H)(D_\mu S_\ell)D^\mu\ell_R
-\frac{g_Xq_{S_\ell}}2(\bar L_\ell H)
\sigma^{\mu\nu}F^X_{\mu\nu}S_\ell\ell_R ,
\end{aligned}
\]
where \(\doteq\) denotes equality modulo the leading light EOM and total derivatives. The \(C_5^*\) term is a dimension-seven four-fermion/source companion and is not optional.

An equivalent IBP representative follows from
\[
-2(\bar L H)(D_\mu S)D^\mu\ell_R
\doteq
2D_\mu(\bar L H)(D^\mu S)\ell_R
+2(\bar L H)(D^2S)\ell_R.
\]
Using the scalar EOM in the second term gives
\[
\begin{aligned}
\mathcal O_{7,\ell}^{\rm rep}\doteq{}&
-(\bar L_\ell H)
\left[
S_\ell(-\mu_S^2+2\lambda_SY+\lambda_{HS}X)
+C_{5,\ell}^*(\bar\ell_RH^\dagger L_\ell)
\right]\ell_R\\
&+2D_\mu(\bar L_\ell H)(D^\mu S_\ell)\ell_R
-\frac{g_Xq_{S_\ell}}2(\bar L_\ell H)
\sigma^{\mu\nu}F^X_{\mu\nu}S_\ell\ell_R .
\end{aligned}
\]
The two forms are equivalent; they must not be added. The derivative-current term and the Pauli/field-strength term remain in the Green basis unless a further specified basis reduction removes them. In particular, the absence of the renormalizable \(\bar L H\ell_R\) Yukawa does not make \(D_\mu(\bar L H)D^\mu S\,\ell_R\) vanish.

**Tree-level EOM conclusion:** the \(1/M_E^3\) representative is not simply zero by the massless \(\ell_R\) EOM. It generates scalar-potential/source, four-fermion/source, derivative-current, and \(F_{\mu\nu}\) companions. Therefore the conditional \(C_5C_7^*\) soft family cannot be discarded merely by saying “\(C_7\) is EOM redundant”. A complete independent operator-basis reduction must retain the displayed companion set and verify whether any linear combination is further redundant.

## 3. Dimension-six operators in current form

For the same massless leading EOM,
\[
Q_{LD,\ell}\doteq
i(\bar L_{\ell i}H_i)\gamma^\mu(D_\mu H_j^\dagger)L_{\ell j},
\qquad
Q_{RD,\ell}\doteq
iS_\ell^\dagger(D_\mu S_\ell)\bar\ell_R\gamma^\mu\ell_R.
\]
After combining each operator with its hermitian conjugate and dropping a total derivative, use the explicitly hermitian current representatives
\[
J^L_{\mu,ij}=\frac{i}{2}
\left[H_iD_\mu H_j^\dagger-(D_\mu H_i)H_j^\dagger\right],
\qquad
J^R_\mu=\frac{i}{2}
\left[S_\ell^\dagger D_\mu S_\ell-(D_\mu S_\ell^\dagger)S_\ell\right],
\]
\[
Q_{LD,\ell}\doteq J^L_{\mu,ij}\bar L_{\ell i}\gamma^\mu L_{\ell j},
\qquad
Q_{RD,\ell}\doteq J^R_\mu\bar\ell_R\gamma^\mu\ell_R.
\]
This current form is useful for the soft-loop calculation, but it does not replace the unreduced Green-basis operator when matching off-shell amplitudes.

## 4. Universal one-Weyl current bubble

Define the current correlator by
\[
i\int d^dx\,e^{iqx}
\langle0|T\,j_\mu(x)j_\nu(0)|0\rangle
=(q_\mu q_\nu-q^2g_{\mu\nu})\Pi_W(q^2).
\]
For one massless Weyl fermion, the parity-even part is one half of the Dirac result. With \(d=4-2\epsilon\) and the same \(\overline{\rm MS}\) convention,
\[
\Pi_W(q^2)=\frac{1}{24\pi^2}
\int_0^1dx\,x(1-x)
\left[
\Delta_{\rm UV}-\ln\frac{-q^2x(1-x)-i0}{\mu_R^2}
\right].
\]
The exact parameter integrals are
\[
\int_0^1dx\,x(1-x)=\frac16,\qquad
\int_0^1dx\,x(1-x)\ln[x(1-x)]=-\frac5{18},
\]
hence
\[
\boxed{
\Pi_W(q^2)=\frac{1}{24\pi^2}\frac16
\left[
\Delta_{\rm UV}-\ln\frac{-q^2-i0}{\mu_R^2}+\frac53
\right].
}
\]
Equivalently the coefficient is \(1/(144\pi^2)\) multiplying the bracket. In the \(i/(16\pi^2)\) normalization this is \(2/9\) multiplying the bracket. This normalization is for one Weyl current; it does not include the \(1/2\) from expanding the fermion determinant to second order in the background current source, nor any external Wilson coefficients.

For a coefficient \(c_L=|y_\ell|^2/M_{E\ell}^2\) or \(c_R=|\lambda_\ell|^2/M_{E\ell}^2\), the second-order effective action contains the corresponding current-current kernel multiplied by \(c_{L,R}^2/2\), with the full Wick-contraction and weak-index factors retained. The local UV pole is proportional to
\[
J_\mu(q)(q^\mu q^\nu-q^2g^{\mu\nu})J_\nu(-q),
\]
which is a dimension-eight four-scalar derivative structure. The nonlocal logarithm is part of the EFT soft amplitude and must be retained when comparing to the UV hard region.

## 5. Topology correction: the mixed \(Q_{LD}Q_{RD}\) graph is absent at this order

The unbroken-phase EFT propagators are flavor diagonal and chirality preserving:
\[
\langle L_\ell\bar L_\ell\rangle\ne0,\qquad
\langle\ell_R\bar\ell_R\rangle\ne0,\qquad
\langle L_\ell\bar\ell_R\rangle=0.
\]
A \(Q_{LD}\) insertion contains only an \(L_\ell\)-bilinear; a \(Q_{RD}\) insertion contains only an \(\ell_R\)-bilinear. Two such insertions therefore cannot be joined into one connected fermion loop. Contracting each bilinear at its own insertion gives two disconnected one-vertex tadpoles, which vanish in the massless dimensional-regularization setup and are not a connected 1PI four-scalar amplitude.

Thus the earlier SFT-06 label “\(Q_{LD}Q_{RD}\) fermion loop” is not a valid one-loop topology for the stated unbroken EFT. It must be removed from the direct one-loop soft list. A mixed contribution would require additional chirality-changing interactions or mass insertions; those alter both loop order/topology and the \(1/M_E\) power counting and must be separately enumerated. The valid direct one-loop Q6-squared soft families are \(Q_{LD}Q_{LD}\) and \(Q_{RD}Q_{RD}\).

## 6. What is and is not closed

**Derived here:** the product-rule identity for the dimension-seven representative; its leading scalar-EOM/source, derivative-current and field-strength companions; the hermitian current forms of \(Q_{LD}\) and \(Q_{RD}\); the one-Weyl current-correlator pole/log/finite parameter integral; and the absence of a connected \(Q_{LD}Q_{RD}\) one-loop graph in the unbroken massless EFT.

**Still required before declaring Phase A closed:** verify the overall sign and flavor-conjugation conventions directly from the full tree-level Schur complement for both \(\ell=\mu,\tau\); include the complete gauge-group field-strength sum and all light-field EOM sources in the same UV/EFT convention; perform a nonredundant dimension-seven basis reduction with the declared operator basis and record any remaining independent derivative operator. The displayed identity is an EOM-complete intermediate reduction, not a proof that the final dimension-seven basis has been minimized.

**Still required before declaring the soft matching closed:** insert the exact current kernel into the \(J^L_{ij}J^L_{ji}\) and \(J^R_\mu J_R^\mu\) amplitudes with the correct determinant factor, SU(2) contractions, flavor sum, and momentum routing; then compute the corresponding UV hard regions and counterterms. No hard Wilson coefficient is claimed in this note.
