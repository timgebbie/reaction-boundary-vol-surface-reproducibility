# Stage 03 Surface Design Questions v1

Artefact status: Stage 3 planning register

These questions must be answered before implementation.

1. Surface state axis:
   Use internal `S = log x`, but should the figure axis be `S`, stock
   price `x`, or log-moneyness?

2. Liquidity profile:
   What simple `L(S)` should create the first stock-price dependence?
   A homogeneous profile gives no stock-price smile/skew by itself.

3. Resilience-response profile:
   What simple `nu(S)` should be used to create stock dependence through
   `z(S)=nu(S) Delta`, especially in the high-`z` response regime?

4. Forcing profile:
   Should `A_eff(S)` remain constant except in the combined structural
   surface, or should it also be used to model order-flow stress?

5. Activity profile:
   Should `alpha(t)` be constant for the first pass, or should it vary with
   maturity to create term-structure effects?

6. Response regimes:
   Should low-`z` and high-`z` be shown as separate figures or as paired
   panels in one figure file?

7. Volatility versus variance:
   The theory gives variance. The plotted surface should probably be
   volatility, i.e. square root of projected local variance, with the
   variance surface retained as raw output.

8. Surface interpretation:
   The figure caption must say that surface shape comes from declared
   parameter profiles and response-regime choice, not empirical
   calibration.
