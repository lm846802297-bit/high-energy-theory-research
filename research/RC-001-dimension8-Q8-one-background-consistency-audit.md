# RC-001 — Q8 one-background Ward consistency and corrected tensor reduction

**Status (2026-11-10):** the apparent conflict between the ordinary-line Ward contraction and its UV residue is resolved. The earlier tensor reduction omitted loop components transverse to the external \(q,r\) plane. A covariant \(d\)-dimensional angular average gives a transverse ordinary-line pole. The contact-graph angular average has also been corrected. Full R* subtraction and UV-hard matching remain open.

## 1. Exact ordinary-line contraction

Let \(a=k+r\), \(b=k+q\). The numerator is
\[
N^\mu=4a^2[b^\mu(k\cdot a)-(b\cdot k)a^\mu+(b\cdot a)k^\mu].
\]
Using \(q=b-k\),
\[
q_\mu N^\mu=4a^2[b^2(k\cdot a)-k^2(b\cdot a)].
\]
Hence
\[
\frac{q_\mu N^\mu}{k^2b^2}
=4(k+r)^2\left[\frac{k\cdot(k+r)}{k^2}
-\frac{(k+q)\cdot(k+r)}{(k+q)^2}\right].
\]
A translation-invariant shift in the second term turns the integral into a difference of massless one-propagator tadpole integrals. The complete dimensionally regulated longitudinal integral vanishes. This identity is an integrand-level check and is retained.

## 2. Source of the previous discrepancy

The earlier calculation placed \(q\) and \(r\) in a two-dimensional coordinate plane but evaluated scalar factors such as \((k+r)^2\) using only the two displayed loop components. In \(d=4-2\epsilon\), the remaining \(d-2\) transverse components contribute to \(l^2\) and to all angular averages. Omitting them corrupts the coefficients of \(L=l^2\) and \(L^2\), and produced a spurious nonzero longitudinal pole.

The old planar result is superseded. The corrected script uses invariant variables \(L=l^2\), \(u=l\cdot q\), \(v=l\cdot r\) and full \(d\)-dimensional tensor moments.

## 3. Corrected ordinary-line UV residue

The covariant reduction gives
\[
\langle N^\mu\rangle
=[A_0+A_2L+A_4L^2]q^\mu+
[B_0+B_2L+B_4L^2]r^\mu.
\]
The parameter-integrated coefficients are
\[
A_{\rm UV}=\frac43(q\cdot r)[q\cdot r-r^2],\qquad
B_{\rm UV}=-\frac43q^2[q\cdot r-r^2].
\]
Therefore
\[
\boxed{
\mathcal I_{\rm line}^{\mu}\big|_{\rm UV}
=\frac{1}{16\pi^2\epsilon}\frac43(q\cdot r-r^2)
[(q\cdot r)q^\mu-q^2r^\mu].
}
\]
It obeys
\[
q_\mu\mathcal I_{\rm line}^{\mu}\big|_{\rm UV}=0.
\]
This is the ordinary-line graph only, with \(\operatorname{tr}\mathbf1=4\) included and overall Wilson/gauge factors omitted. It is not yet the full Q8 soft pole or a matched Wilson coefficient.

Reproduction: calculations/RC-001-dimension8-Q8-one-background-line-pole-covariant.py. Recorded output: validation/RC-001-dimension8-Q8-one-background-line-pole-covariant.txt.

## 4. Corrected Q8 contact angular average

For
\[
N_{\rm ct}^\mu=4[(P'^2+P^2-P'\cdot P)k^\mu
+(k\cdot P')P^\mu+(k\cdot P)P'^\mu],
\quad P=k+r,\quad P'=k+r+q,
\]
the full \(d\)-dimensional angular average is
\[
\boxed{
\langle N_{\rm ct}^\mu\rangle
=4\,l^2\,\frac{d+2}{d}(q^\mu+2r^\mu).
}
\]
This corrects the earlier coefficient \(16l^2/d\), which came from the same incomplete planar averaging. After division by the single massless propagator, the integral is scaleless in dimensional regularization. With an auxiliary mass, its UV pole is proportional to a positive power of that auxiliary mass and vanishes as the regulator is removed. A common R* prescription is still needed to document the UV/IR split rigorously.

Reproduction: calculations/RC-001-dimension8-Q8-one-background-consistency-audit.py. Recorded output: validation/RC-001-dimension8-Q8-one-background-consistency-audit.txt.

## 5. Remaining matching tasks

1. Fix the exact functional-determinant routing and all external scalar momenta.
2. Apply one common IR rearrangement to line and contact graphs.
3. Show explicitly that the auxiliary-regulator dependence cancels or vanishes in the massless limit.
4. Derive the full composite-source Ward identity including scalar transformations.
5. Compute the UV-hard region with the same regulator/subtraction convention.
6. Verify soft/hard pole cancellation and then perform EOM/IBP reduction.

No complete one-loop Q8 matching coefficient is claimed at this stage.
