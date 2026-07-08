# Stage 03 Parameter Source Map v1

Artefact status: Stage 3 planning register

No numerical defaults or ranges have been accepted.

| Parameter | Source role | First-pass computational status | Notes for Stage 5 |
|---|---|---|---|
| `A_eff(S)` | Effective signed-forcing intensity, `A_m / D_u` | Required | Constant in first two profiles; optional state dependence in combined structural profile |
| `L(S)` | Local liquidity slope | Required | Profile 1 stock-dependence channel; also likely included in combined structural profile |
| `nu(S)` | Resilience | Required | Profile 2 stock-dependence channel through `z(S) = nu(S) Delta` |
| `gamma` or `gamma(S)` | Long-memory exponent, `0 < gamma < 1` | Required | Keep constant first unless Stage 5 intentionally explores memory-state dependence |
| `Delta` | Operational coarse-graining scale | Required | Operational scale, not maturity |
| `F_gamma(z)` | Response factor | Required | Branch into low-`z` and high-`z` cases |
| `K_gamma^(0)` | High-`z` prefactor | Required for high-`z` branch | Use gamma functions; guard endpoints |
| `alpha(t)` | Deterministic activity rate | Required for calendar projection | Constant first pass is likely prudent |
| `alpha(S,t)` | State-dependent activity clock | Optional | Defer unless explicit phenomenology requires it |
| `U(t)` | Deterministic operational clock | Required for calendar projection | If `alpha` constant, `U(t)` is simple |
| `S` or `x` | State axis | Required | Decide internal versus plotted axis |
| `T` | Maturity axis | Required for surface | Simulation axis only |

Mandatory future table:

- `tables/parameter-ranges-v1.csv`
- `tables/parameter-ranges-v1.tex`

The LaTeX table should be standalone and include comments listing required
packages and suggested cut-and-paste explanatory text.
