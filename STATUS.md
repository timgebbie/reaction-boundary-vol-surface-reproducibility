# Reproducibility status

> Historical July 2026 preparation record. The public v1.0.0 release and the subsequent preservation checkpoint are documented in the [baseline audit](docs/audits/baseline-v1.0.0.md).

Version: v1.0 / planned public tag `v1.0.0`
Date prepared: 2026-07-08

## Current situation: v1.0

The current situation is a quantitative-finance reproducibility bundle for the supplementary materials associated with [arXiv:2607.05011](https://arxiv.org/abs/2607.05011).

The bundle supports the following current claim: the reaction-boundary variance construction can be simulated and projected into local-volatility-like surfaces whose shape is driven by liquidity, resilience, and structural response profiles. The current release is therefore a reproducible simulation object for the finance argument, not merely a code archive.

It includes:

- the liquidity-only, resilience/response-only, and combined structural surface regimes;
- low-z and high-z response cases;
- boxed surface and black-line contour views of the projected local-volatility surfaces;
- configuration files linking the model parameters to the numerical profiles;
- generated CSV and LaTeX tables;
- diagnostic and sensitivity-check outputs;
- the supplementary-materials TeX and PDF;
- selected provenance files from the staged workspace.

The current boundary is explicit. The bundle does not calibrate to option prices, does not estimate a Dupire surface from data, does not implement a production pricing engine, and does not claim that the simulated surfaces are fitted market surfaces.

## Current active route

The active v1.0 route is:

```bash
python scripts/run_all.py
```

or, equivalently:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

## Execution gates passed

The reduced v1.0 bundle has passed:

1. the author local execution gate on Windows with Python 3.13.9 using a `venv` under an Anaconda installation;
2. the private GitHub clean-clone gate, in which the private repository was cloned into a fresh directory and `python scripts/run_all.py` completed successfully.

The confirmed final local status was:

> Active v1.0 reproducibility route completed successfully.

See `LOCAL-EXECUTION-GATE-v1.0.md` and `TEST-REPORT-v1.0.md` for the recorded gate notes.

## Future situation: finance-first enhancements

Future versions should be described first in finance terms, not software terms. Possible finance extensions include:

- empirical comparison with option-implied local-volatility surfaces;
- calibration of liquidity, resilience, and response profiles from order-flow or limit-order-book data;
- classification of high-z and low-z regimes as possible market-state regimes;
- links to long-memory order-flow, Hurst-type response behaviour, and market impact persistence;
- no-arbitrage projection, smoothing, or regularisation of the structurally generated surface;
- broader sensitivity analysis over response kernels and liquidity/resilience profiles.

Software improvements such as formal packaging, command-line entry points, notebooks, continuous integration, or locked environments may be useful. They are not required for the v1.0 finance reproducibility claim.

## No-content-loss control

The original staged ZIP is preserved externally and remains the complete workspace record. This reduced release preserves the active reproducibility core, retains selected provenance files, and records intentionally excluded workspace material in `REDUCTION-AUDIT.md` and `provenance/full-workspace-file-index.csv`.
