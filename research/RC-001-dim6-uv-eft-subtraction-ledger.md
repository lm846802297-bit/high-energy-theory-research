# RC-001 — Dimension-six gauge matching: UV–EFT subtraction and common-basis ledger

**Status:** matching protocol and per-amplitude evidence ledger established. The newly identified \(O(g^2/M_E^2)\) gauge-correction amplitudes have not yet been integrated. No finite gauge-correction Wilson coefficient is claimed in this document. Existing bosonic coefficients from master §254 and previously checked scalar/soft kernels are not duplicated.

## 1. Common conventions

Use \(d=4-2\epsilon\), one common \(\overline{\mathrm{MS}}\) convention, and
\[
\Delta_{\rm UV,IR}=\frac1{\epsilon_{\rm UV,IR}}-\gamma_E+\ln4\pi,\quad
L_\ell=\ln\frac{M_{E_\ell}^2}{\mu_R^2},\quad
\ell_q=\ln\frac{-q^2-i0}{\mu_R^2}.
\]
Use the same nonexceptional off-shell external momenta (or one explicitly shared infrared regulator) in the UV and EFT calculations. Do not set all external momenta and light masses to zero before separating UV and IR poles. Keep the same gauge-fixing parameter, external-leg amputation/LSZ convention, and input scheme for \(y_\ell,\lambda_\ell,M_{E_\ell},g_Y,g_2,g_X\), and kinetic mixing.

For each amplitude,
\[
\Gamma_{\rm UV}^{(1)}=
\Gamma_{\rm hard}^{(1)}+\Gamma_{\rm soft}^{(1)},\qquad
\Gamma_{\rm EFT}^{(1)}=\Gamma_{\rm soft}^{(1)}
\]
only after all EFT insertions, external-field terms, parameter counterterms, and contact vertices required by that amplitude are included. The local matching difference is the hard part,
\[
\Delta\Gamma_{\rm hard}^{(1)}
=\Big[\Gamma_{\rm UV}^{(1)}-\Gamma_{\rm EFT}^{(1)}\Big]_
{\text{same IR prescription, same external state}}.
\]
Expand the difference to the required external-momentum order and \(M_E^{-2}\), then project onto the declared operator basis. A pole cancellation at the level of a stripped subgraph is necessary but not sufficient for a Wilson coefficient.

## 2. Required amplitude ledger

Each row is to be populated with explicit UV graphs, EFT graphs, UV and IR poles, finite local terms, counterterms, and basis projection. The status column is deliberately explicit: **NOT EVALUATED** means no loop coefficient has been invented.

