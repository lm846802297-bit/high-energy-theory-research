# RC-001 — QLD UV one-background triangle: exact integrands and Ward ledger

**Status (2026-11-10):** the two full-theory one-loop attachment classes are fixed at the integrand level for the parity-even chiral sector. Their exact four-gamma numerators and the charge-resolved Ward relation are recorded below. The hard expansion through \(M_E^{-4}\), the EFT soft sum, and the matched coefficient are not yet evaluated.

## 1. Frozen interaction and charges

Use
\[
\mathcal L_Y=-y_\ell\bar L_\ell H E_{\ell R}
-y_\ell^*\bar E_{\ell R}H^\dagger L_\ell
-M_E\bar E_\ell E_\ell.
\]
The gauge charges obey
\[
-q_L+q_H+q_E=0,\qquad q_E=q_L-q_H.
\]
The external composite source is \(\Psi_L=H^\dagger L_\ell\), so \(q_{\Psi_L}=q_E\).

For the three gauge sectors:
\[
\begin{array}{c|ccc}
 &q_L&q_H&q_E\\\hline
U(1)_Y&-\frac12&+\frac12&-1\\
U(1)_X&\eta_\ell Q_\ell&0&\eta_\ell Q_\ell\\
SU(2)_L&T^a& T^a&0
\end{array}
\]
The weak generators act on the doublet indices; \(E\) is a weak singlet.

## 2. Momentum routing

Take all external momenta incoming at the vertices, with the background momentum \(q=p'-p\). Choose the light-fermion loop momentum \(k\). Define
\[
K=k+p,\qquad K'=k+p',\qquad k'=k+q.
\]
The two attachment classes have denominators
\[
D_L=k^2(k+q)^2(K^2+M_E^2),
\]
\[
D_E=k^2(K^2+M_E^2)(K'^2+M_E^2).
\]
These are Euclidean denominators. Overall factors of \(i\), the closed-loop minus sign, and the common coupling factor are to be restored consistently when converting the Euclidean integrals to 1PI vertices.

## 3. Exact parity-even chiral numerators

At each Yukawa endpoint the heavy propagator is projected onto its right-handed component, so a single heavy propagator between the two Yukawa endpoints has no mass numerator:
\[
P_R(\slashed K+M_E)P_L=\slashed K P_L,
\]
with the conjugate identity for the opposite orientation. For the parity-even part, the remaining chiral trace is one half of the corresponding four-component trace.

With the ordered routing above, define
\[
N_L^\mu=\frac12\operatorname{tr}
[\slashed K\,\slashed{k'}\,\gamma^\mu\slashed k],
\qquad
N_E^\mu=\frac12\operatorname{tr}
[(\slashed K'+M_E)\gamma^\mu(\slashed K+M_E)\slashed k]_{\rm even}.
\]
Using \(\frac12\operatorname{tr}(\slashed a\slashed b\slashed c\slashed d)
=2[(a\cdot b)(c\cdot d)-(a\cdot c)(b\cdot d)+(a\cdot d)(b\cdot c)]\), these become
\[
N_L^\mu=2\left[
(K\cdot k')k^\mu-(k'\cdot k)K^\mu
+(K\cdot k)k'^\mu
\right],
\]
\[
N_E^\mu=2\left[
(K\cdot k)K'^\mu-(K'\cdot K)k^\mu
+(K'\cdot k)K^\mu+M_E^2 k^\mu
\right].
\]
**Caution:** for the heavy-attachment graph the two heavy propagators are separated by a vector vertex. The (M_E^2 k^mu) term in the trace is therefore retained; dropping it would invalidate the heavy-line Ward contraction. The relative overall sign between the two attachment classes still has to be fixed from one explicit fermion-flow convention. The trace definitions above are the numerator starting point, not yet an accepted integrated result.

The UV amplitude has the structural form
\[
\Gamma^\mu_{\rm UV}
\propto g_A|y_\ell|^2
\left[
q_L\int_k\frac{N_L^\mu}{D_L}
+q_E\int_k\frac{N_E^\mu}{D_E}
\right],
\]
where \(q_L,q_E\) are replaced by the appropriate representation generators for \(B_\mu,A'_\mu,W_\mu^a\). The overall relative sign is fixed by a common fermion-flow convention and must be checked together with the Ward contraction; it is not inferred from the denominator list alone.

## 4. Ward contraction and charge relation

For a fermion line,
\[
q_\mu\gamma^\mu=S_0^{-1}(k+q)-S_0^{-1}(k).
\]
Contracting the light-line attachment therefore collapses one of its two light propagators and produces the difference of the two heavy-light scalar two-point integrands with the external scalar momentum routed at \(p'\) and \(p\). Contracting the heavy-line attachment similarly collapses one heavy propagator and produces the corresponding difference with the heavy charge \(q_E\).

The sum must obey the scalar-source Ward identity
\[
q_\mu\Gamma^\mu_{A H^\dagger H}(p',p)
=g_Aq_H\left[
\Gamma_{H^\dagger H}(p')-\Gamma_{H^\dagger H}(p)
\right],
\]
up to the declared all-incoming \(i\)-convention. Equivalently, the constituent charge coefficients must combine using
\[
q_E-q_L=-q_H.
\]
This relation is a stringent sign/routing test. For \(U(1)_X\), \(q_H=0\), so the light- and heavy-line longitudinal pieces must cancel. For hypercharge and \(SU(2)_L\), the remainder is precisely the scalar-leg transformation term.

## 5. Hard-region expansion target

For \(k\sim M_E\), expand
\[
\frac1{(k+p)^2+M_E^2}
=\frac1{k^2+M_E^2}
\sum_{n\ge0}
\left[-\frac{2k\cdot p+p^2}{k^2+M_E^2}\right]^n,
\]
and analogously for \(p'\). Retain total external-momentum degree five in the sum of the two attachment classes; this is the \(M_E^{-4}\) contribution to the dimension-eight one-background form factor. Keep the \(d\)-dimensional tensor averages until after the radial integrals, since \(O(\epsilon)\) angular terms can multiply UV poles.

The light-attachment graph also has a soft region \(k\sim p,q\), in which the heavy propagator is expanded in \(1/M_E\). Its soft terms must be compared with the ordinary light-line insertion and all ordered covariant-derivative contact vertices generated by \(Q_{LD}^{(8)}\). The heavy-attachment graph has no massless two-propagator bubble, but its soft expansion still contributes local/source terms and must not be discarded by topology alone.

## 6. Acceptance conditions

The QLD one-background matching is accepted only after:
1. the relative sign and exact chiral numerator of both attachments are fixed from one fermion-flow convention;
2. the complete \(d\)-dimensional hard expansion through degree five is integrated;
3. the soft expansion is calculated with the same routing and subtraction scheme;
4. the complete EFT ordinary-line, Q8 contact, and scalar-source terms are summed;
5. the charge-resolved Ward identity is satisfied before and after pole extraction;
6. hard IR poles cancel soft UV poles and the remaining local coefficient is independent of the arbitrary matching scale.

No hard coefficient or complete QLD dimension-eight Wilson coefficient is claimed in this record.
