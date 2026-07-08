# Reproducibility Manifest

Artefact status: Stage 10 reproducibility manifest

## Active Source

| Item | Path |
|---|---|
| Theory source | `source/CATG-BSMFromAdjointProjection-FMF-v1.8-source-v0.tex` |
| BibTeX source | `source/BSMFromAdjointProjection-FMF-v1.8-references-v0.bib` |
| Source freeze record | `source/SOURCE-FREEZE.md` |

## Active Configuration

| Item | Path |
|---|---|
| Parameter ranges | `config/parameter-ranges-v1.csv` |
| Profile definitions | `config/profile-definitions-v1.json` |
| Requirements | `requirements.txt` |
| Figure requirements note | `config/requirements-figures-v3.txt` |

## Active Scripts

| Stage | Command | Purpose |
|---|---|---|
| 7 | `python scripts/03_run_diagnostics.py` | code diagnostics |
| 8 | `python scripts/01_make_tables.py` | table generation |
| 8 | `python scripts/05_generate_matplotlib_figures_v3.py` | preferred figure generation |
| 9 | `python scripts/06_run_sensitivity_checks.py` | sensitivity checks |

## Preferred Outputs

| Output class | Path pattern |
|---|---|
| Tables | `tables/*.csv`, `tables/*.tex` |
| Surface figures | `figures/mpl-surface3d-*-v3.pdf`, `figures/mpl-surface3d-*-v3.png` |
| Contour figures | `figures/mpl-contour-lines-*-v3.pdf`, `figures/mpl-contour-lines-*-v3.png` |
| Captions | `captions/caption-mpl-*-v3.md` |
| Diagnostics | `diagnostics/stage07-diagnostics-v1.*`, `diagnostics/stage09-sensitivity-checks-v1.*` |
| Sensitivity summary | `outputs/stage09-sensitivity-summary-v1.csv` |

## Status

- Stage 7 diagnostics: 42 checks, 0 failures.
- Stage 9 sensitivity checks: 19 checks, 0 failures.
- Preferred figure family: Matplotlib v3.
- Superseded v1/v2 generated artefacts: pruned from active workspace;
  preserved in earlier checkpoint bundles.

