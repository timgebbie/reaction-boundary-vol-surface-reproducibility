# Motion of the zero in the nonlinear field

The imbalance field evolves on a fixed Eulerian grid. Its measured zero drives the reassessment memory and determines the placement of the next deposition profile. All 192 trajectories retained a unique descending zero, and each local phase measurement passed its orthogonality check. The six designs reuse the same eight independent inputs. The covariance identity reconstructed the measured variance to relative error below 2.63 × 10⁻¹⁵ across 816 lag rows.

| Refinement compared with the joint reference | Within pathwise tolerance | Largest displacement difference |
|---|---:|---:|
| Baseline | 20/32 | 0.18365 |
| Spatial mesh | 27/32 | 0.06255 |
| Time step | 7/32 | 0.09397 |
| Wall distance | 2/32 | 0.18365 |
| Rate quadrature | 2/32 | 0.18425 |

The prescribed tolerances were 0.05 for the baseline and 0.03 for each single refinement. The time-averaged absolute weak residual fell on all 32 matched paths from baseline to joint reference. Root preservation, weak-residual improvement and accurate variance decomposition coexist with incomplete pathwise convergence. Four independent inputs per exponent support descriptive local slopes only. The three response offsets at v1.4.0 and the four variance offsets at v1.5.0 retain their inconclusive classifications.

The joint reference gave aligned travelling speed 0.04012 against the whole-line value 0.05000. In a subsequent deterministic diagnostic at fixed cell width 0.1, reducing the time step from 0.125 to 0.015625 increased the measured speed to 0.04855. Both profile perturbations also approached their exact speeds at each successive time refinement on both tested meshes. These additional controls measure constant forcing and zero feedback. Stochastic convergence with feedback on the full lag window remains open.

Run the following from the repository root with the response dependencies installed.

~~~bash
OPENBLAS_NUM_THREADS=1 python -W error scripts/run_nonlinear_field.py
OPENBLAS_NUM_THREADS=1 python -W error scripts/check_nonlinear_speed.py
python -W error -m unittest discover -s tests -v
~~~

The [trajectory checks](../../outputs/v2/nonlinear-field-audit.csv) give failure times, causes, full-time maximum displacement errors and weak residuals. The [sampled coordinates](../../outputs/v2/nonlinear-field-trajectories.csv) give the zero, phase and residual every eight time units in the baseline and joint designs. The [lag estimates](../../outputs/v2/nonlinear-field-variance.csv) use every integer observation after burn-in. The [travelling controls](../../outputs/v2/nonlinear-field-speed.csv) and [subsequent time refinement](../../outputs/v2/nonlinear-speed-refinement.csv) include all control speeds and analytic comparators. The [figure](../../figures/v2/nonlinear-field.svg) and [consolidated supplement](../../supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.pdf) give the field equations, interpolation, numerical update, measurement rules and limitations.
