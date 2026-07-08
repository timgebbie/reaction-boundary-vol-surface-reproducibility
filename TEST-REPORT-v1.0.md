# Reduced-bundle test report

Version tested: v1.0
Date tested: 2026-07-08

## Test object

A clean copy of `ReactionBoundaryVolSurface-Reproducibility-v1.0` was tested independently of the original staged workspace.

## Commands tested

```bash
python -m compileall -q functions scripts
python scripts/run_all.py
```

The wrapper ran the documented active route:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

## Result

The reduced v1.0 bundle completed the active reproducibility route successfully in the test environment.

The diagnostic outputs recorded:

- Stage 7 diagnostics: 42 checks, 0 failures.
- Stage 9 sensitivity checks: 19 checks, 0 failures.

## File-count summary after reduction

| Area | File count |
|---|---:|
| `scripts/` | 5 |
| `functions/` | 4 |
| `config/` | 4 |
| `figures/` | 24 |
| `tables/` | 6 |
| `diagnostics/` | 4 |
| `outputs/` | 1 |
| `captions/` | 6 |
| `supplementary-materials/` | 4 |
| `provenance/` | 54 |

## Note on local environments

The supplied `requirements.txt` is inherited from the staged workspace. Before public release, confirm the final package pins on the user's local machine, especially the Matplotlib version used for final figure rendering.
