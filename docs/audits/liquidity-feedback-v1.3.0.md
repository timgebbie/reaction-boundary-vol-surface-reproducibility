# Causal root response and elimination of fast reassessment rates

The v1.3.0 calculation uses the aligned translating front, one operational clock and zero initial memory. The signed input drives the root velocity through a prescribed positive distribution of reassessment rates. Its unit-step velocity is the same causal function as the displacement under a unit impulse. The versioned supplementary material derives the response, normalisation, finite-rate stability, shell moments and remainder bound.

| Comparison | Domain and independent check | Largest discrepancy |
|---|---|---|
| Finite-rate quadrature | 408 frequency rows over three prescribed exponents, two floors, two ceilings, two grid resolutions and 17 frequencies. Compare the complex transfer with adaptive quadrature at identical endpoints. | Relative error 0.00002462 at 96 nodes. On the widest interval the discrepancy from the infinite continuum is 1.48% or less. |
| Time response | Compare implicit Radau integration with pole inversion of the finite resolvent at 25 lags from 0.1 to 10. Halve the maximum step from 0.2 to 0.1. | Absolute ODE–pole difference below 4.02e-9. The change on halving the step is below 6e-12. The maximum finite–continuum difference is below 0.00370. |
| Shell elimination | Compare full and reduced transfer at 25 frequencies for each of three rate cutoffs, preserving physical units and couplings. | Restoring the full shell gives relative error below 4.51e-16. At cutoff 2 the largest relative errors are 0.2990 for omission, 0.00520 for static memory and 0.0002532 for the first derivative. |

Reproduce from the repository root with the scientific dependencies in the README installed.

```bash
python -W error -m unittest discover -s tests -v
python -W error scripts/run_liquidity_feedback.py
```

The three tables in `outputs/v2/feedback-*.csv` contain the frequency, time and shell results, including each frequency used to test the derivative remainder. The corresponding figure is in `figures/v2/liquidity-feedback.svg`. The finite rate floor leaves positive zero-frequency mobility. The experiment prescribes the feedback exponent. Independent measurement of forcing memory and actual-root variance on a common interval remains open.
