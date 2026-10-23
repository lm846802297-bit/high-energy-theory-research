(* Separate Mathematica check for the UV-EFT PV derivative pilot.
   Not executed in GitHub Actions; do not mark as passed until locally run. *)

ClearAll[r, L, x, bbarMMIntegral, bprimeMMIntegral, bbarMixedIntegral,
  bprimeMixedIntegral, bbarMM, bprimeMM, bbarMixed, bprimeMixed, fprime,
  expectedLeading, expectedFirst, expectedSecond, series2, check, results];

assumptions = 0 < r < 1 && Element[L, Reals] && Element[x, Reals];

bbarMMIntegral = FullSimplify[
  -Integrate[Log[Exp[L]], {x, 0, 1}, Assumptions -> Element[L, Reals]],
  Element[L, Reals]
];
bprimeMMIntegral = Integrate[x (1 - x), {x, 0, 1}];
bbarMixedIntegral = FullSimplify[
  -Integrate[Log[(1 - x + r x) Exp[L]], {x, 0, 1},
    Assumptions -> 0 < r < 1 && Element[L, Reals]],
  0 < r < 1 && Element[L, Reals]
];
bprimeMixedIntegral = FullSimplify[
  Integrate[x (1 - x)/(1 - x + r x), {x, 0, 1},
    Assumptions -> 0 < r < 1],
  0 < r < 1
];

bbarMM = -L;
bprimeMM = 1/6;
bbarMixed = 1 - L + r Log[r]/(1 - r);
bprimeMixed = (1 + r)/(2 (r - 1)^2) - r Log[r]/(r - 1)^3;
fprime = -2 bbarMM + 8 bprimeMM + 4 bbarMixed - 8 (1 + r) bprimeMixed;

expectedLeading = 4/3 - 2 L;
expectedFirst = expectedLeading - 4 r Log[r] - 16 r;
expectedSecond = expectedFirst - 28 r^2 Log[r] - 32 r^2;
series2 = Normal[Series[fprime, {r, 0, 3}]];

check[name_, statement_] := Module[{ok = TrueQ[FullSimplify[statement, assumptions]]},
  Print[If[ok, "PASS: ", "FAIL: "], name]; ok
];

results = {
  check["Bbar_MM parameter integral", bbarMMIntegral == bbarMM],
  check["M2 Bprime_MM parameter integral", bprimeMMIntegral == bprimeMM],
  check["Bbar_mM parameter integral", bbarMixedIntegral == bbarMixed],
  check["M2 Bprime_mM parameter integral", bprimeMixedIntegral == bprimeMixed],
  check["leading small-r coefficient",
    FullSimplify[Coefficient[series2, r, 0] - expectedLeading, assumptions] == 0],
  check["first correction coefficients",
    FullSimplify[series2 - expectedFirst + 28 r^2 Log[r] + 32 r^2, assumptions] == 0],
  check["second-order small-r expansion",
    FullSimplify[series2 - expectedSecond, assumptions] == 0],
  check["1PI insertion factor at mu=M",
    FullSimplify[(-expectedLeading /. L -> 0)/(16 Pi^2) == -1/(12 Pi^2)]],
  check["conditional single-operator projection factor",
    FullSimplify[-2 (-expectedLeading /. L -> 0)/(16 Pi^2) == 1/(6 Pi^2)]]
};

Print["Passed checks: ", Count[results, True], "; failed checks: ", Count[results, False]];
Print["Scope: PV integrals, small-r expansion, and conditional projection factor only."];
Print["Limitation: no full UV loop numerator or complete-basis Wilson coefficient is checked here."];
