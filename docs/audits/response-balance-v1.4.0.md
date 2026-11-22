# Independent forcing memory and response slopes

For the two primary prescribed matches, the independently measured input memory and integrated-root-response slopes satisfy the compatibility criterion at each of 17 lag centres from 32 to 320. The table quotes the envelope across these centres. Each centre combines replicate uncertainty for the input exponent with the observed sensitivity of the deterministic response estimate.

| Input exponent | Prescribed rate exponent | Balance envelope | Whole-window outcome |
|---|---|---|---|
| 0.4 | 0.22 | −0.219 to −0.116 | Negative offset |
| 0.4 | 0.30 | −0.071 to 0.028 | Compatible |
| 0.4 | 0.38 | 0.084 to 0.185 | Inconclusive |
| 0.6 | 0.12 | −0.185 to −0.047 | Inconclusive |
| 0.6 | 0.20 | −0.051 to 0.080 | Compatible |
| 0.6 | 0.28 | 0.095 to 0.219 | Inconclusive |

The signed input is a stationary periodic Gaussian process. Its mean spectral exponent is estimated across independent paths on the reciprocal-lag band, with 32 paths per sampling interval and input exponent. The response calculation inverts the causal displacement transfer. Its maximum absolute discrepancy from independent aligned modal inversion is below 3.32 × 10⁻¹⁰. For both prescribed matches, feedback off and the raised rate floor resolve a negative residual. Lower feedback strength gives an inconclusive result. The raised ceiling and the linearised forcing-placement control retain compatibility. The [consolidated physics supplement](../../supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.4.0.pdf) gives the derivation, units, extent of the sampled lag windows and uncertainty construction.

From the repository root with the documented dependencies installed, run

```bash
OPENBLAS_NUM_THREADS=1 python -W error -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 python -W error scripts/run_response_balance.py
```

The [path estimates](../../outputs/v2/balance-forcing-paths.csv) contain 256 slope estimates from 128 independent forcing paths. The [input intervals](../../outputs/v2/balance-forcing-estimates.csv) cover both temporal resolutions and both Fourier grids. The [full response sweep](../../outputs/v2/balance-window.csv) contains all 612 lag rows and the [figure](../../figures/v2/response-balance.svg) shows the primary cases. The 0.1 tolerance and the one-decade interval were fixed before inspecting outcomes. Three offset controls carry a signed balance but overlap a tolerance edge over part of the window. The physical origin of the rate spectrum and the actual-root variance remain open.
