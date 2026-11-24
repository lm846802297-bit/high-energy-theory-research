# Numerical scans, integration, convergence, and uncertainty

Load this reference for numerical integration, multidimensional quadrature, parameter scans, interpolation, fitting, Monte Carlo calculations, or numerical results used in a physical claim.

This reference governs numerical work **after** the task-complexity gate has established that a numerical result is needed. It does not create a requirement to perform numerical work. For a self-contained exact derivation, prefer an analytic check; do not add a numerical integral merely to demonstrate a second method. Before launching a numerical check, state what specific uncertainty or failure mode it will resolve and what evidence it adds. If it adds no decision-relevant evidence, skip it.

A one-point numerical spot check is not a convergence study. Label it as a diagnostic spot check and do not present it as a converged production result.

## Method selection

Numerical methods are not the default independent check for an analytic result. First decide whether a numerical result is actually needed. If it is, choose the method from the mathematical structure, regularity, dimensionality, boundaries, singularities, and required precision. Possible methods include analytic reduction, adaptive quadrature, Gauss-Kronrod, Gaussian or sparse-grid quadrature, quasi-Monte Carlo, Monte Carlo, importance sampling, deterministic parameter grids, and problem-specific transformations.

Do not select an algorithm merely because a package or Skill recommends it. Record why the method is appropriate and which failure modes are relevant.

## Freeze the mathematical problem

Before a production run, record:

- the exact integral, observable, or parameter-space quantity being computed;
- integration variables, domains, measures, Jacobians, units, boundary conditions, and normalization;
- singular points, thresholds, endpoint behavior, discontinuities, oscillations, tails, and any regularization or subtraction;
- physical approximations, truncations, regulators, and validity domain;
- the source revision, input data and hashes, parameter configuration, command, runtime, dependencies, hardware, and random seeds where applicable.

For a transformed integral, derive and check the transformation and Jacobian independently. Preserve the original formulation in the run record.

## Convergence and error analysis

Use convergence tests that probe the actual numerical approximation:

- Increase quadrature order, adaptive tolerance, grid density, domain extent, or basis/cutoff size.
- Refine difficult regions independently, including endpoints, thresholds, resonances, narrow peaks, and parameter-space boundaries.
- Compare at least three refinement levels when meaningful; report the sequence rather than only the final difference.
- Separate estimated integration error from discretization, truncation, interpolation, fitting, sampling, floating-point, and input uncertainties.
- For stochastic methods, record independent seeds/replicates, estimator variance, effective sample size where relevant, and stability with sample count.
- For scans, report coverage, failed points, rejected points and reasons, boundary refinement, interpolation method/error, and whether disconnected regions are preserved.
- State the stopping criterion before the production run where practical. A small change between two resolutions is evidence about that comparison, not a universal error bound.

Use absolute and relative errors appropriately. Near a zero or cancellation, relative error can be misleading; report absolute scale and a physically meaningful normalization.

## Independent numerical and physical checks

Choose independent checks appropriate to the problem:

- analytic special cases or reduced-dimensional limits;
- known asymptotic behavior, threshold laws, symmetries, conservation laws, positivity, normalization, or sum rules;
- a different quadrature family or variable transformation;
- a separately derived implementation, not merely a second wrapper around the same algebraic kernel;
- benchmark values from a primary source, with exact conventions and version;
- precision escalation or compensated arithmetic where cancellation/conditioning warrants it.

Agreement between two routines that share the same integrand construction, trace, interpolation, or reduction is not a fully independent check. Identify shared dependencies explicitly.

A numerical convergence study does not establish that the integrand, model, or physical assumptions are correct. A physics identity does not establish numerical convergence. Report these evidence classes separately.

## Run-record depth

For a production calculation or a numerical result supporting a quantitative physical claim, retain native outputs and enough information to reconstruct the calculation:

- exact source commit and source-file identities;
- input file paths/immutable source identifiers, byte sizes, and SHA-256;
- full command, parameter values, conventions, precision, grids/orders, tolerances, seeds, and stopping criteria;
- OS/runtime, Python/compiler/package versions, CPU/GPU model and relevant resource limits;
- raw result arrays/tables, logs, checkpoints needed to resume, and machine-readable summary;
- convergence table, error budget, independent-check results, and known failed/blocked checks.

Follow the repository compute and archival policies. Archive extracted native files, not a newly generated ZIP/TAR as the only result. Keep computed, archived, numerically validated, and physically validated statuses distinct.

For a one-off diagnostic spot check that is not used as a production result, retain at minimum the exact expression/point, script or command if code was run, precision and parameters, output, and tool/runtime version. Label its scope explicitly. Do not impose the full production-run archive on a trivial diagnostic, and do not use a spot check as a substitute for convergence evidence when a quantitative numerical result is claimed.

## Interpretation

Do not promote a benchmark point to a full parameter-space statement without coverage evidence. Preserve failed points and disconnected allowed regions. Distinguish theoretical realizability, experimental allowance, exclusion, not assessed, and EFT-inapplicable regions. Every reported numerical claim must state its parameter point/region, assumptions, units, precision, and supporting run/claim identifiers.


## Normalization and absolute observables

For every change of integration variables, derive the full Jacobian and compare the transformed integrand against the original integral, including all constant factors. Do not silently drop a factor because it appears numerically harmless.

If an overall constant cancels only after unit-area or shape normalization, record the cancellation explicitly and label the result as a normalized shape/distribution. Such an implementation must not be reused as an absolute phase-space factor, cross section, rate, or luminosity until the omitted normalization is restored and independently checked.

When reproducing an archived calculation, verify that the manifest command is accepted by the pinned source code and that regenerated output schemas and hashes match the claimed artifacts. A stale command, mismatched output schema, or nonmatching artifact hash is an open provenance issue even when the numerical routine itself converges.
