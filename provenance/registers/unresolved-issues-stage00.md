# Unresolved Issues: Stage 00

Artefact status: draft computational map

These issues are intentionally unresolved at Stage 1 / Stage 1A.

1. Exact numerical treatment of `F_gamma(z)`: simulate both Eq. 22
   asymptotic cases, then decide whether a bridging quadrature,
   finite-cutoff integral, or hybrid method is also needed.
2. How to introduce the correct stock-price dependence; the leading
   candidate is state-dependent liquidity `L(S)`.
3. Whether the first surface is over log-price state, stock price,
   log-moneyness, maturity, operational scale, or a reduced diagnostic grid.
4. Whether `A_eff`, `L`, `nu`, `gamma`, and `alpha` are homogeneous constants
   or state/time-dependent fields in the first implementation.
5. Accepted parameter ranges, units, and normalisations.
6. Environment policy: lightweight requirements file versus pinned lockfile.
7. Random seed policy, if path simulation or Monte Carlo is introduced.
8. Acceptance criteria for a "reasonable approximation" to the
    reaction-boundary volatility surface.
