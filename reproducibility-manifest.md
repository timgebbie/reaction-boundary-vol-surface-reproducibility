# Reproducibility Manifest

Current source map for the released v1.0.0 workflow. The [baseline audit](docs/audits/baseline-v1.0.0.md) explains the relationship between the staged checksum inventory and the tagged Git files.

## Paper and software provenance

The scientific paper is [Angstmann and Gebbie, arXiv:2607.05011v4](https://arxiv.org/abs/2607.05011v4). The [baseline audit](docs/audits/baseline-v1.0.0.md) records integrity checks for the archived software inputs and the historical figure workflow.

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
| W02, v1.2.0 | `python -W error scripts/run_translating_front.py` | [Lattice pole and smooth residual](outputs/v2/translation-spectrum-checks.csv), [pinned and moving box spectra](outputs/v2/translation-spectrum.csv), [weak residual and displaced-forcing control](outputs/v2/aligned-root-checks.csv), [figure](figures/v2/translation-modes.svg) and [accepted audit](docs/audits/translating-front-v1.2.0.md) |
| W03–W04, v1.3.0 | `python -W error scripts/run_liquidity_feedback.py` | [Complex frequency response](outputs/v2/feedback-frequency.csv), [step response](outputs/v2/feedback-time.csv), [shell errors](outputs/v2/feedback-shell.csv) and [audit](docs/audits/liquidity-feedback-v1.3.0.md) |
| W05, v1.4.0 | `python -W error scripts/run_response_balance.py` | [Forcing estimates](outputs/v2/balance-forcing-estimates.csv), [all balance measurements](outputs/v2/balance-window.csv), [figure](figures/v2/response-balance.svg) and [independent-estimator audit](docs/audits/response-balance-v1.4.0.md) |
| W06, v1.5.0 | `python -W error scripts/run_root_variance.py` | [Joint lag table](outputs/v2/root-variance-window.csv), [root checks](outputs/v2/root-variance-roots.csv), [figure](figures/v2/root-variance.svg) and [computational audit](docs/audits/actual-root-variance-v1.5.0.md) |
| W07, v1.6.0 | `python -W error scripts/run_phase_shape.py` | [Full window](outputs/v2/phase-shape-window.csv), [design and spectrum](outputs/v2/phase-shape-designs.csv) and [audit](docs/audits/phase-shape-v1.6.0.md) |

Install `requirements-response.txt`. Run the scientific tests with `python -W error -m unittest discover -s tests -v`. See the [README checkpoint table](README.md#planned-checkpoints-through-v200) for W08–W11 and the [version policy](VERSION_POLICY.md) for acceptance.

The [v1.2.0 mathematical supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.2.0.tex) accompanies the accepted W01/W02 software. From the repository root run `latexmk -pdf -outdir=supplementary-materials supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.2.0.tex`. The two vector figure PDFs in `figures/v2/` render the W01 and W02 SVG outputs for pdfLaTeX. The historical v0.1 source and figures retain their original identities.

The [consolidated v1.3.0 source](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.3.0.tex) and [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.3.0.pdf) include the feedback derivation and the vector figure in `figures/v2/liquidity-feedback.pdf`. Build with the same command, substituting `v1.3.0` in the filename.

The [v1.4.0 consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.4.0.tex) includes the new response measurement. Substitute `v1.4.0` in the build command above.

The [v1.5.0 consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.5.0.tex) adds independent moving-root variance and the finite-rate-floor bound. Use `v1.5.0` in the build command above.

The [v1.6.0 consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.6.0.tex) derives the signed phase–shape covariance. Substitute `v1.6.0` in the build command.

The [v1.7.0 consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.tex) adds the evolving-field equations, measured-zero algorithm, independent speed benchmark and pathwise refinement results. Substitute `v1.7.0` in the build command above. The [field calculation](docs/audits/nonlinear-field-v1.7.0.md) links the complete numerical evidence.

The [v1.8.0 consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.8.0.tex) adds the response surface, conditional increments and matched nonlinear refinement. Build with the preceding command using v1.8.0. The [scale-window audit](docs/audits/scale-window-v1.8.0.md) maps the two executable scripts to the figure and six data tables.
