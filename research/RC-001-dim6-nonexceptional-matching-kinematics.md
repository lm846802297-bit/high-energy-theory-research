# RC-001 — Nonexceptional kinematics and local-projector prescription for dimension-six gauge matching

**Status:** prescribed common kinematic point and tensor-projector setup; no new loop coefficient is claimed.

## 1. Why the existing zero-momentum routing is not the final subtraction prescription

The fixed-routing WW cross-box calculation uses an exceptional local projection with two external momenta set to zero. It is useful for deriving the hard local numerator and for an expansion-by-regions diagnostic, but massless UV and EFT subgraphs can then contain overlapping UV/IR poles. The formal cancellation of the labeled \(\Delta_{\rm UV}\) terms in the scalar-master split is not, by itself, a complete \(R^*\) subtraction or a proof that every IR pole has been identified.

The UV and EFT amplitudes must ultimately be evaluated with identical nonexceptional external momenta, gauge fixing, regulator, field normalization, and tensor projectors. The same local operator coefficient is then extracted from their difference.

## 2. Symmetric nonexceptional four-point Euclidean point

Take all four external momenta incoming, with
\[
p_1+p_2+p_3+p_4=0,
\]
where the ordering is \(\bar L(p_1),H(p_2),H^\dagger(p_3),L(p_4)\). Choose the symmetric Euclidean point
\[
p_i^2=\mu_{\rm IR}^2,\qquad
p_i\cdot p_j=-\frac{\mu_{\rm IR}^2}{3}\quad(i\ne j).
\]
It follows that every two-particle channel is nonexceptional:
\[
(p_i+p_j)^2=\frac{4\mu_{\rm IR}^2}{3}\quad(i\ne j).
\]
The \(4\times4\) Gram matrix has one zero eigenvalue corresponding to momentum conservation and three positive eigenvalues \((4/3,4/3,1/3)\mu_{\rm IR}^2\). Thus no external leg or two-particle channel carries zero momentum. Analytic continuation to Minkowski signature is made only after the Euclidean tensor projection is defined.

Keep \(\mu_{\rm IR}^2\ll M_E^2\), expand the UV amplitude in \(\mu_{\rm IR}^2/M_E^2\), and retain the dimension-six local terms. The EFT is evaluated at the same point without changing the IR prescription.

## 3. Weak and Lorentz tensor projection

Keep the weak tensors separate:
\[
T_0=\delta_{ij}\delta_{kl},\qquad
T_3=2\delta_{il}\delta_{kj}-\delta_{ij}\delta_{kl}.
\]
Do not project onto a single Warsaw-basis current before the complete UV-minus-EFT amplitude is assembled.

For the off-shell fermion bilinear, choose three independent momenta, e.g. \(p_1,p_2,p_3\), and retain
\[
\mathcal M_T=
\bar u(p_1)\left[
F_{1,T}\slashed p_1+
F_{2,T}\slashed p_2+
F_{3,T}\slashed p_3
\right]P_Lu(p_4),
\qquad T=T_0,T_3.
\]
No external Dirac equation is imposed at the projection stage. The \(3\times3\) Gram matrix
\[
G_{ab}=p_a\cdot p_b,\qquad a,b=1,2,3,
\]
is invertible at the symmetric point, with
\[
\det G=\frac{16}{27}\mu_{\rm IR}^6.
\]
Thus the three local momentum structures can be projected independently. The actual Dirac trace projectors must be constructed with the same \(d\)-dimensional gamma algebra and chiral convention in the UV and EFT calculations.

## 4. UV–EFT and \(R^*\) bookkeeping

For each attachment class, record before simplification:
1. the UV integrand and its weak/Dirac numerator;
2. the EFT insertion graph, including the covariant-derivative contact term where present;
3. the UV and IR pole labels separately;
4. the UV parameter, field, and operator counterterms;
5. the projected finite local polynomial at the symmetric point.

If an auxiliary-mass or infrared-rearrangement version is used to simplify a UV pole, apply the same rearrangement to the UV and EFT graphs and include the required IR counterterm forests. A scaleless integral is never set to zero before its UV and IR parts have been separated. The nonexceptional point is the primary common-regulator check; \(R^*\) is an independent UV-pole extraction route, not a replacement for the full finite UV–EFT difference.

## 5. Immediate calculation order

1. Reproduce the fixed-routing Feynman-gauge WW box numerator with the nonexceptional momentum assignment before expanding in external momenta.
2. Construct and test the three Lorentz projectors and the \(T_0/T_3\) weak projectors independently.
3. Generate the matching EFT \(Q_{LD}\) insertion graphs; for the \(T_3\) derivative representative include the adjoint-covariant one-\(W\) contact already recorded in the current-form-factor atlas.
4. Compare UV and EFT pole residues at the same \(\mu_{\rm IR}\), before adding counterterms.
5. Add the parameter/operator counterterms once, then extract the local hard coefficient.
6. Only after the four-point subtraction closes, calculate the independent external-\(W\) five-point form factor and test the full Slavnov–Taylor identity.

## 6. Evidence boundary

This file fixes a reproducible kinematic and projection prescription. It does not claim that the nonexceptional loop integrals, EFT contact graphs, \(R^*\) forests, or one-\(W\) form factors have been evaluated. The fixed-routing \(11/16\) result remains a hard sub-block under its stated exceptional projection and is not promoted to a complete Wilson coefficient.
