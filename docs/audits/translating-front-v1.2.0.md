# v1.2.0 — translating reaction-boundary tangent and shape spectrum

**Status:** W02 computational checkpoint, accepted on 22 November 2026; not a GitHub release or a new theorem for a generic order book. **Immutable source:** [Angstmann and Gebbie, arXiv:2607.05011v4](https://arxiv.org/abs/2607.05011v4). **Extension provenance:** the separate *Toward an Effective Field Theory of Market Microstructure* v1.0.0 companion, G3b and G3d. This checkpoint does not alter either reference.

## Scientific distinction from the frozen response

The original v4 calculation takes a simple-zero tangent of a locally frozen reaction boundary with a damped Abel kernel. The auxiliary field here instead admits a translation-equivariant family of complete liquidity profiles and a zero mode. These are distinct response operators and observables; the new mode does not change the original frozen-boundary response or its low-/high-\(z\) variance interpretation.

Set \(a=\sqrt{\nu/D}\), \(L=\lambda_{\mathrm{dep}}/\sqrt{D\nu}>0\), and use the root-coupled field

\[
\partial_u\Phi=D\Phi_{xx}-\nu\Phi-\lambda_{\rm dep}\operatorname{sgn}(x-y(u))+b(u)h(x-y(u)),\qquad\Phi(y(u),u)=0.
\]

Its unforced translating family is

\[
\Phi_*(\xi)=-\frac{\lambda_{\rm dep}}{\nu}\operatorname{sgn}(\xi)(1-e^{-a|\xi|}),\qquad
\psi(\xi)=-\Phi_*'(\xi)=L e^{-a|\xi|}.
\]

The linearised point-interaction operator on the continuum has the translation tangent \(\psi\) at eigenvalue zero and a stable shape continuum \(( -\infty,-\nu]\):

\[
\mathcal A f=D f''-\nu f+\frac{2\lambda_{\rm dep}}L f(0)\,\delta_0,\qquad
\sigma(\mathcal A)=\{0\}\cup(-\infty,-\nu].
\]

Here the **transverse/shape spectrum is gapped by resilience**, while the collective translation mode is neutral. The “massive reaction boundary” is therefore a useful *sector-specific* analogy, not a mass gap for the entire driven stochastic response.

For **exactly aligned** forcing, choose \(h_*(\xi)=\kappa_*\psi(\xi)\), \(\kappa_*=a/(2L)\). Then

\[
\Phi(x,u)=\Phi_*(x-q(u)),\qquad y(u)=q(u),\qquad \dot q(u)=\kappa_* b(u)
\]

is an exact translated solution for a specified forcing path (in the classical/distributional interpretation appropriate to the sign profile). This is **not** the stochastic feedback law of later W03–W06 experiments, nor a proof of attraction or generic nonlinear-root diffusion.

## Independent observables: phase is not always the root

At first variation, spectral phase \(q_{\rm spec}=\langle\psi,f\rangle/\|\psi\|^2\) and observed root variation \(p=f(0)/L\) need not coincide. The test function

\[
f_\perp(x)=e^{-2a|x|}-\frac23 e^{-a|x|}
\]

has \(\langle\psi,f_\perp\rangle=0\), yet \(f_\perp(0)/L=1/(3L)\). The numerical test measures both independently and checks a small perturbed root; thus future W03+ outputs must specify whether a quantity is a spectral-phase or physical-root response.

## Numerical method and evidence

For a centered finite-difference grid, replace \(\delta_0\) with \(1/\Delta x\) at the central node. The infinite-lattice defect eigenvalue has the **independent** analytical expression

\[
\lambda_0(\Delta x)
=-\nu\frac{(a\Delta x)^2}{\left(1+\sqrt{1+(a\Delta x)^2}\right)^2},
\]

and approaches zero from below at order \(\Delta x^2\). The program compares the finite-Dirichlet matrix eigenvalue against this formula, checks the stable shape threshold, compares the principal eigenvector with \(\psi\), and independently locates the moving zero by interpolation. Away from the nonsmooth root it also checks the exact translating ansatz in the finite-difference PDE residual.

[Machine-readable data](../../outputs/v2/translation-spectrum-checks.csv) and [figure](../../figures/v2/translation-modes.svg) are produced by `python scripts/run_translating_front.py` (no random seeds). A local isolated run on Linux, Python 3.12, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.10.8 gave:

| \(\Delta x\) | Largest discrete eigenvalue | First stable shape eigenvalue | Neutral-mode \(L^2\) error | Smooth-region PDE residual |
|---:|---:|---:|---:|---:|
| 0.16 | -0.00631937 | -1.06673763 | 0.00213084 | 0.00129893 |
| 0.08 | -0.00159490 | -1.06763169 | 0.00053323 | 0.00041255 |
| 0.04 | -0.00039968 | -1.06808365 | 0.00013344 | 0.00011627 |

The results are dimensionless with \(D=\nu=\lambda_{\rm dep}=1\). The neutral eigenvalue converges towards zero; the reported first shape eigenvalue lies strictly below \(-\nu\). The numbers are *numerical evidence on finite grids*, not proof of the continuum point spectrum, which comes from the separate analytical model.

## Reproduction and claim boundary

Run from repository root:

```sh
python -m pip install -r requirements-response.txt
python -W error -m unittest discover -s tests -v
python -W error scripts/run_translating_front.py
```

The initial review bundle passed six W02 tests in isolation.

## Integrated replay, 22 November 2026

The integration starts at accepted W01 commit `33332cfd7ce707079e6bac288b739aa28d6837bd`. One front implementation serves all comparisons. The replay uses Linux, Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and the repository-pinned Matplotlib 3.11.0.

The [box sweep](../../outputs/v2/translation-spectrum.csv) puts Dirichlet walls at half-widths 6, 12 and 24, with 16, 32 and 64 cells per unit length. Removing the central defect gives the pinned control. At width 24 and 64 cells per unit length, its highest eigenvalue is −1.004284. Restoring the moving-root coupling gives −0.00006103 for the translation mode and −1.017135 for the first shape mode. The pinned top mode tends to the band edge −1 as the box widens. The separate lattice-pole sweep holds the outermost interior node at 12, with the Dirichlet wall one grid spacing further out.

The [weak residual](../../outputs/v2/aligned-root-checks.csv) integrates the field equation against three compactly supported test functions at four operational times. It splits quadrature at the zero recovered from sampled field values and differences the translated profile in time. At $(\Delta x,\Delta u)=(0.08,0.04)$ the maximum absolute defect is $2.49\times10^{-3}$. At $(0.01,0.005)$ it is $3.16\times10^{-5}$, and the maximum root interpolation error is $4.79\times10^{-6}$. Shifting the forcing profile by 0.4 on that same fine grid gives a defect of $0.218$. This control tests whether the proposed translate still solves the modified field equation. It does not simulate the resulting off-alignment dynamics.

Eight W02 tests and five W01 tests pass with warnings treated as errors. The legacy workflow runs all 42 diagnostics and 19 sensitivity checks. Both W01 data tables and its figure reproduce byte-for-byte in this environment. The historical supplement PDF and TeX match the published v1.0.0 Git tree.

**Current.** W02/v1.2.0 accepted at [`b65bf06`](https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/commit/b65bf066e28466faa6781548a1f21e1b994e780c).

**Verified evidence.** Neutral translation, the stable shape threshold, an independently located aligned root, and a transverse perturbation that separates observed root and phase.

**Open limitations.** The translated solution assumes the aligned initial profile and forcing. Generic transverse stability, physical feedback kinetics and stochastic actual-root variance remain open.

**Next gate.** W03 introduces causal liquidity reassessment with prescribed rates. W04 compares the full and reduced rate spectra.

**Approval needed.** W02 author acceptance is recorded in the linked commit. The next scientific decision concerns W03/W04.
