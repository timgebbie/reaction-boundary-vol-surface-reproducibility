# Revision Note v2

Artefact status: draft computational map revision

User revision applied:

- The project is simulation only.
- Do not route the current project as mixed simulation/data science.
- Use the main-result equation identified by the user as Eq. 18 rather than
  the earlier equation identified as Eq. 14.
- The first surface should be generated from the reduced-form main-result
  closure using known or declared parameters.
- The response function `F_gamma(z)` is a central unresolved numerical
  concern and should be handled explicitly in Stage 5 before implementation.
- Both asymptotic cases of the response function from the equation
  identified by the user as Eq. 22 should be simulated.
- The likely source of stock-price dependence is the liquidity profile
  `L(S)`, because the closure contains the inverse-square factor
  `1 / L(S)^2`.
- Minimum prudent outputs:
  - a table of parameter ranges and baseline simulation values;
  - a table of Eq. 22 response-regime cases;
  - matched surface-and-contour outputs for both response regimes.
- Optional figures:
  - response-factor diagnostic;
  - liquidity-profile diagnostic;
  - compact sensitivity plot only if it clarifies the surface.

No implementation, figures, tables, or numerical verification were added
in this revision.
