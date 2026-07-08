# Stage 05 Script Plan v1

Artefact status: numerical design, no implementation

No scripts have been created yet.

Recommended Stage 6 implementation order:

| Step | Planned file | Purpose |
|---|---|---|
| 1 | `config/parameter-ranges-v1.csv` | baseline and ranges |
| 2 | `config/profile-definitions-v1.json` | profile coefficients and grid |
| 3 | `functions/response_regimes.py` | low-z and high-z response functions |
| 4 | `functions/structural_profiles.py` | `L(m)`, `A_eff(m)`, `z(m)`, `alpha(T)` |
| 5 | `functions/vol_surface_kernel.py` | projected variance and volatility evaluators |
| 6 | `scripts/01_make_tables.py` | parameter, response, and profile tables |
| 7 | `scripts/02_generate_surfaces.py` | six surface and contour outputs |
| 8 | `scripts/03_run_diagnostics.py` | positivity, finite-value, and shape diagnostics |

Expected Python dependencies:

- `numpy`
- `pandas`
- `matplotlib`

Stage 7 update:

- `scipy` is not needed for the current helper functions. The high-z
  gamma-function prefactor uses the standard-library `math.lgamma`.

No notebook is planned for the first implementation.

Each script should write a log or summary into `diagnostics/` once
implementation begins.
