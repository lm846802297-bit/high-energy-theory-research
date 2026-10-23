# RC-001 — Exact \(SU(2)_L\) tensor factors for \(Q_{LD}\) gauge attachments

**Scope:** exact group-theory factors acting on the tree weak-index tensor. These are not complete Feynman-diagram coefficients: they omit the Lorentz numerator, propagator/vertex signs outside the representation generators, loop integrals, diagram multiplicities, and counterterms.

## 1. Tree tensor and basis

Write the weak-index structure of
\[
Q_{LD}=(\bar L_i H_i)(H^\dagger_k L_k)
\]
as
\[
T_0=\delta_{ij}\delta_{kl},
\qquad
T_x=\delta_{il}\delta_{kj}.
\]
With Pauli matrices normalized by \(\mathrm{tr}(\sigma^I\sigma^J)=2\delta^{IJ}\), define
\[
T_3=\sigma^I_{ij}\sigma^I_{kl}=2T_x-T_0.
\]
Thus \(T_x=(T_0+T_3)/2\). The \(SU(2)_L\) generators are \(t^I=\sigma^I/2\), with \(C_F=3/4\). Treat all external fields as outgoing; \(\bar L\) and \(H^\dagger\) transform in the conjugate representation, with generator \(-t^{I\,T}\).

## 2. Pairwise generator contractions

Label the two Yukawa-singlet vertices as \((\bar L,H)\) and \((H^\dagger,L)\). The pairwise contraction \(t_r^I t_s^I\) acting on \(T_0\) gives:

| Atlas pair ID | Pair | Generator contraction on \(T_0\) | Common tensor basis |
|---|---|---|---|
| LD-W-01 | \(\bar L-L\) | \(-\frac12 T_x+\frac14T_0\) | \(-\frac14T_3\) |
| LD-W-02 | \(\bar L-H^\dagger\) | \(+\frac12 T_x-\frac14T_0\) | \(+\frac14T_3\) |
| LD-W-03 | \(\bar L-H\) | \(-C_F T_0\) | \(-\frac34T_0\) |
| LD-W-04 | \(L-H^\dagger\) | \(-C_F T_0\) | \(-\frac34T_0\) |
| LD-W-05 | \(L-H\) | \(+\frac12 T_x-\frac14T_0\) | \(+\frac14T_3\) |
| LD-W-06 | \(H^\dagger-H\) | \(-\frac12 T_x+\frac14T_0\) | \(-\frac14T_3\) |

The signs follow from conjugate-representation generators and the singlet identities
\[
(t_{\bar L}^I+t_H^I)T_0=0,\qquad
(t_{H^\dagger}^I+t_L^I)T_0=0.
\]
For the cross-vertex contraction, the fundamental completeness relation
\[
\sum_I t^I_{ab}t^I_{cd}
=\frac12\delta_{ad}\delta_{bc}
-\frac14\delta_{ab}\delta_{cd}
\]
produces \(\frac12T_x-\frac14T_0=\frac14T_3\); pairs related by one conjugate-representation generator acquire the opposite sign.

## 3. Consequence for the common-basis reduction

The two same-Yukawa-vertex pairs LD-W-03 and LD-W-04 are pure singlet-tensor contributions, \(-3T_0/4\). The four cross-vertex pairs reduce to pure triplet-tensor contributions, with the signs displayed above. Do not project all six \(WW\) classes onto a single singlet coefficient before summing their loop integrals: each topology has a different momentum numerator and may have a different multiplicity.

For \(Q_{RD}\), every field in the tree exchange is an \(SU(2)_L\) singlet, so there is no \(WW\) attachment class.

## 4. Evidence boundary

These exact tensor identities are a group-theory projection of the structural atlas and can be checked independently of the loop integration. They do not establish which loop integrals multiply the tensors, the finite hard coefficients, or the full UV–EFT difference. The \(SU(2)\) projection must be applied to the summed amplitudes together with their Dirac structures, Ward-identity completion, counterterms, and EOM/source companions.
