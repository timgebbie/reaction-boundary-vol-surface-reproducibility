# Stage 8 v3 Figure Refinement Report

Artefact status: Stage 8 controlled refinement

Reason for refinement:

- The v1 combined figures were useful but not ideal for LaTeX subfigures.
- The v2 figures separated surface and contour outputs, but the contour was
  still closer to a grayscale heatmap than a true contour-line plot.
- The user requested proper contour lines, boxed 3D surface axes, and PNG
  alternatives.

Action taken:

- Installed Matplotlib locally for figure generation.
- Added `scripts/05_generate_matplotlib_figures_v3.py`.
- Added `run-notes/stage08-matplotlib-figures-v3-run-note.md`.
- Added `config/requirements-figures-v3.txt`.
- Generated separate PDF and PNG outputs for each surface and contour.
- Generated `figure-table-manifest-v3-addendum.md`.
- Generated standalone v3 caption drafts.

Preferred figure family:

Use the Matplotlib v3 files for paper-facing figure work:

- `figures/mpl-surface3d-*-v3.pdf`
- `figures/mpl-contour-lines-*-v3.pdf`

Keep the PNG files as visual-review and fallback assets:

- `figures/mpl-surface3d-*-v3.png`
- `figures/mpl-contour-lines-*-v3.png`

Status:

- v1 and v2 figure files are preserved as prior drafts.
- v3 is the preferred figure family.
- This is a Stage 8 refinement, not a change to the theory-to-code map or
  numerical design.

Recommended next stage:

Stage 9: sensitivity, robustness, and edge-case checks.

