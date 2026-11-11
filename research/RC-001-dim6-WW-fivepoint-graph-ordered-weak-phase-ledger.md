# RC-001 — Signed-action weak algebra and provisional graph-order map

**Workstream:** RC-001-WW-UV-FF-02, Stage B2c-III  
**Status:** the SU(2) signed-action commutator and scalar-seagull identities are checked exactly, and the relative Feynman-rule phases are fixed in Stage B2c-I/II. However, the mapping of these signed actions to the raw weak-index matrix products of every oriented five-point Feynman graph is **not yet independently closed**. The ordering labels below are therefore a provisional WTI-basis ledger, not a claim that the complete graph weak tensors have already been derived.

## 1. Pair endpoints and seed tensors

For the all-incoming ordering \((\bar L_i,H_j,H^\dagger_k,L_l)\), use the signed external-index actions \(\mathscr T_r^a\) defined in the Stage-B2b weak-ordering audit. The seed pair tensor is
\[
\mathcal T_{AB}=\sum_b\mathscr T_A^b\mathscr T_B^bT_0,
\qquad
T_0=\delta_{ij}\delta_{kl},
\qquad
T_3=\sigma^I_{ij}\sigma^I_{kl}.
\]

| Pair | A endpoint | B endpoint | \(\mathcal T_{AB}\) |
|---|---|---|---|
| LD-W-01 | \(\bar L\) | \(L\) | \(-T_3/4\) |
| LD-W-02 | \(\bar L\) | \(H^\dagger\) | \(+T_3/4\) |
| LD-W-03 | \(\bar L\) | \(H\) | \(-3T_0/4\) |
| LD-W-04 | \(L\) | \(H^\dagger\) | \(-3T_0/4\) |
| LD-W-05 | \(H\) | \(L\) | \(+T_3/4\) |
| LD-W-06 | \(H\) | \(H^\dagger\) | \(-T_3/4\) |

The six seed projections are reproduced component by component (96/96).

## 2. Candidate ordered tensors in the signed-WTI action basis

The location of the external-W insertion suggests the following ordered products in the signed-action basis:
\[
\mathcal W_{A,\mathrm{cand}}^a
=\sum_b\mathscr T_A^b\mathscr T_A^a\mathscr T_B^bT_0,
\]
\[
\mathcal W_{B,\mathrm{cand}}^a
=\sum_b\mathscr T_A^b\mathscr T_B^a\mathscr T_B^bT_0.
\]
The corresponding reversed products are
\[
\widetilde{\mathcal W}_{A,\mathrm{cand}}^a
=\sum_b\mathscr T_A^a\mathscr T_A^b\mathscr T_B^bT_0,
\]
\[
\widetilde{\mathcal W}_{B,\mathrm{cand}}^a
=\sum_b\mathscr T_A^b\mathscr T_B^b\mathscr T_B^aT_0.
\]
For the signed-action algebra
\[
[\mathscr T_r^a,\mathscr T_r^b]
=-i\epsilon^{abc}\mathscr T_r^c,
\]
the exact relations are
\[
\mathcal W_{A,\mathrm{cand}}^a
-\widetilde{\mathcal W}_{A,\mathrm{cand}}^a
=-i\mathcal G_{AB}^a,
\]
\[
\mathcal W_{B,\mathrm{cand}}^a
-\widetilde{\mathcal W}_{B,\mathrm{cand}}^a
=-i\mathcal G_{AB}^a,
\]
where
\[
\mathcal G_{AB}^a
=\epsilon^{abc}\mathscr T_A^b\mathscr T_B^cT_0.
\]
Each identity is checked for all six pairs, three external-W generators and 16 weak-index components (288/288 for each endpoint).

**Important qualification.** The \(\mathscr T_r^a\) are signed WTI actions, not simply the raw fundamental matrices \(t^a\) at every field slot. For transposed/conjugate slots, composition order can reverse when translated back to a raw matrix chain. Also, a three-generator product changes sign under \(\mathscr T_r=-T_{r,\mathrm{field}}\), whereas the two-generator seed tensor does not. Therefore the pair-projection check alone does not prove that the candidate ordered products above are the exact weak factors of every graph.

