# Real research-task pilot: UV–EFT hard derivative

This case validates the candidate research-record workflow using a bounded subtask from the ongoing Higgs-portal / UV–EFT calculation.

## Task

Independently audit the closed-form Passarino–Veltman functions and small-\(r=m^2/M^2\) expansion used for the hard derivative of the mixed scalar two-point function. The independent method evaluates the corresponding Feynman-parameter integrals by adaptive Simpson quadrature and compares them with the closed forms over four small-\(r\) values and two scale-log values.

The model conventions are cross-referenced to [arXiv:2608.27258v1](https://arxiv.org/html/2608.27258v1), especially the singlet-scalar expansion and vector-like lepton mass matrix. The hard-kernel formula itself is transcribed from the working note excerpt in \`sources/source-excerpt.md\`; it is not attributed to the arXiv paper.

## What the task can establish

- The listed \(B_0\)-type values and derivatives are numerically consistent with independent Feynman-parameter integrals.
- The exact derivative combination approaches \(4/3-2L\), with first correction \(-4r\ln r-16r\) and the independently expanded second correction \(-28r^2\ln r-32r^2\).
- The checked second-order expansion is \(4/3-2L-4r\ln r-16r-28r^2\ln r-32r^2+O(r^3\ln r)\); its residual is tested on the declared finite grid, not proven for all \(r\).
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



## Separate Mathematica verification

The provenance bundle also includes verify_pv_derivative_mathematica.wl. It uses Mathematica symbolic integration and series expansion to check the listed PV integrals and second-order small-r expression. This script is not executed by GitHub Actions and is not marked passed. It is provided for a separate local Mathematica run; record the Mathematica version and actual output before changing its status. Open the .wl file in the Mathematica front end and evaluate it. Review any FAIL result or unevaluated conditional equality rather than changing the expected value to force a pass.


## Output-directory safety

Pass a fresh, non-existent destination to `--output-dir`. The bundle builder refuses to overwrite any existing path and does not recursively delete user-supplied directories. If a previous run left a directory behind, inspect it and choose a new path (or remove it manually only after confirming its contents are disposable).
