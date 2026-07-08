# Stage 05 Numerical Design v1

Artefact status: numerical design, no implementation

## Scope

This stage designs the first simulation. It does not create Python scripts,
figures, tables, outputs, diagnostics, or computational claims.

The first implementation should be a dimensionless structural simulation
of the projected local-volatility surface. It should not be presented as a
calibration.

## Internal State And Surface Axes

Use internal log-moneyness:

```text
m = log(x / x0)
```

This is preferred over raw stock price for the first implementation because
it is dimensionless, centered, and easy to interpret. The source theory uses
`S` as the log-price or boundary state; the first simulation should identify
`S` with `m` after centering at the reference price.

Recommended first grid:

| Axis | Symbol | Planned range | Notes |
|---|---|---:|---|
| log-moneyness | `m` | `[-0.30, 0.30]` | roughly 74% to 135% moneyness |
| maturity | `T` | `[1/12, 2.0]` | years, for plotting only |

The theory gives local variance. The plotted surface should be local
volatility:

```text
sigma_loc(m,T) = sqrt(sigma_loc_squared(m,T)).
```

The variance surface should still be saved as raw machine-readable output
once implementation begins.

## Surface Engine

Use the main-result closure and deterministic-clock projection:

```text
sigma_loc_squared(m,T)
  = alpha(T)
    [A_eff(m) / L(m)^2]
    Delta^(-gamma)
    F_regime(gamma, z(m)).
```

where:

```text
z(m) = nu(m) Delta.
```

For the first design, keep `gamma` constant in all profiles unless a later
revision explicitly introduces `gamma(m)`.

## Response Regimes

Both Eq. 22 asymptotic cases are mandatory:

```text
low_z:
F_low(gamma) = tan(pi gamma / 2) / (2 (1 - gamma))

high_z:
F_high(gamma, z) = K_gamma_0(gamma) z^(gamma - 1)
```

The high-z prefactor is:

```text
K_gamma_0(gamma)
  = Gamma(1-gamma) sin(pi gamma / 2)
    Gamma(gamma/2) Gamma((1-gamma)/2) / (2 pi^(3/2)).
```

Stage 5 recommendation:

- Implement only the two asymptotic regimes first.
- Do not implement the full response integral yet.
- Add a bridging evaluator later only if the asymptotic surfaces leave an
  important intermediate-regime ambiguity.

## First-Pass Profiles

Use three named profiles.

| Profile ID | Vary with `m` | Hold constant | Purpose |
|---|---|---|---|
| `liquidity_only` | `L(m)` | `A_eff`, `nu`, `gamma`, `alpha` | isolate inverse-square liquidity channel |
| `resilience_response_only` | `nu(m)` | `A_eff`, `L`, `gamma`, `alpha` | isolate `z(m)=nu(m) Delta` response channel |
| `combined_structural` | `L(m)`, `nu(m)`, optionally `A_eff(m)` | `gamma`; simple `alpha(T)` | stylised skew/stress mechanism |

## Activity Term Structure

For the first implementation, allow a simple deterministic activity profile
so that the plotted surface can have a maturity dimension:

```text
alpha(T) = alpha0 * activity_shape(T).
```

Recommended first activity shape:

```text
activity_shape(T) = 1 + a_short exp(-T / tau_alpha).
```

This is a simulation phenomenology choice. It means short maturities sample
operational variance more rapidly. It is not an empirical activity estimate.

If the user wants an even cleaner mechanism isolation, set `a_short = 0`
and accept that maturity dependence will be flat unless another
time-dependent profile is introduced.

## Stage 6 Implementation Order

Recommended first implementation target:

1. parameter and profile configuration files;
2. response-regime functions;
3. profile functions;
4. kernel evaluator;
5. parameter and response-regime tables;
6. surface generation script;
7. diagnostics.

