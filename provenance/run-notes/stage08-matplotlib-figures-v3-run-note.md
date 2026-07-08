# Stage 08 Matplotlib Figures v3 Run Note

Artefact status: refinement run note

Dependency setup used:

```bash
python -m pip install --target /workspace/reaction-boundary-vol-surface/.deps matplotlib
```

Figure command:

```bash
python scripts/05_generate_matplotlib_figures_v3.py
```

Purpose:

- Generate boxed 3D surface plots with visible axes.
- Generate true black line-contour plots rather than heatmap projections.
- Save separate PDF and PNG files for LaTeX subfigures.

Preferred LaTeX use:

- Use the PDF files first.
- Use PNG files if Overleaf rendering or compilation becomes awkward.

