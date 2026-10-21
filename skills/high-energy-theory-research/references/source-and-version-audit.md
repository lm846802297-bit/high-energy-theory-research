# Source and version audit

## Literature sources

- Prefer primary articles, official experimental publications, data releases, errata, and versioned repositories.
- Record DOI, arXiv identifier and version, publication date, retrieval date, and the exact equation/table/section supporting a claim.
- Separate what the paper states from what is inferred or newly derived.
- If versions differ, state which version was used and check whether the relevant equation or dataset changed.

## Code and data provenance

Record repository URL, commit SHA or release tag, local file SHA-256, package versions, runtime, configuration, and relevant environment variables. Never include credentials, access tokens, or private secrets in manifests.

## Run and artifact identity

A run should identify the inputs, code, configuration, environment, execution command, and output artifacts. Reuse a previous result only when the relevant fingerprints match. If a required fingerprint is missing or mismatched, mark the result as needing review and rerun the affected checks.

## Experimental constraints

Record the exact experiment/analysis release, observable, confidence level, dataset or likelihood, model assumptions, parameter mapping, and reinterpretation method. State what was evaluated and what remains unassessed. Do not merge results obtained under incompatible assumptions without an explicit justification.
