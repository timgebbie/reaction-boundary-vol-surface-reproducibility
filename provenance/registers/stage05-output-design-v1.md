# Stage 05 Output Design v1

Artefact status: numerical design, no implementation

## Tables

| Output ID | File targets | Purpose | Status |
|---|---|---|---|
| `T1` | `tables/parameter-ranges-v1.csv`, `tables/parameter-ranges-v1.tex` | parameter ranges and baseline values | Planned |
| `T2` | `tables/response-regimes-v1.csv`, `tables/response-regimes-v1.tex` | low-z and high-z formulas from Eq. 22 | Planned |
| `T3` | `tables/profile-definitions-v1.csv`, `tables/profile-definitions-v1.tex` | profile formulas and varied channels | Planned |

LaTeX table policy:

- Every table must be standalone.
- Include comments listing required packages.
- Include comments with short text that can be cut into the paper if useful.

## Figures

The full design has six surface outputs:

| Figure ID | Profile | Response regime | File target |
|---|---|---|---|
| `F1` | `liquidity_only` | `low_z` | `figures/surface-liquidity-only-low-z-v1.pdf` |
| `F2` | `liquidity_only` | `high_z` | `figures/surface-liquidity-only-high-z-v1.pdf` |
| `F3` | `resilience_response_only` | `low_z` | `figures/surface-resilience-response-only-low-z-v1.pdf` |
| `F4` | `resilience_response_only` | `high_z` | `figures/surface-resilience-response-only-high-z-v1.pdf` |
| `F5` | `combined_structural` | `low_z` | `figures/surface-combined-structural-low-z-v1.pdf` |
| `F6` | `combined_structural` | `high_z` | `figures/surface-combined-structural-high-z-v1.pdf` |

Each figure should contain:

- one 3D surface panel;
- one contour projection panel;
- clear label for profile and response regime;
- caption stating that this is simulation, not calibration.

Optional diagnostic figures:

| Figure ID | Concept | Status |
|---|---|---|
| `D1` | response-regime functions versus `gamma` and `z` | Optional, but recommended |
| `D2` | profile components `L(m)`, `z(m)`, `A_eff(m)` | Optional, but recommended |

Practical output-count note:

If six surface files feel too many for the first review, Stage 8 may
combine them into fewer multi-panel figures. The computation should still
generate the six profile-regime combinations as distinct raw outputs.

