# Independent variance of the moving zero

The two prescribed matched configurations pass the joint response and variance criteria at all 17 operational lag centres from 32 to 320. The new measurement uses 192 independent Gaussian inputs across two exponents and three sampling designs. Within each design the controls share forcing paths. Spatially interpolated zeros give the price increments on the exact aligned translating family. The W05 response estimates use a separate forcing stream. The 192 inputs yield 960 field trajectories across the tested configurations.

| Input exponent | Prescribed rate exponent | Variance-slope envelope | Absolute rate envelope | Rate relative to lag 32 |
|---|---|---|---|---|
| 0.4 | 0.30 | 0.937 to 1.073 | 0.01396 to 0.01664 | 0.933 to 1.079 |
| 0.6 | 0.20 | 0.927 to 1.068 | 0.01593 to 0.01868 | 0.904 to 1.045 |

Turning feedback off or raising the minimum rate to 0.02 gives a slope interval entirely above 1.1 throughout the decade in both input laws. All four primary offset variance comparisons remain inconclusive under the whole-window directional rule. The earlier response test resolved one of those four. The response and variance outcomes are recorded separately in the [joint lag table](../../outputs/v2/root-variance-window.csv).

All three designs kept unique brackets at all 104,857,600 field observations. Sparse global field searches agreed with the cell-interpolated zeros. The largest interpolation error relative to the exact continuum phase was 0.000752 or less. All 510 expected finite-period variances fell inside the corresponding measured intervals. The spectral check shares the specified finite transfer and evaluates its expected variance independently of the path and zero measurements. The analytic low-frequency bound and the distinction between intermediate and asymptotic growth are given in the [consolidated supplement](../../supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.5.0.pdf).

From the repository root with the documented scientific dependencies, run

```bash
OPENBLAS_NUM_THREADS=1 python -W error -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 python -W error scripts/run_root_variance.py
```

Inspect the [individual path variances](../../outputs/v2/root-variance-paths.csv), [root diagnostics](../../outputs/v2/root-variance-roots.csv), [design-specific intervals and spectral checks](../../outputs/v2/root-variance-designs.csv) and [slope figure](../../figures/v2/root-variance.svg). The sampling intervals are jackknife–Student approximations corrected across the predeclared comparisons. This finite-window evidence applies to the aligned auxiliary family with prescribed rates.
