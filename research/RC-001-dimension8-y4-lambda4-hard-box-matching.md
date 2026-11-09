# RC-001 — Dimension-eight \(|y|^4\) and \(|\lambda|^4\) UV hard boxes

**Status (2026-11-10):** the transverse current-current projection of the one-ordered-cycle heavy/light fermion box has been evaluated by a \(d\)-dimensional hard-region expansion. Its hard IR pole and finite local term are explicitly matched to the previously computed one-Weyl EFT soft kernel. This closes the Yukawa-only transverse-current projection for \(Q_{LD}^2\) and \(Q_{RD}^2\) at the stripped one-cycle level. It is **not** a complete four-scalar amplitude or the full dimension-eight Wilson vector: independent tensor projections, the complete crossed-channel/weak-index ledger, all same-order EFT insertions, final EOM/source reduction, and diagram-package validation remain open.

## 1. Scope, conventions, and external projection

Use \(d=4-2\epsilon\), dimensional regularization, and the same \(\overline{\mathrm{MS}}\) convention as the soft calculation. Define
\[
L_E=\ln\frac{M_E^2}{\mu_R^2},\qquad
\Delta_{\mathrm{IR,UV}}=\frac1{\epsilon_{\mathrm{IR,UV}}}-\gamma_E+\ln4\pi.
\]
For one flavor, the tree-level coefficients are
\[
C_{LD,\ell}=\frac{|y_\ell|^2}{M_{E\ell}^2},\qquad
C_{RD,\ell}=\frac{|\lambda_\ell|^2}{M_{E\ell}^2}.
\]

