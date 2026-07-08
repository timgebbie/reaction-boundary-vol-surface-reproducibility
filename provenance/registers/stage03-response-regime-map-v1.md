# Stage 03 Response-Regime Map v1

Artefact status: Stage 3 planning register

The response function is the main numerical concern. The first simulation
will therefore treat both asymptotic response regimes as explicit cases.

| Regime ID | Condition | Response approximation | Computational implication | Output requirement |
|---|---|---|---|---|
| `low_z` | `z = nu Delta << 1` | `F_gamma(z) ~ tan(pi gamma / 2) / (2 (1 - gamma))` | Response factor depends on `gamma` but not on `z` at leading order | Surface plus contour |
| `high_z` | `z = nu Delta >> 1` | `F_gamma(z) ~ K_gamma^(0) z^(gamma - 1)` | Response factor decays with `z` because `gamma - 1 < 0` | Matched surface plus contour |

Unresolved Stage 5 question:

Should the first implementation include only these two clean asymptotic
branches, or also a bridging numerical evaluation of the integral
`eq:F-definition` for intermediate `z`?

Recommendation:

Start with the two asymptotic branches. Add a bridging evaluator only after
the low-`z` and high-`z` surfaces exist and diagnostics show that an
intermediate-regime plot is needed.

Stock-dependence consequence:

- In the low-`z` case, `F_gamma(z)` is independent of `z` at leading order
  for fixed `gamma`, so a state-dependent `nu(S)` will not create visible
  stock dependence through the response factor unless `gamma(S)` also
  varies or a bridge/intermediate evaluator is introduced.
- In the high-`z` case, `F_gamma(z) ~ K_gamma^(0) z^(gamma - 1)`, so
  `nu(S)` directly creates stock dependence through `z(S)=nu(S) Delta`.
  Because `gamma - 1 < 0`, larger `nu(S)` suppresses volatility and smaller
  `nu(S)` raises volatility.
