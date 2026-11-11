# RC-001 — EFT local one-\(W\) vertex and SU(2) Ward-covariance audit

**Status:** the local one-\(W\) contacts implied by the fixed internal-\(W\) hard sub-block are now written explicitly and checked for exact \(SU(2)_L\) covariance. This is an EFT-side consistency result. It is **not** a calculation of the UV one-loop five-point form factor and does not close the full Slavnov–Taylor identity.

## 1. Input four-point hard polynomial

Use the already recorded fixed-ordering internal-\(W\) hard polynomial
\[
C_{\rm hard}=a\,v_D+b\,v_-+c\,v_+,\qquad
F=\frac{g_2^2|y_\ell|^2}{16\pi^2M_E^2},
\]
where
\[
v_D=p_3+p_4=-(p_1+p_2),\quad
v_-=p_2-p_3,\quad v_+=p_2+p_3,
\]
and
\[
a=-\frac12+\frac L2,\quad
b=-\frac1{32}+\frac{7L}{16},\quad
c=\frac7{32}-\frac{5L}{16},\quad
L=\ln\frac{M_E^2}{\mu_R^2}.
\]
The local operator coefficients in this redundant off-shell basis are \(F(a,b,c)\).

## 2. Explicit local EFT one-\(W\) vertex

The three representatives are
\[
Q_D^{(3)}=(\bar L\sigma^I H)i\gamma^\mu
(D_\mu^{\rm adj}H^\dagger\sigma^I L),
\]
\[
O_-^{(3)}=T_{3(ij,kl)}(\bar L_i\gamma^\mu L_l)
\,i[H_k^\dagger D_\mu H_j-(D_\mu H^\dagger)_kH_j],
\]
\[
O_+^{(3)}=T_{3(ij,kl)}(\bar L_i\gamma^\mu L_l)
\,i[H_k^\dagger D_\mu H_j+(D_\mu H^\dagger)_kH_j].
\]
Here \(T_{3(ij,kl)}=\sum_A\sigma^A_{ij}\sigma^A_{kl}\), and
\[
D_\mu H=\partial_\mu H-i g_2W_\mu^J\frac{\sigma^J}{2}H,\qquad
D_\mu H^\dagger=\partial_\mu H^\dagger
+i g_2H^\dagger\frac{\sigma^J}{2}W_\mu^J.
\]
For \(Y^I=H^\dagger\sigma^I L\),
\[
(D_\mu^{\rm adj}Y)^I=\partial_\mu Y^I+
g_2\epsilon^{IJK}W_\mu^JY^K.
\]
Therefore the local contact part is
\[
\mathcal L_{\rm EFT}^{(1W)}
=F g_2 W_\mu^J\left[
i a\,\epsilon^{IJK}(\bar L\sigma^I H)\gamma^\mu
(H^\dagger\sigma^K L)
+2b\,T_{3(ij,kl)}(\bar L_i\gamma^\mu L_l)
H_k^\dagger\left(\frac{\sigma^J}{2}\right)_{jm}H_m
\right].
\]
There is no direct \(O_+^{(3)}\) contact: the two Higgs gauge connections cancel in
\(i[H^\dagger D H+(D H^\dagger)H]\).

At the matching point \(\mu_R=M_E\), \(L=0\), so
\[
a=-\frac12,\qquad b=-\frac1{32},\qquad c=\frac7{32},
\]
and
\[
\boxed{
\mathcal L_{\rm EFT}^{(1W)}\big|_{\mu_R=M_E}
=F g_2 W_\mu^J\left[
-\frac i2\epsilon^{IJK}(\bar L\sigma^I H)\gamma^\mu
(H^\dagger\sigma^K L)
-\frac1{16}T_{3(ij,kl)}(\bar L_i\gamma^\mu L_l)
H_k^\dagger\left(\frac{\sigma^J}{2}\right)_{jm}H_m
\right].
}
\]
Equivalently, the two nonzero coefficients including the common \(F\) are
\(-i g_2F/2\) and \(-g_2F/16\). The \(O_+\) direct contact is zero.

## 3. Exact gauge-covariance checks

The calculation script performs the following exact finite-dimensional algebra checks:

1. The Pauli commutator
   \[
   [\sigma^J/2,\sigma^I]=-i\epsilon^{IJK}\sigma^K
   \]
   for all \(I,J=1,2,3\), fixing the adjoint transformation sign.
2. With
   \[
   \delta X=-g_2\alpha\times X,\quad
   \delta Y=-g_2\alpha\times Y,\quad
   \delta W_\mu=\partial_\mu\alpha-g_2\alpha\times W_\mu,
   \]
   it verifies
   \[
   \delta(D_\mu^{\rm adj}Y)=-g_2\alpha\times(D_\mu^{\rm adj}Y),
   \qquad \delta(X^I(D_\mu^{\rm adj}Y)^I)=0.
   \]
   In particular, the inhomogeneous \(\partial_\mu\alpha\) terms cancel between
   \(\partial_\mu Y\) and the adjoint \(W_\mu\) contact.
3. It checks the \(T_3\) tensor is invariant under the four external doublet transformations.
4. It checks exactly, for all weak indices and all three generators,
   \[
   T_{3(ij,kl)}\left(\frac{\sigma^J}{2}\right)_{jm}
   =\delta_{il}\sigma^J_{km}
   -\frac12\sigma^J_{im}\delta_{kl}.
   \]
5. It expands the Higgs covariant derivatives and confirms the \(O_-\) contact is \(+2g_2H^\dagger(\sigma^J/2)H\), while the \(O_+\) contact vanishes.

The explicit logarithmic slopes are also checked:
\[
\frac{d(a,b,c)}{d\ln\mu_R}
=\left(-1,-\frac78,\frac58\right),
\]
using \(dL/d\ln\mu_R=-2\). This is the explicit-log derivative of this one-loop sub-block only; it is not the complete anomalous-dimension equation, because coupling running and the other matching sectors have not been included.

## 4. Reproduction

- calculations/RC-001-dim6-WW-fivepoint-EFT-ward.py
- calculations/test_RC001_dim6_WW_fivepoint_EFT_ward.py
- validation/RC-001-dim6-WW-fivepoint-EFT-ward.txt

The standalone script and five regression tests use exact SymPy algebra. Their PASS status is local execution in the current calculation session; no GitHub Actions run is claimed.

## 5. Boundary and next calculation

This calculation fixes the EFT local contact vertex required by the already matched four-point hard polynomial. It does **not** evaluate the UV one-loop five-point graphs with the external \(W\) attached to the UV heavy/light lines. It also does not include the second external-field routing, all external-leg and gauge-sector terms, counterterms, or the complete Slavnov–Taylor sum. In particular, the transverse part of the UV five-point amplitude has not been computed.

The next independent calculation remains the UV one-loop five-point amplitude in the same nonexceptional off-shell kinematics and Feynman-gauge convention. Its longitudinal contraction must be compared with the gauge variation implied by the four-point sub-block; its transverse form factors must be extracted independently. Only after the UV and EFT five-point amplitudes and their counterterms are combined can the complete \(WW\) matching row be closed.
