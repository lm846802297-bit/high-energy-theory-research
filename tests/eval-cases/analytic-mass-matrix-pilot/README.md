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

The candidate schemas now accept structured payloads for `run_plan.execution_spec`, Run Manifest snapshots, `claim.evidence_status`/`physics_assessment`, Artifact Plan `completeness_rules`, and Artifact Plan/Artifact `schema_or_structure`. The pilot populates these fields and validates them. **Full reproducibility acceptance remains blocked by `run_plan.fingerprint_inputs`:** the design document references `Record<FingerprintInputs>` but does not define its fields or hashing semantics, so the schema still accepts only an empty object rather than inventing a contract.

Regression tests prove that the now-defined structured payloads are accepted and that a non-empty `fingerprint_inputs` payload remains rejected until its contract is reviewed. The pilot passes the algebraic checks and the structured record graph, but does **not** pass full end-to-end reproducibility acceptance. No normative approval is inferred.
