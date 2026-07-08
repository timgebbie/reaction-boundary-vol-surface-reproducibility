"""Projected local-volatility kernel for the Stage 6 implementation."""

from __future__ import annotations

import numpy as np

from .response_regimes import response_factor, validate_gamma, validate_positive
from .structural_profiles import activity_profile, profile_components


def projected_variance_surface(m_grid, T_grid, params, profile_name, regime):
    """Evaluate projected local variance on a maturity by state grid.

    Returns an array with shape ``(len(T_grid), len(m_grid))``.
    """
    m = np.asarray(m_grid, dtype=float)
    T = np.asarray(T_grid, dtype=float)
    if m.ndim != 1 or T.ndim != 1:
        raise ValueError("m_grid and T_grid must be one-dimensional")

    gamma = validate_gamma(params["gamma"])
    Delta = validate_positive("Delta", params["Delta"])
    components = profile_components(profile_name, m, params, regime)

    A_eff = validate_positive("A_eff", components["A_eff"])
    L = validate_positive("L", components["L"])
    z = validate_positive("z", components["z"])

    response = response_factor(regime, gamma, z)
    operational_variance = (
        (A_eff / np.square(L))
        * np.power(Delta, -gamma)
        * response
    )

    alpha = activity_profile(
        T,
        alpha0=params["alpha0"],
        a_short=params["a_short"],
        tau_alpha=params["tau_alpha"],
    )
    return alpha[:, None] * operational_variance[None, :]


def projected_volatility_surface(m_grid, T_grid, params, profile_name, regime):
    """Evaluate projected local volatility on a maturity by state grid."""
    variance = projected_variance_surface(m_grid, T_grid, params, profile_name, regime)
    return np.sqrt(variance)

