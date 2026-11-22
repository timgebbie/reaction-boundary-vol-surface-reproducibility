"""Auxiliary translation-equivariant reaction boundary (EFT G3b/G3d).

Scientific status: exactly specified auxiliary field, *not* the physical
nonlinear Donier book or the frozen Abel response in arXiv:2607.05011v4.
All times are operational time.  The root is the zero of the signed
imbalance field, not a calendar-time diffusion or option-price process.
"""

from math import isfinite, sqrt

import numpy as np
from scipy.linalg import eigh_tridiagonal


def _parameters(diffusion, resilience, deposition):
    vals = (diffusion, resilience, deposition)
    if not all(isfinite(float(z)) and z > 0 for z in vals):
        raise ValueError("D, nu and lambda_dep must be finite and positive")
    a = sqrt(resilience / diffusion)
    L = deposition / sqrt(diffusion * resilience)
    kappa = a / (2 * L)
    return a, L, kappa


def front_profile(x, q=0., *, diffusion=1., resilience=1., deposition=1.):
    """Translated steady profile Phi_*(x-q), exactly zero at x=q."""
    a, _, _ = _parameters(diffusion, resilience, deposition)
    xi = np.asarray(x, dtype=float) - q
    # expm1 avoids loss of significance when |x-q| is small.
    return (deposition / resilience) * np.sign(xi) * np.expm1(-a * np.abs(xi))


def root_slope(*, diffusion=1., resilience=1., deposition=1.):
    """Positive simple-zero slope L=-Phi_*'(q)."""
    return _parameters(diffusion, resilience, deposition)[1]


def translation_mode(x, q=0., *, diffusion=1., resilience=1., deposition=1.):
    """Translation tangent psi(x-q)=-Phi_*'(x-q) = L exp(-a|x-q|)."""
    a, L, _ = _parameters(diffusion, resilience, deposition)
    return L * np.exp(-a * np.abs(np.asarray(x, dtype=float) - q))


def zero_phase_shape(x, *, diffusion=1., resilience=1., deposition=1.):
    """Shape f_perp orthogonal to translation, yet shifting observed root.

    f_perp(x)=exp(-2a|x|)-(2/3)exp(-a|x|); its inner product with
    psi=L exp(-a|x|) vanishes on R but f_perp(0)=1/3. Thus the
    translation spectral phase is zero at first order while the
    observed-root variation is 1/(3L). This is a tangent-space
    counterexample, not a driven nonlinear solution.
    """
    a, _, _ = _parameters(diffusion, resilience, deposition)
    r = a * np.abs(np.asarray(x, dtype=float))
    return np.exp(-2*r) - (2/3) * np.exp(-r)


def aligned_placement(x, q=0., *, diffusion=1., resilience=1., deposition=1.):
    """Normalised G3d source h_*=kappa_* psi; integral over R is 1."""
    _, _, kappa = _parameters(diffusion, resilience, deposition)
    return kappa * translation_mode(x, q, diffusion=diffusion,
                                    resilience=resilience, deposition=deposition)


def aligned_gain(*, diffusion=1., resilience=1., deposition=1.):
    """Exact aligned root velocity is qdot=kappa_* b(u)."""
    return _parameters(diffusion, resilience, deposition)[2]


def lattice_bound_eigenvalue(dx, *, diffusion=1., resilience=1., deposition=1.):
    """Exact isolated eigenvalue of the *infinite-lattice* delta defect.

    Centered second differences and delta_0 -> 1/dx at node zero give
    lambda_0(dx)=-nu+2D/dx^2(sqrt(1+nu dx^2/D)-1).
    The cancellation-free form is used for small dx. It tends to 0 from
    below, with O(dx^2) discretisation error. This is a discretisation
    diagnostic, not the continuum assertion sigma(A)={0} U (-inf,-nu].
    """
    if not isfinite(float(dx)) or dx <= 0:
        raise ValueError("dx must be finite and positive")
    a, _, _ = _parameters(diffusion, resilience, deposition)
    t = a * dx
    return -resilience * t**2 / (1 + sqrt(1 + t**2))**2


def _box_modes(n_half, dx, diffusion, resilience, defect):
    """Interior nodes run from -n_half to n_half. Dirichlet walls lie one cell beyond."""
    n = 2 * n_half + 1
    x = dx * np.arange(-n_half, n_half + 1)
    diag = np.full(n, -2 * diffusion / dx**2 - resilience)
    diag[n_half] += defect / dx
    off = np.full(n - 1, diffusion / dx**2)
    values, vectors = eigh_tridiagonal(diag, off, select='i',
                                       select_range=(n - 3, n - 1))
    return x, values, vectors


def pinned_top_eigenvalue(n_half, dx, *, diffusion=1., resilience=1.):
    """Largest box eigenvalue with a fixed source, using the same Dirichlet stencil."""
    _parameters(diffusion, resilience, 1.)
    if not isinstance(n_half, int) or n_half < 10 or not isfinite(dx) or dx <= 0:
        raise ValueError("Require at least ten nodes per half and a finite positive spacing")
    _, values, _ = _box_modes(n_half, dx, diffusion, resilience, 0.)
    return float(values[-1])


