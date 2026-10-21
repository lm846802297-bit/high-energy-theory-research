# Evidence and claim gates

## Claim statuses

Use explicit status labels; do not infer one status from another.

- **draft:** proposed but not yet checked.
- **derived:** obtained in the current work under stated assumptions and conventions.
- **literature-supported:** supported by a cited source that has been inspected sufficiently to identify the relevant claim.
- **independently-checked:** checked by a genuinely distinct route, with the method and result recorded.
- **experimentally-allowed:** passes the specific experimental constraints actually evaluated under the stated assumptions.
- **excluded:** excluded by a named constraint or analysis in a defined parameter region.
- **blocked:** cannot be decided because an input, method, or validation is missing.
- **not-assessed:** no adequate test has been performed.
- **contradicted:** conflicting evidence or a failed check remains unresolved.

## Minimum claim record

For each consequential claim, retain:

1. Stable claim identifier and precise statement.
2. Equations/sections, parameter point or region, and scope.
3. Assumptions, conventions, approximations, and validity domain.
4. Source identifiers and exact supporting location, or derivation/run identifiers.
5. Validation method, result, and artifact references.
6. Dependencies and invalidation conditions.
7. Status, uncertainty, and unresolved questions.

## Gate rules

- A failed test cannot be converted to pass by rewriting the prose.
- A citation is evidence provenance, not proof that the cited source supports the exact claim.
- A benchmark validates only that benchmark unless coverage arguments establish more.
- “Allowed” means allowed by the explicitly evaluated constraints, not by every possible experiment.
- “Not excluded” is not equivalent to “experimentally established.”
- Missing raw-byte integrity must remain visible; alternative identity is not byte equality.
- Any change to a dependency that affects a result invalidates or re-runs downstream checks.