The actual mapping must be derived from explicit weak-index contractions at each Feynman vertex, including the fermion-arrow orientation and the \(H\) versus \(H^\dagger\) scalar orientation. Until that is done, the \(-i\mathcal G_{AB}^a\) relations are algebraic identities in the signed-action basis only.

## 3. Scalar-seagull algebra

For \(t^a=\sigma^a/2\),
\[
\{t^a,t^b\}=\frac12\delta^{ab}\mathbf1.
\]
The signed-action algebra consequently gives the candidate endpoint identities
\[
\mathcal S_{A,\mathrm{cand}}^a
=\sum_b\{\mathscr T_A^a,\mathscr T_A^b\}\mathscr T_B^bT_0
=\frac12\mathscr T_B^aT_0,
\]
\[
\mathcal S_{B,\mathrm{cand}}^a
=\sum_b\mathscr T_A^b\{\mathscr T_B^a,\mathscr T_B^b\}T_0
=\frac12\mathscr T_A^aT_0.
\]
The algebraic identities are checked for all scalar endpoints, all external-W generators and all weak-index components (288/288).

This still does not fix the complete graph weak tensor until the seagull's raw \(H^\dagger t^at^bH\) index contraction is mapped to the chosen signed-action convention.

## 4. Feynman-rule phases: fixed, but not yet multiplied by a fully mapped graph tensor

For
\[
D_\mu=\partial_\mu-ig_2t^aW_\mu^a,\qquad
W_{\mu\nu}^a=\partial_\mu W_\nu^a-\partial_\nu W_\mu^a
+g_2\epsilon^{abc}W_\mu^bW_\nu^c,
\]
the phase ratios relative to the four-point skeleton are
\[
\frac{P_{\rm matter\ insertion}}{P_4}=-g_2,\qquad
\frac{P_{\rm seagull}}{P_4}=+g_2,\qquad
\frac{P_{3W}}{P_4}=-ig_2.
\]
These phase ratios are fixed by the explicit Feynman-rule products. They are not sufficient to establish the cancellation until each graph's raw weak-index tensor is translated into the signed-action basis with the correct ordering.

## 5. Required B2c-IV: raw weak-index bridge

The next calculation must not assume the candidate orderings in §2. For each of the 24 graphs:

1. Write the weak indices at the two Yukawa vertices explicitly, starting from \(T_0=\delta_{ij}\delta_{kl}\).
2. Insert the raw matrices \(t^a_{ij}\) at the actual fermion/scalar gauge vertex.
3. Track whether the line is \(L\), \(\bar L\), \(H\), or \(H^\dagger\), including the reversed index order on conjugate fields.
4. Derive the matrix product in the same order as the spinor/scalar propagator chain.
5. Translate that raw tensor into the \(\mathscr T_r^a\) signed-action basis.
6. Only then multiply by the phase ratios in §4 and compare the matter-line commutator with the three-W tensor.

The same raw-index derivation is required for both scalar seagulls. The anticommutator identity is not enough to settle their graph signs.

## 6. Reproduction and evidence boundary

The exact SymPy audit remains in
calculations/RC-001-dim6-WW-fivepoint-graph-ordered-weak-phase-ledger.py
with output in
validation/RC-001-dim6-WW-fivepoint-graph-ordered-weak-phase-ledger.txt.

It establishes the signed-action algebra:
- six pair tensors: 96/96;
- candidate A-order commutator identity: 288/288;
- candidate B-order commutator identity: 288/288;
- candidate scalar-seagull identities: 288/288.

It does **not** establish:
1. the raw weak-index tensor of each five-point Feynman graph;
2. the mapping of each raw tensor to the candidate signed-action order;
3. the Lorentz-weighted matter-line/three-W cancellation;
4. the scalar-line/seagull Lorentz and group sum;
5. the ghost/gauge-fixing Slavnov–Taylor completion;
6. external-leg/counterterm completion or any integrated Wilson coefficient.

The PR must remain Open/Draft until the raw weak-index bridge and the Lorentz-weighted longitudinal sum are completed.
