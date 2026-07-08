# Stage 8 Figure, Table, And Caption Generation

Artefact status: Stage 8 completion candidate

Commands run:

```bash
python scripts/01_make_tables.py
python scripts/02_generate_surfaces.py
```

Generated tables:

- `tables/parameter-ranges-v1.csv`
- `tables/parameter-ranges-v1.tex`
- `tables/response-regimes-v1.csv`
- `tables/response-regimes-v1.tex`
- `tables/profile-definitions-v1.csv`
- `tables/profile-definitions-v1.tex`

Generated figures:

- `figures/surface-liquidity-only-low-z-v1.pdf`
- `figures/surface-liquidity-only-high-z-v1.pdf`
- `figures/surface-resilience-response-only-low-z-v1.pdf`
- `figures/surface-resilience-response-only-high-z-v1.pdf`
- `figures/surface-combined-structural-low-z-v1.pdf`
- `figures/surface-combined-structural-high-z-v1.pdf`

Generated raw and summary outputs:

- six compressed raw surface arrays in `raw-outputs/`;
- six summary CSV files in `outputs/`.

Generated captions and provenance:

- six standalone caption drafts in `captions/`;
- `figure-table-manifest.md`;
- `figure-table-provenance-register.csv`.

Verification performed:

- Stage 7 diagnostics had already verified 42 checks before generation.
- Stage 8 scripts compiled successfully.
- A representative generated PDF was rendered to PNG:
  `diagnostics/render-checks/surface-combined-structural-high-z-v1.png`.
- The representative render was visually inspected and confirmed nonblank,
  with readable labels, a surface-style panel, a filled contour projection,
  and a color scale.

Implementation note:

- Matplotlib was unavailable in the runtime, so figure generation uses
  ReportLab vector PDF rendering.
- The script embeds DejaVu Sans fonts to avoid PDF text-rendering issues.

Current output status:

- Tables: table drafts.
- Figures: figure drafts. The Matplotlib v3 figure family is preferred
  after controlled refinement.
- Captions: standalone caption drafts.
- Interpretation: not yet written.

Recommended next stage:

Stage 9: sensitivity, robustness, and edge-case checks.
