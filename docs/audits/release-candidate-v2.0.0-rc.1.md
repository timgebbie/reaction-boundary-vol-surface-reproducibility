# Reproduction of the reaction-boundary calculations

The accepted scientific source is [`a3c4eab`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/a3c4eab3290c4de4ea36e0eb7476bc0aa8d6ce4e). The versioned v1.9.0 companion is pinned at [`8aee853`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/8aee853482fced712fbe543a2093f2449e4ad603). The candidate adds an explicit finite-band variance bound to §17 of the [consolidated supplement](../../supplementary-materials/ReactionBoundaryVolSurface-Supplement-v2.0.0-rc.1.tex).

The replay used a fresh clone with an independent Git object store, a clean starting worktree, and the recorded Linux environment with Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.11.0. The numerical libraries used one thread. All extension tables, directly generated extension figures, historical structural panels, historical diagnostic CSVs and the low-regime README pair were removed from this disposable checkout before executing the scripts. The seven PDF derivatives were exported anew from the regenerated SVGs with Inkscape 1.4.

| Comparison | Reproduction result |
|---|---|
| Scientific regression and historical checks | 33 scientific tests, 42 baseline diagnostics and 19 sensitivity checks passed. |
| Extension tables | 28 of 29 files matched byte for byte. Fifteen numeric cells of `feedback-time.csv` differed, with maximum absolute difference 1.11023 × 10⁻¹⁶ or less. All other cells matched. |
| Historical CSVs | The three parameter and regime tables and both diagnostic tables agreed after parsing. Five numeric cells of the sensitivity summary differed by at most 4.44090 × 10⁻¹⁶. |
| Figure files | The seven regenerated extension SVGs and both formats of the regime map matched byte for byte. The twelve historical structural PNGs had identical decoded pixels. Their file encodings differed. |
| Consolidated companion | Three pdfLaTeX passes using the regenerated figures produced 33 pages. At 72 dpi, every page matched the distributed candidate in rendered pixels. Extracted text also matched page by page. |

From the repository root, install `requirements-response.txt` and use the candidate companion source. Run the following sequence in a disposable checkout.

~~~bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
python -W error -m unittest discover -s tests -v
for stage in run_all run_frozen_response run_translating_front run_liquidity_feedback \
    run_response_balance run_root_variance run_phase_shape run_nonlinear_field \
    check_nonlinear_speed run_scale_window run_matched_refinement compose_readme_low_z
do
    python -W error "scripts/$stage.py" || exit 1
done
for figure in figures/v2/*.svg
do
    inkscape "$figure" --export-filename="${figure%.svg}.pdf" || exit 1
done
latexmk -pdf -outdir=supplementary-materials supplementary-materials/ReactionBoundaryVolSurface-Supplement-v2.0.0-rc.1.tex
~~~

The two prescribed matches satisfy the aligned-root response and variance criteria across the original 17 operational lags. Three response offsets and four primary variance offsets retain their inconclusive classifications. All 32 continuing nonlinear paths meet the refined displacement tolerance. Each of the eight nonlinear variance series has lags outside the 0.9–1.1 slope interval. General nonlinear diffusion, closure on price alone and the emergence of a state-conditioned local-volatility surface from the translating field remain questions for the subsequent EFT project. [Supplement §§13–17](../../supplementary-materials/ReactionBoundaryVolSurface-Supplement-v2.0.0-rc.1.pdf)
