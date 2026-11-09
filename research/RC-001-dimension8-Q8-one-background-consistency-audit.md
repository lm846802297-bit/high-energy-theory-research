# RC-001 — Q8 one-background Ward-consistency audit and provisional-pole correction

**Status (2026-11-10):** a direct Ward-contraction identity exposes an unresolved inconsistency in the previously recorded ordinary-line UV residue. The displayed line-graph pole must be treated as provisional and must not be used for UV matching until the discrepancy is resolved.

## 1. Exact contraction before integration

Let \(a=k+r\), \(b=k+q\). With the ordinary-line numerator
\[
N^\mu=4a^2\left[b^\mu(k\cdot a)-(b\cdot k)a^\mu+(b\cdot a)k^\mu\right],
\]
the contraction is exactly
\[
q_\mu N^\mu
=4a^2\left[b^2(k\cdot a)-k^2(b\cdot a)\right].
\]
Therefore
\[
\frac{q_\mu N^\mu}{k^2b^2}
=4(k+r)^2\left[
\frac{k\cdot(k+r)}{k^2}
-\frac{(k+q)\cdot(k+r)}{(k+q)^2}
\right].
\]
After shifting the loop momentum in the second term, this becomes the difference of two one-propagator tadpole integrands, with scalar momenta \(r\) and \(r-q\). In translation-invariant dimensional regularization each is scaleless in the massless theory. Thus the complete dimensionally regulated ordinary-line integral has a vanishing longitudinal contraction before any UV/IR pole split.

This is a stringent algebraic check and is independent of the previous Feynman-parameter tensor reduction.

## 2. Contact-vertex numerator

For the Q8 contact vertex
\[
V_8^\mu(P',P)=P'^2\gamma^\mu+\slashed P'\gamma^\mu\slashed P+\gamma^\mu P^2,
\quad P=k+r,\quad P'=k+r+q,
\]
the one-propagator loop numerator is
\[
N_{\rm ct}^\mu=\operatorname{tr}[\slashed k V_8^\mu(P',P)].
\]
Its angular average in \(d\) dimensions is
\[
\left\langle N_{\rm ct}^\mu\right\rangle
=\frac{16\,k^2}{d}(q^\mu+2r^\mu).
\]
Consequently the massless contact integral is scaleless:
\[
\int\frac{d^dk}{(2\pi)^d}\frac{\langle N_{\rm ct}^\mu\rangle}{k^2}
\propto(q^\mu+2r^\mu)\int\frac{d^dk}{(2\pi)^d}1=0.
\]
An auxiliary-mass IR rearrangement generates only regulator-mass-proportional UV poles in this one-propagator integral; such terms vanish when the auxiliary mass is removed. The contact graph by itself therefore does not obviously supply the mass-independent degree-five pole previously attributed to the ordinary-line graph.

## 3. Consequence: previous line-pole formula is not accepted yet

The previously recorded result in research/RC-001-dimension8-Q8-one-background-vertex.md has a nonzero longitudinal UV residue. That conflicts with the exact contraction identity above if the same translation-invariant regulator and the same UV/IR separation are used consistently.

The likely failure point is not the Dirac trace alone: it may involve an invalid extraction of UV poles from power-divergent tensor integrals, an omitted contribution in the momentum routing/operator insertion, or an incomplete set of one-loop diagrams/functional derivatives. The scalar constituent charge-flow identity must also be included. No single explanation is selected without a complete re-derivation.

**Action:** the old coefficient is explicitly provisional and is not to be used as a dimension-eight Wilson coefficient or as evidence of a nonzero local pole.

## 4. Required resolution sequence

1. Re-derive the one-background amplitude from the fermion functional determinant with all scalar momenta and fermion momentum orientations fixed.
2. Check the Ward contraction at the integrand level before Feynman parametrization.
3. Reconcile the two-propagator representation with the difference of one-propagator tadpoles using a regulator that preserves translations.
4. Perform UV/IR separation with an explicit R* or equivalent prescription, tracking power-divergent and logarithmic terms separately.
5. Include Q8 contact and scalar constituent charge-flow terms with the exact composite-source charges.
6. Only after the above agree, recompute the transverse/local form factors and extract the genuine UV pole.

No complete one-loop Q8 soft pole, counterterm, or hard-matched Wilson coefficient is claimed.
