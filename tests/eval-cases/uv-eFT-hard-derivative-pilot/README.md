# Real research-task pilot: UV–EFT hard derivative

This case validates the candidate research-record workflow using a bounded subtask from the ongoing Higgs-portal / UV–EFT calculation.

## Task

Independently audit the closed-form Passarino–Veltman functions and small-\(r=m^2/M^2\) expansion used for the hard derivative of the mixed scalar two-point function. The independent method evaluates the corresponding Feynman-parameter integrals by adaptive Simpson quadrature and compares them with the closed forms over four small-\(r\) values and two scale-log values.

The model conventions are cross-referenced to [arXiv:2608.27258v1](https://arxiv.org/html/2608.27258v1), especially the singlet-scalar expansion and vector-like lepton mass matrix. The hard-kernel formula itself is transcribed from the working note excerpt in \`sources/source-excerpt.md\`; it is not attributed to the arXiv paper.

## What the task can establish

- The listed \(B_0\)-type values and derivatives are numerically consistent with independent Feynman-parameter integrals.
- The exact derivative combination approaches \(4/3-2L\), with first correction \(-4r\ln r-16r\).
- At \(\mu=M\), the declared insertion convention gives \(\Pi'_{\rm hard}(0)=-K/(12\pi^2)+O(Kr\ln r)\).
- Under the declared single-operator projection convention only, the coefficient factor is \(C_{\Phi D}/\Lambda^2=K/(6\pi^2v_hv_s)\).

## What it does not establish

It does not recompute the full UV diagram numerator or prove completeness of the diagram set. It does not establish a unique Wilson coefficient after complete IBP/EOM basis reduction, field redefinitions, and wave-function/parameter renormalization. No experimental interpretation or parameter-space claim is made.

## Reproducible bundle

Run:

\`\`\`bash
python tests/eval-cases/uv-eFT-hard-derivative-pilot/run_record_chain.py --output-dir /tmp/uv-eFT-hard-derivative-bundle
\`\`\`

The bundle contains versioned source excerpts, input/configuration files, exact executed code, candidate schemas, numerical output, per-record JSON, a full record-chain JSON, and a cross-record validation report. The CI uploads it as an Actions artifact.

The execution contract is approved only for this bounded automated pilot. The Claim and evidence review status remain pending human scientific review. Passing software tests is not a physics-correctness certificate for the full UV–EFT matching problem.

