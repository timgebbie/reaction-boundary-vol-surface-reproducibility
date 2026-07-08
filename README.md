# Reaction-boundary volatility surface reproducibility bundle

Version: v1.0.0

Supplementary code and materials for:

> Chris Angstmann and Tim Gebbie, **"Reaction-boundary variance and adjoint-consistent local-volatility projection"**, [arXiv:2607.05011](https://arxiv.org/abs/2607.05011).

The supplementary-materials document is included here:

> [ReactionBoundaryVolSurface-Supplement-v0.1.pdf](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.pdf)

This repository is a quantitative-finance reproducibility bundle. Its purpose is to show how the reaction-boundary variance construction generates projected local-volatility surface shapes from liquidity, resilience, and response terms. The code is included so that the figures, tables, diagnostics, and sensitivity checks can be regenerated from the same parameter profiles used in the supplementary materials. This is slightly over-engineered so that it can be easily extended for more sophisticated simulation and calibration work if required. 

## Key figure: combined structural high-z response

![Combined structural high-z surface and contour pair](figures/readme-combined-structural-high-z-pair-v1.png)

**Figure. Combined structural reaction-boundary volatility surface under the high- $z$ response regime.** Panel A gives the boxed surface view of the projected local volatility $\sigma_{\mathrm{loc}}$ over log-moneyness $m=\ln(x/x_0)$ and maturity $T$. Panel B gives the corresponding black-line contour projection of the same surface. This is the key pair in the supplement because it shows the point of the exercise: the model is not fitting an option-implied surface, but generating a structurally interpretable local-volatility shape from reaction-boundary ingredients. The high- $z$ case emphasises the response-sensitive regime in which liquidity, resilience, and the structural response profile combine to produce a persistent skew-like surface over maturity. The contour view is included because it is easier to compare shape, monotonicity, and curvature across regimes without the visual distortion of a 3D perspective plot.

## Current situation: v1.0.0

The current v1.0 bundle supports the claim that a reaction-boundary variance closure can be projected into local-volatility-like surfaces whose shape reflects structural order-book ingredients rather than direct option calibration.

In this current situation:

- reproducible simulations for the liquidity-only, resilience/response-only, and combined structural regimes;
- low-\(z\) and high-\(z\) response cases;
- surface and contour representations of the projected local-volatility surfaces;
- parameter tables linking the mathematical construction to the numerical profiles;
- diagnostics and sensitivity checks used to verify the active simulation route;
- the supplementary-materials PDF and LaTeX source.

This is a **simulation and interpretation bundle** for the supplementary materials. It is not an empirical market-data calibration, not a Dupire inversion from option prices, not a trading strategy, and not a production pricing library.

## Future situation: possible extensions

Future versions could be extended in several directions:

- compare the simulated reaction-boundary surfaces with empirical option-implied local-volatility surfaces;
- calibrate liquidity, resilience, and response profiles from order-flow or limit-order-book data;
- study whether the high-\(z\) and low-\(z\) regimes correspond to identifiable market states;
- connect the reaction-boundary surface shape to long-memory order-flow effects and Hurst-type response behaviour;
- examine how no-arbitrage projection or regularisation would interact with the structural surface;
- extend the sensitivity analysis to richer parameter sweeps and alternative response kernels.

Possible software improvements include: formal packaging, command-line entry points, notebooks, continuous integration, and locked environments, are useful future enhancements. 

## Scientific boundary

The code simulates projected structural volatility surfaces from the reaction-boundary variance construction. It does not estimate a calibrated Dupire local-volatility surface from market option data. The local-volatility comparison in the supplement is qualitative and phenomenological.

## Repository structure

```text
config/                  Parameter ranges and profile definitions
functions/               Reusable numerical helpers
scripts/                 Active v1.0 reproducibility scripts
data/                    Data instructions; no empirical data are required
figures/                 Preferred generated v3 figure outputs and README figure
tables/                  Generated CSV and LaTeX tables
diagnostics/             Diagnostic and sensitivity-check reports
outputs/                 Sensitivity summary outputs
captions/                Standalone caption drafts for generated figures
supplementary-materials/ Supplementary-materials TeX and PDF
provenance/              Stage notes, audits, registers, source freeze, legacy scripts
```

## Installation

From a fresh clone:

```bash
python -m venv .venv
```

Activate the environment.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Then install the requirements:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Reproducing the active outputs

Run the convenience wrapper:

```bash
python scripts/run_all.py
```

or run the scripts explicitly:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

Running the active route regenerates or checks:

- tables in `tables/`;
- preferred v3 figures in `figures/`;
- diagnostics in `diagnostics/`;
- sensitivity summaries in `outputs/`;
- figure captions in `captions/`.

## Execution gates passed

The reduced v1.0 bundle has passed two execution gates:

1. **Author local execution gate:** Windows, Python 3.13.9, `venv` under an Anaconda installation. The author confirmed successful completion of Stage 7 diagnostics, Stage 8 table generation, Matplotlib v3 figure generation, and Stage 9 sensitivity checks.
2. **Private GitHub clean-clone gate:** the private GitHub repository was cloned into a fresh directory, dependencies were installed into a fresh virtual environment, and `python scripts/run_all.py` completed successfully.

The expected final status line is:

```text
Active v1.0 reproducibility route completed successfully.
```

The original staged workspace recorded:

- Stage 7 diagnostics: 42 checks, 0 failures;
- Stage 9 sensitivity checks: 19 checks, 0 failures.

### Note on regenerated PDF figures

Running the figure-generation script may cause Git to mark generated PDF figures as modified even when the run has succeeded. This is expected: Matplotlib PDF output can differ byte-for-byte across local systems because of backend metadata, font embedding, or rendering details. The reproducibility claim is that the scripts regenerate the intended scientific figures, tables, diagnostics, and sensitivity checks; it is not a claim of byte-identical PDF files across all machines.

## Version-control policy

This repository starts at v1.0 because the simulation workflow, generated outputs, and supplementary-materials PDF were already completed in the staged workspace before reduction. Future releases should increment from this public reproducibility baseline.

Recommended tags:

```text
v1.0.0        first public reproducibility release
v1.0.1        documentation-only corrections
v1.1.0        minor reproducibility or interpretation enhancements without changing the scientific boundary
v2.0.0        major restructure, formal packaging, empirical calibration, or expanded scientific scope
```

## DOI, citation, and license

Reserved ZivaHub/Figshare DOI:

https://doi.org/10.25375/uct.32936867

Suggested citation:

Gebbie, Tim; Angstmann, Chris (2026). *Code: Reaction-boundary volatility surface reproducibility code for arXiv:2607.05011*. University of Cape Town. Software. https://doi.org/10.25375/uct.32936867

Concrete placeholders for the public release are below. Replace the bracketed fields once the ZivaHub/Figshare DOI has been issued.

| Item | Value |
|---|---|
| Associated paper | [arXiv:2607.05011](https://arxiv.org/abs/2607.05011) |
| Supplementary PDF | [ReactionBoundaryVolSurface-Supplement-v0.1.pdf](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.pdf) |
| GitHub repository | `https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility` |
| GitHub release | `https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/releases/tag/v1.0.0` |
| ZivaHub/Figshare DOI | [`10.25375/uct.32936867`](https://doi.org/10.25375/uct.32936867) |
| ZivaHub/Figshare landing page | [`Code: Reaction-boundary volatility surface reproducibility code for arXiv:2607.05011`](https://zivahub.uct.ac.za/account/articles/32936867?file=66436139) |
| Code license | MIT License |
| Supplement/text/figures license | `[CC BY 4.0]` |

## License

Code is released under the MIT License.

Supplementary text, captions, figures, tables, and documentation are released under CC BY 4.0 unless otherwise stated.

The associated paper remains governed by its own arXiv/submission terms and is not relicensed by this repository.

See also `CITATION.cff` and `DOI-CITATION-LICENSE.md`.
