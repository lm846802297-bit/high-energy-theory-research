# Benchmark evaluator package

Runtime dependencies are pinned in evaluators/requirements.txt. The lightweight CI/unit-test dependencies are pinned separately in evaluators/requirements-test.txt. The package uses Python 3.12+ and JSON Schema Draft 2020-12.

## Deterministic evaluators

- evaluate.py: validates immutable run records and A/B pair integrity, checks all staged source bytes against the task manifest, validates registered evaluator payloads, recomputes scores, and produces the preregistered comparison report.
- verify_dirac_trace.py: checks the T04 Dirac trace against an explicit 4x4 representation.
- verify_repro_package.py: checks T06 input/output hashes and independently recomputes the weighted mean without executing model-generated code.
- verify_public_t05.py: verifies all nine public T05 inputs by Git blob SHA-1, byte size, and SHA-256. Its PDF mode screens both axial-vector paper figure panels using the pinned PDF text auditor. Its figures mode executes only the trusted standard-library AFH plotting adapter and requires both model-submitted SVGs to be byte-identical to fresh trusted outputs.

## T05 source separation

T05-A audits the two actual constraint-panel PDFs used together in the axial-vector manuscript. The companion TeX establishes their common caption and intended panel width. The 5 pt text-size check is only a screening tool; visual inspection at intended physical size remains a separate human-review item.

T05-B uses the public Native AFH Xe-131 response CSV, its WLS exporter, run manifest, README, and checksum list. The plotting adapter creates two presentation SVGs from the existing CSV. It does not regenerate the Native AFH data, execute the unavailable original AFH package, or calculate new nuclear responses. The Native dataset's source-comparison evidence is not evidence that the complete P3-C particle-nuclear current contraction has been validated.

The CI workflow stages all T05 inputs from exact public commit URLs. It needs no secret, token, or access to the private LZ-3-body-for-hdm repository. The CI SVG self-test compares the trusted generator with its own freshly generated outputs; it is not a scored model run.

## Run and compare

From the benchmark root:

    python -m pip install -r evaluators/requirements-test.txt
    python -m unittest discover -s evaluators -v

For scored runs, the model workspace must contain the byte-identical staged files listed in tasks/development/manifest.json. The evaluator workspace separately retains the evaluator manifest, PDF auditor, and scoring keys.

Before comparison, run the required deterministic evaluator for every task and store its JSON result as a run artifact. For T05, the PDF result is produced with:

    python evaluators/verify_public_t05.py --part pdf --task-manifest tasks/development/manifest.json --evaluator-manifest evaluators/manifest.json --input-root path/to/staged-inputs --pdf-audit-script path/to/audit_pdf_text_reconstructed.py --output path/to/t05-pdf-audit.json

The model-submitted AFH SVGs are verified with:

    python evaluators/verify_public_t05.py --part figures --task-manifest tasks/development/manifest.json --evaluator-manifest evaluators/manifest.json --input-root path/to/staged-inputs --submitted-output-root path/to/model/results/plots --output path/to/t05-afh-figure-check.json

The comparison command consumes immutable A/B run records and exact frozen protocol artifacts. It verifies each source byte, prompt hash, evaluator payload, evaluator output artifact, protocol commit, and pair control before scoring. Round 1 remains descriptive only; the sealed Holdout is not part of development runs.
