# Symbolic calculation and algebraic verification

Load this reference when using Mathematica, SymPy, FeynCalc, FORM, custom tensor algebra, or symbolic code generation for a physics derivation.

## Model and convention contract

Record all conventions that can change signs, factors, or tensor structures:

- metric signature, index placement, Levi-Civita convention, Fourier transform and momentum-flow convention;
- gamma matrices, gamma5 prescription, chiral projectors, traces, charge conjugation, and spinor ordering;
- field, generator, coupling, and operator normalization;
- gauge fixing, regulator, renormalization scheme and scale;
- masses, mixing conventions, external-state normalization, and perturbative/EFT truncation.

Do not infer a convention from a package default. Verify the package's actual convention and encode it explicitly.

## Symbolic workflow

1. Translate the physical expression into a minimal symbolic representation with named assumptions and dimensions.
2. Preserve the unsimplified expression and the exact substitutions/identities used.
3. Apply simplifications only under justified assumptions. Keep denominator exclusions, branch conditions, tensor symmetries, and regulator dependence visible.
4. Verify the result in the original expression and requested domain.
5. Export generated code only after checking that the generated expression preserves precision, branches, dimensions, and conventions.

Use exact rationals and exact symbolic constants where appropriate. Do not introduce floating-point literals into an exact derivation without a reason.

## Independent checks

For important expressions, select a genuinely different route where feasible:

- hand-derived special cases or a second algebraic decomposition;
- dimensional analysis and index/symmetry checks;
- substitution into the original identity;
- numerical evaluation at generic nonsingular points with high precision;
- comparison with an independent package or representation;
- limiting cases such as vanishing mixing, decoupling, equal masses, or a controlled regulator limit.

A second simplifier applied to the same expression is a consistency check, not necessarily an independent derivation. Record common inputs and shared transformations.

## Loop and matching calculations

For loop work, keep diagram enumeration, numerator algebra, tensor reduction, scalar integral reduction, UV/IR separation, counterterms, EFT subtraction, and operator-basis reduction as distinct stages.

- Enumerate relevant diagrams, contact terms, counterterms, and gauge/Goldstone/ghost contributions before claiming completeness.
- Do not set a scaleless integral to zero until UV and IR poles have been distinguished.
- Apply compatible IR prescriptions on both sides of a matching calculation and subtract the soft EFT contribution exactly once.
- Distinguish a subdiagram, topology family, polarization, coupling sector, or projected amplitude from a complete matching result.
- Verify signs, symmetry factors, mass dimensions, tensor structures, and gauge/symmetry identities in the declared conventions.

## Tool choice

The model selects the symbolic tool based on the task and available environment. Mathematica, FeynCalc, FORM, SymPy, and direct analytic derivation are alternatives, not a mandatory stack. Verify the actual executable, package version, license/runtime availability, and input/output interface before claiming a tool was used.

Retain the source expression, executable script/notebook, package versions, exact command, output, and validation evidence under the canonical research record.
