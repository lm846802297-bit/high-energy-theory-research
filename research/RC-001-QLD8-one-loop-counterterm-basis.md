# RC-001 QLD8: one-loop Green-basis and evanescent seed closure

**Date:** 2026-11-10  
**Workstream:** PR #11, strict \(O(M_E^{-4})\) Higgs-source-square sector  
**Stage:** P1.0 basis construction and exact Dirac/color checks  
**Status:** source-pair, representation, color, derivative, and rank-3/rank-4 seed checks pass; the one-loop \(Z\) matrix is not yet calculated.

## 1. Scope and non-negotiable boundary

The retained source is
\[
\mathcal J_H^{(4)}=\mathcal J_d+\mathcal J_u+\mathcal J_e,
\]
with
\[
\begin{aligned}
\mathcal J_d^k&=\bar d_{R\,r,a}(Y_d^\dagger)_{rp}Q_{L\,p,a}^k,\\
\mathcal J_u^k&=\epsilon_{ik}\bar Q_{L\,p,a}^{\,i}(Y_u)_{pr}u_{R\,r,a},\\
\mathcal J_e^k&=y_e^*\bar e_R L_e^k.
\end{aligned}
\]
The strict source-square sector is
\[
\mathcal O_{\rm src}^{(8)}
=\sum_{A,B=d,u,e}(D_\mu\mathcal J_A^k)^\dagger
D^\mu\mathcal J_B^k.
\]
The \(C_{5,\ell}\) axial-lepton sources are not included: their cross terms start at \(M_E^{-5}\), and their squares at \(M_E^{-6}\).

This is a four-fermion/two-derivative operator-renormalization problem. It is not a calculation of the \(hh\), \(hs\), or \(ss\) scalar two-point functions. No coefficient from this note is to be inserted into PR #69.

## 2. Freeze the source-pair sectors