The target is the parity-even transverse scalar-current projection. For the Higgs channel choose the complex external fields
\[
H(p_1),\quad H^\dagger(p_2),\quad H(p_3),\quad H^\dagger(p_4),
\]
with
\[
p_1=P+\frac q2,\quad p_2=-P+\frac q2,\quad
p_3=P'-\frac q2,\quad p_4=-P'-\frac q2,
\qquad P\cdot q=P'\cdot q=0.
\]
The scalar currents have matrix elements \(\mathcal J_H=-2P\) and \(\mathcal J'_H=-2P'\) in the all-incoming convention. The transverse projector is
\[
T_{\mu\nu}(q)=q^2\delta_{\mu\nu}-q_\mu q_\nu.
\]
The projection isolates \(P_\mu T^{\mu\nu}P'_\nu=q^2P\cdot P'\). The singlet \(S\) channel is identical with \(P,P'\) interpreted as the corresponding scalar-current momenta.

The ordered full-theory box has two massless chiral propagators and two heavy VLL propagators:
\[
\mathcal I_{\mathrm{UV}}^{\mathrm{ord}}=
\int_k
\frac{\mathcal N(k;p_i)}
{k^2(k+q)^2[(k+p_1)^2+M_E^2][(k-p_4)^2+M_E^2]},
\]
where \(\int_k=\mu_R^{2\epsilon}\int d^dk/(2\pi)^d\), with the Euclidean continuation understood. The parity-even Weyl numerator in NDR is
\[
\mathcal N
=\frac12\operatorname{tr}
\left[
(\slashed k+\slashed p_1)
(\slashed k+\slashed q)
(\slashed k-\slashed p_4)
\slashed k
\right].
\]
The \(\gamma_5\)-odd trace vanishes for this four-scalar projection because momentum conservation leaves at most three independent external four-vectors.

The one-cycle integral is evaluated first. The effective action has the usual \(1/2\) from the second-order current-source expansion; converting the current matrix elements from \(P,P'\) to \(\mathcal J_H,\mathcal J'_H\) supplies a further factor \(1/4\). Thus the effective-action coefficient is the one-cycle projected amplitude coefficient divided by eight. This convention is the same as the \(1/8\) factor in the previously derived EFT soft current kernel.

## 2. Hard-region expansion

In the hard region \(k\sim M_E\), expand the three shifted denominators in the external momenta through total degree four, retaining the coefficient of \(P P' q^2\). The required angular averages are
\[
\left\langle k_1^{2m}k_4^{2n}\right\rangle
=(k^2)^{m+n}
\frac{(\frac12)_m(\frac12)_n}{(\frac d2)_{m+n}},
\]
with odd powers vanishing. The remaining radial integrals reduce to
\[
I_{a b n}=
\int_k\frac{(k^2)^{n-a}}{(k^2+M_E^2)^b}
=
\frac{(M_E^2)^{d/2+n-a-b}}{(4\pi)^{d/2}}
\frac{\Gamma(d/2+n-a)\Gamma(b-d/2-n+a)}
{\Gamma(d/2)\Gamma(b)}.
\]

The exact sum of the radial terms for this transverse projection is
\[
\mathcal I_{\mathrm{hard}}^{\mathrm{ord}}\big|_{P T P'}
=
-\frac{P_\mu T^{\mu\nu}(q)P'_\nu}{24\pi^2M_E^4}
\left[
\Delta_{\mathrm{IR}}-L_E+\frac{17}{12}
\right].
\]
The \(-\Delta_{\mathrm{IR}}\) residue is an infrared pole of the hard region. It is not a UV divergence of the full renormalizable UV box.

After the determinant \(1/2\) and current normalization are included, the hard contribution to the Euclidean effective action is
\[
\boxed{
\begin{aligned}
\Gamma_{\mathrm{hard},H}^{(8),E}
={}&-\frac{1}{192\pi^2}
\sum_{\ell=\mu,\tau}\frac{|y_\ell|^4}{M_{E\ell}^4}
\int_q
\operatorname{tr}_2\!\left[
\mathcal J_{H,\mu}(q)\mathcal J_{H,\nu}(-q)
\right]T^{\mu\nu}(q)
\\[-2pt]
&\hspace{35mm}\times
\left[
\Delta_{\mathrm{IR}}-L_{E\ell}+\frac{17}{12}
\right].
\end{aligned}
}
\]
For the right-handed singlet channel,
\[
\boxed{
\begin{aligned}
\Gamma_{\mathrm{hard},S}^{(8),E}
={}&-\frac{1}{192\pi^2}
\sum_{\ell=\mu,\tau}\frac{|\lambda_\ell|^4}{M_{E\ell}^4}
\int_q
j_{S_\ell,\mu}(q)j_{S_\ell,\nu}(-q)T^{\mu\nu}(q)
\\[-2pt]
&\hspace{35mm}\times
\left[
\Delta_{\mathrm{IR}}-L_{E\ell}+\frac{17}{12}
\right].
\end{aligned}
}
\]
The left-handed result is a weak-index trace, not an extra multiplicity of two appended to a fixed external component. The right-handed loop has one Weyl singlet and no weak multiplicity. Since \(S_\tau=S^*\), \(j_{S_\tau}=-j_{S_\mu}\), but the quadratic current kernel has the same sign for both flavors.

## 3. Soft region and pole cancellation

The soft region expands the two heavy propagators in \(1/M_E\). The remaining massless Weyl current bubble is the kernel already evaluated in the tree/EFT soft audit:
\[
\Pi_{\mu\nu}^{W,E}(q)
=\frac{T_{\mu\nu}(q)}{24\pi^2}
\left[
\Delta_{\mathrm{UV}}-\ln\frac{q^2}{\mu_R^2}+\frac53
\right].
\]
The \(+5/3\) follows from
\[
\int_0^1dx\,x(1-x)=\frac16,\qquad
\int_0^1dx\,x(1-x)\ln[x(1-x)]=-\frac5{18}.
\]
With the same determinant and current normalization,
\[
\begin{aligned}
\Gamma_{\mathrm{soft},H}^{(8),E}
={}&+\frac{1}{192\pi^2}
\sum_\ell\frac{|y_\ell|^4}{M_{E\ell}^4}
\int_q\operatorname{tr}_2[
\mathcal J_{H,\mu}(q)\mathcal J_{H,\nu}(-q)]T^{\mu\nu}(q)
\\[-2pt]
&\hspace{35mm}\times
\left[
\Delta_{\mathrm{UV}}-\ln\frac{q^2}{\mu_R^2}+\frac53
\right],
\end{aligned}
\]
and
\[
\begin{aligned}
\Gamma_{\mathrm{soft},S}^{(8),E}
={}&+\frac{1}{192\pi^2}
\sum_\ell\frac{|\lambda_\ell|^4}{M_{E\ell}^4}
\int_q j_{S_\ell,\mu}(q)j_{S_\ell,\nu}(-q)T^{\mu\nu}(q)
\\[-2pt]
&\hspace{35mm}\times
\left[
\Delta_{\mathrm{UV}}-\ln\frac{q^2}{\mu_R^2}+\frac53
\right].
\end{aligned}
\]

Thus, in each flavor channel,
\[
\boxed{\operatorname{Res}_{\mathrm{IR}}\Gamma_{\mathrm{hard}}
+\operatorname{Res}_{\mathrm{UV}}\Gamma_{\mathrm{soft}}=0.}
\]
The poles are kept distinct until the method-of-regions sum is formed. The EFT local counterterm has the opposite sign to the soft UV pole; the hard-region IR pole cancels that soft pole in the full-theory expansion.

## 4. Finite hard coefficients and matched kernels

The renormalized local hard coefficients in this current Green basis are
\[
\boxed{
c_{8,H}^{\mathrm{hard}}(\mu_R)
=\frac{1}{192\pi^2}
\sum_{\ell=\mu,\tau}\frac{|y_\ell|^4}{M_{E\ell}^4}
\left[
\ln\frac{M_{E\ell}^2}{\mu_R^2}-\frac{17}{12}
\right],
}
\]
\[
\boxed{
c_{8,S}^{\mathrm{hard}}(\mu_R)
=\frac{1}{192\pi^2}
\sum_{\ell=\mu,\tau}\frac{|\lambda_\ell|^4}{M_{E\ell}^4}
\left[
\ln\frac{M_{E\ell}^2}{\mu_R^2}-\frac{17}{12}
\right].
}
\]
These multiply the momentum-space local structures \(\mathcal J_H T\mathcal J_H\) and \(j_S Tj_S\), respectively. They are finite hard matching coefficients for the transverse current projection, not yet coefficients in a fully minimized scalar-operator basis.

Adding the soft terms gives the scale-independent matched kernels
\[
\boxed{
\Gamma_{\mathrm{matched},H}^{(8),E}
=\frac{1}{192\pi^2}
\sum_\ell\frac{|y_\ell|^4}{M_{E\ell}^4}
\int_q\operatorname{tr}_2[
\mathcal J_{H,\mu}(q)\mathcal J_{H,\nu}(-q)]T^{\mu\nu}(q)
\left[\ln\frac{M_{E\ell}^2}{q^2}+\frac14\right],
}
\]
\[
\boxed{
\Gamma_{\mathrm{matched},S}^{(8),E}
=\frac{1}{192\pi^2}
\sum_\ell\frac{|\lambda_\ell|^4}{M_{E\ell}^4}
\int_q j_{S_\ell,\mu}(q)j_{S_\ell,\nu}(-q)T^{\mu\nu}(q)
\left[\ln\frac{M_{E\ell}^2}{q^2}+\frac14\right].
}
\]
The constant \(+1/4\) is the difference \(5/3-17/12\). The arbitrary matching scale cancels between the hard logarithm and the soft logarithm.

## 5. Reproducibility and acceptance boundary

The exact d-dimensional expansion, angular averages, radial Gamma integrals, soft Feynman-parameter expansion, and pole/finite-term identities are implemented in:
- calculations/RC-001-dimension8-y4-lambda4-hard-box.py
- validation/RC-001-dimension8-y4-lambda4-hard-box.txt

The six local exact checks pass. They verify the displayed stripped transverse projection and its hard/soft pole and finite-term reconciliation. They do not replace an independent diagram-generation package.

**Closed in this note:** the one-ordered-cycle transverse \(y^4\) and \(\lambda^4\) hard kernels; the opposite hard-IR/soft-UV pole residues; the finite local hard coefficient in the current Green basis; and the scale-independent hard-plus-soft transverse kernel.

**Still open:**
1. all independent external-momentum tensor projections and the full crossed-channel/weak-index amplitude ledger;
2. the additional \(O(M_E^{-4})\) soft insertions from \(Q_{LD}^{(8)},Q_{RD}^{(8)}\), \(C_5C_7^*\), VEV/wavefunction insertions, and source/current companions;
3. the common scalar/gauge EOM and integration-by-parts reduction to a nonredundant dimension-eight basis;
4. UV parameter, field, and operator counterterms in the complete amplitude set;
5. independent FeynArts/FeynCalc or equivalent diagram-level validation.

No complete dimension-eight Wilson vector is claimed by this partial hard/soft closure.
