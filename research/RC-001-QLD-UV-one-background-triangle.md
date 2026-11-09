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

Use a consistent mixed incoming/outgoing convention: scalar momentum \(p\) enters the first Yukawa vertex, scalar momentum \(p'\) leaves the second, and background momentum \(q\) leaves the fermion loop. Momentum conservation gives \(q=p-p'\). Choose the light-fermion loop momentum \(k\). Define
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

## 2A. Metric convention: keep Minkowski Ward algebra separate from Euclidean hard integrals

The routing/numerator identities in §§2–4 are first defined in Minkowski signature \((+---)\), where the heavy inverse propagator is \(K^2-M_E^2\). Since \(q=K-K'\), the Ward contraction in the heavy attachment is
\[
q_\mu N_E^\mu=
2\left[(K'\cdot k)(K^2-M_E^2)
-(K\cdot k)(K'^2-M_E^2)\right].
\]
The Euclidean hard-region integrals are obtained only after Wick rotation, with
\[
K_M^2-M_E^2\longrightarrow -(K_E^2+M_E^2),
\qquad k_M^2\longrightarrow-k_E^2,
\]
and corresponding factors of \(i\) in slash numerators and loop measures. The denominator symbols \(D_L,D_E\) in §2 are therefore Euclidean denominators; they must not be inserted directly into the Minkowski Ward identities of §4.

For clarity, the Euclidean hard expansion is
\[
\frac1{(k_E+p_E)^2+M_E^2}
=\frac1{k_E^2+M_E^2}
\sum_{n=0}^\infty
\left[-\frac{2k_E\cdot p_E+p_E^2}
{k_E^2+M_E^2}\right]^n.
\]
The previous shorthand mixed the Minkowski Ward denominators \(K^2-M_E^2\) with Euclidean denominators \(K_E^2+M_E^2\) without displaying the Wick rotation. This subsection fixes that convention. All subsequent tensor integration must be done wholly in Euclidean signature, and the Ward identity checked before Wick rotation in Minkowski signature (or after a fully consistent Euclidean continuation), never by mixing the two.

## 3. Exact parity-even chiral numerators

At each Yukawa endpoint the heavy propagator is projected onto its right-handed component, so a single heavy propagator between the two Yukawa endpoints has no mass numerator:
\[
P_R(\slashed K+M_E)P_L=\slashed K P_L,
\]
with the conjugate identity for the opposite orientation. For the parity-even part, the remaining chiral trace is one half of the corresponding four-component trace.

With the ordered routing above, \(k'=k+q\) and \(K=k+p=k'+p'\). For the heavy attachment \(K'=k+p'=K-q\), so \(q=K-K'\). Define
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
q_\mu\gamma^\mu=S_0^{-1}(k+q)-S_0^{-1}(k),\qquad q=k'-k=K-K'.
\]
Contracting the light-line attachment therefore collapses one of its two light propagators and produces the difference of the two heavy-light scalar two-point integrands with the external scalar momentum routed at \(p'\) and \(p\). Contracting the heavy-line attachment similarly collapses one heavy propagator and produces the corresponding difference with the heavy charge \(q_E\).

With the common fermion-flow convention, the two attachment classes enter with the same relative sign in the trace convention of §3: their longitudinal contractions are opposite for equal constituent charges. The sum must obey the scalar-source Ward identity
\[
q_\mu\Gamma^\mu_{A H^\dagger H}(p',p)
=g_Aq_H\left[
\Gamma_{H^\dagger H}(p')-\Gamma_{H^\dagger H}(p)
\right],
\]
with the outgoing-\(q\) convention above. Equivalently, the constituent charge coefficients combine using \(q_L-q_E=q_H\), which follows from \(-q_L+q_H+q_E=0\). This is a stringent sign/routing test. For \(U(1)_X\), \(q_H=0\) and \(q_L=q_E\), so the light- and heavy-line longitudinal pieces cancel. For hypercharge and \(SU(2)_L\), the remainder is precisely the scalar-leg transformation term.

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

## 5A. Mandatory correction to the hard-region expansion

The expansion written in §5 is incomplete if read as expanding only the heavy propagators. In the hard region \(k\sim M_E\), **every propagator carrying a shifted momentum must be expanded**, including the massless light propagator \((k+q)^{-2}\) in the light-attachment graph. The correct Euclidean expansions are
\[
\frac1{(k+q)^2}
=\frac1{k^2}\sum_{n=0}^\infty
\left[-\frac{2k\cdot q+q^2}{k^2}\right]^n,
\]
\[
\frac1{(k+p)^2+M_E^2}
=\frac1{k^2+M_E^2}\sum_{n=0}^\infty
\left[-\frac{2k\cdot p+p^2}{k^2+M_E^2}\right]^n,
\]
and similarly for \(p'\). The numerator must also be expanded by its explicit polynomial dependence on \(p,p',q\), with \(q=p-p'\) imposed only after the expansion.

Both trace numerators are polynomials of external-momentum degree at most two (the heavy numerator also contains the mass term \(M_E^2 k^\mu\), of external degree zero). Explicitly, with \(k^2\equiv k_E^2\),
\[
N_L^\mu=2\left[
(k^2+2k\cdot p+p\cdot q)k^\mu
-(k^2+k\cdot q)p^\mu
+(k^2+k\cdot p)q^\mu
\right],
\]
\[
N_E^\mu=2\left[
(k^2+M_E^2-p\cdot p')k^\mu
+(k^2+k\cdot p')p^\mu
+(k^2+k\cdot p)p'^\mu
\right].
\]
The degree-five coefficient therefore comes from degree-five denominator-series terms multiplied by the degree-zero numerator, degree-four denominator terms multiplied by degree-one numerator terms, and so on through degree-three denominator terms multiplied by the degree-two numerator. For the heavy graph the \(M_E^2 k^\mu\) contribution is tracked separately because its radial master has a different power of \(M_E\). The coefficient of total external degree five must be assembled from **all** partitions of degree five between numerator, light denominator (where present), and both heavy denominators. Expanding only the heavy denominators misses terms and cannot yield the complete hard coefficient.

A reproducible expansion generator should represent the external momenta as formal commuting vectors, generate the series to total degree five, reduce tensor integrals using \(d\)-dimensional rotational invariance, and only then perform the radial integrals. In particular, do not impose \(q=p'-p\) before generating the series, because it obscures the independent Taylor coefficients needed to identify the local operator basis.

## 5B. Euclidean hard-region master integrals

After expanding all shifted propagators, every tensor integral is reduced to rotationally invariant scalar masters. For an even-rank tensor,
\[
\int_k k^{\mu_1}\cdots k^{\mu_{2n}} f(k^2)
=\frac{\mathcal S^{\mu_1\cdots\mu_{2n}}}
{d(d+2)\cdots(d+2n-2)}
\int_k (k^2)^n f(k^2),
\]
where \(\mathcal S\) is the sum over all \((2n-1)!!\) metric pairings. Odd-rank tensors vanish.

A convenient radial master, with \(\int_k\equiv\mu^{2\epsilon}\int d^dk_E/(2\pi)^d\), is
\[
J_{a b}^{(t)}
=\int_k\frac{(k_E^2)^t}
{(k_E^2)^a(k_E^2+M_E^2)^b}
=\frac{\mu^{2\epsilon}}{(4\pi)^{d/2}}
(M_E^2)^{d/2+t-a-b}
\frac{\Gamma(d/2+t-a)\Gamma(a+b-d/2-t)}
{\Gamma(d/2)\Gamma(b)}.
\]
The formula is understood by analytic continuation in dimensional regularization. It keeps UV and IR singularities visible as separate Gamma-function singularities when a given expanded term has both. It must not be replaced by a four-dimensional cutoff integral.

For the two attachment classes, the denominator-series terms reduce to this master with:
- light attachment: \(a=2+n_L\), \(b=1+n_E\);
- heavy attachment: \(a=1\), \(b=2+n_{E1}+n_{E2}\);
where the nonnegative expansion indices are further constrained by total external degree five, including the explicit numerator degree. The heavy-line \(M_E^2 k^\mu\) term and the cubic trace term must be expanded separately before applying the tensor reduction.

This gives a reproducible route to the hard coefficient, but the finite sums over Taylor partitions and the final \(1/\epsilon\) and finite terms have not yet been evaluated. In particular, a Gamma-function pole in an individual hard Taylor term is not by itself the matched UV pole: it must be combined with the EFT soft region in the same subtraction convention.

## 5C. Superseded first Taylor-count attempt

The earlier 28/20/20 count treated the scalar coefficient degree as the full vector-amplitude degree and therefore selected degree five before accounting for the explicit external Lorentz vector. It also did not provide the claimed dedicated generator on the PR head. **Those counts are superseded and must not be used for matching.**

For a decomposition \(\Gamma^\mu=p^\mu F_p+q^\mu F_q\), a total degree-five vector amplitude requires degree-four scalar form factors. The corrected generator and radial reduction are in calculations/RC-001-QLD-hard-expansion-numerator-audit.py.

## 5D. Corrected degree-five vector amplitude: d-dimensional radial reduction

The corrected extraction uses scalar form-factor degree four, so that the explicit vector supplies the fifth external momentum. All shifted propagators are expanded. The radial denominator indices are assigned separately:
\[
L\text{-attachment}:\quad a=2+n_q,\quad b=1+n_p,
\]
\[
E\text{-attachment}:\quad a=1,\quad b=2+n_p+n_{p'}.
\]
In particular, the light-graph \(p\)-shift increases the massive denominator power \(b\), not the massless power \(a\). This is essential.

After exact \(d\)-dimensional angular averaging, the surviving form-factor structures are:
\[
L:\quad F_p^L=\sum_{12\ {\rm terms}}c^L_{p;abt}J_{ab}^{(t)},\qquad
F_q^L=\sum_{12\ {\rm terms}}c^L_{q;abt}J_{ab}^{(t)},
\]
\[
E:\quad F_p^E=\sum_{3\ {\rm terms}}c^E_{p;abt}J_{ab}^{(t)},\qquad
F_{p'}^E=\sum_{3\ {\rm terms}}c^E_{p';abt}J_{ab}^{(t)}.
\]
The \(k^\mu\) numerator components vanish in this degree-four scalar projection by odd-rank rotational invariance. The complete radial-master inventory is
\[
\begin{split}
&(1,4,1),(1,5,2),(1,6,3),\\
&(2,3,1),(2,4,2),(2,5,3),\\
&(3,2,1),(3,3,2),(3,4,3),\\
&(4,1,1),(4,2,2),(4,3,3),\\
&(5,1,2),(5,2,3),(6,1,3).
\end{split}
\]
Here each tuple is \((a,b,t)\) in \(J_{ab}^{(t)}\).

For the Euclidean master
\[
J_{ab}^{(t)}=\mu^{2\epsilon}\int\frac{d^{4-2\epsilon}k}{(2\pi)^{4-2\epsilon}}
\frac{(k^2)^t}{(k^2)^a(k^2+M_E^2)^b},
\]
define
\[
L_M=\ln\frac{\mu^2}{M_E^2}+\ln(4\pi)-\gamma_E.
\]
All 15 masters are UV convergent in this hard-region coefficient. Six have an IR pole:
\[
\begin{array}{c|c}
(a,b,t)&J_{ab}^{(t)}\\\hline
(3,2,1)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(4,1,1)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right)\\
(4,2,2)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(5,1,2)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right)\\
(5,2,3)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(6,1,3)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right).
\end{array}
\]
The remaining nine masters are finite:
\[
\begin{array}{c|c@{\qquad}c|c}
(a,b,t)&J_{ab}^{(t)}&(a,b,t)&J_{ab}^{(t)}\\\hline
(1,4,1)&\frac1{96\pi^2M_E^4}&(1,5,2)&\frac1{192\pi^2M_E^4}\\
(1,6,3)&\frac1{320\pi^2M_E^4}&(2,3,1)&\frac1{32\pi^2M_E^4}\\
(2,4,2)&\frac1{96\pi^2M_E^4}&(2,5,3)&\frac1{192\pi^2M_E^4}\\
(3,3,2)&\frac1{32\pi^2M_E^4}&(3,4,3)&\frac1{96\pi^2M_E^4}\\
(4,3,3)&\frac1{32\pi^2M_E^4}&&
\end{array}
\]

Summing the radial masters gives the following Euclidean hard-region form factors in the trace/routing convention of §3, **before** inserting \(g_A|y_\ell|^2\), representation charges, the closed-loop sign, and the still-to-be-fixed relative sign of the two attachment classes. Write \(P=p^2\), \(Q=q^2\), \(R=p\cdot q\), \(P'=p'^2\), and \(T=p\cdot p'\). For the light attachment:
\[
F_p^L\big|_{\rm hard}=
\frac{Q(P-R)}{32\pi^2M_E^4\epsilon_{\rm IR}}
+\frac{6L_M Q(P-R)-2P^2+4PR+13PQ-4R^2-11RQ+2Q^2}
{192\pi^2M_E^4},
\]
\[
F_q^L\big|_{\rm hard}=
-\frac{3PR+PQ-4R^2}{96\pi^2M_E^4\epsilon_{\rm IR}}
+\frac{-18L_MPR-6L_MPQ+24L_MR^2+18P^2-87PR+PQ+92R^2-36RQ+6Q^2}
{576\pi^2M_E^4}.
\]
For the heavy attachment:
\[
F_p^E\big|_{\rm hard}=
\frac{3P^2+16PP'+3PT+18P'^2-12P'T+2T^2}
{2880\pi^2M_E^4},
\]
\[
F_{p'}^E\big|_{\rm hard}=
\frac{18P^2+16PP'-12PT+3P'^2+3P'T+2T^2}
{2880\pi^2M_E^4}.
\]
The poles shown here are **infrared poles of the hard region**, not UV counterterm poles. They must cancel the corresponding UV poles from the EFT soft region. The heavy-attachment hard contribution is finite in this projection.

These results are an evaluated hard-region subgraph decomposition, not yet the complete UV amplitude: the common Wick/Feynman-rule phase, relative attachment sign, charge-weighted sum, \(q=p'-p\) reduction, EFT soft graphs, and final matching remain to be completed.

## 6. Acceptance conditions

The QLD one-background matching is accepted only after:
1. the relative sign and exact chiral numerator of both attachments are fixed from one fermion-flow convention;
2. the complete \(d\)-dimensional hard expansion through degree five is integrated;
3. the soft expansion is calculated with the same routing and subtraction scheme;
4. the complete EFT ordinary-line, Q8 contact, and scalar-source terms are summed;
5. the charge-resolved Ward identity is satisfied before and after pole extraction;
6. hard IR poles cancel soft UV poles and the remaining local coefficient is independent of the arbitrary matching scale.

No hard coefficient or complete QLD dimension-eight Wilson coefficient is claimed in this record.
