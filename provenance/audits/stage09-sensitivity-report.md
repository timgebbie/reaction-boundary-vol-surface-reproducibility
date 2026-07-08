# Stage 9 Sensitivity, Robustness, And Edge-Case Checks

Artefact status: Stage 9 completion candidate

Command run:

```bash
python scripts/06_run_sensitivity_checks.py
```

Generated outputs:

- `diagnostics/stage09-sensitivity-checks-v1.csv`
- `diagnostics/stage09-sensitivity-checks-v1.md`
- `outputs/stage09-sensitivity-summary-v1.csv`

Diagnostic result:

- Total checks: 19.
- Failed checks: 0.

Verified:

- Baseline and edge-case surfaces are positive and finite.
- Increasing `A_eff0` increases projected volatility.
- Increasing `L0` suppresses projected volatility through the inverse
  liquidity channel.
- Increasing the high-z resilience marker suppresses high-z volatility.
- The low-z branch remains independent of the high-z marker.
- Coarse and fine grid summaries are stable relative to the baseline grid.

Controlled pruning:

- Superseded v1/v2 generated figure artefacts were removed from the active
  workspace after the Matplotlib v3 figure family was accepted as the
  preferred output.
- Prior v1/v2 artefacts remain available in earlier checkpoint bundles.
- The active manifest now points to tables and v3 figures only.

Recommended next stage:

Stage 10: reproducibility package.

