"""W02 deterministic tangent-spectrum and translating-front evidence generator.

Run from repository root with `python scripts/run_translating_front.py`.
Does not modify the legacy v1.0.0 figure/table generation route.
"""

from pathlib import Path
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapezoid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions.translating_front import (
    aligned_gain, aligned_root_path, front_profile, grid_root,
    moving_profile_pde_residual, point_interaction_spectrum, root_slope,
    aligned_placement, pinned_top_eigenvalue,
)

from scripts.run_frozen_response import write_csv


def aligned_check(dx, dt, *, forcing_offset=0.):
    """Weak PDE defect against three compact test functions straddling the root.

    The nonlinear sign and forcing use the measured zero of the sampled field.
    Spatial quadrature splits there and uses the two one-sided source limits.
    """
    x = np.arange(-round(6/dx), round(6/dx)+1) * dx
    def position(u):
        return .37 + .8*np.sin(1.3*u)
    defects, errors, slopes = [], [], []
    for u in (.11, .58, 1.07, 2.19):
        q = position(u)
        field = front_profile(x-q)
        y = grid_root(field, x)
        errors.append(abs(y-q))
        i = np.searchsorted(x, y)
        slopes.append(-(field[i]-field[i-1])/dx)
        b = .8 * 1.3 * np.cos(1.3*u) / aligned_gain()
        for centre in (-.45, .35, 1.15):
            defect = 0.
            for side, nodes in ((-1, np.r_[x[x<y], y]), (1, np.r_[y, x[x>y]])):
                s = (nodes-centre)/2
                w = np.maximum(0., 1-s**2)
                test = w**4
                test_xx = (-8+56*s**2)*w**2/4
                phi = front_profile(nodes-q)
                phi_u = (front_profile(nodes-position(u+dt))-front_profile(nodes-position(u-dt)))/(2*dt)
                source = -side + b * aligned_placement(nodes-y-forcing_offset)
                integrand = (phi_u + phi - source)*test - phi*test_xx
                defect += trapezoid(integrand, nodes)
            defects.append(abs(defect))
    return dict(dx=dx, dt=dt, forcing_offset=forcing_offset, root_error=max(errors),
                slope_error=max(abs(np.array(slopes)-root_slope())), weak_residual=max(defects))


def spectrum_box(width, resolution):
    dx = 1 / resolution
    n_half = width * resolution - 1
    result = point_interaction_spectrum(n_half, dx)
    neutral = result['neutral_eigenvector']
    scaled = neutral / neutral[n_half]
    return dict(widths=width, resolution=resolution,
                neutral=result['eigenvalues'][-1], stable=result['eigenvalues'][-2],
                pinned=pinned_top_eigenvalue(n_half, dx),
                mode_error=max(abs(scaled - np.exp(-abs(result['x'])))),
                odd_box_prediction=-1 - (np.pi / width)**2)


def main():
    # Fixed outermost interior node while dx is refined. Finite-box and lattice effects
    # remain distinct in the exported table.
    rows = []
    for dx in (0.16, 0.08, 0.04):
        n_half = round(12 / dx)
        result = point_interaction_spectrum(n_half=n_half, dx=dx)
        eig = result['eigenvalues']
        x = np.arange(-5., 5.+dx/2, dx)
        q = .223
        root = grid_root(front_profile(x, q), x)
        resid = moving_profile_pde_residual(x, .137, -.7, dx)
        rows.append(dict(dx=dx, outer_node=n_half*dx, wall=(n_half+1)*dx,
                         neutral_eigenvalue=eig[-1],
                         infinite_lattice_eigenvalue=result['infinite_lattice_prediction'],
                         first_shape_eigenvalue=eig[-2],
                         mode_l2_error=result['mode_l2_error'],
                         root_interpolation_error=abs(root-q),
                         smooth_pde_residual=resid,
                         root_slope=root_slope()))

    write_csv("translation-spectrum-checks.csv", rows)
    write_csv("translation-spectrum.csv",
              [spectrum_box(width, res) for width in (6, 12, 24) for res in (16, 32, 64)])
    checks = [aligned_check(dx, dt) for dx in (.08, .04, .02, .01)
              for dt in (.04, .02, .01, .005)]
    checks.append(aligned_check(.01, .005, forcing_offset=.4))
    write_csv("aligned-root-checks.csv", checks)

    # A deterministic smooth forcing supplies a moving nonlinear invariant
    # profile; the feedback-spectrum and Brownian-limit experiments are W03+.
    t = np.linspace(0., 4., 2001)
    b = .8 + .5 * np.sin(t)
    q = aligned_root_path(t, b, q0=.18)
    x = np.linspace(-4, 7, 1501)

    with mpl.rc_context({'svg.hashsalt': 'reaction-boundary-W02', 'font.size': 10}):
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), layout='constrained')
        e = point_interaction_spectrum(240, 0.05)
        axes[0].plot(e['x'], e['continuum_mode'], label='Continuum neutral tangent')
        axes[0].plot(e['x'][::4], e['neutral_eigenvector'][::4], 'o', ms=2.1,
                     fillstyle='none', label='Point-interaction lattice mode')
        axes[0].set(xlim=(-5,5), xlabel=r'$x-q$', ylabel=r'Normalised $\psi$',
                    title='Neutral translation and stable shape sector')
        axes[0].grid(alpha=.16)
        axes[0].legend(frameon=False, fontsize=8)
        for idx in (0, 500, 1000, 1500, 2000):
            axes[1].plot(x, front_profile(x, q[idx]), label=rf'$u={t[idx]:.1f}$')
            axes[1].plot([q[idx]], [0.], '.', ms=4)
        axes[1].axhline(0, color='gray', lw=.7)
        axes[1].set(xlabel='Operational log-price coordinate $x$',
                    ylabel=r'Signed imbalance $\Phi(x,u)$',
                    title='Exact aligned translating nonlinear root')
        axes[1].grid(alpha=.16)
        axes[1].legend(frameon=False, fontsize=8)
        figure = ROOT / 'figures/v2/translation-modes.svg'
        figure.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(figure, metadata={'Date': None})
        plt.close(fig)

    print('W02 translation/shape evidence (dimensionless, deterministic):')
    for row in rows:
        print(f"dx={row['dx']:6.3f}: lambda_0={row['neutral_eigenvalue']:.6g}, "
              f"lambda_shape={row['first_shape_eigenvalue']:.6g}, "
              f"mode L2 error={row['mode_l2_error']:.3g}, "
              f"root error={row['root_interpolation_error']:.3g}, "
              f"PDE residual={row['smooth_pde_residual']:.3g}")
    print('W02 outputs: outputs/v2/translation-spectrum-checks.csv; '
          'figures/v2/translation-modes.svg')


if __name__ == '__main__':
    main()
