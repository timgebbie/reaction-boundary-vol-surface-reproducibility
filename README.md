# Reaction-boundary volatility surface reproducibility bundle

Version: v1.0

This repository contains the reduced reproducibility bundle for the supplementary simulation materials associated with:

> Chris Angstmann and Tim Gebbie, **"Reaction-boundary variance and adjoint-consistent local-volatility projection"**, arXiv:2607.05011.

The repository is intended to reproduce the simulation figures, tables, diagnostics, and sensitivity checks used in the supplementary materials. It is a simulation-reproducibility bundle, not an empirical calibration package and not a production pricing library.

## Current situation: v1.0

The v1.0 bundle contains:

- the active Python scripts used to regenerate the tables, diagnostics, sensitivity checks, and preferred v3 Matplotlib figures;
- the reusable numerical helper functions;
- the parameter and structural-profile configuration files;
- generated figure, table, diagnostic, and sensitivity outputs;
- the supplementary-materials PDF and LaTeX source;
- provenance notes documenting the staged construction of the bundle.

The active reproducibility route is intentionally small. Earlier development scripts and registers are retained under `provenance/` so that the reduction from the staged workspace is auditable without making the public route ambiguous.

## Future situation: possible enhancements

Future versions could add:

- a formal Python package structure;
- command-line entry points;
- automated unit tests;
- GitHub continuous-integration checks;
- environment locking through `environment.yml`, `uv.lock`, or similar;
- a notebook-based walkthrough;
- additional parameter sweeps;
- empirical calibration examples, if the project is later expanded beyond the current simulation-only boundary.

These are possible enhancements, not requirements for reproducing the current supplementary figures.

## Scientific boundary

The code simulates projected structural volatility surfaces from the reaction-boundary variance construction. It does not estimate a calibrated Dupire local-volatility surface from market option data. The local-volatility comparison in the supplement is qualitative and phenomenological.

## Repository structure

```text
config/                  Parameter ranges and profile definitions
functions/               Reusable numerical helpers
scripts/                 Active v1.0 reproducibility scripts
data/                    Data instructions; no empirical data are required
figures/                 Preferred generated v3 figure outputs
captions/                Standalone caption drafts for generated figures
tables/                  Generated CSV and LaTeX tables
diagnostics/             Diagnostic and sensitivity-check reports
outputs/                 Sensitivity summary outputs
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

Run the scripts in this order:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

Alternatively, run the convenience wrapper:

```bash
python scripts/run_all.py
```

Running the active route regenerates or checks:

- tables in `tables/`;
- preferred v3 figures in `figures/`;
- diagnostics in `diagnostics/`;
- sensitivity summaries in `outputs/`;
- figure captions in `captions/`.

## Expected checks

The original staged workspace recorded:

- Stage 7 diagnostics: 42 checks, 0 failures;
- Stage 9 sensitivity checks: 19 checks, 0 failures.

The reduced v1.0 bundle was constructed so that the active scripts can be run independently of the larger staged workspace.

## Version-control policy

This repository starts at v1.0 because the simulation workflow, generated outputs, and supplementary-materials PDF were already completed in the staged workspace before reduction. Future releases should increment from this public reproducibility baseline.

Recommended tags:

```text
v1.0.0        first public reproducibility release
v1.0.1        documentation-only corrections
v1.1.0        minor reproducibility enhancements without changing the scientific boundary
v2.0.0        major restructure, formal packaging, or expanded scientific scope
```

## DOI and archive plan

The intended archival route is:

1. make a private GitHub repository from this reduced v1.0 bundle;
2. clean-clone test the repository locally;
3. make the repository public;
4. archive the public release and supplementary PDF through ZivaHub/Figshare;
5. use the ZivaHub DOI in the arXiv paper update.

## Citation

Use `CITATION.cff` for repository citation metadata. Once a ZivaHub DOI is assigned, update `CITATION.cff`, this README, and the arXiv code/data availability statement.

## License

A draft MIT license is included for the code. Confirm the final licensing choice with all authors before making the repository public. If the supplementary text and figures are to be licensed separately, state that explicitly before public release.
