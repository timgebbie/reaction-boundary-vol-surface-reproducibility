# Stage 08 Generation Run Note v1

Artefact status: figure/table generation run note

Commands:

```bash
python scripts/01_make_tables.py
python scripts/02_generate_surfaces.py
```

Expected table outputs:

- `tables/parameter-ranges-v1.csv`
- `tables/parameter-ranges-v1.tex`
- `tables/response-regimes-v1.csv`
- `tables/response-regimes-v1.tex`
- `tables/profile-definitions-v1.csv`
- `tables/profile-definitions-v1.tex`

Expected figure outputs:

- `figures/surface-liquidity-only-low-z-v1.pdf`
- `figures/surface-liquidity-only-high-z-v1.pdf`
- `figures/surface-resilience-response-only-low-z-v1.pdf`
- `figures/surface-resilience-response-only-high-z-v1.pdf`
- `figures/surface-combined-structural-low-z-v1.pdf`
- `figures/surface-combined-structural-high-z-v1.pdf`

Rendering note:

- The surface figures are rendered directly as vector PDFs with ReportLab.
  Matplotlib is not required in the current runtime.

Expected provenance outputs:

- `figure-table-manifest.md`
- `figure-table-provenance-register.csv`
- `captions/caption-surface-*-v1.md`
