# Reproducibility status

Version: v1.0
Date prepared: 2026-07-08

## Current situation: v1.0

This repository is the reduced reproducibility bundle for the supplementary simulation materials associated with arXiv:2607.05011.

It includes:

- active Python scripts for diagnostics, table generation, figure generation, and sensitivity checks;
- reusable helper functions;
- configuration files for parameter ranges and structural profiles;
- generated v3 Matplotlib figures in PDF and PNG form;
- generated CSV and LaTeX tables;
- diagnostic and sensitivity-check outputs;
- supplementary-materials TeX and PDF;
- selected provenance files from the staged workspace.

The bundle is intended to reproduce the figures, tables, diagnostics, and sensitivity checks used in the supplementary materials. It is not an empirical calibration package, not a market-data pipeline, and not a production local-volatility implementation.

## Current active route

The active v1.0 route is:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

or:

```bash
python scripts/run_all.py
```

## Future situation: possible enhancements

Future versions could add:

- a formal package layout;
- automated tests;
- continuous integration;
- locked environments;
- notebook walkthroughs;
- additional parameter sweeps;
- empirical calibration examples, if the project is later expanded.

These enhancements are optional. They are not required for the v1.0 reproducibility claim.

## No-content-loss control

The original staged ZIP is preserved externally and remains the complete workspace record. This reduced release preserves the active reproducibility core verbatim, retains selected provenance files, and records intentionally excluded workspace material in `REDUCTION-AUDIT.md` and `provenance/full-workspace-file-index.csv`.
