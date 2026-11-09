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
