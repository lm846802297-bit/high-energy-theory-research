# RC-001 local validation status — 2026-10-23

**CI disposition:** explicitly skipped by project decision because GitHub Actions repeatedly failed before starting a runner. This is not a CI pass and is not treated as a physics result.

## Local checks performed

| Check | Result | What it establishes | What it does not establish |
|---|---|---|---|
| Charge-aware \(Q_{LD}/Q_{RD}\) attachment census | PASS | Counts of allowed unordered gauge line-pair classes for \(\mu,\tau\); signed \(B-A'\) charge-factor cancellations | Individual Feynman-diagram multiplicities, loop numerators, or coefficients |
| \(Q_{LD}\) \(SU(2)_L\) generator contractions | PASS | Exact tensor decomposition of all six \(WW\) line-pair classes into singlet/triplet tensors | Loop integrals, graph signs beyond the generator contraction, or finite Wilson coefficients |
| Diagonal-gauge input-parameter counterterm algebra | PASS | Exact rational combination \(2\delta y/y-2\delta M_E/M_E\) and \(2\delta\lambda/\lambda-2\delta M_E/M_E\) for the stated standard MS pole formulas | Independent derivation of the general counterterm formulas, mixed kinetic-mixing terms, EFT operator counterterms, or full UV–EFT matching |
| Light-only external-leg factor cancellation | ANALYTIC IDENTITY | With matched tree amplitudes and identical light-field conventions, common light-leg gauge factors multiply the same tree amplitude and cancel in the UV–EFT difference at \(O(M_E^{-2})\) | Heavy-line corrections, finite field decoupling, external gauge-field thresholds, or the complete Ward-identity sum |

| Heavy-\(E\) self-energy and scalar master integrals | PASS | Exact Feynman-parameter integrals at \(p^2=0\), the \(B_0(0;0,M_E^2)\) kernel, crossed-box partial fractions, and the displayed UV/IR split | Full vertex/box graph signs, multiplicities, and Wilson coefficients |
| Additive \(B-A'\) kinetic mixing | PASS | \(\operatorname{Tr}(YX)=0\) for the stated light sector and across the \(\mu,\tau\) heavy pair; finite heavy threshold \(\propto\ln(M_{E_\mu}^2/M_{E_\tau}^2)\) | Independent \(\chi\) boundary, full kinetic-matrix scheme, and mixed-propagator four-point amplitudes |

## Open physics evidence

- No FeynArts/FeynCalc, QGRAF, FORM, Cadabra, Sage, or equivalent diagram-level package was available in the probed runtime.
- The heavy-line self-energy and selected scalar master integrals are evaluated, but complete Yukawa-vertex and crossed-box amplitudes have not been summed; the associated LD/RD ledger rows remain NOT EVALUATED.
- The new \(O(g^2/M_E^2)\) UV loop integrals and corresponding EFT soft integrals have not been evaluated as a complete set.
- No finite gauge-correction Wilson coefficient is claimed.
- The shared UV/EFT pole tables, counterterm matrix, Ward-identity completion, kinetic-mixing terms, and full EOM/source/current projection remain open.
- PR #4 may be merged as a research-continuity checkpoint. Merge does not close the physics gates above; CI remains skipped by explicit project decision and is not claimed to pass.
