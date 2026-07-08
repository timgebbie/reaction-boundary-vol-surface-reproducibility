Reaction Boundary Volatility Surface
Reproducibility build notes

Artefact status: Stage 10 reproducibility README

Project status
Simulation-only computational project. The current preferred outputs are
the Matplotlib v3 figures, standalone LaTeX/CSV tables, diagnostics, and
sensitivity checks.

Source freeze
Frozen theory source and BibTeX files are in:

- source/CATG-BSMFromAdjointProjection-FMF-v1.8-source-v0.tex
- source/BSMFromAdjointProjection-FMF-v1.8-references-v0.bib
- source/SOURCE-FREEZE.md

Python environment
Recommended setup from the project root:

python -m pip install --target .deps -r requirements.txt

The scripts that need Matplotlib insert `.deps` into `sys.path`. The
checkpoint bundle does not include `.deps` to avoid shipping local package
caches.

Core run commands

1. Diagnostics:

python scripts/03_run_diagnostics.py

2. Tables:

python scripts/01_make_tables.py

3. Preferred v3 figures:

python scripts/05_generate_matplotlib_figures_v3.py

4. Sensitivity checks:

python scripts/06_run_sensitivity_checks.py

Current preferred outputs

- tables/*.csv and tables/*.tex
- figures/mpl-surface3d-*-v3.pdf
- figures/mpl-surface3d-*-v3.png
- figures/mpl-contour-lines-*-v3.pdf
- figures/mpl-contour-lines-*-v3.png
- captions/caption-mpl-*-v3.md
- diagnostics/stage07-diagnostics-v1.*
- diagnostics/stage09-sensitivity-checks-v1.*
- outputs/stage09-sensitivity-summary-v1.csv

Reproducibility boundary
The outputs are simulation artefacts, not empirical calibration. The
figures illustrate declared structural profiles and Eq. 22 response
regimes in the reaction-boundary volatility closure.

