# RC-001 — QLD UV one-background triangle: exact integrands and Ward ledger

**Status (2026-11-10):** the two full-theory attachment classes, their routing, parity-even numerators, and relative sign are fixed at the integrand/Ward level. The complete degree-five Euclidean hard-region subgraph reduction through \(M_E^{-4}\) is evaluated. The corrected ordinary light-line EFT soft UV poles cancel both hard IR poles exactly in the \(p^\mu\) and \(q^\mu\) form factors. The \(Q_{LD}^{(8)}\) covariant one-background contact vertex and its Ward identity are recorded below. Overall Wick/Feynman-rule factors, the charge-weighted full amplitude, finite hard/soft comparison in a common basis, and final Wilson-coefficient projection remain open.

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
**Caution:** for the heavy-attachment graph the two heavy propagators are separated by a vector vertex. The \(M_E^2 k^\mu\) term in the trace is therefore retained; dropping it would invalidate the heavy-line Ward contraction. With the momentum routing and common fermion flow fixed in §2, the Ward contractions below select the same relative sign for the two attachment classes. The trace definitions above are the numerator starting point, not yet an accepted integrated result.

The UV amplitude has the structural form
\[
\Gamma^\mu_{\rm UV}
\propto g_A|y_\ell|^2
\left[
q_L\int_k\frac{N_L^\mu}{D_L}
+q_E\int_k\frac{N_E^\mu}{D_E}
\right],
\]
where \(q_L,q_E\) are replaced by the appropriate representation generators for \(B_\mu,A'_\mu,W_\mu^a\). The same relative sign is fixed by the common fermion-flow convention and checked by the charge-resolved Ward contraction in §4.

## 4. Ward contraction and charge relation

For a fermion line,
\[
q_\mu\gamma^\mu=S_0^{-1}(k+q)-S_0^{-1}(k),\qquad q=k'-k=K-K'.
\]
Contracting the light-line attachment therefore collapses one of its two light propagators and produces the difference of the two heavy-light scalar two-point integrands with the external scalar momentum routed at \(p'\) and \(p\). Contracting the heavy-line attachment similarly collapses one heavy propagator and produces the corresponding difference with the heavy charge \(q_E\).

With \(\Sigma(p)\equiv\int_k (K\cdot k)/[k^2(K^2-M_E^2)]\), the adjacent-propagator reductions give
\[
q_\mu I_L^\mu=2[\Sigma(p)-\Sigma(p')],\qquad
q_\mu I_E^\mu=2[\Sigma(p')-\Sigma(p)].
\]
Thus the plus sign between the two attachment classes in the trace convention of §3 is fixed: the charge-weighted sum is proportional to
\[
(q_L-q_E)[\Sigma(p)-\Sigma(p')]
=q_H[\Sigma(p)-\Sigma(p')].
\]
This matches the scalar-source Ward identity for the stated outgoing-\(q\) convention.

With the common fermion-flow convention, the two attachment classes enter with the same relative sign in the trace convention of §3: their longitudinal contractions are opposite for equal constituent charges. The sum must obey the scalar-source Ward identity
\[
q_\mu\Gamma^\mu_{A H^\dagger H}(p,p')
=g_Aq_H\left[
\Gamma_{H^\dagger H}(p)-\Gamma_{H^\dagger H}(p')
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

The light-attachment graph also has a soft region \(k\sim p,q\), in which the heavy propagator is expanded in \(1/M_E\). Its soft terms must be compared with the ordinary light-line insertion and all ordered covariant-derivative contact vertices generated by \(Q_{LD}^{(8)}\). The heavy-attachment graph has no massless two-propagator bubble. At this order its soft expansion contains only one massless denominator; in the unbroken massless dimensional-regularization setup it is scaleless. This is established by the explicit expansion, not by topology alone. If light masses, VEVs, or another IR scale are retained, this conclusion must be revisited.

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
N_{E,\mathrm{Euclidean}}^\mu=2\left[
(k^2-M_E^2-p\cdot p')k^\mu
+(k^2+k\cdot p')p^\mu
+(k^2+k\cdot p)p'^\mu
\right].
\]
The Lorentz vector itself carries one external momentum after tensor reduction. Therefore the degree-five vector amplitude requires degree-four scalar form factors. For explicit external-vector components, the contributions come from degree-four denominator-series terms times degree-zero numerator coefficients, degree-three denominator terms times degree-one numerator coefficients, and degree-two denominator terms times degree-two numerator coefficients. For a free \(k^\mu\) component, the loop vector itself is converted into an external vector by the angular average; its scalar coefficient must therefore be extracted at degree five, and its odd-rank tensor average can be nonzero. Expanding only the heavy denominators misses terms and cannot yield the complete hard coefficient.

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
where the nonnegative expansion indices are constrained by scalar form-factor degree four. The \(M_E^2 k^\mu\) and other free-\(k^\mu\) terms must be retained: at scalar degree five their odd number of loop-momentum contractions combines with the free vector index to give an even-rank rotational tensor and can contribute to the external-vector form factors.

The complete Taylor-partition sums and radial master integrations are evaluated in §5D. A Gamma-function pole in an individual hard Taylor term is not by itself a matched UV pole: it must be combined with the EFT soft region in the same subtraction convention. The corrected ordinary-line soft pole comparison is given in §5E.

## 5C. Superseded first Taylor-count attempt

The earlier 28/20/20 count treated the scalar coefficient degree as the full vector-amplitude degree and therefore selected degree five before accounting for the explicit external Lorentz vector. It also did not provide the claimed dedicated generator on the PR head. **Those counts are superseded and must not be used for matching.**

For a decomposition \(\Gamma^\mu=p^\mu F_p+q^\mu F_q\), a total degree-five vector amplitude requires degree-four scalar form factors. The corrected generator and radial reduction are in calculations/RC-001-QLD-hard-expansion-numerator-audit.py.

## 5D. Corrected degree-five vector amplitude: complete d-dimensional radial reduction

The corrected tensor reduction treats the two vector structures separately:
- explicit \(p^\mu,q^\mu,p'^\mu\) numerator components require scalar form-factor degree four;
- a free \(k^\mu\) component requires scalar coefficient degree five, because its angular average pairs the free index with one external momentum.

After angular averaging, the structures combine into 17 radial terms each for the light-attachment \(p^\mu\) and \(q^\mu\) form factors, and 7 terms each for the heavy-attachment \(p^\mu\) and \(p'^\mu\) form factors. The free-\(k^\mu\) contributions are included in these counts. There are 25 distinct radial masters:
\[
\begin{split}
&(1,4,1),(1,5,1),(1,5,2),(1,6,2),(1,6,3),(1,7,3),(1,7,4),\\
&(2,3,1),(2,4,2),(2,5,3),(2,6,4),\\
&(3,2,1),(3,3,2),(3,4,3),(3,5,4),\\
&(4,1,1),(4,2,2),(4,3,3),(4,4,4),\\
&(5,1,2),(5,2,3),(5,3,4),(6,1,3),(6,2,4),(7,1,4).
\end{split}
\]
Each tuple denotes \((a,b,t)\) in \(J_{ab}^{(t)}\). The denominator indices are
\[
L:\quad a=2+n_q,\quad b=1+n_p,\qquad
E:\quad a=1,\quad b=2+n_p+n_{p'}.
\]
The \(p\)-shift in the light graph raises the massive denominator power \(b\), not the massless power \(a\).

For all 25 masters, the UV Gamma-function argument \(a+b-2-t\) is positive, so the hard-region integrals are UV convergent. Eight masters have IR poles:
\[
\begin{array}{c|c}
(a,b,t)&J_{ab}^{(t)}\\\hline
(3,2,1)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(4,1,1)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right)\\
(4,2,2)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(5,1,2)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right)\\
(5,2,3)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(6,1,3)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right)\\
(6,2,4)&-\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+2\right)\\
(7,1,4)&+\dfrac{1}{16\pi^2M_E^4}\left(\dfrac1{\epsilon_{\rm IR}}+L_M+1\right).
\end{array}
\]
The remaining 17 masters are finite. Here
\[
L_M=\ln\frac{\mu^2}{M_E^2}+\ln(4\pi)-\gamma_E.
\]

Summing the radial masters gives the following Euclidean hard-region form factors in the trace/routing convention of §3, before restoring the common Wick/Feynman-rule phase, \(g_A|y_\ell|^2\), and representation charges. Let \(P=p^2\), \(Q=q^2\), \(R=p\cdot q\), \(P'=p'^2\), and \(T=p\cdot p'\). For the light attachment:
\[
F_p^L\big|_{\rm hard}=
\frac{Q(P-R)}{24\pi^2M_E^4\epsilon_{\rm IR}}
+\frac{12L_MQ(P-R)-9P^2+18PR+16PQ-12R^2-13RQ+3Q^2}
{288\pi^2M_E^4},
\]
\[
F_q^L\big|_{\rm hard}=
-\frac{R(P-R)}{24\pi^2M_E^4\epsilon_{\rm IR}}
+\frac{-24L_MPR+24L_MR^2+9P^2-68PR+9PQ+62R^2-24RQ+3Q^2}
{576\pi^2M_E^4}.
\]
For the heavy attachment:
\[
F_p^E\big|_{\rm hard}=
\frac{5P^2+13PP'+13P'^2-8PT-14P'T+6T^2}
{960\pi^2M_E^4},
\]
\[
F_{p'}^E\big|_{\rm hard}=
\frac{13P^2+13PP'+5P'^2-14PT-8P'T+6T^2}
{960\pi^2M_E^4}.
\]

For the pure \(U(1)_X\) sector, \(q_L=q_E\) and \(q_H=0\). After imposing \(p'=p-q\), the heavy-attachment contribution in the \((p^\mu,q^\mu)\) basis is
\[
F_{p}^{E,pq}=
\frac{15P^2+20PQ-30PR+9Q^2-25QR+20R^2}
{480\pi^2M_E^4},
\]
\[
F_{q}^{E,pq}=
-\frac{15P^2+15PQ-20PR+5Q^2-12QR+10R^2}
{960\pi^2M_E^4}.
\]
Adding the light and heavy attachments gives the compact result
\[
F_{p,\mathrm{hard}}^{X}=
\frac{Q}{720\pi^2M_E^4}
\left[
\frac{30(P-R)}{\epsilon_{\rm IR}}
+30L_M(P-R)+70P+21Q-70R
\right],
\]
\[
F_{q,\mathrm{hard}}^{X}=
-\frac{R}{720\pi^2M_E^4}
\left[
\frac{30(P-R)}{\epsilon_{\rm IR}}
+30L_M(P-R)+70P+21Q-70R
\right].
\]
Consequently,
\[
R F_{p,\mathrm{hard}}^{X}+QF_{q,\mathrm{hard}}^{X}=0
\]
for both the pole and finite terms. This is the charge-resolved hard-region Ward check for \(q_L=q_E\). The common factor \(g_X q_\ell |y_\ell|^2\) and the overall 1PI phase are still omitted.

A useful internal check is that the light-attachment hard IR pole is transverse:
\[
R\,F_p^{L,\rm pole}+Q\,F_q^{L,\rm pole}=0.
\]
The poles are IR poles of the hard region, not UV counterterms. They must cancel UV poles from the complete EFT soft sector. These are subgraph form factors, not yet the charge-weighted full UV amplitude or the matched Wilson coefficient; the EFT contact/source/EOM soft contributions and the full hard-soft cancellation remain open.

The reproducible symbolic reduction, including the free-\(k^\mu\) tensor contributions, is in calculations/RC-001-QLD-hard-expansion-numerator-audit.py, with checks in validation/RC-001-QLD-hard-expansion-numerator-audit.txt.

## 5E. Corrected EFT-soft pole comparison: ordinary light-line insertion

The \(M_E^{-4}\) soft expansion of the light-attachment graph is
\[
I_{L,\mathrm{soft}}^{(M^{-4}),\mu}
=-\frac1{M_E^4}\int_k
\frac{N_L^\mu(k,p,q)(k+p)^2}{k^2(k+q)^2}.
\]
Combine the two massless denominators with one Feynman parameter \(x\) and shift \(k=\ell-xq\). Then
\[
k=\ell-xq,\quad k'=\ell+(1-x)q,\quad K=\ell+p-xq.
\]
Writing \(A=K\cdot k'\), \(B=k'\cdot k\), and \(C=K\cdot k\), the numerator becomes
\[
N_L^\mu K^2
=2K^2\left[
(A-B+C)\ell^\mu
-Bp^\mu
+\big(-xA+xB+(1-x)C\big)q^\mu
\right].
\]
The \(p^\mu\) coefficient is \(-B\), not \(-B+C\): \(k'^\mu\) has no \(p^\mu\) component after this shift. The previous soft audit used \(-B+C\), which was an algebraic projection error and generated a spurious \(p^\mu\) residual. The corrected coefficient is used in the current script.

After the exact \(d\)-dimensional angular average and extraction of the UV pole,
\[
F_{p,\mathrm{soft,line}}^{\rm UV}
=-\frac{Q(P-R)}
{24\pi^2M_E^4\epsilon_{\rm UV}},
\qquad
F_{q,\mathrm{soft,line}}^{\rm UV}
=+\frac{R(P-R)}
{24\pi^2M_E^4\epsilon_{\rm UV}},
\]
where \(P=p^2,\ Q=q^2,\ R=p\cdot q\). Hence the soft UV pole is transverse:
\[
R F_{p,\mathrm{soft,line}}^{\rm UV}
+Q F_{q,\mathrm{soft,line}}^{\rm UV}=0.
\]
Comparing with §5D gives exact cancellation in both components:
\[
F_{p,\mathrm{hard}}^{\rm IR}
+F_{p,\mathrm{soft,line}}^{\rm UV}=0,\qquad
F_{q,\mathrm{hard}}^{\rm IR}
+F_{q,\mathrm{soft,line}}^{\rm UV}=0.
\]
Thus **the ordinary light-line soft graph already cancels both hard IR poles** in this parity-even projection. The previously reported \(p^\mu\) remainder is superseded and must not be used to motivate an additional pole counterterm or to assign a pole to a particular Q8/source graph.

The corrected soft calculation and its pole/Ward checks are included in calculations/RC-001-QLD-hard-expansion-numerator-audit.py and the paired validation output. This closes the pole-level hard/soft comparison for the ordinary light-line subgraph only; it does not yet establish the finite, charge-weighted, complete UV–EFT matching coefficient.

## 5F. Covariant \(Q_{LD}^{(8)}\) contact vertex

The chiral heavy propagator gives the tree-level derivative expansion of the \(H^\dagger L_\ell\) composite. With \(\Psi_L=H^\dagger L_\ell\), the operator at the next order is the full covariant product
\[
Q_{LD}^{(8)}=(\bar L_\ell H)(i\slashed D)^3(H^\dagger L_\ell),
\qquad
\Delta\mathcal L_{\rm EFT}^{(8)}
=\frac{|y_\ell|^2}{M_{E_\ell}^4}Q_{LD}^{(8)}
\]
in the sign convention where \(Q_{LD}^{(6)}=(\bar L_\ell H)i\slashed D(H^\dagger L_\ell)\) has coefficient \(+|y_\ell|^2/M_E^2\). The operator is \((i\slashed D)^3\), not merely \(i\slashed D D^2\): the noncommuting covariant derivatives also contain the field-strength commutator terms.

For \(D_\mu=\partial_\mu+i g_A q_E A_\mu\), define \(\Pi_\mu=iD_\mu\). The stripped one-background vertex between composite momenta \(K\) and \(K'\), with \(q=K-K'\), is
\[
V_{Q8}^\mu(K',K)
=-g_Aq_E\left[
K'^2\gamma^\mu+\slashed K'\gamma^\mu\slashed K+K^2\gamma^\mu
\right].
\]
Its Ward contraction is
\[
q_\mu V_{Q8}^\mu
=-g_Aq_E\left[K^2\slashed K-K'^2\slashed K'\right],
\]
using
\[
\slashed K'\slashed q\slashed K
=K^2\slashed K'-K'^2\slashed K.
\]
This is exactly the difference of the zero-background \(Q_{LD}^{(8)}\) inverse kernels and fixes the ordered contact vertex. The formula includes the gauge coupling to the full composite charge \(q_E=q_L-q_H\), not just the \(L\) constituent charge.

Closing the light-lepton pair at this local contact gives a one-propagator tadpole. In the unbroken massless EFT it has no external scale; after expanding the numerator, all terms reduce to scaleless integrals of polynomials divided by \(k^2\). It therefore produces no logarithmic \(1/\epsilon_{\rm UV}\) pole in dimensional regularization at this order. It must still be retained in the Ward/source ledger if an IR mass, VEV, or a different off-shell regulator is introduced.

The heavy-attachment soft expansion likewise has only one massless propagator after both heavy denominators are expanded. In the unbroken massless dimensional-regularization setup it is scaleless at this order and gives no logarithmic soft UV pole. This is a result of the explicit expansion, not a reason to omit the attachment from the full-theory hard calculation.

## 6. Acceptance conditions

The QLD one-background matching is accepted only after:
1. the common Wick/Feynman-rule phase and charge-normalization conventions are restored and checked against the fixed fermion-flow/Ward convention;
2. the complete \(d\)-dimensional hard expansion through degree five is integrated;
3. the soft expansion is calculated with the same routing and subtraction scheme;
4. the complete EFT ordinary-line, Q8 contact, and scalar-source terms are summed;
5. the charge-resolved Ward identity is satisfied before and after pole extraction;
6. hard IR poles cancel soft UV poles and the remaining local coefficient is independent of the arbitrary matching scale.

The hard subgraph form factors and ordinary-line hard/soft pole cancellation are established in the stated trace/routing convention. No complete charge-weighted QLD dimension-eight Wilson coefficient is claimed in this record.
