# Stage 5 Algorithm, Tooling, And Numerical Design

Artefact status: Stage 5 completion candidate

Completed:

- Selected dimensionless log-moneyness `m = log(x/x0)` as internal state.
- Selected maturity `T` as the plotting time axis.
- Designed the projected local-volatility surface engine.
- Kept both Eq. 22 response regimes as mandatory branches.
- Designed three structural simulation profiles:
  `liquidity_only`, `resilience_response_only`, and `combined_structural`.
- Proposed dimensionless baseline values and ranges for first
  implementation.
- Planned table, figure, script, and diagnostic outputs.
- Confirmed Python-first standalone script workflow.

Not completed, by design:

- No code has been written.
- No configuration files have been instantiated as executable inputs.
- No tables or figures have been generated.
- No diagnostics have been run.

Recommended next stage:

Stage 6: implementation of the first computational target. The recommended
first target is configuration and response-regime functions, followed by
profile functions and kernel evaluation.

