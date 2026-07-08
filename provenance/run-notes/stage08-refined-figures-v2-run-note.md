# Stage 08 Refined Figures v2 Run Note

Artefact status: refinement run note

Command:

```bash
python scripts/04_generate_refined_figures_v2.py
```

Purpose:

- Keep the v1 combined surface/contour figures intact.
- Generate separate surface and contour files for LaTeX subfigures.
- Generate both PDF and PNG versions.
- Render contours in black and white.
- Box the surface plots.
- Use clearer axis labels:
  - `log-moneyness m = ln(x/x0)`;
  - `maturity T`;
  - `projected local volatility`.

Expected figure pattern:

- `figures/surface3d-*-v2.pdf`
- `figures/surface3d-*-v2.png`
- `figures/contour-*-v2.pdf`
- `figures/contour-*-v2.png`

