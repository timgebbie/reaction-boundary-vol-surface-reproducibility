# Operational scales, price memory and nonlinear refinement

On the aligned translating family the intermediate response compensates persistent signed input over the measured decade. At input exponent 0.4 the reference floor gives a response exponent of 0.2978–0.2987 and a measured price-variance slope envelope of 0.937–1.073. Raising the slowest rate to 0.02 moves its relaxation time into the measured window and gives a slope envelope of 1.285–1.584. The map uses two independent coordinates, operational lag in resilience units and minimum reassessment rate in resilience units. Their product compares the lag to the longest reassessment time. [Scale map](../../figures/v2/scale-window.pdf) · [Surface values](../../outputs/v2/response-surface.csv)

| Calculation | Observation | Scope |
|---|---|---|
| Gaussian price history | Across 64 time triples on each of three grids, maximum absolute partial correlations were 0.00637 and 0.01397 for the two matched rate laws. Raised-floor controls gave 0.19695 and 0.11932. | Population covariances of the aligned Gaussian model. The tested triples have ages and gaps of 32, 80, 160 or 320. |
| Nonlinear travelling speed | The earlier deterministic two-mesh check found 0.04855 at time step 0.015625 and width 0.1, against exact aligned speed 0.05000. | Finite-box motion between times 8 and 32 from the resting profile. |
| Unique zero and displacement | All 160 finer-grid runs retained the root and phase. All 32 paths on the previous joint grid met 0.05 against the new reference. Every other comparison met 0.03. | Same eight inputs, four placements or cutoffs, fixed walls and rate quadrature. The original coarse baseline passed on 20/32. |
| Ensemble variance | The largest rate differences on halving space or time separately at the refined end were 1.38% and 2.03%. All eight nonlinear cases have lags outside the 0.9–1.1 slope band. | Maximum differences over the common 17 centres. Four independent inputs per exponent. A nonlinear diffusion law remains open. |
| Held-out prediction | Earlier price improved pooled squared error in 17/216 comparisons. Changes ranged from a 20.45% deterioration to a 1.21% improvement. | Linear predictions scored by holding out whole paths. Overlapping triples share observations. |

The relative-clock control accelerates only relaxation in the memory equation. It is exactly equivalent in the finite transfer to rescaling both rate endpoints and the coupling. Identifying an independent liquidity clock therefore requires kinetic information beyond this response. The three earlier inconclusive response offsets, four inconclusive variance offsets and the projected-field covariance qualification retain their original interpretation.

From the repository root, install the response dependencies and run

~~~bash
OPENBLAS_NUM_THREADS=1 python -W error scripts/run_scale_window.py
OPENBLAS_NUM_THREADS=1 python -W error scripts/run_matched_refinement.py
python -W error -m unittest discover -s tests -v
~~~

The [equal-spacing](../../outputs/v2/conditional-history.csv) and [unequal-spacing results](../../outputs/v2/unequal-history.csv) contain the population coefficients. The nonlinear tables give [all pathwise comparisons](../../outputs/v2/matched-field-refinement.csv), [phase, shape and signed covariance at every lag](../../outputs/v2/matched-field-variance.csv) and [held-out prediction errors](../../outputs/v2/matched-field-history.csv). The [consolidated supplement](../../supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.8.0.pdf) derives the response exponent, conditional variance and clock equivalence, and records numerical limitations.
