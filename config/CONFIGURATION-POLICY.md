# Configuration Policy

> The following Stage 2 note records the original configuration decisions. The released workflow uses [profile-definitions-v1.json](profile-definitions-v1.json) and [parameter-ranges-v1.csv](parameter-ranges-v1.csv). The change-control rule below applies to future changes.

Artefact status: Stage 2 configuration-control note

No numerical parameter defaults have been accepted yet.

Configuration files to create in later stages:

- `config/parameters-baseline.yaml` or `.json`
- `config/parameter-ranges.csv`
- `config/response-regimes.csv`
- `config/surface-grid.yaml` or `.json`

Required configuration decisions before implementation:

1. Surface state axis: stock price, log-price state, or log-moneyness.
2. Maturity axis and units.
3. Baseline and range for `A_eff`.
4. Baseline and range/profile for `L(S)`.
5. Baseline and range for `nu`.
6. Baseline and range for `gamma`.
7. Operational coarse-graining scale `Delta`.
8. Deterministic activity profile `alpha(t)`.
9. Low-z and high-z response cases from Eq. 22.
10. Whether a bridging evaluator for `F_gamma(z)` is needed after the two
    asymptotic cases are implemented.

Change-control rule:

Any later change to parameter ranges, defaults, grids, units, or response
regime definitions must be recorded in the artefact register and in the
relevant run note.

