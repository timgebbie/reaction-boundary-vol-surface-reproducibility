# Local Volatility Interpretation Note v1

Artefact status: science review note

The simulated reaction-boundary volatility surfaces are reasonable as a first
phenomenological mechanism model, but they should not be described as
calibrated market local-volatility surfaces.

## Main Distinction

The generated surface is a projected structural volatility surface. It assigns
a volatility value to log-moneyness and maturity using declared order-book
profiles. A calibrated Dupire local-volatility surface is inferred from option
prices, typically under a risk-neutral pricing measure, and must be consistent
with the associated option surface.

## Reasonable Market Phenomenology

The combined structural high-z case is the most market-like first simulation.
It combines:

- lower downside liquidity through the inverse-square liquidity channel;
- weaker downside resilience through `z(m)=nu(m) Delta`;
- stronger downside signed-flow forcing.

These mechanisms are qualitatively consistent with equity-like downside skew:
stress states tend to be less liquid, more order-flow dominated, and less
resilient.

## Interpretation Limits

- The surfaces are not calibrated to option data.
- The surfaces have not been passed through a pricing PDE.
- No static-arbitrage constraints have been imposed on an option price
  surface.
- The figures should not be compared directly with implied volatility except
  as a qualitative shape comparison.
- A later empirical comparison should align the state coordinate with
  log-strike or log-forward moneyness, such as `log(K/S0)` or `log(K/F0(T))`.

## Figure Implications

The low-z resilience-response-only figure is primarily diagnostic. At fixed
`gamma`, the leading low-z response approximation does not depend on `z`, so
varying `z(m)` alone does not create leading stock dependence. The high-z
branch is the relevant first branch for visible response-channel stock
dependence.

The supplement should therefore frame the six surfaces as mechanism
illustrations. The combined structural high-z surface can be emphasized as
the closest first-pass candidate for comparison with calibrated local
volatility morphology.
