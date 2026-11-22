# Numerical scans, integration, convergence, and uncertainty

Load this reference for numerical integration, multidimensional quadrature, parameter scans, interpolation, fitting, Monte Carlo calculations, or numerical results used in a physical claim.

## Method selection

Choose the method from the mathematical structure, regularity, dimensionality, boundaries, singularities, and required precision. Possible methods include analytic reduction, adaptive quadrature, Gauss-Kronrod, Gaussian or sparse-grid quadrature, quasi-Monte Carlo, Monte Carlo, importance sampling, deterministic parameter grids, and problem-specific transformations.

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

## Required run record

Retain native outputs and enough information to reconstruct the calculation:

- exact source commit and source-file identities;
- input file paths/immutable source identifiers, byte sizes, and SHA-256;
- full command, parameter values, conventions, precision, grids/orders, tolerances, seeds, and stopping criteria;
- OS/runtime, Python/compiler/package versions, CPU/GPU model and relevant resource limits;
- raw result arrays/tables, logs, checkpoints needed to resume, and machine-readable summary;
- convergence table, error budget, independent-check results, and known failed/blocked checks.

Follow the repository compute and archival policies. Archive extracted native files, not a newly generated ZIP/TAR as the only result. Keep computed, archived, numerically validated, and physically validated statuses distinct.

## Interpretation

Do not promote a benchmark point to a full parameter-space statement without coverage evidence. Preserve failed points and disconnected allowed regions. Distinguish theoretical realizability, experimental allowance, exclusion, not assessed, and EFT-inapplicable regions. Every reported numerical claim must state its parameter point/region, assumptions, units, precision, and supporting run/claim identifiers.
