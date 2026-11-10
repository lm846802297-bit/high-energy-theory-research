# RC-001 QLD8: direct-pairing \(RL\) tensor evanescent seed

**Date:** 2026-11-10  
**Stage:** P1.1c — Dirac-chain decomposition for the \(d^\dagger d\) QCD pilot  
**Status:** the formal \(d\)-dimensional gamma decomposition and the exact 4D vanishing of the opposite-chirality tensor contraction are established. The complete graph numerator and its UV pole are not calculated.

## 1. The two-gamma open-line chain

For the direct source pairing in the \(d^\dagger d\) channel,
\[
(\bar Q P_R d)(\bar d P_L Q),
\]
a two-gamma open-line chain has the Dirac structure
\[
\left(\gamma^\mu\gamma^\nu P_R\right)
\otimes
\left(P_L\gamma_\nu\gamma_\mu\right).
\]
Use
\[
\gamma^\mu\gamma^\nu=g^{\mu\nu}-i\sigma^{\mu\nu},
\qquad
\gamma_\nu\gamma_\mu=g_{\mu\nu}+i\sigma_{\mu\nu},
\qquad
[\sigma^{\mu\nu},\gamma_5]=0.
\]
The cross terms vanish after contraction because the metric is symmetric and
\(\sigma^{\mu\nu}\) is antisymmetric. Thus, in \(D\) dimensions,
\[
\boxed{
\left(\gamma^\mu\gamma^\nu P_R\right)
\otimes
\left(P_L\gamma_\nu\gamma_\mu\right)
=
D\,P_R\otimes P_L
+
\sigma^{\mu\nu}P_R\otimes\sigma_{\mu\nu}P_L.
}
\]
This identity is an algebraic reduction of the displayed gamma chain. It does not by itself assert that a particular complete one-loop graph has this numerator with unit coefficient; that requires the graph's propagator routing, vertex ordering, and Feynman-rule signs.

## 2. The direct \(RL\) tensor contraction is evanescent

In exactly four dimensions, \(\sigma^{\mu\nu}P_R\) and
\(\sigma^{\mu\nu}P_L\) have opposite duality. Therefore
\[
\boxed{
(\bar Q\sigma^{\mu\nu}P_R d)
(\bar d\sigma_{\mu\nu}P_L Q)=0
\qquad (D=4).
}
\]
The exact \(4\times4\) gamma-matrix representation check also verifies the corresponding \(16\times16\) spinor-index tensor product vanishes.

In \(D=4-2\epsilon\), this contraction is not set to zero. A direct-pairing evanescent seed is
\[
E_{T;RL}^{\rm dir}
=
(\bar Q\sigma^{\mu\nu}P_R d)
(\bar d\sigma_{\mu\nu}P_L Q).
\]
No \(O(\epsilon)\) physical-operator admixture is included in this definition.

Combining this with the gamma-chain decomposition gives
\[
(4-2\epsilon)\,O_{S;RL}+E_{T;RL}^{\rm dir},
\qquad
O_{S;RL}=(\bar QP_Rd)(\bar dP_LQ).
\]
The \(-2\epsilon\,O_{S;RL}\) term must be retained: when multiplied by a \(1/\epsilon\) UV pole it contributes to the finite local term. It cannot be replaced by \(4O_{S;RL}\) before the UV subtraction.

## 3. Do not double-count evanescent representations

The upstream basis note already defines:
- the crossed-pairing scalar/vector Fierz-difference evanescent \(E_{RL}^{(rs)}\);
- the rank-three gamma-string seed \(E_{3;RL}\) in the crossed vector-current representation.

The direct tensor seed \(E_{T;RL}^{\rm dir}\) is written in the original source pairing. Its relation to the crossed-pairing evanescents must be obtained from the \(D\)-dimensional Fierz transformation, with the Grassmann exchange sign and derivative labels preserved. It must not be declared an additional independent evanescent direction until that transformation and the rank of the full evanescent projection matrix have been computed.

For the \(d^\dagger d\) QCD pilot, keep the raw direct-pairing tensor chain and the crossed-basis rank-three structure in the numerator ledger. Choose one canonical independent evanescent basis only after the d-dimensional Fierz map is known.

## 4. Validation boundary

The companion exact gamma-matrix audit checks:
1. the \(D=4\) direct \(RL\) tensor contraction vanishes;
2. the displayed gamma-chain identity reduces to \(4P_R\otimes P_L+E_{T;RL}^{\rm dir}\) in four dimensions;
3. the chiral projectors and Minkowski metric use the same conventions as the existing QLD8 Fierz audit.

This establishes a candidate evanescent structure and its \(D\)-dependence. It does not calculate the one-loop graph coefficient, the loop integral, the UV pole, the mixing into \(E_{RL}^{(rs)}\) or \(E_{3;RL}\), or the finite matching term.
