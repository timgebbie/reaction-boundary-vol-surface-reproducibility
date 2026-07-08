# Stage 09 Sensitivity Run Note v1

Artefact status: sensitivity run note

Command:

```bash
python scripts/06_run_sensitivity_checks.py
```

Purpose:

- Check parameter edge cases for the dimensionless simulation ranges.
- Check monotonicity implied by the closure.
- Check grid robustness using coarse, baseline, and fine grids.
- Preserve a machine-readable sensitivity summary.

Expected outputs:

- `diagnostics/stage09-sensitivity-checks-v1.csv`
- `diagnostics/stage09-sensitivity-checks-v1.md`
- `outputs/stage09-sensitivity-summary-v1.csv`

This stage does not create new paper figures.

