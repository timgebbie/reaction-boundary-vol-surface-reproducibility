# Stage 4 Modelling And Numerical-Method Audit

Artefact status: Stage 4 completion candidate

Completed:

- Refactored the stock-dependence strategy beyond a liquidity-only view.
- Identified all plausible stock-dependence channels in the main closure:
  `L(S)`, `A_eff(S)`, `nu(S)`, `gamma(S)`, and activity.
- Recorded that `z(S)=nu(S) Delta` inside `F_gamma(z)` is a genuine
  response-channel source of stock dependence.
- Recorded three first-pass simulation profiles:
  `liquidity_only`, `resilience_response_only`, and `combined_structural`.
- Audited the low-`z` and high-`z` response regimes:
  low-`z` does not carry leading-order `nu(S)` dependence for fixed
  `gamma`, while high-`z` does through `z^(gamma-1)`.

Modelling conclusions:

- The project remains simulation-only.
- The first implementation should make structural channels visible rather
  than produce one over-compressed surface.
- Parameter profiles are phenomenological simulation choices unless a
  later empirical workflow is explicitly opened.
- A bridging response evaluator for intermediate `z` is optional and should
  not be introduced before the two asymptotic cases are implemented.

Risks carried forward:

- Too many profile/regime combinations could bloat the first figure set.
- A state-dependent liquidity or resilience profile could be mistaken for
  empirical calibration unless captions are explicit.
- The low-`z` branch may show no resilience-driven state dependence if
  `gamma` is constant; this should be explained rather than hidden.

Recommended next stage:

Stage 5: algorithm, Python-first tooling, and numerical design.