All three sources transform as \((\mathbf1,\mathbf2,+1/2)\) under \(SU(3)_c\times SU(2)_L\times U(1)_Y\). The retained source fermions \(Q_L,u_R,d_R,L_e,e_R\) are neutral under \(U(1)_{L_\mu-L_\tau}\). Thus this restricted source-square block has no direct \(A'\) or \(F_X^{\mu\nu}\) gauge vertex. The Wilson coefficient can still inherit UV-model parameters; that does not create a light-field \(U(1)_X\) interaction in this block.

| Pair | Chiral seed after source expansion | 4D Fierz physical seed | Color basis | Weak contraction | Flavor tensor |
|---|---|---|---|---|---|
| \(d^\dagger d\) | \(P_R\otimes P_L\) | vector \(\otimes\) vector | \(1,8\) | singlet | \(Y_d\otimes Y_d^\dagger\) |
| \(u^\dagger u\) | \(P_L\otimes P_R\) | vector \(\otimes\) vector | \(1,8\) | singlet | \(Y_u^\dagger\otimes Y_u\) |
| \(e^\dagger e\) | \(P_R\otimes P_L\) | vector \(\otimes\) vector | \(1\) | singlet | \(|y_e|^2\) |
| \(d^\dagger u\) | \(P_R\otimes P_R\) | scalar plus tensor | \(1,8\) | \(\epsilon_{ik}\) singlet | \(Y_d\otimes Y_u\) |
| \(d^\dagger e\) | \(P_R\otimes P_L\) | vector \(\otimes\) vector | \(1\) | singlet | \(Y_d\otimes y_e^*\) |
| \(u^\dagger e\) | \(P_L\otimes P_L\) | scalar plus tensor | \(1\) | \(\epsilon_{ik}\) singlet | \(Y_u^\dagger\otimes y_e^*\) |

The six rows are three diagonal pairs and three independent cross pairs; each cross pair is accompanied by its Hermitian conjugate. Equivalently, the ordered expansion contains nine pairs. Each ordered pair has four product-rule derivative placements, hence 36 ordered placements in the full source square. These are not 36 independent Wilson coefficients.

For quark crossed-color contractions, use the fixed normalization
\[
\operatorname{tr}(T^AT^B)=\frac12\delta^{AB},\qquad
\delta_{ad}\delta_{cb}
=\frac1{N_c}\delta_{ab}\delta_{cd}
+2T^A_{ab}T^A_{cd},\qquad N_c=3.
\]
The singlet/octet basis must be retained. A crossed contraction is not to be replaced by a singlet-current product alone. Quark-lepton rows have only the quark singlet color contraction.

The weak \(\epsilon_{ik}\) in \(d^\dagger u\) and \(u^\dagger e\) is an \(SU(2)\) singlet contraction. Do not split it into independent weak components before applying the weak-index identities. Flavor tensors remain general; no diagonal-Yukawa or generation-degeneracy approximation is introduced.

## 3. Green basis first; EOM quotient later

For the loop calculation, use an off-shell Green basis. Do **not** apply the first- or second-order fermion EOM before extracting UV poles. EOM reduction is a quotient on the renormalized local operator space and can otherwise hide EOM counterterms or contaminate the off-shell projectors.

For a source pair \(A^\dagger B\), label the two derivative placements by \(r,s\in\{0,1\}\):
- \(r=0\): the derivative in the first source acts on its barred fermion; \(r=1\): it acts on its unbarred fermion;
- \(s=0\): the derivative in the second source acts on its barred fermion; \(s=1\): it acts on its unbarred fermion.

Fierz rearrangement changes the spinor pairing, not the field on which a derivative acts. Keep \((r,s)=(0,0),(0,1),(1,0),(1,1)\) distinct until the full IBP/EOM map is applied.

For four off-shell external momenta \(p_1,\ldots,p_4\), impose only
\[
p_1+p_2+p_3+p_4=0.
\]
The scalar momentum polynomials of degree two span six independent Gram invariants. One possible choice is
\[
p_1^2,\ p_2^2,\ p_3^2,\ p_4^2,\ p_1\!\cdot p_2,\ p_1\!\cdot p_3.
\]
Keep \(\slashed p_i\) and any free Lorentz-index projectors as separate Dirac/tensor structures. The four source placements are only a tree-level subspace of this off-shell polynomial space: one-loop counterterms may also contain \(p_i^2\) structures and derivative placements related by EOM or total derivatives.

The EOM-reduced physical quotient must retain, rather than discard, the following dimension-eight classes:
1. four fermions with two covariant derivatives;
2. four fermions with one covariant Higgs derivative, generated by the Yukawa part of the second-order EOM;
3. four fermions with a gauge-field strength, generated by the curvature term;
4. gauge-EOM/current representatives where a derivative acts on a field strength.

The commutator \([D_\mu,D_\nu]\) must be kept until the field-strength operators have been projected. If a gauge-field EOM is used, choose either the field-strength-derivative representative or its complete matter-current replacement, never both.

## 4. Evanescent seed tower beyond the tree-level Fierz differences

Use unit-weight antisymmetrized gamma strings
\[
\Gamma_{(n)}^{\mu_1\ldots\mu_n}
=\gamma^{[\mu_1}\cdots\gamma^{\mu_n]}.
\]
For \(g_{\mu\nu}=(+---)\), \(\epsilon^{0123}=+1\), and
\(\gamma_5=i\gamma^0\gamma^1\gamma^2\gamma^3\), define
\(\eta_R=+1,\eta_L=-1\). Exact four-dimensional identities are
\[
\Gamma_{(3)}^{\mu\nu\rho}
=i\epsilon^{\mu\nu\rho\sigma}\gamma_\sigma\gamma_5,
\qquad
\Gamma_{(4)}^{\mu\nu\rho\sigma}
=-i\epsilon^{\mu\nu\rho\sigma}\gamma_5.
\]
Consequently, for direct spinor pairing,
\[
\begin{aligned}
(\Gamma_{(3)}^{\mu\nu\rho}P_X)\otimes
(\Gamma_{(3)\mu\nu\rho}P_Y)
&\xrightarrow{4D}
6\eta_X\eta_Y
(\gamma^\mu P_X)\otimes(\gamma_\mu P_Y),\\
(\Gamma_{(4)}^{\mu\nu\rho\sigma}P_X)\otimes
(\Gamma_{(4)\mu\nu\rho\sigma}P_Y)
&\xrightarrow{4D}
24\eta_X\eta_Y
P_X\otimes P_Y.
\end{aligned}
\]
The coefficients and signs have been checked with explicit Minkowski gamma matrices for all four \(XY=RR,RL,LR,LL\) choices.

This motivates the direct-pairing evanescent seeds
\[
\begin{aligned}
E_{3;XY}&=
(\bar\psi\Gamma_{(3)}^{\mu\nu\rho}P_X\chi)
(\bar\eta\Gamma_{(3)\mu\nu\rho}P_Y\xi)
-6\eta_X\eta_Y
(\bar\psi\gamma^\mu P_X\chi)
(\bar\eta\gamma_\mu P_Y\xi),\\
E_{4;XY}&=
(\bar\psi\Gamma_{(4)}^{\mu\nu\rho\sigma}P_X\chi)
(\bar\eta\Gamma_{(4)\mu\nu\rho\sigma}P_Y\xi)
-24\eta_X\eta_Y
(\bar\psi P_X\chi)(\bar\eta P_Y\xi).
\end{aligned}
\]
Each seed inherits the same color, weak, flavor, and derivative-placement labels as its parent physical operator. These definitions use no \(O(\epsilon)\) physical-operator admixture. They are direct-pairing definitions; if a crossed spinor pairing is used, the Grassmann exchange sign must be applied separately. Do not combine that sign twice with the existing \(E_{XY;V/T}^{\mu,\mu\nu}\) Fierz-difference definitions.

The one-loop gauge-exchange graphs acting on the current-current and scalar/tensor seeds can generate rank-three and rank-four antisymmetrized strings. The rank-three/rank-four seeds above are therefore required candidates. This is **not yet a proof of closure**: the actual set of \(\Gamma_{(n)}\otimes\Gamma_{(m)}\) structures, including mixed-rank structures and derivative-index correlations, must be read from the explicit one-loop numerators. The counterterm generator must fail loudly if it encounters a structure outside the declared basis; it must not project it away using four-dimensional identities.

## 5. Counterterm-matrix definition and calculation boundary

For a chosen off-shell operator vector \(\mathcal O=(\mathcal O_P,\mathcal O_E,\mathcal O_{\rm EOM})\), define
\[
\mathcal O^{\rm bare}_i=Z_{ij}\mathcal O^{\rm ren}_j,\qquad
Z_{ij}=\delta_{ij}+\frac{1}{16\pi^2\epsilon}
\left[g_s^2 Z^{(s)}_{ij}+g_2^2 Z^{(2)}_{ij}
+g'^2 Z^{(1)}_{ij}+\cdots\right]+\cdots.
\]
Yukawa-dependent entries and background-gauge mixing are separate blocks. There is no direct \(g_X\) exchange on the retained \(J_H^{(4)}\) constituent fields. The displayed equation is a matrix organization, not a computed result.

The UV pole calculation must include:
- all one-loop attachments to the four external fermion legs;
- gauge exchange between every allowed pair of legs;
- the gauge-contact vertices contained in the covariant derivatives;
- external-leg/wavefunction counterterms;
- all color and weak contractions;
- the complete set of local degree-two momentum and Dirac projectors;
- background-gauge amplitudes needed to identify \(4\psi F_{\mu\nu}\) and gauge-EOM counterterms.

Use generic nonexceptional Euclidean external momenta so the UV poles are not confused with scaleless UV/IR cancellations. The same NDR/\(\overline{\rm MS}\) and evanescent definitions must be used in the UV and EFT calculations.

## 6. Staged one-loop calculation order

1. **QCD pilot block:** start with \(d^\dagger d\), retaining the color singlet/octet and all four derivative placements. This is the cleanest test of the RL vector-current sector and the covariant-derivative contact terms.
2. **QCD same-chirality block:** add \(d^\dagger u\), which tests the RR scalar/tensor sector and the weak-\(\epsilon\) contraction.
3. **Remaining gauge blocks:** add \(u^\dagger u\), then \(d^\dagger e\), \(u^\dagger e\), and \(e^\dagger e\); include \(SU(2)_L\) and hypercharge exchange with their exact representation factors.
4. **Background-field block:** calculate one- and two-background-gauge Green functions and check the Ward identities before replacing any gauge-EOM operators by currents.
5. **Yukawa and EOM blocks:** include Higgs/Yukawa interactions and the EOM-generated \(4\psi D H\), \(4\psi F\), and gauge-current operators.
6. **EFT soft subtraction:** calculate the same external Green functions with the same IR rearrangement and scheme, then perform hard-minus-soft matching.
7. **Only after matching:** reduce to the final nonredundant physical dimension-eight basis and compare any induced scalar-sector projection separately.

The first two steps are chosen to expose both color mixing and same-chirality tensor mixing before the full SM gauge/Yukawa calculation is attempted.

## 7. Validation and claim boundary

The exact companion audit checks:
- all 64 rank-three and 256 rank-four index assignments for the four-dimensional gamma dualities;
- the contracted rank-three and rank-four projections for \(RR,RL,LR,LL\);
- the \(SU(3)\) fundamental completeness relation in all 81 color-index assignments;
- the Higgs-source hypercharges and the \(SU(2)\)-singlet epsilon contraction;
- the nine ordered source pairs and 36 derivative placements.

It does **not** evaluate a loop integral, a UV pole, \(Z_{ij}\), an anomalous dimension, or a finite Wilson coefficient. P1.0 closes the bookkeeping and exact four-dimensional projection seeds needed to start P1.1; the complete d-dimensional counterterm basis and one-loop renormalization remain open.
