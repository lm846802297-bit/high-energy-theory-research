# RC-001 — UV five-point Lorentz endpoint audit: fermion lines, scalar seagulls, and the three-W chain

**Workstream:** RC-001-WW-UV-FF-02, Stage B2c-IVc  
**Status:** the Lorentz contractions of both oriented fermion-line insertions, both scalar-line insertions together with their seagulls, the bare three-W vertex, and the Feynman-gauge propagator chain have been checked exactly. The six-pair topology census is mapped to these endpoint classes. This is an exact **Lorentz endpoint audit**, not yet the full weak-index/phase-weighted 24-graph sum. In particular, no cancellation of the matter-line terms against the three-W graph is claimed.

## 1. Fixed routing variables and scope

Retain the external-W routing used in the Stage-B2c numerator templates:
\[
r_A^W=r_A,\qquad r_A^Y=r_A-q,
\]
\[
r_B^W=r_B,\qquad r_B^Y=r_B+q.
\]
Define
\[
\Delta(r)=\frac1{r^2},\qquad
G_F(r)=\frac{\slashed r}{r^2}.
\]
The labels \(W,Y\) refer to the two segments adjacent to the internal-W and Yukawa ends, respectively. The A and B line orientations are opposite.

The present audit factors out the common four-point skeleton and checks the Lorentz endpoint functions. It does not independently regenerate every weak-index matrix product, every external momentum-conservation equation, or every heavy propagator denominator in the five-point diagrams. Those remain separate inputs to the complete graph sum.

## 2. Fermion-line longitudinal contractions

For the A orientation, the stripped numerator is
\[
N_{A,F}^\alpha
=(-\slashed r_A^W)\gamma^\alpha(-\slashed r_A^Y).
\]
Using \(r_A^W-r_A^Y=q\),
\[
\frac{q_\alpha N_{A,F}^\alpha}
{(r_A^W)^2(r_A^Y)^2}
=
\frac{\slashed r_A^Y}{(r_A^Y)^2}
-\frac{\slashed r_A^W}{(r_A^W)^2}.
\]
Thus
\[
\boxed{
\mathcal W_{A,F}
=G_F(r_A^Y)-G_F(r_A^W).
}
\tag{2.1}
\]

For the B orientation,
\[
N_{B,F}^\alpha
=\slashed r_B^Y\gamma^\alpha\slashed r_B^W,
\]
and \(r_B^Y-r_B^W=q\) gives
\[
\boxed{
\mathcal W_{B,F}
=G_F(r_B^W)-G_F(r_B^Y).
}
\tag{2.2}
\]
Both identities are exact off shell. The numerator/denominator identities are checked as \(4\times4\) Dirac-matrix identities for generic symbolic \(r,q\), not only at the exceptional local projection.

When restoring the chiral projectors, use the oriented propagator WTIs from Stage B2c-I/II. Equations (2.1)–(2.2) display the reduced numerator functions after the common chiral chain has been factored out.

## 3. Scalar-line and seagull longitudinal contractions

For the scalar-line numerators used in the fixed routing,
\[
q\cdot(r_A^W+r_A^Y)
=(r_A^W)^2-(r_A^Y)^2,
\]
\[
q\cdot(r_B^W+r_B^Y)
=(r_B^Y)^2-(r_B^W)^2.
\]
Therefore the ordinary scalar-line insertions reduce to
\[
\boxed{
\mathcal W_{A,S}
=\Delta(r_A^Y)-\Delta(r_A^W),
}
\tag{3.1}
\]
\[
\boxed{
\mathcal W_{B,S}
=\Delta(r_B^W)-\Delta(r_B^Y).
}
\tag{3.2}
\]

