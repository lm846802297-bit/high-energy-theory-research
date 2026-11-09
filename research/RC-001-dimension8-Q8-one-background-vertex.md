# RC-001 — Explicit one-background Q8 vertex and Ward contraction

**Status (2026-11-10):** exact momentum-space one-background contact vertex and its algebraic Ward contraction derived and symbolically checked. This is not yet the integrated one-loop soft amplitude.

## 1. Frozen convention and source charges

Use the convention already fixed in the dimension-six gauge atlas,
\[
D_\mu=\partial_\mu-i g_Y Y B_\mu-i g_XQ_XA'_\mu+\cdots,
\]
so
\[
i\slashed D=i\slashed\partial+g_YY\slashed B+g_XQ_X\slashed A'+\cdots.
\]
For both composite sources,
\[
\Psi_{L,\ell}=H^\dagger L_\ell,\qquad
\Psi_{R,\ell}=S_\ell\ell_R,
\]
the charges are
\[
(Y_\Psi,Q_{X,\Psi})=(-1,\eta_\ell Q_\ell),
\quad \eta_\mu=+1,\quad\eta_\tau=-1.
\]
The Q8 insertion therefore has direct one-background contacts
\[
g_YY_\Psi=-g_Y\quad(B_\mu),\qquad
g_XQ_{X,\Psi}=+\eta_\ell g_XQ_\ell\quad(A'_\mu),
\]
and no direct \(W_\mu^a\) contact. The absence of a direct W contact does not remove the ordinary W insertion on the L constituent line in QLD.

## 2. Exact one-background contact vertex

Let \(P\) be the momentum carried by the composite source immediately before the background insertion, \(P'=P+q\) the momentum immediately after it, and \(q\) the incoming background-gauge momentum. With \(\slashed P=\gamma^\alpha P_\alpha\), the linear term in \((i\slashed D)^3\) is the sum of the three possible ordered positions of the gauge vertex:
\[
\boxed{
V_{8,A}^{\mu}(P',P)
=g_Aq_{\Psi,A}
\left[
\slashed P'^{\,2}\gamma^\mu
+\slashed P'\gamma^\mu\slashed P
+\gamma^\mu\slashed P^{\,2}
\right].
}
\]
Here \(q_{\Psi,A}\) means the corresponding representation generator for a non-Abelian background and the charge for an Abelian background. For the actual QLD and QRD composite sources, the direct contacts are only B and A-prime as listed above.

The expression follows directly from
\[
(\mathscr D_0+V)^3\big|_{V}
=\mathscr D_0^2V+\mathscr D_0V\mathscr D_0+V\mathscr D_0^2.
\]
No commuting of adjacent covariant derivatives is used.

## 3. Ward contraction

Since \(\slashed q=\slashed P'-\slashed P\),
\[
\begin{aligned}
q_\mu V_{8,A}^{\mu}
&=g_Aq_{\Psi,A}\big[
\slashed P'^{\,2}(\slashed P'-\slashed P)
+\slashed P'(\slashed P'-\slashed P)\slashed P\\
&\hspace{34mm}
+(\slashed P'-\slashed P)\slashed P^{\,2}
\big]\\
&=\boxed{
g_Aq_{\Psi,A}
\left(\slashed P'^{\,3}-\slashed P^{\,3}\right).
}
\end{aligned}
\]
This is the exact one-background Ward identity for the Q8 contact vertex. It is an algebraic identity before loop integration and does not by itself establish the Ward identity of the complete one-loop Green function. The ordinary gauge insertion on the light-fermion propagator and the scalar-source charge flow must also be included.

## 3A. Ordinary fermion-line Ward identity and complete check target

For the massless fermion propagator \(S(k)=\slashed k/(k^2+i0)\), the ordinary gauge vertex obeys
\[
S(k+q)\slashed q\,S(k)=S(k)-S(k+q),
\]
equivalently \(S_{\rm out}(S_{\rm out}^{-1}-S_{\rm in}^{-1})S_{\rm in}=S_{\rm in}-S_{\rm out}\). Thus contraction of the ordinary-line graph telescopes into the difference of the Q8 insertion evaluated at the two adjacent loop momenta. The contact identity in §3 supplies precisely the corresponding difference of \(\slashed P^3\). After the loop-momentum shift is made with a regulator that preserves translations, the complete one-background amplitude must satisfy the background Ward identity.

For the two-scalar Q8 projection in the massless unbroken theory, the zero-background one-loop two-point integral contains only one massless propagator and polynomial numerators; it is scaleless in dimensional regularization. Hence its renormalized value is zero in this restricted setup. The corresponding full one-background Ward identity therefore requires a transverse amplitude, \(q_\mu\Gamma^\mu_{8,A}=0\), after the ordinary-line and Q8-contact pieces are combined. This is a target for the integrated calculation, not a claim that the integrated amplitude has already been evaluated.

The ordinary-line propagator identity and the Q8 contact identity are both included in the symbolic audit script. The script verifies algebraic building blocks; it does not perform the loop integration or prove the regulated momentum-shift step for a chosen subtraction prescription.

## 4. One-loop integrand to be evaluated

For a massless light fermion \(f=L_\ell\) or \(\ell_R\), define the zero-background Q8 insertion on the fermion line by
\[
V_8^{(0)}(k;r)=\left(\slashed k+\slashed r\right)^3,
\]
where \(r\) is the momentum carried by the scalar factor multiplying the differentiated fermion. Let \(S_f(k)\) be the massless propagator in the same Euclidean/Minkowski convention used throughout the matching. The one-background amplitude has the schematic, consistently routed form
\[
\Gamma_{8,A}^{(1)\mu}\propto c_8\int_k
\operatorname{tr}\left[
S_f(k)\,V_{8,A}^{\mu}(P',P)
-
S_f(k+q)\,G_{f,A}^{\mu}\,S_f(k)\,
V_8^{(0)}(k;r)
\right],
\]
with \(G_{f,A}^{\mu}=g_AT_f^A\gamma^\mu\), and with the momentum arguments of the contact term chosen so that \(P'=P+q\). The relative minus sign is the resolvent-expansion sign from
\[
(\mathscr D_0+V_A)^{-1}=S_0-S_0V_AS_0+\cdots.
\]
The complete routing and external scalar momenta must be fixed before performing the integral.

The first term is the Q8 contact graph. The second is the ordinary background-gauge insertion on the light-fermion line. Both are one-loop graphs. They must be summed before applying the full Green-function Ward identity.

## 4A. Explicit routed one-loop numerator and an important Ward-identity qualification

Choose the routing in which the ordinary gauge vertex carries incoming momentum \(q\), the two massless fermion propagators carry \(k\) and \(k+q\), and the scalar factor inside the differentiated composite carries momentum \(r\). The zero-background Q8 insertion on the segment adjacent to the Q8 vertex is
\[
V_8^{(0)}(k;r)=(\slashed k+\slashed r)^3
=(k+r)^2(\slashed k+\slashed r).
\]
The ordinary-line graph therefore has the explicit numerator
\[
\begin{aligned}
N^\mu(k;q,r)
&=\operatorname{tr}\!\left[
\slashed{k+q}\gamma^\mu\slashed k
(\slashed k+\slashed r)^3
\right]\\
&=4(k+r)^2\big[
(k+q)^\mu\,k\!\cdot\!(k+r)
-(k+q)\!\cdot k\,(k+r)^\mu\\
&\hspace{37mm}
+(k+q)\!\cdot\!(k+r)\,k^\mu
\big].
\end{aligned}
\]
Thus, apart from the common \(i\)'s and coupling/charge factors fixed by the chosen propagator convention,
\[
\mathcal I_{\rm line}^\mu(q,r)
=\int\!\frac{d^dk}{(2\pi)^d}
\frac{N^\mu(k;q,r)}{[k^2+i0][(k+q)^2+i0]}.
\]
The Q8 contact graph is
\[
\mathcal I_{\rm ct}^\mu(q,r)
=\int\!\frac{d^dk}{(2\pi)^d}
\operatorname{tr}\!\left[
\frac{\slashed k}{k^2+i0}
V_{8,A}^\mu(k+r,k+r-q)
\right],
\]
with the momentum assignment chosen consistently with the line graph. It has only one massless denominator and is scaleless in dimensional regularization, but setting it to zero before separating UV and IR contributions is not an acceptable UV-pole extraction procedure. Use a common IR rearrangement (for example nonexceptional external momenta or an auxiliary mass, with the same prescription on the hard and soft sides).

Combining denominators in the line graph gives
\[
\frac1{k^2(k+q)^2}
=\int_0^1\!dx\,
\frac1{\left[(k+xq)^2-x(1-x)q^2+i0\right]^2}.
\]
After \(l=k+xq\), the numerator is a polynomial of degree at most five in \(l\). Its odd-\(l\) terms integrate to zero; the remaining rank-zero, rank-two, and rank-four tensor integrals reduce to scalar bubble masters. This is the concrete reduction target for the next calculation.

**Ward-identity qualification.** The direct Q8 contact charge is the charge of the full composite source, not just that of the light fermion:
\[
q_{\Psi,A}=q_{f,A}+q_{\phi^\dagger,A}
\quad(Q_{LD}),\qquad
q_{\Psi,A}=q_{\ell_R,A}+q_{S,A}
\quad(Q_{RD}),
\]
with the appropriate conjugate/representation generators. The ordinary propagator insertion carries only \(q_{f,A}\). Therefore the line-graph Ward contraction cannot be canceled against the total-composite contact term by simply identifying the two charges. The remaining scalar-constituent charge flow is part of the functional Ward identity for the external scalar legs. In particular, the statement \(q_\mu\Gamma^\mu=0\) must not be imposed diagram by diagram or inferred solely from the scaleless zero-background tadpole. The correct check is the full background-gauge Ward identity with the scalar transformations and all contact pieces included, using a regulator that preserves momentum shifts.

For the model:
\[
\begin{array}{c|cc|c}
& q_{f,Y}&q_{\phi^\dagger,Y}&q_{\Psi,Y}\\\hline
Q_{LD}&-\frac12&-\frac12&-1\\
Q_{RD}&-1&0&-1
\end{array}
\qquad
\begin{array}{c|cc|c}
& q_{f,X}/Q_\ell&q_{\phi^\dagger,X}/Q_\ell&q_{\Psi,X}/Q_\ell\\\hline
Q_{LD}&\eta_\ell&0&\eta_\ell\\
Q_{RD}&-\eta_\ell&2\eta_\ell&\eta_\ell
\end{array}
\]
This charge-flow distinction must be retained in the explicit Ward contraction.

## 4B. Scalar master integrals for the UV-pole extraction

After Wick rotation and the Feynman shift \(l=k+xq_E\), write the angularly reduced numerator as
\[
\langle N^\mu(l-xq_E;q_E,r_E)\rangle_{\Omega}
=A_0^\mu(x)+A_2^\mu(x)\,l^2+A_4^\mu(x)\,(l^2)^2.
\]
The odd-rank terms vanish under the symmetric \(l\) integration. With
\[
\Delta=x(1-x)q_E^2,
\]
the required scalar masters are
\[
J_n(\Delta)=\mu^{2\epsilon}\int\frac{d^{4-2\epsilon}l}{(2\pi)^{4-2\epsilon}}
\frac{(l^2)^n}{(l^2+\Delta)^2}
=\frac{\mu^{2\epsilon}}{(4\pi)^{2-\epsilon}}
\Delta^{n-\epsilon}
\frac{\Gamma(n+2-\epsilon)\Gamma(\epsilon-n)}
{\Gamma(2-\epsilon)}.
\]
Their UV pole parts are
\[
J_0\big|_{\rm UV}=\frac{1}{16\pi^2}\frac1\epsilon,\qquad
J_1\big|_{\rm UV}=-\frac{\Delta}{16\pi^2}\frac1\epsilon,\qquad
J_2\big|_{\rm UV}=+\frac{\Delta^2}{32\pi^2}\frac1\epsilon.
\]
Consequently the ordinary-line graph's pole is obtained from
\[
\mathcal I_{\rm line}^{\mu}\big|_{\rm UV}
=\frac{1}{16\pi^2\epsilon}
\int_0^1 dx\left[
A_0^\mu(x)-\Delta A_2^\mu(x)
+\frac{\Delta^2}{2}A_4^\mu(x)
\right],
\]
including the overall trace, gauge generator, coupling, Wilson coefficient, and propagator-convention factors. The \(A_i^\mu\) are to be computed from the explicit numerator in §4A with \(d\)-dimensional tensor reduction; the displayed formula fixes the scalar master normalization but does not claim the \(x\)-integral or the resulting local pole has been evaluated.

The one-propagator contact graph must be treated with the same IR rearrangement before declaring its UV pole. In particular, a scaleless integral set to zero in dimensional regularization is not by itself a UV-pole audit.

## 5. Model-specific channel ledger

| Sector | Light fermion \(f\) | Scalar factor in \(\Psi\) | Direct Q8 contact | Ordinary gauge insertion |
|---|---|---|---|---|
| QLD | \(L_\ell\) | \(H^\dagger\) | \(B,A'\) | \(B,A',W^a\) on \(L_\ell\) |
| QRD | \(\ell_R\) | \(S_\ell\) | \(B,A'\) | \(B,A'\) on \(\ell_R\) |

For QLD, \(Y_L=-1/2\), \(x_L=\eta_\ell\), \(Y_{H^\dagger}=-1/2\), and \(x_{H^\dagger}=0\). For QRD, \(Y_{\ell_R}=-1\), \(x_{\ell_R}=-\eta_\ell\), \(Y_{S_\ell}=0\), and \(x_{S_\ell}=2\eta_\ell\). Thus the total composite charges are \((Y,x)=(-1,\eta_\ell)\) in both sectors.

For the W insertion in QLD, the weak-index structure is \(H^\dagger T^a H\) after the L-line generator is contracted with the scalar indices. It is not a direct Q8 contact term. There is no W contribution in QRD.

## 6. Symbolic check and acceptance boundary

The noncommuting-slash Ward contraction and the flavor/charge assignments are checked in calculations/RC-001-dimension8-Q8-one-background-vertex-audit.py, with output in validation/RC-001-dimension8-Q8-one-background-vertex-audit.txt.

Completed:
- exact one-background Q8 contact vertex;
- exact algebraic contraction \(q_\mu V_8^\mu\);
- model-specific B, A-prime, and W attachment classification;
- explicit one-loop integrand structure separating contact and ordinary propagator insertion.

Open:
- fully fixed external momentum routing and evaluated one-loop integrals;
- complete Green-function Ward identity including scalar-source transformations;
- two-background amplitude;
- local UV pole and counterterm mixing;
- one-loop hard-region partner and finite matching;
- EOM/IBP reduction and Benchmark A/B numerical checks.

No integrated one-loop soft coefficient or matched Wilson coefficient is claimed.
