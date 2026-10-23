# End-to-end Skill pilot: 2x2 mass-squared matrix

## Purpose and boundary

This is a small, deterministic workflow pilot for the reusable research Skill. It exercises intake, explicit units/assumptions, analytic calculation, independent checks, result artifact generation, and a synthetic candidate-record chain.

It is deliberately **not** presented as a physical model result. It does not test gauge invariance, a scalar potential, perturbativity, UV/EFT matching, or experimental constraints.

## Input and derivation

The input is the real symmetric matrix

\[
M^2 = \begin{pmatrix}5&2\\2&8\end{pmatrix}\;\mathrm{TeV}^2.
\]

For a symmetric matrix \(\begin{pmatrix}a&b\\b&d\end{pmatrix}\), the characteristic equation gives

\[
\lambda_{\pm}=\frac{a+d\pm\sqrt{(a-d)^2+4b^2}}{2}.
\]

Here \(a+d=13\), \(ad-b^2=36\), and the discriminant is \(5\), so the eigenvalues are \(4\) and \(9\;\mathrm{TeV}^2\), corresponding to masses \(2\) and \(3\;\mathrm{TeV}\).

## Independent checks

The test harness verifies:
- trace and determinant reconstructed from the eigenvalues;
- normalized and orthogonal eigenvectors;
- eigenpair residuals;
- positive definiteness using the leading principal minor and determinant.

Run it with:

~~~bash
python tests/eval-cases/analytic-mass-matrix-pilot/run_pilot.py
~~~

The script uses only the Python standard library. `expected-results.json` records the independent acceptance values.

## Candidate-record chain and current limitation

The unit test constructs a synthetic Task → approved test contract → Run Plan → Run → Run Manifest → Artifact → Validation Plan/Activity/Report → Evidence Fragment → Claim chain and validates it against the candidate schemas. The generated result file is hash-checked and local source/artifact paths are checked.

The candidate now defines FingerprintInputs as a versioned input declaration. Source bytes and input artifacts require explicit SHA-256 digests; configuration, code and environment components carry record IDs plus component digests, or null plus an explicit not-applicable reason. Execution specifications and fingerprint payloads use RFC 8785 canonicalization. Source/artifact entries are sorted by ID for hashing, duplicate IDs are rejected, and the Run Manifest bundle is recomputed from the declared inputs.

The golden vector at tests/fixtures/fingerprint-inputs-v1/golden-vector.json fixes canonical JSON bytes and expected SHA-256 values. Unit tests check order independence, duplicate-ID rejection, execution-spec tampering, component semantics and cross-record consistency. The candidate contract remains unapproved pending review; the real-physics pilot is a separate acceptance gate.
