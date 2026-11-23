# Reaction-boundary volatility surface reproducibility bundle

Version: v1.7.0 — Motion of the zero in the nonlinear field

Supplementary code and materials for:

> Chris Angstmann and Tim Gebbie, **“Reaction-boundary variance and adjoint-consistent local-volatility projection,”** [arXiv:2607.05011v4](https://arxiv.org/abs/2607.05011v4).

The mathematical and computational supplement for the current checkpoint is **v1.7.0**. It includes the finite-cutoff variance, the translating-front spectrum, the algorithm for the moving zero and the causal response induced by fast and slow liquidity reassessment. It now also derives the forcing and response estimators and reports the matched and offset tests on a common lag window. The same window now carries an independent variance measurement of the moving zero. The phase–shape calculation traces the signed covariance from common forcing to total variance. The nonlinear calculation follows the descending zero on an Eulerian grid and measures its displacement error against joint refinement.

> [Supplement v1.7.0 (PDF)](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.pdf) · [Consolidated LaTeX source](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.tex)

The historical supplement accompanies the [published v1.0.0 software release](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/releases/tag/v1.0.0):

> [ReactionBoundaryVolSurface-Supplement-v0.1.pdf](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.pdf)

The [v1.2.0 source](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/b65bf066e28466faa6781548a1f21e1b994e780c) and its [computational audit](docs/audits/translating-front-v1.2.0.md) give the translating-front calculation. The [baseline audit](docs/audits/baseline-v1.0.0.md) and [finite-cutoff comparison](docs/audits/frozen-response-v1.1.0.md) document the two earlier checkpoints.

This repository is a quantitative-finance reproducibility bundle. Its purpose is to show how the reaction-boundary variance construction generates projected local-volatility surface shapes from liquidity, resilience, and response terms. The code is included so that the figures, tables, diagnostics, and sensitivity checks can be regenerated from the same parameter profiles used in the supplementary materials. This is slightly over-engineered so that it can be easily extended for more sophisticated simulation and calibration work if required. 

## Key figure: combined structural high-z response

![Combined structural high-z surface and contour pair](figures/readme-combined-structural-high-z-pair-v1.png)

**Figure. Combined structural reaction-boundary volatility surface under the high-<i>z</i> response regime.** Panel A gives the boxed surface view of the projected local volatility $`\sigma_{\mathrm{loc}}`$ over log-moneyness $`m=\ln(x/x_0)`$ and maturity $`T`$. Panel B gives the corresponding black-line contour projection of the same surface. This is the key pair in the supplement because it shows the point of the exercise: the model is not fitting an option-implied surface, but generating a structurally interpretable local-volatility shape from reaction-boundary ingredients. The high-<i>z</i> case emphasises the response-sensitive regime in which liquidity, resilience, and the structural response profile combine to produce a persistent skew-like surface over maturity. The contour view is included because it is easier to compare shape, monotonicity, and curvature across regimes without the visual distortion of a 3D perspective plot.

The combined high-<i>z</i> figure uses the profile definitions and the high-<i>z</i> asymptote in the v1.0.0 structural-surface calculation. The sensitivity summary reports the numerical characteristics of all six surfaces. [Profile definitions](config/profile-definitions-v1.json) · [Sensitivity summary](outputs/stage09-sensitivity-summary-v1.csv) · [Figure register](figure-table-provenance-register.csv)

## The physics

### From the structural surfaces to the frozen variance (v1.0.0–v1.1.0)

The first calculation asks how liquidity slope, forcing intensity and resilience shape the projected surface. For the stationary frozen boundary let $`V_\Delta`$ be the variance of a log-price increment over an operational lag $`\Delta`$. The variance per unit operational time has the separated-scale form

```math
\frac{V_\Delta}{\Delta}\simeq
\frac{\mathcal A_{\mathrm{eff}}}{\mathcal L^2}\cdot\Delta^{-\gamma}
\mathcal F_\gamma(\nu\Delta).
```

The dimensionless lag $`z=\nu\Delta`$ compares the observation interval $`\Delta`$ with the liquidity replenishment time $`\nu^{-1}`$. On the ultraviolet (short-time) side of this crossover, $`\tau_0\ll\Delta\ll\nu^{-1}`$. The boundary responds to persistent signed order flow before liquidity has time to replenish, giving $`V_\Delta\propto\Delta^{1-\gamma}`$. Resilience therefore drops out of the leading variance law, and the microscopic cutoff $`\tau_0`$ sets the lower limit of this scaling window. On the infrared (long-time) side, $`z\gg1`$, replenishment limits the displacement of the frozen boundary. Its increment variance approaches twice the stationary level variance, so the variance per unit operational time falls as $`1/\Delta`$. This distinction motivates the proposed renormalisation-group calculation for the translating boundary: when fast liquidity-reassessment modes are integrated out, which memory terms must be retained to reproduce the root response at lower frequencies?

A state-conditioned local-pricing coefficient requires additional information even when the stationary variance is known. The accepted W01 calculation checks the finite-cutoff result in both time and frequency. [Variance comparison and crossover](docs/audits/frozen-response-v1.1.0.md)

### From a frozen zero to a translating root (v1.2.0)

When the deposition profile follows the observed zero, the auxiliary field admits translated profiles $`\Phi_{\ast}(x-q)`$. Their tangent $`\psi=-\Phi_{\ast}'`$ is a neutral mode. The transverse spectrum lies at or below $`-\nu`$. For initial data on this family and forcing aligned with $`\psi`$, the observed root is exactly $`y=q`$. A shape perturbation with zero spectral phase can still move the observed zero. This distinction determines which coordinate must be measured in later variance tests. [Profile, spectrum and measured root](docs/audits/translating-front-v1.2.0.md)

### What would carry the result to v2.0.0?

The proposed extension asks whether delayed liquidity reassessment can compensate persistent order flow over a common interval of operational lags. Write $`H(s)`$ for the transfer from signed input to root **velocity**. The impulse response of the **root displacement** has transform $`\widehat G_{\mathrm{eff}}(s)=H(s)/s`$. The response slope and the balance to be tested are

```math
\beta_{\mathrm{eff}}(\Delta)=-\frac{d\log |G_{\mathrm{eff}}(\Delta)|}{d\log\Delta}
```

```math
B(\Delta)=2\beta_{\mathrm{eff}}(\Delta)+\gamma-1.
```

v1.3.0 measures the causal transfer and the error from eliminating fast reassessment rates. v1.4.0 independently estimates the input exponent $`\gamma`$. v1.5.0 measures the aligned actual-root increment variance $`V_y(\Delta)`$, and a positive, approximately constant $`V_y(\Delta)/\Delta`$ on the same prespecified interval. Off-match rates, a finite slow-rate floor and non-aligned forcing test the limits of the construction. If these observations disagree, that disagreement belongs in the v2.0.0 result. The feedback spectrum is prescribed in this construction. v1.6.0 measures the transverse contribution in a specified linearised field. The v1.7.0 calculation observes the nonlinear zero directly. Its variance law and the origin of the feedback spectrum remain open.

## Current situation: v1.7.0 accepted

The accepted v1.1.0 calculation returns the operational increment variance of the stationary frozen boundary at positive microscopic cutoff. Its independent time-domain evaluation gives a direct check on the spectral calculation in Appendix A of the paper. The original structural surfaces remain the published baseline.

The v1.2.0 calculation asks what changes when the deposition profile follows the observed zero. In the auxiliary field the translated profile has a neutral tangent, while the shape sector retains the resilience gap. With forcing proportional to that tangent, the zero follows the translation coordinate exactly. An orthogonal shape perturbation can shift the zero even when its spectral phase vanishes. [Translating-front calculation and tests](docs/audits/translating-front-v1.2.0.md)

### From reassessment rates to effective memory (v1.3.0)

The calculation gives the causal response of the aligned root to a distribution of liquidity reassessment rates. The finite-rate velocity response agrees with independent pole inversion to within 4.02 × 10⁻⁹ on the tested lags. Eliminating fast rates induces a memory term whose first-derivative approximation can be checked directly on the retained frequency band. This calculation leaves the forcing exponent to the independent v1.4.0 measurement and the root-variance slope to v1.5.0. [Calculation and reproduction commands](docs/audits/liquidity-feedback-v1.3.0.md) · [Consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.3.0.pdf)

### Independent response balance (v1.4.0)

The input memory is measured from forcing paths and the response exponent from a separate displacement experiment. Both prescribed matches satisfy the fixed tolerance at all 17 sampled lags from 32 to 320. Of four primary offset controls, one clears the separation threshold over the full window. The other three remain inconclusive under that rule. The independent variance measurement on this window follows below. [All cases and reproduction commands](docs/audits/response-balance-v1.4.0.md) · [Consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.4.0.pdf)

### Variance of the moving zero (v1.5.0)

The two matched constructions also pass the independent root-variance test on the 17 operational lags used to measure response. On newly generated paths the measured variance-slope envelopes are 0.937–1.073 and 0.927–1.068. The variance per unit lag stays positive and within the predeclared relative-rate tolerance. Removing feedback or raising the slow-rate floor gives superlinear variance across the tested decade. The primary offset variance comparisons remain inconclusive under the whole-window separation rule. [Actual-root calculation and evidence](docs/audits/actual-root-variance-v1.5.0.md) · [Consolidated supplement](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.5.0.pdf)

### How does shape enter the observed variance? (v1.6.0)

The observed displacement is the sum of the phase and a shape contribution. Their increment covariance changes sign when forcing placement is reversed. In the linearised moving field its magnitude contributes less than 0.059% of total variance over the tested decade. Two additive benchmarks meet both the shape and total scaling criteria. No projected-field case does so. The fresh aligned control at input exponent 0.6 also misses the lower total-slope threshold. [Signed covariance and controls](docs/audits/phase-shape-v1.6.0.md) · [All lag outcomes](outputs/v2/phase-shape-window.csv)

### Motion of the zero in the nonlinear field (v1.7.0)

With feedback driven by the measured zero, all 192 finite-grid trajectories retained a unique descending crossing. Only 20 of 32 baseline paths met the displacement tolerance against joint refinement. In the deterministic aligned control, reducing the time step eightfold at fixed cell width moved the speed from 0.04012 to 0.04855, against the exact 0.05000. Nonlinear variance slopes remain exploratory. [Field evolution and convergence](docs/audits/nonlinear-field-v1.7.0.md) · [Consolidated supplement v1.7.0 (PDF)](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.tex)

### Historical structural-surface baseline: v1.0.0

The current v1.0 bundle supports the claim that a reaction-boundary variance closure can be projected into local-volatility-like surfaces whose shape reflects structural order-book ingredients rather than direct option calibration.

In this current situation:

- reproducible simulations for the liquidity-only, resilience/response-only, and combined structural regimes;
- low-<i>z</i> and high-<i>z</i> response cases;
- surface and contour representations of the projected local-volatility surfaces;
- parameter tables linking the mathematical construction to the numerical profiles;
- diagnostics and sensitivity checks used to verify the active simulation route;
- the supplementary-materials PDF and LaTeX source.

This is a **simulation and interpretation bundle** for the supplementary materials. It is not an empirical market-data calibration, not a Dupire inversion from option prices, not a trading strategy, and not a production pricing library.

### Evidence inventory

| Identifier | Claim, experiment, or feature | Evidence artifact | Verification status |
|---|---|---|---|
| Structural surfaces | Three structural profiles in the low- and high-<i>z</i> regimes | [Diagnostics](diagnostics/stage07-diagnostics-v1.csv) · [Sensitivity checks](diagnostics/stage09-sensitivity-checks-v1.csv) | 42 diagnostics and 19 sensitivity checks passed in the baseline replay. |
| Frozen increment variance | Independent spectral and time-domain evaluations at finite cutoff | [48 comparisons](outputs/v2/frozen-variance-checks.csv) · [Audit](docs/audits/frozen-response-v1.1.0.md) | Maximum observed relative discrepancy $`3.84\times10^{-11}`$ on the stated grid. |
| SV2-F01 | Cutoff dependence and the full zero-cutoff crossover | [Figure](figures/v2/response-crossover.svg) · [Figure data](outputs/v2/response-crossover.csv) | Reproduced on the recorded Linux environment. |
| Translating front (W02) | Pinned and moving spectra, translated root, weak field residual across the zero | [Spectra](outputs/v2/translation-spectrum.csv) · [Root and residual](outputs/v2/aligned-root-checks.csv) · [Mode figure](figures/v2/translation-modes.svg) | Eight W02 tests passed. The field and the placement of forcing are specified by the auxiliary construction. |
| Causal reassessment and fast-rate elimination | Finite transfer, time response and effective memory on the retained band | [Evidence and commands](docs/audits/liquidity-feedback-v1.3.0.md) · [Response and error figure](figures/v2/liquidity-feedback.svg) | 408 frequency comparisons, 25 time points and 75 shell comparisons. |
| Response balance | Independent forcing and response exponents | [612 lag measurements](outputs/v2/balance-window.csv) · [Figure](figures/v2/response-balance.svg) | Two prescribed matches satisfy the tolerance. One of four primary offsets separates across the full grid. |
| Aligned moving zero | Independent increment variance on the response window | [All lag comparisons](outputs/v2/root-variance-window.csv) · [Slope figure](figures/v2/root-variance.svg) | Two joint matches, with superlinear variance under feedback-off and raised-floor controls. |
| Phase and shape | Independent and jointly forced components | [Spectral and path comparison](outputs/v2/phase-shape-designs.csv) · [Figure](figures/v2/phase-shape.svg) | Signed covariance checked for all 612 design and lag entries. |
| Nonlinear field | Measured zero and local phase | [Resolution table](outputs/v2/nonlinear-field-audit.csv) · [Speed refinement](outputs/v2/nonlinear-speed-refinement.csv) | 192 unique roots. Twenty of 32 baseline paths meet the displacement tolerance. |

### Prior implementations and methodological antecedents

| Source | Exact version / commit | Reused or adapted element | Differences and checks |
|---|---|---|---|
| [Reaction-boundary paper](https://arxiv.org/abs/2607.05011v4) | arXiv:2607.05011v4 | Eqs. (21) and (47), with Gaussian tangent-state conditioning in Appendix D | Separate implementations compare the finite-cutoff coefficient with the zero-cutoff crossover. |
| [Translating-front implementation](functions/translating_front.py) | W02 at `b65bf06` | Auxiliary field and aligned forcing used by the numerical extension | [Spectrum and root checks](docs/audits/translating-front-v1.2.0.md) |

## Future situation: possible extensions

### Planned checkpoints through v2.0.0

| Checkpoint | Scientific question or evidence |
|---|---|
| v1.0.1 and v1.1.0 (accepted) | Replay the released surfaces and verify the frozen, finite-cutoff boundary variance independently in frequency and time. |
| v1.2.0 (accepted) | Resolve the translation mode and stable shape spectrum, and test the exact aligned moving root. |
| v1.3.0 (accepted) | Introduce prescribed liquidity feedback and quantify the response error from eliminating fast rates. |
| v1.4.0 (accepted) | Measure the integrated root propagator and input memory independently to test the Bouchaud balance. |
| v1.5.0 (accepted) | Measure actual-root variance on the same prespecified operational-time window, including off-match and finite-rate-floor controls. |
| v1.6.0 (accepted) | Measure signed phase–shape covariance under independent and common driving. |
| v1.7.0 (accepted) | Test root preservation and convergence for the nonlinear, non-aligned field. |
| v1.8.0 and v1.9.x | Compare mechanisms and controls, then audit claims and reproduce the expanded supplement from a clean checkout. |
| v2.0.0 | Assemble the verified results and their limits in a citable code and supplement milestone, subject to approval. |

### Beyond v2.0.0: an effective field theory from bid and ask liquidity

Can the separately evolving bid and ask densities, with depletion and delayed, displaced replenishment, supply the kinetics for an effective theory of the moving boundary? A first comparison would extract the zero of the simulated signed imbalance wherever it is unique and simple, and measure its displacement alongside the threshold-quote log midpoint and quoted spread on the same operational clock. The difference between the root and the midpoint would itself be an observable. Matched perturbations of replenishment placement or delay could then test whether a single boundary coordinate predicts the measured response, or whether spread or pending replenishment must remain explicit slow variables. A further question is whether the measured relaxation spectrum accounts for the feedback law currently prescribed in the auxiliary model. [Two-field spread paper](https://arxiv.org/abs/2610.07985) · [Simulated density paths, quotes and controls](https://github.com/timgebbie/two-field-spread-reproducibility)

### Other possible extensions

- **Can observed order flow explain the imposed liquidity, resilience and forcing profiles?** The six structural surfaces use declared synthetic profiles. The [sensitivity summary](outputs/stage09-sensitivity-summary-v1.csv) shows how the surface changes when these inputs vary. Estimate the profiles from book and order-flow data. Test their predictive content on held-out observations.
- **Are the low- and high-<i>z</i> regimes observable in market data?** W01 resolves the frozen-response crossover in $`z=\nu\Delta`$ under controlled parameters. Estimate resilience and the observation scale on a common operational clock and test whether the two regimes can be distinguished statistically.
- **How do persistent order flow and replenishment affect the moving root?** W01 establishes the frozen variance. W02 separates translation and shape, and tests the aligned root. W03–W04 establish the response of the aligned construction to prescribed feedback. W05 tests the input and response slopes independently. W06 measures the moving-zero variance. W07–W09 address the covariance of phase and shape and the placement of forcing. A kinetic derivation from bid and ask liquidity remains the separate question above.
- **Can the structural surface be compared quantitatively with option-implied local volatility?** The existing plots illustrate surface shape. The stationary high-<i>z</i> coefficient has an unconditional interpretation. Specify the pricing measure and state conditioning, map state and maturity coordinates, and quantify the effect of no-arbitrage projection or regularisation before making a calibration claim.
- **How sensitive are the conclusions to the response law?** The historical workflow already includes 19 sensitivity checks. W09 addresses alternative rate spectra, finite rate floors, and forcing alignment. Broader empirical kernel and profile comparisons remain open.

Packaging, command-line entry points, notebooks, continuous integration and a fully locked environment remain possible software improvements. The scientific checkpoints above use the documented script entry points and recorded replay environment.

## Scientific boundary

The code simulates projected structural volatility surfaces from the reaction-boundary variance construction. It does not estimate a calibrated Dupire local-volatility surface from market option data. The local-volatility comparison in the supplement is qualitative and phenomenological.

The high-<i>z</i> figures illustrate the unconditional stationary variance response. Using that response as a state-conditioned pricing coefficient requires separate justification.

## Repository structure

```text
VERSION_POLICY.md        Checkpoint acceptance, tags and major releases
tests/                   Claim-bearing numerical checks for the extension
docs/audits/             Baseline replay and checkpoint evidence
outputs/v2/              Supplement extension data, including pre-v2.0.0 work
figures/v2/              Supplement extension figures
config/                  Parameter ranges and profile definitions
functions/               Reusable numerical helpers
scripts/                 Active v1.0 reproducibility scripts
data/                    Data instructions; no empirical data are required
figures/                 Preferred generated v3 figure outputs and README figure
tables/                  Generated CSV and LaTeX tables
diagnostics/             Diagnostic and sensitivity-check reports
outputs/                 Sensitivity summary outputs
captions/                Standalone caption drafts for generated figures
supplementary-materials/ Supplementary-materials TeX and PDF
provenance/              Stage notes, audits, registers, source freeze, legacy scripts
```

## Installation

The historical Windows author run used Python 3.13.9. The November replay and v1.1.0–v1.7.0 calculations used Linux, Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.11.0. The requirements files specify the supported installation constraints. The exact versions above identify the recorded run.

### Obtain the accepted scientific source

```bash
git clone https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility.git
cd reaction-boundary-vol-surface-reproducibility
git checkout f83f8690c45505b5f73cbc9a2a707dc88d0faf32
```

For the original published surfaces alone, use the same repository at tag `v1.0.0`.

### Install dependencies

From a fresh clone:

```bash
python -m venv .venv
```

Activate the environment.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Windows CMD:

```cmd
.venv\Scripts\activate.bat
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

For the finite-cutoff comparison and the extension tests, install the additional response requirements in the same environment:

```bash
python -m pip install -r requirements-response.txt
```

## Reproducing the accepted outputs

### Inputs and configuration

| Input | Source / location | Version or fingerprint | Access conditions |
|---|---|---|---|
| Structural profiles and parameter ranges | [Profiles](config/profile-definitions-v1.json) · [Ranges](config/parameter-ranges-v1.csv) | Released v1.0.0 Git tree | Public synthetic inputs. |
| Frozen-variance quadrature and parameter grid | [Calculation](functions/frozen_response.py) · [Experiment](scripts/run_frozen_response.py) | v1.1.0 source in the version table | Deterministic calculation. The grid and numerical tolerances are given in the audit. |

### Reproducing the active outputs

Run the convenience wrapper:

```bash
python scripts/run_all.py
```

or run the scripts explicitly:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

Running the active route regenerates or checks:

- tables in `tables/`;
- preferred v3 figures in `figures/`;
- diagnostics in `diagnostics/`;
- sensitivity summaries in `outputs/`;
- figure captions in `captions/`.

### Frozen variance, translating front, response and moving-zero variance

```bash
python -W error -m unittest discover -s tests -v
python -W error scripts/run_frozen_response.py
python -W error scripts/run_translating_front.py
python -W error scripts/run_liquidity_feedback.py
python -W error scripts/run_response_balance.py
python -W error scripts/run_root_variance.py
python -W error scripts/run_phase_shape.py
python -W error scripts/run_nonlinear_field.py
python -W error scripts/check_nonlinear_speed.py
```

| Output | Location | Format | Acceptance criterion |
|---|---|---|---|
| Six structural surfaces and sensitivity summary | [Figures](figures) · [Summary](outputs/stage09-sensitivity-summary-v1.csv) | PNG, PDF, CSV | Baseline diagnostics and sensitivity checks, with rendering and rounding differences recorded. |
| Finite-cutoff coefficient | [Comparisons](outputs/v2/frozen-variance-checks.csv) | CSV | Relative discrepancy and refinement changes below $`10^{-6}`$ for each of 48 cases. |
| Crossover and its running slope | [Figure](figures/v2/response-crossover.svg) · [Data](outputs/v2/response-crossover.csv) | SVG, CSV | Low- and high-<i>z</i> checks against Eq. (22), using the tolerances in the [tests](tests/test_frozen_response.py). |
| Translating front | [Field and root tests](docs/audits/translating-front-v1.2.0.md) · [Root residuals](outputs/v2/aligned-root-checks.csv) | CSV, SVG | On the finest grid the aligned weak residual was $`3.16\times10^{-5}`$ and the displaced-forcing control gave 0.218. |
| Causal feedback | [Frequency](outputs/v2/feedback-frequency.csv) · [Time](outputs/v2/feedback-time.csv) · [Shell](outputs/v2/feedback-shell.csv) | CSV, SVG | At cutoff 2 the first-derivative memory has maximum relative transfer error 0.0002532 on the retained band. |
| Matched and offset response | [Window estimates](outputs/v2/balance-window.csv) | CSV | Two prescribed matches pass the response criterion. |
| Aligned moving zero | [Per-design variances](outputs/v2/root-variance-designs.csv) · [Joint lag table](outputs/v2/root-variance-window.csv) | CSV, SVG | Both matched root-variance intervals pass on the accepted common window. |
| Phase and shape | [Per-design comparisons](outputs/v2/phase-shape-designs.csv) · [Whole-window outcomes](outputs/v2/phase-shape-window.csv) | CSV, SVG | All 612 expected cross terms lie inside the corresponding design intervals. Two additive configurations meet both scaling criteria. |
| Nonlinear moving zero | [Fields, speeds and lag estimates](docs/audits/nonlinear-field-v1.7.0.md) | CSV, SVG | Five output CSVs and the figure reproduced byte for byte from clean source. |

### Repeating the analysis in an already-used tree

The same commands regenerate the derived files in place. Use the reference checkout above to compare against the accepted outputs. For an existing checkout, inspect local edits before rerunning the figure and table scripts.

## Verification status

| Check category | Command or evidence record | Result |
|---|---|---|
| Environment and dependencies | [Baseline replay](docs/audits/baseline-v1.0.0.md) · [Finite-cutoff run](docs/audits/frozen-response-v1.1.0.md) | Recorded on 22 November 2026. |
| Unit and scientific regression | v1.7.0 scientific suite | All 29 tests passed with warnings treated as errors, including checks of root interpolation, fractional lag increments and spectral normalisation. |
| Source integrity | [Archived file and checksum reconciliation](docs/audits/baseline-v1.0.0.md) | Frozen TeX and BibTeX verified. The staged inventory differs from the Git tree. |
| Clean source reproduction | Independent checkout of the v1.5.0 source | The response and root-variance CSVs and SVGs reproduced byte-for-byte with single-threaded BLAS. Changing BLAS threading moved two earlier time-response columns by at most 1.12 × 10⁻¹⁶. All 61 historical checks passed. |
| Cross-platform evidence | [Original author and clean-clone report](TEST-REPORT-v1.0.md) | Windows evidence applies to the historical route. The extension was verified on Linux. |

### Execution gates passed

The reduced v1.0 bundle has passed two execution gates:

1. **Author local execution gate:** Windows, Python 3.13.9, `venv` under an Anaconda installation. The author confirmed successful completion of Stage 7 diagnostics, Stage 8 table generation, Matplotlib v3 figure generation, and Stage 9 sensitivity checks.
2. **Private GitHub clean-clone gate:** the private GitHub repository was cloned into a fresh directory, dependencies were installed into a fresh virtual environment, and `python scripts/run_all.py` completed successfully.

The expected final status line is:

```text
Active v1.0 reproducibility route completed successfully.
```

The original staged workspace recorded:

- Stage 7 diagnostics: 42 checks, 0 failures;
- Stage 9 sensitivity checks: 19 checks, 0 failures.

### Note on regenerated PDF figures

Running the figure-generation script may cause Git to mark generated PDF figures as modified even when the run has succeeded. This is expected: Matplotlib PDF output can differ byte-for-byte across local systems because of backend metadata, font embedding, or rendering details. The reproducibility claim is that the scripts regenerate the intended scientific figures, tables, diagnostics, and sensitivity checks; it is not a claim of byte-identical PDF files across all machines.

## Version-control and release policy

Development proceeds on `main`. Accepted checkpoints can receive immutable version tags. GitHub releases require a separately approved major scientific or reproducibility milestone. See the [version policy](VERSION_POLICY.md).

| Version or stage | Verified change | Evidence / status | Release reference |
|---|---|---|---|
| v1.0.0 | Original structural surfaces, diagnostics and v0.1 supplement | Published reproducibility baseline | [Tag and GitHub release](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/releases/tag/v1.0.0) · [`ee37d99`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/ee37d994b72b64395560de1126531bb259c1f794) |
| v1.0.1 | Historical replay, source map and checksum reconciliation | Accepted preservation checkpoint · [audit](docs/audits/baseline-v1.0.0.md) | [`48aad39`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/48aad392734a228455df743d1c9a6453c4fecee8) · commit on GitHub |
| v1.1.0 | Exact finite-cutoff cumulant, independent time-domain check and zero-cutoff crossover | Accepted scientific checkpoint · [audit](docs/audits/frozen-response-v1.1.0.md) | [`33332cf`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/33332cfd7ce707079e6bac288b739aa28d6837bd) · commit on GitHub |
| v1.2.0 | Translating profile, pinned control, stable shape band and measured root | [Computational audit](docs/audits/translating-front-v1.2.0.md) · accepted scientific checkpoint | [`b65bf06`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/b65bf066e28466faa6781548a1f21e1b994e780c) |
| v1.3.0 | Causal root response and fast-rate memory | [Finite-rate and shell audit](docs/audits/liquidity-feedback-v1.3.0.md) · accepted scientific checkpoint | [`fcc1f40`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/fcc1f40cb7b401c2408f13a324ed06e0e97261ef) |
| v1.4.0 | Independent response balance on a fixed operational window | [Measurements and controls](docs/audits/response-balance-v1.4.0.md) · accepted scientific checkpoint | [`1052471`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/10524718cda8aa53bc605a3f8bce49f79f99c03f) |
| v1.5.0 | Independent moving-zero variance | [Variance and spectral checks](docs/audits/actual-root-variance-v1.5.0.md) · accepted scientific checkpoint | [`3ea466e`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/3ea466ecb17673b7d695efde696bab26a591479a) |
| v1.6.0 | Signed phase–shape covariance | [Decomposition and numerical checks](docs/audits/phase-shape-v1.6.0.md) · accepted scientific checkpoint | [`018d011`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/018d01162f09d2986c937c286297ec966d437bda) |
| v1.7.0 | Nonlinear field, measured root and travelling speed | [Convergence and controls](docs/audits/nonlinear-field-v1.7.0.md) · accepted scientific checkpoint | [`f83f869`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/f83f8690c45505b5f73cbc9a2a707dc88d0faf32) |

The public tag and hosted release at the 22 November audit were both v1.0.0. The v0.1 supplement, the paper revision and the dated inputs and figure families each retain their own identifiers. The `v2/` output directories identify work towards the expanded supplement.

## Release archive and provenance

| Record | Reference | Scope |
|---|---|---|
| Archived software | [ZivaHub deposit](https://doi.org/10.25375/uct.32936867), `ReactionBoundaryVolSurface-Reproducibility-v1.0-stage5.zip` | Staged v1 software deposit. |
| Released Git source | [v1.0.0](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/releases/tag/v1.0.0) · [Release notes](RELEASE-NOTES-v1.0.md) | Reduced public repository and historical supplement. |
| Inventory | [Staged checksums](FILE-MANIFEST-SHA256.csv) · [Current source map](reproducibility-manifest.md) | Of 132 staged entries, 98 match tagged Git bytes, six match with CRLF conversion, 27 differ and one file is absent. |
| Frozen-response extension | [v1.1.0 source](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/tree/33332cfd7ce707079e6bac288b739aa28d6837bd) | Accepted mainline computation. The v1 deposit describes the staged historical archive. |
| Translating-front extension | [`b65bf06`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/b65bf066e28466faa6781548a1f21e1b994e780c) | Accepted W02 source, including the integrated clean replay. |
| Causal liquidity reassessment | [`fcc1f40`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/fcc1f40cb7b401c2408f13a324ed06e0e97261ef) | Accepted transfer, time-response and shell-reduction source and consolidated supplement. |
| Independent response balance | [`1052471`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/10524718cda8aa53bc605a3f8bce49f79f99c03f) | Input path estimates, collective response, all controls and consolidated supplement. |
| Moving-zero variance | [`3ea466e`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/3ea466ecb17673b7d695efde696bab26a591479a) | Accepted common-window root variance, controls and consolidated supplement. |
| Signed phase–shape covariance | [`018d011`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/018d01162f09d2986c937c286297ec966d437bda) | Common-input and independent benchmarks, projected field and consolidated supplement. |
| Nonlinear moving boundary | [`f83f869`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/f83f8690c45505b5f73cbc9a2a707dc88d0faf32) | Accepted unique-root evidence, matched pathwise resolution, speed benchmark and consolidated supplement. |

## DOI, citation, and license

Registered ZivaHub/Figshare DOI:

https://doi.org/10.25375/uct.32936867

Suggested citation:

Gebbie, Tim and Angstmann, Chris (2026). *Reaction-boundary volatility surface reproducibility code for arXiv:2607.05011*. University of Cape Town. Software. https://doi.org/10.25375/uct.32936867

| Item | Value |
|---|---|
| Associated paper | [arXiv:2607.05011v4](https://arxiv.org/abs/2607.05011v4) |
| Historical supplement v0.1 | [ReactionBoundaryVolSurface-Supplement-v0.1.pdf](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.pdf) |
| Translating-front supplement v1.2.0 | [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.2.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.2.0.tex) |
| Causal reassessment supplement v1.3.0 | [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.3.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.3.0.tex) |
| Response-balance supplement v1.4.0 | [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.4.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.4.0.tex) |
| Moving-zero supplement v1.5.0 | [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.5.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.5.0.tex) |
| Covariance supplement v1.6.0 | [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.6.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.6.0.tex) |
| Current supplement v1.7.0 | [PDF](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.pdf) · [TeX](supplementary-materials/ReactionBoundaryVolSurface-Supplement-v1.7.0.tex) |
| GitHub repository | `https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility` |
| GitHub release | `https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/releases/tag/v1.0.0` |
| ZivaHub/Figshare DOI | [`10.25375/uct.32936867`](https://doi.org/10.25375/uct.32936867) |
| ZivaHub/Figshare landing page | [`Code: Reaction-boundary volatility surface reproducibility code for arXiv:2607.05011`](https://zivahub.uct.ac.za/articles/software/Reaction-boundary_volatility_surface_reproducibility_code_for_arXiv_2607_05011/32936867) |
| Code license | MIT License |
| Supplement/text/figures license | `[CC BY 4.0]` |

## License

Code is released under the MIT License.

Supplementary text, captions, figures, tables, and documentation are released under CC BY 4.0 unless otherwise stated.

The associated paper retains the licence recorded on arXiv.

See also `CITATION.cff` and `DOI-CITATION-LICENSE.md`.

## Current decision and next gate

The v1.1.0 checkpoint verifies the stationary frozen tangent variance on the operational clock. Independent spectral and time-domain calculations agree within $`4\times10^{-11}`$ across the 48 tested configurations. The accepted v1.2.0 checkpoint verifies the neutral translation mode and stable shape spectrum. The v1.3.0 checkpoint checks the causal response of that aligned root and the error from eliminating fast rates. [Feedback calculation and reproduction commands](docs/audits/liquidity-feedback-v1.3.0.md). See the [scientific audit and reproduction commands](docs/audits/frozen-response-v1.1.0.md) and the [crossover figure](figures/v2/response-crossover.svg).


| Decision record | Current position |
|---|---|
| Current situation | W08/v1.7.0 accepted on `main`. Published software baseline v1.0.0. |
| Future situation | Map the response exponent across operational scales and assess the precision of the nonlinear displacement. |
| Accepted evidence | Historical surface replay, independent frozen-variance comparison, translating spectrum and aligned-root residual, independent causal-response and shell-reduction checks, the matched and offset balance measurements, and the independent moving-zero variance. The signed phase–shape decomposition agrees with the cross-spectral comparison. See the version table. |
| Unresolved issues | Historical archive reconciliation and the derivation of effective liquidity feedback from physical kinetics. |
| Decision required | Evaluate stochastic refinement before attributing a nonlinear variance slope to a change of mechanism. Three response and four primary offset variance classifications remain inconclusive. A GitHub release requires a separate major-milestone decision. |
| Next gate | W09 compares mechanisms and tests the scale and state dependence of an effective variance rate. |
