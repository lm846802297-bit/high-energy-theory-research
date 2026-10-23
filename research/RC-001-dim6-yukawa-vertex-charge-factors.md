# RC-001 — Signed charge factors for both conjugate Yukawa vertices

**Status:** charge-conservation and gauge-factor algebra completed for the three line pairs at each of the four Yukawa vertices. This is the vertex-graph input layer, not the loop amplitude: momentum routing, Lorentz numerators, overall Feynman-rule signs, integration, EFT subtraction, and full Ward-identity sum remain open.

## 1. Conventions

Use all fields entering a Yukawa vertex as incoming. Let \(x=Q_X/Q_\ell\), \(\eta_\mu=+1\), and \(\eta_\tau=-1\). For a pair \(i,j\), define the diagonal and mixed charge factors
\[
F_B(i,j)=Y_iY_j,\qquad
F_X(i,j)=x_ix_j,\qquad
F_{BX}(i,j)=Y_ix_j+x_iY_j.
\]
The corresponding coupling prefactors are \(g_Y^2F_B\), \(g_X^2Q_\ell^2F_X\), and \(g_Yg_XQ_\ell F_{BX}\), respectively. The mixed factor applies only when the off-diagonal \(B-A'\) propagator is included; its overall propagator normalization is not absorbed into \(F_{BX}\).

Every listed vertex is separately hypercharge- and \(X\)-charge-neutral. The table retains the signed \(F_{BX}\) factor, rather than merely marking a mixed attachment as allowed.

## 2. \(y_\ell\bar L_\ell H E_{\ell R}\) and its conjugate

### Original vertex: \(\bar L_\ell H E_{\ell R}\)

| Pair | \(F_B=Y_iY_j\) | \(F_X=x_ix_j\) | \(F_{BX}=Y_ix_j+x_iY_j\) |
|---|---:|---:|---:|
| \(\bar L-H\) | \(+1/4\) | \(0\) | \(-\eta_\ell/2\) |
| \(\bar L-E_R\) | \(-1/2\) | \(-1\) | \(+3\eta_\ell/2\) |
| \(H-E_R\) | \(-1/2\) | \(0\) | \(+\eta_\ell/2\) |

### Conjugate vertex: \(\bar E_{\ell R}H^\dagger L_\ell\)

| Pair | \(F_B=Y_iY_j\) | \(F_X=x_ix_j\) | \(F_{BX}=Y_ix_j+x_iY_j\) |
|---|---:|---:|---:|
| \(\bar E_R-H^\dagger\) | \(-1/2\) | \(0\) | \(+\eta_\ell/2\) |
| \(\bar E_R-L\) | \(-1/2\) | \(-1\) | \(+3\eta_\ell/2\) |
| \(H^\dagger-L\) | \(+1/4\) | \(0\) | \(-\eta_\ell/2\) |

The \(W^I\) exchange exists only between the doublet and Higgs legs. With \(T^I=\sigma^I/2\), the singlet contraction at either same-vertex pair is
\[
\sum_I \bar T^I T^I=-C_F\,\mathbf 1=-\frac34\mathbf 1.
\]
No \(W E E\) vertex exists because \(E\) is an \(SU(2)_L\) singlet.

## 3. \(\lambda_\ell S_\ell\bar E_{\ell L}\ell_R\) and its conjugate

### Original vertex: \(S_\ell\bar E_{\ell L}\ell_R\)

| Pair | \(F_B=Y_iY_j\) | \(F_X=x_ix_j\) | \(F_{BX}=Y_ix_j+x_iY_j\) |
|---|---:|---:|---:|
| \(S-\bar E_L\) | \(0\) | \(-2\) | \(+2\eta_\ell\) |
| \(S-\ell_R\) | \(0\) | \(-2\) | \(-2\eta_\ell\) |
| \(\bar E_L-\ell_R\) | \(-1\) | \(+1\) | \(0\) |

### Conjugate vertex: \(S_\ell^\ast\bar\ell_R E_{\ell L}\)

| Pair | \(F_B=Y_iY_j\) | \(F_X=x_ix_j\) | \(F_{BX}=Y_ix_j+x_iY_j\) |
|---|---:|---:|---:|
| \(S^\ast-\bar\ell_R\) | \(0\) | \(-2\) | \(-2\eta_\ell\) |
| \(S^\ast-E_L\) | \(0\) | \(-2\) | \(+2\eta_\ell\) |
| \(\bar\ell_R-E_L\) | \(-1\) | \(+1\) | \(0\) |

The \(B\) boson attaches to the fermion–fermion pair only. The \(A'\) boson can attach to all three pairs. For mixed propagation, the fermion–fermion factor vanishes exactly at both conjugate vertices, while the two scalar–fermion pair factors have opposite signs.

## 4. What this fixes—and what it does not

The tables fix the signed representation/charge products to be inserted into the vertex integrals and prevent accidental sign loss when the conjugate vertices are combined. They do not fix the overall sign from the oriented fermion/scalar propagators or the gauge propagator, nor do they determine the Dirac numerator, finite integral, or local operator coefficient.

Next, for each row, attach explicit momenta and Feynman rules, evaluate the tensor numerator before setting external momenta to zero, reduce the scalar integrals in \(d=4-2\epsilon\), and subtract the EFT graph with the same IR prescription. Only then combine both conjugate vertices with heavy-line self-energy, boxes, field/parameter/operator counterterms, and contact graphs.
