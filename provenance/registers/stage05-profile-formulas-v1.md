# Stage 05 Profile Formulas v1

Artefact status: numerical design, no implementation

Use log-moneyness `m = log(x / x0)`.

## Shared Components

Activity profile:

```text
alpha(T) = alpha0 * (1 + a_short exp(-T / tau_alpha)).
```

Low-z response:

```text
F_low(gamma) = tan(pi gamma / 2) / (2 (1 - gamma)).
```

High-z response:

```text
F_high(gamma, z) = K_gamma_0(gamma) z^(gamma - 1).
```

## Profile 1: `liquidity_only`

Vary liquidity only:

```text
L(m) = L0 * max(L_floor, 1 + L_skew m + L_smile m^2)
A_eff(m) = A_eff0
nu(m) Delta = z_regime
gamma(m) = gamma0
```

Interpretation:

- Positive `L_skew` makes downside `m < 0` less liquid.
- Positive `L_smile` makes both tails less liquid relative to the center.
- Volatility responds through `1 / L(m)^2`.

## Profile 2: `resilience_response_only`

Vary resilience-response only:

```text
L(m) = L0
A_eff(m) = A_eff0
z(m) = z_regime * exp(nu_skew * m)
gamma(m) = gamma0
```

Interpretation:

- With `nu_skew > 0`, downside `m < 0` has smaller `z`.
- In the high-z branch, smaller `z` increases volatility because
  `gamma - 1 < 0`.
- In the low-z branch, `nu(m)` has no leading-order effect for constant
  `gamma`; this should be visible and explained.

## Profile 3: `combined_structural`

Vary liquidity, resilience, and downside forcing:

```text
L(m) = L0 * max(L_floor, 1 + L_skew m + L_smile m^2)
z(m) = z_regime * exp(nu_skew * m)
A_eff(m) = A_eff0 * exp(-A_stress m)
gamma(m) = gamma0
```

Interpretation:

- Downside may be less liquid, less resilient, and more strongly forced.
- This is a stylised structural stress/skew profile.
- It must be captioned as simulation phenomenology.

## Floor Policy

Use a small positive floor for liquidity:

```text
L_floor = 0.20.
```

This avoids accidental negative liquidity values in exploratory ranges. If
the floor is hit, diagnostics should report it.