These are not the complete scalar endpoint contributions. The scalar seagull has
\[
V_{\rm sg}^{ab,\alpha\mu}
=ig_2^2\{t^a,t^b\}g^{\alpha\mu},
\qquad
q_\alpha V_{\rm sg}^{ab,\alpha\mu}
=ig_2^2\{t^a,t^b\}q^\mu.
\]
Using the relative phases of the Stage-B2c Feynman-rule ledger (ordinary line insertion \(-g_2\), seagull replacement \(+g_2\)), and retaining the internal scalar-current vectors
\[
V_A^\mu=2p_A^\mu-k^\mu,\qquad
V_B^\nu=-2p_B^\nu-k^\nu,
\]
the phase-weighted Lorentz combinations are
\[
\boxed{
\mathcal S_A^\mu
=g_2\left[
\Delta(r_A^W)V_A^\mu
-\Delta(r_A^Y)(V_A^\mu-q^\mu)
\right],
}
\tag{3.3}
\]
\[
\boxed{
\mathcal S_B^\nu
=g_2\left[
\Delta(r_B^Y)(V_B^\nu+q^\nu)
-\Delta(r_B^W)V_B^\nu
\right].
}
\tag{3.4}
\]
The equations are stated after factoring the common four-point skeleton and the corresponding weak tensor. They are vector identities, not just scalar propagator identities. In particular, the \(q^\mu\) pieces are retained.

The A and B forms differ because the scalar propagator momenta have opposite orientations. Replacing both by one common sign convention would lose the endpoint information needed for the three-W comparison.

## 4. Three-W contraction and the Feynman-gauge remainder

For all incoming momenta \((q,k,-k-q)\), define
\[
\Gamma_{\alpha\mu\nu}
=g_{\alpha\mu}(q-k)_\nu
+g_{\mu\nu}(2k+q)_\alpha
+g_{\nu\alpha}(-k-2q)_\mu.
\]
Then
\[
\boxed{
q^\alpha\Gamma_{\alpha\mu\nu}
=\mathcal K_{\mu\nu}(k+q)-\mathcal K_{\mu\nu}(k),
}
\tag{4.1}
\]
where
\[
\mathcal K_{\mu\nu}(k)=k^2g_{\mu\nu}-k_\mu k_\nu.
\]

For clarity, the index positions in the Feynman-gauge chain are
\[
D^{\mu\alpha}(k+q)
\left[\mathcal K_{\alpha\beta}(k+q)-\mathcal K_{\alpha\beta}(k)\right]
D^{\beta\nu}(k),
\qquad
D^{\mu\nu}(k)=\frac{g^{\mu\nu}}{k^2}.
\]
The exact decomposition is
\[
\boxed{
D^{\mu\alpha}(k+q)\Delta\mathcal K_{\alpha\beta}D^{\beta\nu}(k)
=
D^{\mu\nu}(k)-D^{\mu\nu}(k+q)
+R_{\rm FG}^{\mu\nu},
}
\tag{4.2}
\]
with
\[
\boxed{
R_{\rm FG}^{\mu\nu}
=\frac{k^\mu k^\nu-(k+q)^\mu(k+q)^\nu}
{k^2(k+q)^2}.
}
\tag{4.3}
\]
The remainder is generically nonzero. For example, with metric signature \(+---\), \(k=(3,2,0,0)\) and \(q=(1,0,1,0)\),
\[
R_{\rm FG}^{\mu\nu}
=\frac1{55}
\begin{pmatrix}
-7&-2&-4&0\\
-2&0&-2&0\\
-4&-2&-1&0\\
0&0&0&0
\end{pmatrix}.
\]
This numerical point is only a non-vanishing diagnostic; the symbolic matrix identity (4.2) is the actual check.

Do not drop \(R_{\rm FG}\), and do not identify it by itself with a ghost-loop contribution. It is the remainder generated when the transverse Yang–Mills inverse kernel is sandwiched between ordinary Feynman-gauge propagators. Its role must be settled in the full gauge-fixing/Slavnov–Taylor bookkeeping.

## 5. Six-pair Lorentz endpoint census

The attachment classes map to the following line types:

