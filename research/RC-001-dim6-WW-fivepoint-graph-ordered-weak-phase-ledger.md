# RC-001 — Graph-ordered weak tensors and phase ledger for the external-W attachments

**Workstream:** RC-001-WW-UV-FF-02, Stage B2c-III  
**Status:** the weak-generator orderings are now attached to the actual A/B line positions in the five-point numerator templates, and their commutator differences are checked with the relative Feynman-rule phases fixed in Stage B2c-I/II. The scalar-seagull weak tensors are also mapped to the opposite-endpoint generator. This is still a group/phase ledger: the Lorentz-weighted 24-graph sum and full Slavnov–Taylor identity are not claimed.

## 1. Pair endpoints

Use the signed external-index actions \(\mathscr T_r^a\) for the all-incoming ordering
\[
(\bar L_i,H_j,H^\dagger_k,L_l),
\]
as defined in the Stage-B2b weak-ordering audit. For an internal-W pair \(A,B\), the seed weak tensor is
\[
\mathcal T_{AB}=\sum_b\mathscr T_A^b\mathscr T_B^bT_0.
\]

| Pair | A endpoint | B endpoint | \(\mathcal T_{AB}\) |
|---|---|---|---|
| LD-W-01 | \(\bar L\) | \(L\) | \(-T_3/4\) |
| LD-W-02 | \(\bar L\) | \(H^\dagger\) | \(+T_3/4\) |
| LD-W-03 | \(\bar L\) | \(H\) | \(-3T_0/4\) |
| LD-W-04 | \(L\) | \(H^\dagger\) | \(-3T_0/4\) |
| LD-W-05 | \(H\) | \(L\) | \(+T_3/4\) |
| LD-W-06 | \(H\) | \(H^\dagger\) | \(-T_3/4\) |

Here \(T_0=\delta_{ij}\delta_{kl}\) and \(T_3=\sigma^I_{ij}\sigma^I_{kl}\).

## 2. Actual generator order in each five-point graph

The external W is inserted on the propagator between the Yukawa vertex and the internal-W endpoint. The graph order is therefore fixed by the position of the external vertex relative to the internal-W vertex:

- A-line insertion: the internal-W generator is encountered first, then the external-W generator:
  \[
  \mathcal W_A^a
  =\sum_b\mathscr T_A^b\mathscr T_A^a\mathscr T_B^bT_0.
  \]
- B-line insertion: the external-W generator is encountered first, then the internal-W generator:
  \[
  \mathcal W_B^a
  =\sum_b\mathscr T_A^b\mathscr T_B^a\mathscr T_B^bT_0.
  \]
- A scalar seagull:
  \[
  \mathcal S_A^a
  =\sum_b\{\mathscr T_A^a,\mathscr T_A^b\}\mathscr T_B^bT_0.
  \]
- B scalar seagull:
  \[
  \mathcal S_B^a
  =\sum_b\mathscr T_A^b\{\mathscr T_B^a,\mathscr T_B^b\}T_0.
  \]
- Internal-W three-gauge insertion:
  \[
  \mathcal G_{AB}^a
  =\epsilon^{abc}\mathscr T_A^b\mathscr T_B^cT_0.
  \]

These are the ordered weak tensors that multiply the graph-specific Lorentz numerators. They must not be replaced by the unordered seed tensor \(\mathcal T_{AB}\) before the external-W generator ordering has been retained.

## 3. Commutator relation with the Yukawa-endpoint ordering

