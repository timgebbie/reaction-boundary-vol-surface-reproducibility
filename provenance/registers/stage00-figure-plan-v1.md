# Stage 00 Figure Plan v1

Artefact status: draft computational map

No figures have been generated.

| Figure ID | Concept | Theory object | Purpose | Status |
|---|---|---|---|---|
| F1 | Volatility surface and contour projection for Eq. 22 low-`z` response case | Eq. 18 closure with low-`z` case of `F_gamma(z)` | Mandatory surface output | Planned only |
| F2 | Volatility surface and contour projection for Eq. 22 high-`z` response case | Eq. 18 closure with high-`z` case of `F_gamma(z)` | Mandatory matched surface output | Planned only |
| F3 | Response-regime diagnostic | Both cases of `F_gamma(z)` from Eq. 22 | Show how the two response approximations differ before they enter the surface | Mandatory diagnostic |
| F4 | Liquidity profile diagnostic, if state-dependent liquidity is used | `L(S)` and the `1/L(S)^2` channel | Make the source of stock-price dependence visible | Optional |
| F5 | Small sensitivity panel | `gamma`, `nu`, `A_eff`, `L`, `Delta`, `alpha` | Only add if it clarifies the surface rather than bloating the project | Deferred |

Caption policy:

- Every figure should have a rich standalone caption draft.
- The caption must state the equation or object plotted, parameter values,
  grid choices, data or simulation source, and what the figure does not
  prove.
- Figure provenance must identify the script, config, raw output, and
  diagnostic status.

Prudent figure policy:

- Start with matched mandatory surface outputs for the two Eq. 22 response
  regimes: low `z` and high `z`.
- Include the response-factor diagnostic, because the response function is
  the central numerical concern.
- Add the liquidity-profile diagnostic if `L(S)` is the source of the
  stock-price dependence.
- Do not include calibrated data or fitted market surfaces in this
  simulation-only project.
