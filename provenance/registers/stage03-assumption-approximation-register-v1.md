# Stage 03 Assumption And Approximation Register v1

Artefact status: Stage 3 planning register

No assumptions have been numerically instantiated yet.

| Item | Source basis | Computational treatment | Status |
|---|---|---|---|
| Simulation-only routing | User revision and Stage 00 revision note | No empirical data or calibration workflow | Accepted workflow constraint |
| Main-result closure | `eq:main-operational-result`, `eq:operational-result` | First surface engine | Accepted route |
| Deterministic clock | `eq:deterministic-localvol` | Use deterministic `alpha(t)` and `U(t)` only | Accepted route |
| Non-unique time | Section on adjoint-real projections | Out of scope for first simulation | Deferred |
| Response function | `eq:F-asymp` | Simulate both low-`z` and high-`z` asymptotic cases | Accepted route |
| Bridging response evaluator | `eq:F-definition` | Possible later quadrature or hybrid check | Deferred |
| Finite cutoff | Appendix finite-cutoff spectral form | Not part of first surface | Deferred |
| Stock-price dependence | All state-dependent factors in the closure | Use explicit simulation profiles rather than a single hidden surface shape | Needs Stage 5 modelling choice |
| Liquidity channel | Liquidity factor `1 / L(S)^2` in main closure | Profile 1: liquidity-only surface | Accepted first profile |
| Resilience-response channel | `z(S)=nu(S) Delta` inside `F_gamma(z)` | Profile 2: resilience-response-only surface | Accepted first profile |
| Combined structural channel | `L(S)`, `nu(S)`, and possibly `A_eff(S)` | Profile 3: combined structural surface | Accepted first profile |
| Other state dependence | `A_eff(S,u)`, `gamma(S,u)`, `alpha(t)` | Optional declared phenomenology only | Deferred unless Stage 5 includes them |
| Parameter ranges | Theory constraints and simulation judgement | Table required later | Unresolved |
| Surface axes | Source uses `S = log x`; user-facing plot may use stock price or log-moneyness | Decide before implementation | Unresolved |

Approximation boundary:

- Low-`z` and high-`z` response cases are asymptotic regimes, not a full
  numerical solution of the response integral.
- Any state-dependent profile used to produce stock-price dependence is a
  modelling choice unless independently derived in a later stage. The
  profile should be named explicitly: liquidity-only, resilience-response,
  or combined structural.
- The simulated surface is an illustration of the closure, not an empirical
  calibration or validation.