| ID | Amplitude / coupling sector | UV contribution to compute | EFT subtraction to compute | Counterterm / projection requirement | Status |
|---|---|---|---|---|---|
| LD-B (atlas LD-B-01…10) | \(\bar L L H^\dagger H\), \(y_\ell^2 g_Y^2/M_E^2\) | All \(BB\) attachment classes in gauge atlas §3, heavy-line insertions, vertex/box graphs | \(Q_{LD}\) insertion with \(B\) exchange and its \(B\)-contact graphs; external legs | \(\delta y,\delta M_E,\delta g_Y,\delta Z_L,\delta Z_H,\delta C_{LD}\); singlet projection | NOT EVALUATED |
| LD-W (atlas LD-W-01…06) | Same amplitude, \(y_\ell^2 g_2^2/M_E^2\) | All six doublet-pair \(WW\) classes, including crossed weak tensors | \(Q_{LD}\) insertion with \(W\) exchange on external doublet lines; no direct \(W\) contact from \(D(H^\dagger L)\) | \(\delta Z_L,\delta Z_H,\delta g_2,\delta C_{LD}\); retain singlet/triplet tensors until projection | NOT EVALUATED |
| LD-X (atlas LD-X-01…03) | Same amplitude, \(y_\ell^2 g_X^2/M_E^2\) | \(A'A'\) pairs among \(E,\bar L,L\), heavy self-energy and vertex corrections | \(Q_{LD}\) insertion with \(A'\) exchange and \(A'\)-contact graphs | \(\delta g_X,\delta Z_L,\delta M_E,\delta C_{LD}\); flavor-resolved \(\eta_\ell\) factors | NOT EVALUATED |
| LD-BX (atlas LD-BX-01…09) | Same amplitude with mixed propagator | Every nonzero signed \(BA'\) pair from atlas §3; use the full kinetic matrix | EFT mixed-propagator exchange and contact graphs | Fix \(\chi(\mu_R)\)/threshold scheme; mixed charge factor \(Y_i x_j+x_iY_j\) | CONDITIONAL / NOT EVALUATED |
| RD-B (atlas RD-B-01…03) | \(\bar\ell_R\ell_R S_\ell^\ast S_\ell\), \(|\lambda_\ell|^2 g_Y^2/M_E^2\) | Three \(BB\) pair classes and heavy-line/vertex corrections | \(Q_{RD}\) insertion with \(B\) exchange and \(B\)-contact graphs | \(\delta\lambda,\delta M_E,\delta g_Y,\delta Z_{\ell_R},\delta Z_S,\delta C_{RD}\) | NOT EVALUATED |
| RD-X (atlas RD-X-01…10) | Same amplitude, \(|\lambda_\ell|^2 g_X^2/M_E^2\) | All ten \(A'A'\) pair classes, heavy and scalar lines, vertex/box graphs | \(Q_{RD}\) insertion with \(A'\) exchange and contact graphs | \(\delta g_X,\delta Z_{\ell_R},\delta Z_S,\delta M_E,\delta C_{RD}\); retain \(\eta_\ell\) signs | NOT EVALUATED |
| RD-BX (atlas RD-BX-01…07) | Same amplitude with mixed propagator | Seven nonzero signed \(BA'\) pair classes from atlas §4 | EFT mixed exchange/contact graphs | Fix kinetic-mixing boundary; explicitly verify the three charge-factor zeros | CONDITIONAL / NOT EVALUATED |
| LD-EXT | \(Q_{LD}\) external-field sector | \(L,H\) self-energies, seagulls and LSZ/parameter pieces in the UV convention | EFT \(L,H\) self-energies and matching field convention | Avoid counting an external-field correction both as LSZ and as a local vertex | NOT EVALUATED |
| RD-EXT | \(Q_{RD}\) external-field sector | \(\ell_R,S\) self-energies, scalar seagull and LSZ/parameter pieces | EFT \(\ell_R,S\) self-energies and matching field convention | Same external-field convention as UV | NOT EVALUATED |
| LD-CUR | \(\bar L L V\) and \(H^\dagger H V\) current/form-factor amplitudes | Gauge-invariant vertex sets and contact terms, separated from reducible gauge exchange | EFT current insertions, EOM terms and counterterms | Do not count current exchange as a local 1PI scalar coefficient; preserve \(SU(2)\) tensors | NOT EVALUATED |
| RD-CUR | \(\bar\ell_R\ell_R V\) and \(S^\dagger S V\) current/form-factor amplitudes | \(B,A'\), and conditional mixed current sets | EFT current insertions, contact terms and counterterms | Use the same \(U(1)\) current and kinetic-mixing convention | NOT EVALUATED |
| BASIS | Full common-basis coefficient vector | Sum only amplitudes at the same coupling order and external-state projection | Apply EOM/IBP/Fierz once to the summed coefficients | Record redundant coefficients, nonredundant coefficients, source/potential companions and four-fermion shifts separately | OPEN |

## 3. Pole and finite-part table to fill per diagram family

For every graph family \(a\), store the amplitude in a fixed common normalization:
\[
\Gamma_a^{\rm UV}=\frac{1}{16\pi^2M_E^2}
\left[\frac{u_{a,\rm UV}}{\epsilon_{\rm UV}}+
\frac{u_{a,\rm IR}}{\epsilon_{\rm IR}}+
u_{a,\log}L_\ell+u_{a,\rm fin}\right]\mathcal T_a(p_i),
\]
with the coupling product, group factor, weak tensor and Dirac tensor written outside or inside \(\mathcal T_a\) consistently. The EFT graph has the same external tensor decomposition:
\[
\Gamma_a^{\rm EFT}=\frac{1}{16\pi^2M_E^2}
\left[\frac{e_{a,\rm UV}}{\epsilon_{\rm UV}}+
\frac{e_{a,\rm IR}}{\epsilon_{\rm IR}}+
e_{a,\log}\ell_q+e_{a,\rm fin}\right]\mathcal T_a(p_i).
\]
These are data-entry templates, not asserted values. The entries \(u_{a,*}\) and \(e_{a,*}\) remain blank until the corresponding integral is calculated. After summing all graphs and counterterms, verify:

1. Identical IR poles cancel in \(\Gamma_{\rm UV}-\Gamma_{\rm EFT}\).
2. Gauge-parameter dependence cancels in the matching coefficient or is accounted for by the declared off-shell/EOM basis.
3. Remaining UV poles are removed by the EFT counterterm matrix in the chosen basis.
4. The finite polynomial has the expected dimension, chirality, weak tensor, flavor charge, and decoupling power \(M_E^{-2}\).
5. The same result follows after the allowed field redefinition/EOM transformation, with companion source and potential terms included.

A nonzero uncancelled IR pole, an unexplained gauge-parameter dependence, or a missing counterterm blocks coefficient promotion.

## 4. Common operator-basis reduction ledger

Use the following order; do not apply EOM before the UV-minus-EFT difference and tensor decomposition are recorded.

1. **Raw redundant basis.** Keep \(Q_{LD},Q_{RD}\), the explicit current operators, and the tensor structures generated by each graph. Preserve the \(SU(2)\) singlet/triplet tensors separately.
2. **Lorentz/Dirac reduction.** Apply gamma identities and chiral projectors with the stated external spinor order. For four-fermion amplitudes, keep scalar-bilinear and vector-current bases distinct until the Fierz sign and Grassmann reordering are explicitly applied.
3. **Weak-index projection.** Use the declared Pauli-matrix normalization. The completeness identity is an algebraic projection check, not a substitute for deriving the coefficient of each tensor from the diagrams.
4. **Gauge Ward identities.** Include external-leg graphs, gauge contact vertices and the gauge-parameter-dependent pieces before checking longitudinal contractions. The \(Q_{LD}/Q_{RD}\) insertion has a \(B\) and \(A'\) contact from \(D(H^\dagger L)\) or \(D(S_\ell\ell_R)\), but no direct \(W\) contact because each differentiated composite is an \(SU(2)\) singlet.
5. **EOM/IBP.** Only after the summed local amplitude is known, map redundant derivative structures into the selected master basis. Include all induced scalar-potential and source rows. Master §252.8–§252.10 gives the scalar-source map; master §254.10–§254.11 gives the optional gauge-EOM/current map. Use one representative only.
6. **Current and four-fermion ledger.** Keep local current operators, reducible gauge-exchange amplitudes, EOM-generated current-current operators, and independently matched four-fermion coefficients as separate entries. Do not add an EOM image on top of the operator it replaces.
7. **External-field/input scheme.** Record whether coefficients are for amputated 1PI Green functions or LSZ-normalized amplitudes. Parameter counterterms and finite field redefinitions must follow the same scheme on both sides.

## 5. Existing analytic results that are not to be recomputed or double-counted

The current analytic note already records the stripped hard/soft kernels for three loop-dependent \(C_5C_5^\ast\) crossed-current channels, the \(C_5C_5^\ast\) four-fermion scalar bubble, and the \(Q_{LD}/Q_{RD}\)-plus-quartic EOM kernel. The primary SymPy script reports 41 exact checks; the separate compact script reports 23 local exact checks. These validate selected integral kernels and algebraic reductions only.

Master §§252–255 also contain the previously calculated bosonic field-strength/current-to-gauge and scalar/source blocks. They remain existing modules. The missing target here is the one-loop gauge correction to the fermionic derivative/current sector, including heavy-line attachments, external legs, contact vertices, counterterms, and a common-basis sum.

## 6. Independent diagram-level validation and CI state

The current runtime has SymPy but no Mathematica/Wolfram executable, FeynCalc, FeynArts, pyfeyn, or QGRAF installation. The local attachment-census script therefore cannot validate loop numerators, symmetry factors, diagram signs, or finite coefficients. This absence is recorded as missing evidence, not as a successful independent check.

The dedicated GitHub Actions workflow was re-run for the then-current HEAD \(ae7358ab505d4e4c0a6c3bf14aa0f652821dd332\). GitHub still reports the job as failed with no recorded steps and runner ID zero; the combined commit status is empty. This is an infrastructure/runner-level failure signature, not evidence that either symbolic script failed. The workflow must run on the newer commit after the atlas files are integrated. A local pass is not a substitute for that run.

## 7. Closure criteria

Do not close the gauge sector until the diagram-level generated list is reconciled against this attachment census; each amplitude row has UV and EFT pole/finite data; the common-basis projection includes current/source/potential and four-fermion companions; the kinetic-mixing boundary is fixed or explicitly left conditional; and the latest HEAD has a real CI run with executed steps and checked-in-output comparisons. PR #4 remains Draft/Open.
