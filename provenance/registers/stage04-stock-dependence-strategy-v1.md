# Stage 04 Stock-Dependence Strategy v1

Artefact status: Stage 4 modelling audit register

The surface-generating closure admits stock dependence through several
channels:

```text
sigma_loc^2(S,t)
  = alpha(t)
    [A_eff(S,U(t)) / L(S,U(t))^2]
    Delta^(-gamma(S,U(t)))
    F_gamma(S,U(t))(nu(S,U(t)) Delta).
```

## Channels

| Channel | How stock dependence enters | Phenomenology |
|---|---|---|
| `L(S)` | Inverse-square factor `1 / L(S)^2` | Thin liquidity regions create larger volatility; deep liquidity suppresses volatility |
| `A_eff(S)` | Multiplicative forcing intensity | More aggressive signed-flow regions create larger volatility |
| `nu(S)` | Through `z(S)=nu(S) Delta` in `F_gamma(z)` | Slower/weaker resilience can raise volatility; stronger resilience suppresses it in high-`z` |
| `gamma(S)` | Through `Delta^(-gamma)` and `F_gamma` | More persistent order flow changes scale dependence |
| `alpha(t)` or `alpha(S,t)` | Calendar-time sampling rate | Higher activity samples operational variance faster |

## First-Pass Simulation Profiles

| Profile ID | Vary with `S` | Hold constant | Purpose |
|---|---|---|---|
| `liquidity_only` | `L(S)` | `A_eff`, `nu`, `gamma`, `alpha` | Isolate the inverse-square liquidity channel |
| `resilience_response_only` | `nu(S)` | `A_eff`, `L`, `gamma`, `alpha` | Isolate the response-channel stock dependence through `z(S)` |
| `combined_structural` | `L(S)`, `nu(S)`, optionally `A_eff(S)` | `gamma` and simple `alpha(t)` initially | Produce a stylised structural skew/stress surface |

## Audit Conclusion

The first implementation should not attempt to infer the correct empirical
stock dependence. It should show which declared structural channel produces
which surface morphology.

The cleanest pedagogical sequence is:

1. liquidity-only surface;
2. resilience-response-only surface;
3. combined structural surface.

Each should be run under both Eq. 22 response regimes unless Stage 5
decides to restrict the output count for clarity.