| Pair | A endpoint | B endpoint | Matter-line insertions | Scalar seagulls | Three-W |
|---|---|---|---:|---:|---:|
| LD-W-01 | F | F | 2 | 0 | 1 |
| LD-W-02 | F | S | 2 | 1 (B) | 1 |
| LD-W-03 | F | S | 2 | 1 (B) | 1 |
| LD-W-04 | S | F | 2 | 1 (A) | 1 |
| LD-W-05 | S | F | 2 | 1 (A) | 1 |
| LD-W-06 | S | S | 2 | 2 (A and B) | 1 |
| **Total** |  |  | **12** | **6** | **6** |

Here F denotes a fermion endpoint and S a scalar endpoint. The table reproduces the 24 internal attachment topologies in the existing census:
\[
12\text{ matter-line insertions}
+6\text{ scalar seagulls}
+6\text{ three-W insertions}=24.
\]
This is a topology count, not a FeynArts/QGRAF-generated diagram count.

For a cross-vertex pair, the Lorentz endpoint factors (2.1)–(3.4) multiply the appropriate heavy-line numerator and the opposite endpoint current. The three-W term multiplies the two internal-W propagators and the shifted matter current at the second W endpoint. For LD-W-03/04, the heavy propagator is a spectator external-channel propagator in the four-point seed; its momentum in each five-point attachment must be fixed by the actual all-incoming momentum conservation at the corresponding Yukawa vertex.

## 6. Routing gate for the same-vertex pairs LD-W-03/04

The four-point same-vertex routing is
\[
r_F=k+p_1,\qquad r_S=p_2-k,\qquad r_F+r_S=P=p_1+p_2
\]
for LD-W-03, with the conjugate right-vertex routing for LD-W-04.

An external W inserted on one of the matter propagators changes the momentum entering the Yukawa vertex and therefore changes the heavy-channel momentum. In a three-W insertion, the two internal-W legs carry momenta differing by \(q\); consequently one of \(r_F,r_S\) is shifted while the other is not. The heavy momentum must be reconstructed from their sum for that specific orientation.

Accordingly, the earlier schematic statement that every attachment in LD-W-03/04 carries the same \((P_{FS}+q)^2-M_E^2\) denominator is **not used as an input to this audit**. It requires a graph-by-graph momentum-conservation derivation, especially for the three-W insertion. The present script checks only the Lorentz endpoint identities and does not validate that heavy denominator assignment.

## 7. Reproduction and evidence boundary

The exact local audit is in
calculations/RC-001-dim6-WW-fivepoint-Lorentz-endpoint-audit.py
with captured output in
validation/RC-001-dim6-WW-fivepoint-Lorentz-endpoint-audit.txt.

It checks:
- A/B fermion numerator differences: 16/16 Dirac components each;
- A/B scalar propagator differences: 2/2;
- A scalar-line plus seagull vector identity: 4/4 Lorentz components;
- B scalar-line plus seagull vector identity: 4/4 Lorentz components;
- three-W contraction: 16/16 Lorentz components;
- Feynman-gauge propagator chain including \(R_{\rm FG}\): 16/16 components;
- non-vanishing of \(R_{\rm FG}\) at a generic rational diagnostic point;
- six-pair topology census: 12+6+6=24.

This does **not** establish:
1. the raw weak-index matrix ordering of every five-point graph;
2. the phase-weighted sum of the matter-line commutator pieces with the three-W graph;
3. cancellation of \(D(k)-D(k+q)\) against the shifted matter endpoint terms after a common loop-momentum routing;
4. the complete scalar-line/seagull/three-W sum for each pair;
5. the same-vertex LD-W-03/04 heavy-channel routing for every attachment;
6. the gauge-fixing/ghost Slavnov–Taylor completion;
7. external-leg/LSZ and counterterm completion;
8. any integrated five-point hard coefficient or transverse form factor.

The next step is not a new hard integral. First derive the raw weak-index order and the exact shifted heavy/light momenta for each graph, then place the Lorentz endpoint expressions above over a common loop variable and perform the pairwise matter-line plus three-W sum. Only after that algebra closes should the UV and EFT five-point hard/soft integrals be evaluated.
