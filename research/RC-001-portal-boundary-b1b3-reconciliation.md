# RC-001 — Portal Boundary and B1/B3 Kernel Reconciliation Ledger

> **Record type:** Dated internal reconciliation supplement; it does not replace the frozen primary source or claim complete model-level matching.
>
> **Audit date:** 2026-10-27
>
> **Status:** The portal matching relation and a working scalar-suppressed reference boundary are now explicit. The historical B1/B3 candidate-kernel sign issue remains **unresolved at the physical-amplitude level**.

## 1. Provenance and version relationship

### 1.1 Repository baseline

- **Repository:** [`high-energy-theory-research`](https://github.com/lm846802297-bit/high-energy-theory-research)
- **Baseline `main` HEAD at audit:** [`d6143c2aa15191ac8521e062d90860ba86713f00`](https://github.com/lm846802297-bit/high-energy-theory-research/commit/d6143c2aa15191ac8521e062d90860ba86713f00)
- **RC-001 source record:** [`research/RC-001-vll-higgs-singlet-uv-eft.md`](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/research/RC-001-vll-higgs-singlet-uv-eft.md)
- **Source-record blob SHA:** `4a334a2ad0ca1ebed9063b9657588c82cdf2f14b`
- **Live claim matrix:** [`research/RC-001-claim-evidence-matrix.md`](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/research/RC-001-claim-evidence-matrix.md)
- **Current source-aligned two-point algebra audit:** [script](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/calculations/RC-001-uv-eft-two-point-difference.py) and [captured output](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/validation/RC-001-uv-eft-two-point-difference.txt).

### 1.2 Frozen primary working source

The RC-001 record identifies the source baseline as:

- **File:** `higgs_portal_mixing_unified_reviewer_response_and_uv_eft_UPDATED_v2(8)(20261021)(153)_matchete_mapping_version_history.md`
- **Library file ID:** `file_00000000b7b48230a2ada1957a9ed4a0`
- **Version ID:** `1`
- **Size:** `1,989,214` bytes
- **SHA-256:** `f30af8ccc62feafa3923e8356437e4b80b40e518fc9b1188646b4d763e2791f1`

Relevant source sections:

- §§272–274: portal threshold, UV pole, zero-momentum sign convention, and parameterized \(h\)–\(s\) self-energy;
- §§248–252: fixed-sector hard-minus-soft matching and off-shell completion;
- §§276–285: mass-basis self-energy, EFT soft bubble, and the old on-shell \(4/3\) finite difference;
- §§286–302: projection/EOM analysis and reconciliation of the \(4/3\) difference;
- §§76–89 and §§238–239: historical B-kernel/Wick audits and path-resolved candidate integrations.

This ledger is a dated supplement to that frozen source. It does not rewrite the source file, change the claim matrix, or alter the historical v66 archive.

## 2. Portal boundary: one explicit reference benchmark

### 2.1 Matching equation and scheme

Use the potential convention

\[
V(H,S)\supset \lambda_{HS}(H^\dagger H)(S^\dagger S),
\qquad \mathcal L\supset -V.
\]

For the VLL Yukawa sector recorded in RC-001, in dimensional regularization and \(\overline{\mathrm{MS}}\), the one-loop zero-momentum threshold is

\[
\Delta\lambda_{HS}^{E}
=-\frac{1}{8\pi^2}
\sum_{\ell=\mu,\tau}|y_\ell|^2|\lambda_\ell|^2.
\]

At a common matching scale \(\mu_M\), with both heavy states integrated out at that scale,

\[
\boxed{
\lambda_{HS}^{<}(\mu_M)
=\lambda_{HS}^{>}(\mu_M)
+\Delta\lambda_{HS}^{E}
+O(\text{two loops},\text{higher-dimensional matching}).
}
\]

Here \(>\) denotes the UV theory and \(<\) the EFT after integrating out the heavy vector-like leptons. The source calculation finds no one-loop **additive UV pole** proportional to \(|y_\ell|^2|\lambda_\ell|^2\) in this sector, but it does find the finite threshold above. Other beta-function terms and other sectors are not thereby set to zero.

### 2.2 Working boundary selected for the scalar-suppressed reference benchmark

For the next calculation, freeze the following as a **reference benchmark condition**, not as a claim about an input already specified in the original paper:

\[
\boxed{\lambda_{HS}^{<}(\mu_M)=0,\qquad \mu_M=M_E}
\]

for the degenerate reference case \(M_{E_\mu}=M_{E_\tau}=M_E\). The corresponding UV boundary at the same matching scale must be

\[
\boxed{
\lambda_{HS}^{>}(\mu_M)
=+\frac{1}{8\pi^2}
\sum_{\ell=\mu,\tau}|y_\ell|^2|\lambda_\ell|^2.
}
\]

This choice makes the *matched dimension-four EFT portal parameter* vanish at \(\mu_M\) to the displayed order. It is a boundary-condition choice that cancels the finite threshold; it is not a cancellation predicted without input and should not be described as technically automatic.

The comparison case remains:

\[
\lambda_{HS}^{>}(\mu_M)=0
\quad\Longrightarrow\quad
\lambda_{HS}^{<}(\mu_M)=\Delta\lambda_{HS}^{E}<0
\]

for nonzero Yukawa products. Thus “zero UV portal” and “zero matched EFT portal” are distinct assumptions and must not be used interchangeably.

If \(M_{E_\mu}\ne M_{E_\tau}\), do not apply the summed formula as if both thresholds were at one common mass: match sequentially at the respective heavy thresholds and run between them.

### 2.3 What is and is not fixed by this choice

The matching-scale reference condition is now explicit, but the following are not yet calculated:

1. The RG evolution from an arbitrary UV scale \(\mu_0\) to \(\mu_M\):
   \[
   \lambda_{HS}^{>}(\mu_M)
   =\lambda_{HS}^{>}(\mu_0)
   +\int_{\ln\mu_0}^{\ln\mu_M}\beta_{HS}^{>}(\mu)\,d\ln\mu.
   \]
2. The EFT evolution from \(\mu_M\) to the electroweak scale:
   \[
   \lambda_{HS}^{<}(\mu_R)
   =\lambda_{HS}^{<}(\mu_M)
   +\int_{\ln\mu_M}^{\ln\mu_R}\beta_{HS}^{<}(\mu)\,d\ln\mu.
   \]
3. Other finite thresholds, nonzero kinetic mixing, the complete broken-phase scalar pole equation, and the constraints on the resulting scalar sector.

Consequently, \(\lambda_{HS}^{<}(\mu_M)=0\) is a defined matching benchmark, not yet proof that the physical Higgs–singlet mixing is negligible at \(p^2=m_h^2\).

## 3. Zero-momentum threshold, finite momentum, and EFT soft terms

### 3.1 Sign convention and no-double-counting rule

RC-001 §274 uses

\[
\Gamma_{\mathrm{inv}}(p^2)
=p^2\mathbf 1-\mathcal M_{\mathrm{loc}}^2
+\widehat\Pi_{\mathrm{soft}}^{\mathrm{ren}}(p^2).
\]

The effective-potential threshold gives the local Hessian contribution

\[
\delta(\mathcal M_{\mathrm{loc}}^2)_{hs}
=v_hv_s\,\Delta\lambda_{HS}^{E},
\]

while the source-convention hard self-energy satisfies

\[
\boxed{\Pi_{hs}^{F,\mathrm{hard}}(0)
=-v_hv_s\,\Delta\lambda_{HS}^{E}.}
\]

These signs are consistent because the local mass matrix enters the inverse propagator with a minus sign and \(\Pi\) enters with a plus sign.

**No-double-counting rule:** choose one representation.

- **Matched-EFT representation:** absorb \(\Delta\lambda_{HS}^{E}\) into \(\lambda_{HS}^{<}\) and \(\mathcal M_{\mathrm{loc}}^2\); do not add the same \(\Pi_{hs}^{F,\mathrm{hard}}(0)\) again.
- **Explicit-hard-self-energy representation:** keep the hard constant in \(\Pi^{\mathrm{hard}}(0)\); do not also include that same threshold in the local EFT portal parameter.

The same threshold cannot be counted once as a portal coefficient and again as a hard zero-momentum self-energy.

### 3.2 Finite momentum requires a common UV–EFT subtraction

For the fixed unbroken-phase Yukawa sector, RC-001 §248 records

\[
i\Gamma_{\mathrm{hard},\mu}^{(2)}
=\frac{i|C_{5,\mu}|^2}{16\pi^2}
\left[
(-\Delta_{\mathrm{IR}}+L_\mu-2)s+\frac{t}{6}
\right],
\qquad
L_\mu=\ln\frac{M_{E_\mu}^2}{\mu_R^2},
\]

and the corresponding bare EFT soft bubble

\[
i\Gamma_{\mathrm{EFT},\mu}^{\mathrm{bare}}
=\frac{i|C_{5,\mu}|^2s}{16\pi^2}
\left[
\Delta_{\mathrm{UV}}
-\ln\frac{-s-i0}{\mu_R^2}+2
\right].
\]

After the method-of-regions pole cancellation, their sum contains the finite nonlocal logarithm and local \(t/6\) term. The UV and EFT expressions must use the same external-state, momentum, IR, and renormalization conventions. The labels \(\Delta_{\mathrm{IR}}\) and \(\Delta_{\mathrm{UV}}\) must be kept distinct until the region subtraction is performed.

In the broken-phase two-point calculation, the EFT side must include all same-order soft insertions and counterterms required by the chosen operator basis—not merely the \(C_5C_5^\ast\) bubble. The RC-001 soft-topology census explicitly keeps the full soft-insertion closure as an acceptance gate. Therefore the zero-momentum portal relation is supported within its recorded scope; it does not close the complete finite-\(p^2\) pole/mixing calculation.

### 3.3 The \(4/3\) difference is not the B1/B3 issue

The source-aligned audit distinguishes the old on-shell four-point representative from the off-shell-completed coefficient set. With

\[
a_\ell=\frac{|y_\ell\lambda_\ell|^2}{16\pi^2M_{E_\ell}^2},
\qquad L_\ell=\ln\frac{M_{E_\ell}^2}{\mu_R^2},
\]

the old representative has

\[
c_{H,\ell}^{\mathrm{old}}=c_{S,\ell}^{\mathrm{old}}
=a_\ell\left(L_\ell-\frac{13}{6}\right),
\qquad
c_{D,\ell}^{\mathrm{old}}=\frac{a_\ell}{2}(L_\ell-2).
\]

The off-shell/EOM-completed representative in source §301 is

\[
c_{H,\ell}^{\mathrm{off/EOM}}
=c_{S,\ell}^{\mathrm{off/EOM}}
=a_\ell\left(L_\ell-\frac32\right),
\qquad
c_{D,\ell}^{\mathrm{off/EOM}}
=\frac{a_\ell}{2}\left(L_\ell-\frac23\right).
\]

Each of \(c_H,c_S,c_D\) shifts by \(+2a_\ell/3\), while the EOM-reduced combination

\[
c_D-\frac12(c_H+c_S)
\]

is invariant. Source §301 records the off-shell external-leg-square terms and the required EOM completion, and the corresponding algebra audits pass. This resolves the comparison between the **old on-shell representative** and the **off-shell-completed/two-point representative** in the stated operator basis.

It does **not** settle the historical B1/B3 path-kernel issue: that candidate kernel has not been mapped term by term to the full §248/§252 amplitude, soft subtraction, and common operator basis.

## 4. B1/B3 candidate kernel: item-by-item evidence comparison

### 4.1 Historical artifacts and exact scope

The candidate kernel is confined to the immutable historical v66 archive:

| Artifact | Blob SHA | What the recorded check establishes | What it does not establish |
|---|---|---|---|
| [`audit_pathwise_wick_kernel.py`](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/artifacts/higgs-portal-v66-20261019/%E8%AE%A1%E7%AE%97%E8%84%9A%E6%9C%AC/audit_pathwise_wick_kernel.py) | `2a7ac2ba589fa99e982c63cb87bcf448c64c8047` | The 32 path records satisfy the script's declared B1/B3 sign-flip and unchanged-B2 algebra | Does not determine physical signs; omits the complete labeled external-leg sum, pathwise denominator integration, and EFT subtraction |
| [`verify_numerator_to_B_kernel.py`](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/artifacts/higgs-portal-v66-20261019/%E8%AE%A1%E7%AE%97%E8%84%9A%E6%9C%AC/verify_numerator_to_B_kernel.py) | `304186f8bc70821254c550a88e376615385a0afd` | Reconstructs the stated \(f_{ij},g,d_\alpha\) polynomials and confirms the **old kernel's internal algebra** | Explicitly does not verify the overall Minkowski diagram sign |
| [`audit_minkowski_wick_signs.py`](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/artifacts/higgs-portal-v66-20261019/%E8%AE%A1%E7%AE%97%E8%84%9A%E6%9C%AC/audit_minkowski_wick_signs.py) | `3063ed03c6de1aacd4094c9ef7a809dff0ce9886` | Applies \(J_{M,r}^{(n)}=i(-1)^{n+r}I_{E,r}^{(n)}\) under its stated metric/denominator convention | Takes the numerator coefficients as inputs; does not derive the complete model-specific amplitude |
| [`derive_consistent_minkowski_to_euclidean_B.py`](https://github.com/lm846802297-bit/high-energy-theory-research/blob/d6143c2aa15191ac8521e062d90860ba86713f00/artifacts/higgs-portal-v66-20261019/%E8%AE%A1%E7%AE%97%E8%84%9A%E6%9C%AC/derive_consistent_minkowski_to_euclidean_B.py) | `4f17b33d648190a8386cfa98dfc20de76b2de5b2` | Derives the candidate B kernel from the numerator decomposition and Wick rules explicitly listed in that script | Does not independently derive the input numerator, complete all external-leg cycles, or perform EFT subtraction |

The historical source states that the earlier Euclidean denominator \(K_E^2+\Delta_0+\delta\Delta\) was inconsistent with the original Minkowski denominator. Under the stated routing,

\[
D_M=K_M^2-\Delta_0+\delta\Delta,
\qquad K_M^2=-K_E^2,
\]

so

\[
D_M=-(K_E^2+\Delta_0-\delta\Delta).
\]

For an \(n=4\) denominator, the corrected Euclidean expansion has a \(+4\delta\Delta/(K_E^2+\Delta_0)^5\) linear term. Thus the \(d_\alpha\) convention must be fixed before comparing the B coefficients. A sign change in the denominator shift cannot be ignored, nor can one mechanically flip the entire kernel.

### 4.2 Algebraic comparison of the two recorded B definitions

If the **same** \(d_\alpha\) convention is held fixed, the historical definitions and the kernel derived under the §84 Minkowski/Wick assumptions are

\[
\begin{aligned}
B_{1}^{\mathrm{legacy}}&=H\left(\frac23g_\alpha-2d_\alpha\right),&
B_{1}^{\mathrm{Wick}}&=H\left(-\frac23g_\alpha+2d_\alpha\right),\
B_{2}^{\mathrm{legacy}}&=\frac13F_\alpha-\frac23S\,d_\alpha,&
B_{2}^{\mathrm{Wick}}&=\frac13F_\alpha-\frac23S\,d_\alpha,\
B_{3}^{\mathrm{legacy}}&=-\frac23M\,d_\alpha,&
B_{3}^{\mathrm{Wick}}&=+\frac23M\,d_\alpha.
\end{aligned}
\]

The algebraic relation is \(B_1^{\mathrm{Wick}}=-B_1^{\mathrm{legacy}}\), \(B_2^{\mathrm{Wick}}=B_2^{\mathrm{legacy}}\), and \(B_3^{\mathrm{Wick}}=-B_3^{\mathrm{legacy}}\) **under that fixed-\(d_\alpha\) comparison**. This is what the new exact symbolic check reproduces.

It is not a physical verdict. The \(d_\alpha\) coefficients are defined by the denominator shift; they must be regenerated from the same routed Minkowski denominators and then carried through the same Wick rotation as the numerator. The §84 script assumes its displayed numerator decomposition and does not establish that the coefficients \(F_\alpha,H,S,M\) are the exact result of the complete model-specific trace and vertex mapping.

### 4.3 Comparison against the source-aligned §248/§252 matching

| Matching layer | Historical B1/B3 path calculation | Source-aligned §248/§252 calculation | Reconciliation status |
|---|---|---|---|
| External fields | Broken-phase real \(h,s\) fields; mass-eigenstate Yukawa matrices | Unbroken-phase fixed complex legs \(H,S,H^\dagger,S^\dagger\), followed by a separate off-shell/EOM completion | **Not mapped term by term.** The real-field permutations and the complex-field projection need an explicit common-basis map |
| Internal states/topology | Two vertex-type patterns with 16 internal mass paths each; later six labeled external cycles | One connected UV 1PI box for the fixed complex external legs at the stated Yukawa order, plus its EFT \(C_5C_5^\ast\) bubble | Topological equivalence and multiplicities have not been proven in a shared labeled-amplitude ledger |
| Numerator | \(H,C_{ij},M\) and \(f,g,d_\alpha\) decomposition; selected-path and fixed-rational-point trace checks exist | Explicit fixed-sector numerator \(2M_E^2\,k\cdot(k-q)\) under the stated chiral routing, with hard expansion | The full mass-basis path sum has not been analytically reduced to the §248 numerator with all phases, conjugations, and external-leg permutations |
| Denominators | Path-specific \(\Delta_{0,\rho}(x)=\sum_i x_i m_{\mathrm{edge},i}^2\); candidate integrands were generated | Fixed-route UV denominator \(k^2(k-q)^2[(k-p_2)^2-M_E^2][(k+p_4)^2-M_E^2]\), expanded in the hard region | No exact route-by-route identity between the path denominators and the fixed-route hard expansion is recorded |
| Wick rotation and loop prefactor | Separate sign ledgers exist, but the candidate numerator-to-kernel chain retains assumptions; historical denominator-shift conventions differ | §248 gives the hard/soft local subtraction under its declared \(i\Gamma\), PV, and \(\overline{\mathrm{MS}}\) conventions | The common loop phase, fermion-loop sign, reversed cycles, and symmetry factors have not been closed in one calculation |
| UV/IR poles | Candidate path integration does not perform the complete EFT subtraction or counterterm closure | §248 explicitly separates the hard IR pole from the EFT soft UV pole and cancels them by regions | Cannot compare candidate finite integrals directly with the matched coefficient |
| Finite terms | Numerical path projections are candidate-kernel diagnostics; earlier outputs omit the final common loop and/or graph factors and are not matched coefficients | §248 gives the conditional hard local polynomial; §252 adds off-shell external-leg-square terms and EOM completion | No common-basis, same-IR-prescription finite-term equality has been demonstrated |
| Diagram-package validation | No complete current FeynArts/FeynCalc run is recorded | The source record explicitly says the FeynArts/FeynCalc scaffold remains unrun | **Open** |

### 4.4 What the existing checks do establish

1. The geometric \(f_{ij}\), \(g_\alpha\), and \(d_\alpha\) polynomial identities can be checked algebraically for the declared routing.
2. The historical B1/B3 script verifies the sign map it was written to test; it does not derive the physical sign from the complete model amplitude.
3. The Minkowski/Wick script checks termwise signs for its declared numerator decomposition; it does not independently derive that decomposition from every model-specific path.
4. The old pathwise integration records explicitly lack the full labeled external-leg sum, loop/symmetry-factor audit, EFT subtraction, counterterms, and final operator projection.
5. The current source-aligned two-point audit reproduces 15 exact symbolic/algebraic checks, including the leading portal sign and the historical \(4/3\) difference. Source §301 reconciles that \(4/3\) difference with the off-shell/EOM completion. This does not supply the missing B1/B3-to-§248 map.

### 4.5 Decision on B1/B3

**Status: unresolved; do not promote either candidate kernel to the final Wilson coefficient.**

The working dimension-six result should continue to be quoted only with the scope and caveats of the source-aligned §248/§252 ledger and the live CL-001 claim. The historical B1/B3 calculation is a diagnostic branch, not an accepted independent derivation of that coefficient. The evidence does not yet justify calling it physically wrong, nor does it justify declaring it superseded by a proven term-by-term identity.

Required closure steps:

1. Choose one labeled external cycle and derive its complete mass-basis Dirac trace from the actual \(G_h,G_s\) vertices, including conjugation and the parity-odd trace terms.
2. Substitute \(k_i=K+t_i\), retain all terms through second order in external momenta, and derive \(F_\alpha,H,S,M\) and \(d_\alpha\) in one Minkowski convention without taking those coefficients as inputs.
3. Repeat for all six labeled external cycles, retain each path-dependent \(\Delta_{0,\rho}\), and independently determine the fermion-loop sign, reversed-cycle relation, and graph/symmetry factors.
4. Map the resulting sum to the same complex external states and momentum basis used in §248/§252, including the off-shell \(\Sigma=\sum_i p_i^2\) terms and EOM-generated potential/source companions.
5. Subtract the complete same-order EFT soft amplitudes and counterterms in the same IR and renormalization prescription, then compare poles and finite local terms separately.
6. Only after the analytic mapping passes should the corresponding FeynArts/FeynCalc calculation be executed and archived. A successful algebra-only script is not a substitute for this diagram-level check.

## 5. Reproducible algebra check

The companion script is [`calculations/RC-001-portal-boundary-b1b3-reconciliation.py`](../calculations/RC-001-portal-boundary-b1b3-reconciliation.py). Its captured output is [`validation/RC-001-portal-boundary-b1b3-reconciliation.txt`](../validation/RC-001-portal-boundary-b1b3-reconciliation.txt).

The script runs 14 exact symbolic checks covering:

- the portal matching relation and the two distinct boundary choices;
- the potential-Hessian/1PI sign relation;
- the §301 \(2a_\ell/3\) EOM completion and invariant reduced derivative combination;
- the algebraic B1/B3 sign map at fixed \(d_\alpha\), with B2 unchanged;
- the corrected Minkowski-to-Euclidean denominator shift and its \(n=4\) linear expansion;
- the fixed-sector hard/soft pole-residue and finite-log bookkeeping.

**Scope limitation:** these checks do not integrate loop functions, reconstruct the full model-specific numerator, sum all labeled external legs, complete all EFT soft insertions/counterterms, or run FeynArts/FeynCalc.


## 6. Independent trace, six-cycle, and normalization audit (2026-10-27)

### 6.1 New executable evidence

The following new audit artifacts are on this PR branch:

- [Generic trace, six-cycle routing, and normalization script](../calculations/RC-001-six-cycle-trace-normalization-audit.py)
- [Trace/normalization execution log](../validation/RC-001-six-cycle-trace-normalization-audit.txt)
- [Symbolic six-cycle O(p^2) candidate-kernel ledger script](../calculations/RC-001-six-cycle-oq2-candidate-kernel-ledger.py)
- [O(p^2) candidate-kernel execution log](../validation/RC-001-six-cycle-oq2-candidate-kernel-ledger.txt)
- [Fixed-sector hard/soft pole ledger script](../calculations/RC-001-fixed-sector-hard-soft-pole-ledger.py)
- [Fixed-sector hard/soft pole ledger output](../validation/RC-001-fixed-sector-hard-soft-pole-ledger.txt)
- [C5 C5* soft-bubble trace audit script](../calculations/RC-001-C5-soft-bubble-trace-audit.py)
- [C5 C5* soft-bubble trace audit output](../validation/RC-001-C5-soft-bubble-trace-audit.txt)

The trace audit uses the model matrices

\[
Y_h=a\begin{pmatrix}c_Ls_R&c_Lc_R\\s_Ls_R&s_Lc_R\end{pmatrix},
\qquad
Y_s=b\begin{pmatrix}s_Lc_R&-s_Ls_R\\-c_Lc_R&c_Ls_R\end{pmatrix},
\]

and the declared real-Yukawa vertex convention \(V_{ij}=Y_{ij}P_R+Y_{ji}P_L\). It tests all six labeled cycles and all 16 internal-state paths at exact rational routed Minkowski momenta, comparing an explicit 4-by-4 Dirac trace with the projector decomposition. The test passes for 96/96 cycle-path cases.

The second script additionally derives the generic trace identity symbolically for arbitrary \(u_i,v_i,m_i,k_i\), then constructs the model-specific \(H_\rho,C_{ij}^{(\rho)},S_\rho,M_\rho\), route-specific \(f_{ij,\alpha},g_\alpha,d_\alpha,\Delta_{0,\rho}\), and conditional \(B^{(1,2,3)}\) coefficients in the common external-invariant basis. It emits 576 rows: 6 labeled cycles × 16 internal paths × 6 invariants.

### 6.1.1 Positive-light-mass versus signed-light-mass convention

There are two displayed vertex-matrix conventions in the frozen v153 source, and they must not be mixed without the corresponding chiral rephasing.

The Eq. (13) matrices used by the six-cycle candidate kernels are

\[
Y_h=a\begin{pmatrix}c_Ls_R&c_Lc_R\\s_Ls_R&s_Lc_R\end{pmatrix},
\qquad
Y_s=b\begin{pmatrix}s_Lc_R&-s_Ls_R\\-c_Lc_R&c_Ls_R\end{pmatrix}.
\]

The real-rotation, signed-light-mass convention in v153 §276 instead gives

\[
G_h=a\begin{pmatrix}-c_Ls_R&c_Lc_R\\-s_Ls_R&s_Lc_R\end{pmatrix},
\qquad
G_s=b\begin{pmatrix}-s_Lc_R&-s_Ls_R\\c_Lc_R&c_Ls_R\end{pmatrix}.
\]

They obey the exact matrix identities

\[
G_h=Y_hD,\qquad G_s=Y_sD,\qquad D=\operatorname{diag}(-1,1).
\]

This is the right-handed light-state rephasing associated with switching between the positive-light-mass convention and the signed-light-mass convention. The new trace/normalization script checks these identities symbolically.

The six-cycle candidate ledger uses the Eq. (13) matrices and positive mass symbols in its propagator denominators. The §276 two-point formula keeps the signed light eigenmass in chirality-flip numerators. A comparison between these routes is valid only after the vertex rephasing and the sign of the mass-flip terms are transformed consistently. The matrix identity alone does not prove the full loop amplitudes equal; it removes an avoidable convention ambiguity from the next matching step.

### 6.2 Six labeled cycles and reverse-loop counting

Fixing \(h_1\) as the representative start point leaves

\[
\frac{4!}{4}=6
\]

inequivalent cyclic orderings. The three reverse pairs are already included among these six orderings. The path-level audit checks 48 reverse path pairs, and the O(p²) candidate-kernel audit checks 1,152 exact coefficient comparisons after the path map, Feynman-parameter permutation, and simplex constraint.

This supports the following bookkeeping rules:

- count each of the six labeled cycles once;
- do not sum all six cycles and then multiply by an extra factor of two for loop reversal;
- retain the 16 path-dependent mass denominators until the parameter integrations or a proven symmetry reduction justify combining them.

The reverse-kernel checks prove consistency of the generated candidate kernels under the declared mapping. They do not independently establish the physical global loop sign.

### 6.3 \(\Gamma(4)\), simplex normalization, and the fermion-loop sign

The four-propagator Feynman-parameter identity contributes

\[
\frac{\Gamma(4)}{\prod_{i=1}^4\Gamma(1)}=\Gamma(4)=6,
\]

while the standard four-parameter simplex has volume \(1/6\). Their product is one. Therefore the factor of six must be included exactly once: if the integral is written with the explicit Feynman-parameter prefactor, do not also normalize the simplex average by six a second time.

The audit also checks the five convergent Euclidean scalar-integral factors used in the candidate-kernel reduction:

\[
I_0^{(4)}=\frac{1}{6\Delta^2},\quad
I_1^{(4)}=\frac{1}{3\Delta},\quad
I_2^{(5)}=\frac{1}{4\Delta},\quad
I_1^{(5)}=\frac{1}{12\Delta^2},\quad
I_0^{(5)}=\frac{1}{12\Delta^3},
\]

each in units of \(1/(16\pi^2)\).

For the effective-action convention \(\Gamma_f=-i\,\mathrm{Tr}\ln(1+X)\), the fourth-order determinant-log coefficient is \(+i/4\). The closed-fermion-loop factor \(-1\) in diagrammatic Feynman rules is a separate bookkeeping item. The audit records both conventions but does not claim to have reconciled them with all four vertex factors, propagator factors, loop integration, and the final common Minkowski/Wick phase. The overall diagrammatic \(i\) and sign therefore remain open.

### 6.4 What has and has not been established

| Layer | Status | Evidence boundary |
|---|---|---|
| Generic chiral Dirac trace | **Verified symbolically** | Exact identity for arbitrary chiral coefficients, masses, and four independent Minkowski momenta |
| All six cycles × 16 paths | **Verified at numerator/weight level** | 96 exact rational-point direct-trace comparisons; model-specific weights are assembled symbolically |
| Routed \(O(p^2)\) candidate coefficients | **Generated and cross-checked** | 576 symbolic rows; reverse-cycle coefficient map passes 1,152/1,152 checks |
| \(\Gamma(4)\), simplex volume, five Euclidean integral factors | **Verified algebraically** | Exact Gamma-function identities |
| Determinant-log \(+i/4\) and diagrammatic \(-1\) | **Recorded separately** | Their complete Feynman-rule/Wick reconciliation is still open |
| Path-dependent simplex integrals | **Not completed** | The generated CSV is a candidate-integrand ledger, not an integrated Wilson coefficient |
| Complete EFT soft diagrams and counterterms | **Not completed** | See §7; the existing two-point audit is not a substitute for full four-scalar matching |
| Final UV–EFT Wilson coefficient | **Not established** | No final coefficient or exclusion claim is promoted |

The O(p²) CSV generated by the script has SHA-256 2a11b12173f983d2055f9ef6ba556e3d64bb042ef057a0f5145232065c14c181 and 990,656 bytes. It is not committed separately; the script regenerates it.

## 7. EFT soft terms, counterterms, and UV–EFT subtraction: remaining closure gate

The repository already contains a source-aligned two-point audit ([script](../calculations/RC-001-uv-eft-two-point-difference.py), [captured result](../validation/RC-001-uv-eft-two-point-difference.txt)) with 15 exact symbolic/algebraic checks. Those checks cover the specified \(h\)-\(s\) two-point kernel, its EFT bubble/contact pole bookkeeping, the local counterterm cancellation within that kernel, and the finite \(p^2=0\) hard-minus-soft expression.

The separate soft-topology census ([script](../calculations/RC-001-eft-soft-topology-census.py), [research note](RC-001-eft-soft-topology-census.md), [captured result](../validation/RC-001-eft-soft-topology-census.txt)) explicitly says that the \(C_5C_5^\ast\) bubble has an existing soft integral but still needs an independent graph-level check. The census is a structural/power-counting audit, not a complete diagrammatic evaluation.

The new [fixed-sector hard/soft pole ledger](../calculations/RC-001-fixed-sector-hard-soft-pole-ledger.py) passes 12 exact symbolic checks. It keeps the hard-region IR pole and bare EFT soft-loop UV pole separately labeled, verifies their opposite residues in the method-of-regions sum, checks the local counterterm against the soft UV pole, and records the finite hard polynomial \((L-2)s+t/6\) in the source normalization. It also repeats the existing two-point bubble/contact and derivative-counterterm pole identities. This is a stronger fixed-sector bookkeeping check, but it still does not evaluate the full same-order four-scalar EFT soft-graph set or integrate the six-cycle kernels.

The new [C5 C5* soft-bubble trace audit](../calculations/RC-001-C5-soft-bubble-trace-audit.py) passes 10 exact symbolic checks. It independently computes the massless chiral trace, reduces the numerator to the scalar B0 bubble using scaleless-tadpole vanishing, multiplies the two vertices, two propagators, and closed-loop sign, and checks the soft UV counterterm and §248 hard/soft pole cancellation. This validates the algebra of the specified SFT-01 bubble under the recorded B0 convention; it does not independently generate the full EFT graph set or integrate the six-cycle UV candidate kernels.

Accordingly, the fourth requested stage is **not yet complete**. Before promoting any B1/B3 kernel to a physical Wilson coefficient, the remaining work is:

1. derive the complete set of EFT soft graphs and same-order insertions for the selected four-scalar 1PI amplitude from the operator basis, rather than relying only on a topology classification;
2. calculate each graph in the same IR prescription and renormalization scheme as the UV amplitude;
3. include the required local counterterms and keep UV and IR poles labeled separately until subtraction;
4. compare UV and EFT pole residues term by term, then compare the finite local \(O(p^2)\) coefficients in the same external-invariant and operator basis;
5. complete the loop/symmetry-factor and common \(i\)-sign reconciliation, and independently verify the result with FeynArts/FeynCalc or an equivalent diagram-level calculation.

Until those gates pass, the B1/B3 result remains a **conditional candidate-kernel result**, not the final physical matching coefficient. No manuscript result, formal response, or exclusion statement should be changed on the basis of this audit.

## 8. Archiving decision and change control

- Keep the v66 archive unchanged as historical evidence.
- Keep the B1/B3 candidate scripts in the research repository only; **do not copy them into `axial-vector-review-response`** while their physical sign and matching status remain unresolved.
- The existing [review-response PR #7](https://github.com/lm846802297-bit/axial-vector-review-response/pull/7) remains Draft and unmerged. Its evidence note is not a substitute for this calculation ledger.
- Do not change the formal response letter, manuscript PDF, v5.6 task checkboxes, or final physical conclusions on the basis of this audit.
- This ledger and its algebra check are a dated supplement on a separate research branch. They do not replace the frozen v153 baseline or assert complete model-level Wilson-vector closure.
