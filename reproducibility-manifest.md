# Reproducibility Manifest

Current source map for the released v1.0.0 workflow. The [baseline audit](docs/audits/baseline-v1.0.0.md) explains the relationship between the staged checksum inventory and the tagged Git files.

## Active Source

| Item | Path |
|---|---|
| Historical FMF v1.8 TeX | `provenance/source-freeze/CATG-BSMFromAdjointProjection-FMF-v1.8-source-v0.tex` |
| BibTeX source | `provenance/source-freeze/BSMFromAdjointProjection-FMF-v1.8-references-v0.bib` |
| Source freeze record | `provenance/source-freeze/SOURCE-FREEZE.md` |

The frozen files identify the source used during development. The scientific reference for the extension is [arXiv:2607.05011v4](https://arxiv.org/abs/2607.05011v4).

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


## Extension calculations on the operational clock

| Checkpoint | Source or reproduction command | Evidence and scope |
|---|---|---|
| W00, v1.0.1 | `python scripts/run_all.py` | [Historical replay, staged checksums and tagged source](docs/audits/baseline-v1.0.0.md) |
| W01, v1.1.0 | `python -W error scripts/run_frozen_response.py` | [48 finite-cutoff comparisons](outputs/v2/frozen-variance-checks.csv), [crossover data](outputs/v2/response-crossover.csv), [figure](figures/v2/response-crossover.svg) and [accepted audit](docs/audits/frozen-response-v1.1.0.md) |
| W02, v1.2.0 candidate | `python -W error scripts/run_translating_front.py` | [Lattice pole and smooth residual](outputs/v2/translation-spectrum-checks.csv), [pinned and moving box spectra](outputs/v2/translation-spectrum.csv), [weak residual and displaced-forcing control](outputs/v2/aligned-root-checks.csv), [figure](figures/v2/translation-modes.svg) and [candidate audit](docs/audits/translating-front-v1.2.0.md) |

Install `requirements-response.txt`. Run the scientific tests with `python -W error -m unittest discover -s tests -v`. See the [README checkpoint table](README.md#planned-checkpoints-through-v200) for W03–W11 and the [version policy](VERSION_POLICY.md) for acceptance.
