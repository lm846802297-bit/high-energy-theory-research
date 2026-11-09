# RC-001 — Dimension-eight UV–EFT matching: staged calculation protocol

**Status:** active research branch; no dimension-eight Wilson vector is claimed complete. This document fixes the first calculation stage and the acceptance criteria. It deliberately separates the tree-level heavy-field expansion, EFT soft contributions, UV hard contributions, and final EOM/source reduction.

**Frozen source:** \`research/RC-001-vll-higgs-singlet-uv-eft.md\`, especially §§3, 10.9–10.11, and the linked EFT soft-topology census. The working interaction and sign convention are
\[
\mathcal L_{\mathrm{int}}\supset
-\left[y_\ell\bar L_\ell H E_{\ell R}
+\lambda_\ell S_\ell\bar E_{\ell L}\ell_R
+M_{E\ell}\bar E_{\ell L}E_{\ell R}\right]+\mathrm{h.c.},
\qquad S_\mu=S,\quad S_\tau=S^*,
\]
\[
\mathcal L_{\mathrm{EFT5}}\supset-C_{5,\ell}\mathcal O_{5,\ell}+\mathrm{h.c.},
\qquad C_{5,\ell}=-\frac{y_\ell\lambda_\ell}{M_{E\ell}},
\qquad \mathcal O_{5,\ell}=(\bar L_\ell H)S_\ell\ell_R.
\]
All UV and EFT amplitudes use dimensional regularization and the same \(\overline{\mathrm{MS}}\) prescription. The matching is performed first in the unbroken phase, with light masses set to zero, and then projected to the broken-phase benchmark observables only after the local operator basis is fixed.

## 1. Scope and target

The target is the complete local one-loop matching at fixed order \(M_E^{-4}\) for the amplitudes needed to determine the scalar-potential and \(h\)-\(s\) two-point subsectors. A claim of a *complete model-level dimension-eight Wilson vector* additionally requires the fermionic, gauge/current, source, and external-field sectors listed below. The scalar-potential subsector and the full Wilson vector must never be conflated.

The matching equation is organized amplitude by amplitude:
\[
\Gamma_{\mathrm{UV}}^{(1)}\big|_{M_E^{-4}}
-\Gamma_{\mathrm{EFT,soft}}^{(1)}\big|_{M_E^{-4}}
=\sum_i C_{i,\mathrm{hard}}^{(1,8)}\,
\Gamma_{\mathcal O_i}^{(0)}
+\Gamma_{\mathrm{local\,CT}}.
\]
The subtraction is made before EOM reduction. UV and EFT terms must share external momenta, field normalization, gauge fixing, IR prescription, and subtraction scheme.

## 2. Tree-level heavy-propagator expansion: dimension-seven representative

For the cross-chirality heavy propagator between the two Yukawa sources, the Dirac inverse gives
\[
P_R(i\slashed D-M_E)^{-1}P_R
=M_E P_R\big[(i\slashed D)^2-M_E^2\big]^{-1}.
\]
At low covariant momentum this has the formal expansion
\[
P_R(i\slashed D-M_E)^{-1}P_R
=-\frac{P_R}{M_E}
-\frac{P_R(i\slashed D)^2}{M_E^3}
+O(M_E^{-5}),
\]
where the operator ordering acts on the complete right-hand source. With the source interaction and \(C_5\) convention above, the induced candidate is therefore
\[
\Delta\mathcal L_{\mathrm{EFT}}^{(7)}
\supset
-\frac{y_\ell\lambda_\ell}{M_{E\ell}^3}
(\bar L_\ell H)(i\slashed D)^2(S_\ell\ell_R)+\mathrm{h.c.}
=
\frac{C_{5,\ell}}{M_{E\ell}^2}
(\bar L_\ell H)(i\slashed D)^2(S_\ell\ell_R)+\mathrm{h.c.},
\]
subject to confirmation of the overall source/operator sign against the full tree-level Schur complement in the same derivative convention.

This is a *redundant-basis representative*, not yet an independent dimension-seven Wilson coefficient. The reduction must expand the covariant derivatives, use the light-field equations of motion only after the off-shell matching, and retain all induced terms. In particular, \((i\slashed D)^2\) contains both covariant Laplacian and field-strength pieces; replacing it by an ordinary \(\partial^2\), or setting it to zero by the massless fermion EOM before expanding the derivative on \(S_\ell\), is not allowed. The \(\mu,\tau\) renormalizable Yukawa source vanishes in the frozen model, but derivatives acting on \(S_\ell\) and gauge-field-strength terms need not vanish.

Acceptance checks for this stage:
1. Derive the same term from the exact tree-level heavy-field equations of motion and from the momentum-space propagator expansion.
2. Verify the sign by reproducing \(C_{5,\ell}=-y_\ell\lambda_\ell/M_{E\ell}\) at zeroth derivative order.
3. Reduce the dimension-seven representative with explicit integration by parts, commutators \([D_\mu,D_\nu]\), and the model-specific light EOM.
4. Record every generated scalar-derivative, field-strength, current, and source companion, including terms that are EOM-redundant in the chosen basis.
5. Decide whether a nonzero independent \(C_{7,\ell}\) remains. Only then decide whether the SFT-12 \(C_5C_7^*\) soft topology is an independent graph or is represented by induced companion insertions.

## 3. Required EFT soft sectors at \(M_E^{-4}\)

The following are separate amplitude families. They must be calculated with explicit symmetry factors, flavor orientation, and complex conjugation; a topology count alone is not a coefficient.

| ID | EFT insertion family | Target amplitude / structure | Status before this branch |
|---|---|---|---|
| D8-S1 | \(Q_{LD}Q_{LD}\) | pure-Higgs four-scalar channel | Identified topologically; integral and projection not evaluated |
| D8-S2 | \(Q_{RD}Q_{RD}\) | pure-singlet four-scalar channel | Identified topologically; integral and projection not evaluated |
| D8-S3 | \(Q_{LD}Q_{RD}\) | mixed four-scalar channel | Identified topologically; integral and projection not evaluated |
| D8-S4 | \(C_5^4\) | eight-scalar \(X^2Y^2\) potential sector | Leading constant-pole subset checked; not the full amplitude matching |
| D8-S5 | \(C_5C_7^*\) and conjugate | dimension-eight soft/source sector | Conditional on the dimension-seven EOM reduction |
| D8-S6 | \(C_5C_5^*\) with \(Q_{LD}\) or \(Q_{RD}\) VEV wavefunction insertion | broken-phase \(h\)-\(s\) two-point projection | Power counted; finite and pole pieces not evaluated |
| D8-S7 | all other tree-level \(M_E^{-4}\) insertions generated by the exact heavy-field solution | scalar, fermionic, current/source amplitudes | Must be generated from the same tree-level action before declaring the census complete |

The \(C_5^2\) constant two-point pole already recorded in the master source is a VEV projection of the \(C_5^4\) potential topology. It is not an additional graph. Likewise, the archived Plan-C finite soft function already contains its dimension-five contact tadpole; the contact must not be appended a second time.

## 4. UV hard sectors to match against the soft result

For each external amplitude in Sec. 3, derive the full-theory one-loop graphs from the frozen UV Lagrangian, expand the heavy propagators by regions, and retain the hard \(M_E^{-4}\) terms. Include:
- pure-heavy and mixed heavy/light graphs;
- full-theory mass, Yukawa, scalar-potential, field, and tadpole counterterm insertions;
- all gauge-covariant derivative contact vertices required by the chosen amplitude;
- external-field normalization and the declared VEV/tadpole prescription;
- operator mixing and local counterterms on the EFT side.

The heavy-eigenstate Coleman–Weinberg result for the restricted scalar-potential \(O_8\) coefficient is one hard-sector cross-check. It is not a substitute for the full momentum-dependent hard amplitudes or the other Wilson coefficients.

## 5. Common operator basis and EOM/source map

Maintain two parallel records until matching is complete:
- **Green basis:** off-shell local operators before EOM reduction, sufficient to compare UV and EFT amplitudes without hiding contact/source terms.
- **Physical basis:** nonredundant operators after integration by parts, algebraic identities, gauge identities, and leading light-field EOM.

For every basis transformation, record the coefficient shift and all induced operators. Gauge-field EOM transformations must preserve the current/source amplitudes and the kinetic-mixing boundary. Fermion EOM transformations must preserve scalar-source terms and their flavor dependence. Do not drop an EOM operator until its induced companion coefficients have been added to the physical basis.

## 6. Numerical benchmarks and acceptance tests

Use the same \(M_{E\mu},M_{E\tau},y_\ell,\lambda_\ell,v_h,v_s\) values as the archived Benchmark A/B records. The matching itself is symbolic in the unbroken phase; numerical benchmark substitution is a check, not a replacement for the analytic coefficient.

Every completed sector must provide:
1. an explicit UV amplitude and its hard expansion;
2. an explicit EFT soft amplitude with all lower-dimensional insertions at the same \(M_E^{-4}\) order;
3. separate UV and IR poles before cancellation;
4. the finite hard coefficient in the declared Green basis;
5. the EOM/source map to the physical basis;
6. exact symbolic checks and an independent numerical evaluation at A/B;
7. a no-double-counting map showing where each topology is counted once.

A sector passes only when the hard/soft IR poles cancel, the UV poles are absorbed by the stated EFT counterterms, and the result is independent of the arbitrary matching scale through the retained order. The full dimension-eight claim additionally requires closure of all gauge/current and source sectors and an independent diagram-level implementation.

## 7. Execution order

1. Derive and EOM-reduce the tree-level \(M_E^{-3}\) representative in Sec. 2.
2. Generate the complete tree-level EFT action through \(M_E^{-4}\), not just the named \(Q_{LD},Q_{RD}\) insertions.
3. Evaluate D8-S1/S2/S3 and D8-S6 soft sectors with explicit tensor and flavor projections.
4. Resolve D8-S5 using the result of Step 1; include either the surviving \(C_7\) operator or its EOM-induced companions, never both independently.
5. Re-evaluate D8-S4 in the same common Green basis, keeping its already-validated pole as a cross-check rather than adding a second copy.
6. Calculate the corresponding UV hard amplitudes and counterterms by method of regions.
7. Build the common Green-basis subtraction ledger, then perform the EOM/source reduction.
8. Validate the scalar-potential subsector, then the full fermionic/current/source Wilson vector. Keep these acceptance levels distinct.

**Current acceptance state:** Step 1 is specified but not yet independently derived and validated. No new dimension-eight integral, Wilson coefficient, or matching closure is claimed by this protocol.
