# Development task T04 — symbolic Dirac trace

Status: development only; intended for Round 2.

## Conventions

Use four spacetime dimensions and metric (g^{\mu\nu}=\mathrm{diag}(+1,-1,-1,-1)). Gamma matrices obey
[
\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}.
]
Define (
ot p=p_\alpha\gamma^\alpha), (
ot k=k_\alpha\gamma^\alpha), and use the standard spin sums (u(p)\bar u(p)=\not p+m), (v(k)\bar v(k)=\not k-m).

## Prompt

Evaluate
[
T^{\mu\nu}=\mathrm{Tr}[(\not p+m)\gamma^\mu(\not k-m)\gamma^\nu].
]

1. Derive the result analytically.
2. Check it with an explicit (4\times4) Dirac representation for generic symbolic or numerical four-vectors.
3. Verify the Clifford algebra and relevant trace identities in the same convention.
4. Check mass dimensions and a simple kinematic limit.
5. State clearly which steps are convention-dependent and which are representation-independent.

Do not use a package result as the derivation. Preserve the exact convention and a runnable verification script or notebook.

## Required output

A line-by-line trace reduction, final tensor expression, explicit representation check, convention record, and native output.
