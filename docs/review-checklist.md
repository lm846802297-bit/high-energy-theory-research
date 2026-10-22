# Scientific Change Review Checklist

Use this checklist when reviewing a research-change record, a pull request containing scientific work, or a manuscript update. Not every check applies to every task; N/A requires a reason.

## A. Baseline and scope

- [ ] The baseline revision and relevant input/output artifacts are identifiable.
- [ ] The scientific question is explicit and not phrased to presuppose an outcome.
- [ ] The delta, controls, exclusions, and target outputs are specified.
- [ ] Assumptions, conventions, approximations, parameter ranges, and benchmark dependence are recorded.
- [ ] The change is small enough to review, or independent subchanges are clearly separated.

## B. Theory and derivation

- [ ] Definitions, field content, charges, basis, and normalization match the stated model.
- [ ] Algebra, signs, factors, indices, and conventions have been checked.
- [ ] Dimensional consistency and relevant symmetries have been checked.
- [ ] Known limits, controlled approximations, and perturbative order are documented.
- [ ] Renormalization scheme, scale, subtraction conventions, and matching definitions are recorded where relevant.
- [ ] Any symbolic-computation assumptions and simplifications are visible.
- [ ] Independent derivation or cross-check is documented for results where it is needed.

## C. Computation and data

- [ ] Inputs, source revision, software/package versions, settings, and outputs are traceable.
- [ ] Numerical precision, tolerance, convergence, and stability are appropriate to the claimed accuracy.
- [ ] Failed runs, warnings, discarded data, and post-processing are documented.
- [ ] Plots and tables can be regenerated from identifiable inputs.
- [ ] External data and experimental limits have a traceable source/version and correct units.
- [ ] The mapping from model parameters to observables follows the experiment's actual assumptions and validity domain.
- [ ] Confidence levels, likelihoods, correlations, and statistical interpretations are not conflated.

## D. Physical claim

- [ ] Each important claim is stated precisely and linked to supporting evidence.
- [ ] Evidence supports the full stated domain, not merely a single benchmark or selected point.
- [ ] Uncertainties, limitations, and competing explanations are addressed where relevant.
- [ ] Missing work is marked unresolved rather than described as passed or negligible.
- [ ] A numerical difference is not automatically treated as physically or phenomenologically significant.
- [ ] Claim status is separate from work status and individual check status.

## E. Dependency and manuscript impact

- [ ] Downstream coefficients, scans, constraints, plots, tables, and conclusions have been reviewed.
- [ ] Stale outputs have not been reused after upstream inputs changed.
- [ ] Manuscript text, equations, captions, appendices, abstract, and conclusion are consistent with the assessed claim.
- [ ] Reviewer replies do not state that incomplete calculations or revisions have been completed.
- [ ] The record identifies remaining work and the next concrete action.

## F. Decision

- [ ] The decision is stated: retain, qualify, revise, withdraw, or continue investigating.
- [ ] The decision follows from recorded evidence and is limited to its valid scope.
- [ ] Important evidence and outputs are preserved with versions or hashes where appropriate.
- [ ] The work status, claim status, and check statuses are mutually consistent.

**Review outcome:** [Accept for stated scope / Accept with limitations / Changes required / Blocked]

**Rationale and required actions:** [Record the evidence-based decision]
