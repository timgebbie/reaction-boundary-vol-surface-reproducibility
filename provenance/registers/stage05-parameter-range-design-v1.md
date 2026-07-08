# Stage 05 Parameter-Range Design v1

Artefact status: numerical design, no implementation

The ranges below are dimensionless simulation ranges, not empirical
estimates.

| Parameter | Baseline | Planned range | Role |
|---|---:|---:|---|
| `gamma` | `0.55` | `[0.30, 0.80]` | long-memory exponent; avoid endpoints |
| `Delta` | `1.0` | `[0.5, 2.0]` | operational coarse-graining scale |
| `A_eff0` | `1.0` | `[0.5, 2.0]` | effective signed-forcing intensity scale |
| `L0` | `1.0` | `[0.75, 1.5]` | baseline liquidity slope |
| `z_low` | `0.05` | `[0.01, 0.10]` | low-z response-regime marker |
| `z_high0` | `10.0` | `[5.0, 25.0]` | high-z response-regime marker |
| `alpha0` | `1.0` | `[0.5, 2.0]` | baseline deterministic activity |
| `a_short` | `0.25` | `[0.0, 0.75]` | short-maturity activity lift |
| `tau_alpha` | `0.50` | `[0.25, 1.0]` | activity decay scale in years |

Profile-shape coefficients:

| Parameter | Baseline | Planned range | Role |
|---|---:|---:|---|
| `L_skew` | `0.80` | `[0.0, 1.5]` | lower liquidity on downside when positive |
| `L_smile` | `1.50` | `[0.0, 3.0]` | thinner liquidity away from center |
| `nu_skew` | `1.00` | `[0.0, 2.0]` | weaker downside resilience when positive |
| `A_stress` | `0.75` | `[0.0, 1.5]` | stronger downside forcing in combined profile |

Accepted constraints:

- Clamp or design profiles so `L(m) > 0`, `A_eff(m) > 0`, `nu(m) > 0`,
  and `alpha(T) > 0`.
- Keep `0 < gamma < 1`.
- Treat all values as simulation controls, not measured market quantities.

Required future files:

- `config/parameter-ranges-v1.csv`
- `config/profile-definitions-v1.yaml` or `.json`
- `tables/parameter-ranges-v1.csv`
- `tables/parameter-ranges-v1.tex`