The line WTI has two endpoint terms. The term at the internal-W endpoint has the graph ordering in §2; the term at the Yukawa endpoint has the reversed ordering on the same representation slot. With the signed-action algebra
\[
[\mathscr T_r^a,\mathscr T_r^b]
=-i\epsilon^{abc}\mathscr T_r^c,
\]
the graph-order minus Yukawa-endpoint-order differences are
\[
\boxed{
\mathcal W_A^a-\widetilde{\mathcal W}_A^a
=-i\mathcal G_{AB}^a,
}
\]
\[
\boxed{
\mathcal W_B^a-\widetilde{\mathcal W}_B^a
=-i\mathcal G_{AB}^a,
}
\]
where
\[
\widetilde{\mathcal W}_A^a
=\sum_b\mathscr T_A^a\mathscr T_A^b\mathscr T_B^bT_0,
\qquad
\widetilde{\mathcal W}_B^a
=\sum_b\mathscr T_A^b\mathscr T_B^b\mathscr T_B^aT_0.
\]
The equality is checked for all six pairs, all three external-W generators, and all 16 external weak-index components.

This fixes the group-theory sign for the actual graph ordering. It does not yet establish the cancellation with the three-W graph: the A/B Lorentz endpoint signs from the oriented fermion/scalar WTI, the propagator factors, and the \(R_{\rm FG}\) term must still be included in the same expression.

## 4. Seagull weak tensors

For a scalar endpoint,
\[
\{t^a,t^b\}=\frac12\delta^{ab}\mathbf1.
\]
Consequently,
\[
\mathcal S_A^a=\frac12\mathscr T_B^aT_0,
\qquad
\mathcal S_B^a=\frac12\mathscr T_A^aT_0.
\]
These identities hold for every scalar endpoint in LD-W-02…06 and for all external-W generators. They fix the group tensor but not the Lorentz coefficient \(q^\mu\) from the seagull contraction; that coefficient must be combined with the scalar-line WTI before the scalar endpoint is declared to telescope.

## 5. Combining the group identities with the B2c phases

The phase ratios relative to the four-point skeleton are now fixed by the action convention in Stage B2c-I/II:
\[
\frac{P_{\rm matter\ insertion}}{P_4}=-g_2,\qquad
\frac{P_{\rm seagull}}{P_4}=+g_2,\qquad
\frac{P_{3W}}{P_4}=-ig_2.
\]
Thus the pure group commutator factor \(-i\mathcal G_{AB}^a\) from either matter-line ordering is multiplied by the matter-line phase \(-g_2\), giving \(+ig_2\mathcal G_{AB}^a\) before the orientation-dependent Lorentz endpoint sign is applied. The three-W graph carries \(-ig_2\mathcal G_{AB}^a\) times its contracted Lorentz kernel. The relative phase is therefore now unambiguous; whether and how these terms cancel is a Lorentz-weighted graph-sum question, not a group-algebra question.

For the scalar endpoint, the seagull carries \(+g_2\) times the anticommutator tensor and \(q^\mu\), while the ordinary scalar-line insertion carries \(-g_2\) times its oriented propagator difference. Their sum must be evaluated before simplifying the scalar endpoint. The anticommutator identity alone is not the scalar Compton Ward identity.

## 6. Reproduction and evidence boundary

The exact SymPy audit is in
calculations/RC-001-dim6-WW-fivepoint-graph-ordered-weak-phase-ledger.py
with captured output in
validation/RC-001-dim6-WW-fivepoint-graph-ordered-weak-phase-ledger.txt.

It checks:
- six seed pair tensors: 96/96 components;
- A-line graph ordering minus Yukawa-endpoint ordering: 288/288;
- B-line graph ordering minus Yukawa-endpoint ordering: 288/288;
- scalar-seagull weak tensors: 288/288.

This does not establish:
1. the Lorentz-weighted cancellation of the matter-line and three-W graphs;
2. the scalar-line/seagull Lorentz sum;
3. the ordinary-Feynman-gauge ghost/gauge-fixing Slavnov–Taylor completion;
4. external-leg/LSZ and counterterm terms;
5. a five-point hard integral, transverse form factor, or Wilson coefficient.

The next step is to assemble each of the 24 graph-specific Lorentz numerators with these ordered weak tensors and phase ratios, contract \(q_\alpha\), and sum the A/B endpoint pieces pair by pair. The four-point shifted-momentum Ward variation is the target; the EFT contact comparison follows after that UV identity is established.