def point_interaction_spectrum(n_half=160, dx=0.05, *, diffusion=1.,
                               resilience=1., deposition=1.):
    """Highest 3 eigenpairs for a centered, finite Dirichlet lattice.

    The linearised root-coupled operator is
       A f = D f'' - nu f + (2 lambda_dep/L) f(0) delta_0.
    Its continuum neutral eigenfunction is psi=L exp(-a|x|), with
    translation eigenvalue zero. Stable shape spectrum is <= -nu.
    The finite-box result has discretisation and boundary errors.
    """
    if not isinstance(n_half, int) or n_half < 10:
        raise ValueError("n_half must be an integer >=10")
    if not isfinite(float(dx)) or dx <= 0:
        raise ValueError("dx must be finite and positive")
    a, L, _ = _parameters(diffusion, resilience, deposition)
    x, values, vectors = _box_modes(n_half, dx, diffusion, resilience, 2 * deposition / L)
    # Values are in ascending order; column -1 corresponds to neutral mode.
    exact = translation_mode(x, diffusion=diffusion, resilience=resilience,
                             deposition=deposition)
    exact /= np.linalg.norm(exact)
    neutral = vectors[:, -1]
    if np.dot(neutral, exact) < 0:
        neutral = -neutral
    return dict(x=x, eigenvalues=values, neutral_eigenvector=neutral,
                continuum_mode=exact,
                mode_l2_error=float(np.linalg.norm(neutral - exact)),
                infinite_lattice_prediction=lattice_bound_eigenvalue(
                    dx, diffusion=diffusion, resilience=resilience,
                    deposition=deposition),
                stable_gap_lower_bound=resilience)


def aligned_root_path(time, forcing, q0=0., *, diffusion=1., resilience=1.,
                      deposition=1.):
    """Trapezoidal integration of exact aligned law qdot=kappa_* b(u).

    This deterministic quadrature tests the invariant-family identity;
    it does not implement a distribution of feedback rates or noisy forcing.
    """
    t = np.asarray(time, dtype=float)
    b = np.asarray(forcing, dtype=float)
    if t.ndim != 1 or len(t) < 2 or b.shape != t.shape:
        raise ValueError("time and forcing must be equal 1-D arrays (length>=2)")
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(b)):
        raise ValueError("time and forcing must be finite")
    h = np.diff(t)
    if not np.all(h > 0):
        raise ValueError("time must be strictly increasing")
    kappa = aligned_gain(diffusion=diffusion, resilience=resilience,
                         deposition=deposition)
    return q0 + kappa * np.r_[0., np.cumsum(h * (b[:-1] + b[1:]) / 2.)]


def grid_root(field, x):
    """Interpolate a unique positive-to-negative simple crossing.

    Generic data with multiple crossings or wrong sign orientation are
    rejected; this must not silently repair a failed moving front.
    """
    f, x = np.asarray(field, dtype=float), np.asarray(x, dtype=float)
    if f.ndim != 1 or f.shape != x.shape or len(x) < 3:
        raise ValueError("field and grid must be one-dimensional and matched")
    if not np.all(np.isfinite(f)) or not np.all(np.isfinite(x)) or not np.all(np.diff(x) > 0):
        raise ValueError("field/grid values must be finite and x increasing")
    exact = np.where(f == 0)[0]
    crosses = np.where((f[:-1] > 0) & (f[1:] < 0))[0]
    reverse = np.where((f[:-1] < 0) & (f[1:] > 0))[0]
    if len(reverse) or len(crosses) + len(exact) != 1:
        raise ValueError("Expected precisely one simple positive-to-negative root")
    if len(exact):
        j = exact[0]
        if j == 0 or j == len(f)-1 or not f[j-1] > 0 or not f[j+1] < 0:
            raise ValueError("Exact grid zero does not have the required orientation")
        return float(x[j])
    j = crosses[0]
    return float(x[j] - f[j] * (x[j+1]-x[j])/(f[j+1]-f[j]))


def moving_profile_pde_residual(x, q, b, dx, *, diffusion=1.,
                                resilience=1., deposition=1.):
    """Interior finite-difference residual of the EXACT aligned PDE ansatz.

    Compare Phi_t = kappa b psi with D Phi_xx - nu Phi
    - lambda sign(x-q) + b h_*(x-q). The cutoff mask excludes the
    non-smooth second derivative at the root (three dx), and the grid
    endpoints. Report this as a *local* finite-difference check, not a
    full nonlinear PDE convergence theorem.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size < 7 or not np.allclose(np.diff(x), dx, rtol=1e-9, atol=1e-12):
        raise ValueError("Uniform x grid and matching dx required")
    field = front_profile(x, q, diffusion=diffusion, resilience=resilience,
                          deposition=deposition)
    rhs = diffusion * (field[2:] - 2 * field[1:-1] + field[:-2]) / dx**2
    rhs -= resilience * field[1:-1]
    rhs -= deposition * np.sign(x[1:-1] - q)
    rhs += b * aligned_placement(x[1:-1], q, diffusion=diffusion,
                                 resilience=resilience, deposition=deposition)
    lhs = b * aligned_gain(diffusion=diffusion, resilience=resilience,
                           deposition=deposition) * translation_mode(
                               x[1:-1], q, diffusion=diffusion,
                               resilience=resilience, deposition=deposition)
    valid = np.abs(x[1:-1] - q) > 3 * dx
    if not np.any(valid):
        raise ValueError("Grid does not resolve the smooth region")
    return float(np.max(np.abs(lhs[valid]-rhs[valid])))
