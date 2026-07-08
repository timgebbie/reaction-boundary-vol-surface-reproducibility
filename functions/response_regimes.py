"""Response-regime functions for the reaction-boundary surface.

Implements the two asymptotic cases from the source equation labelled
``eq:F-asymp``. These helpers do not evaluate the full response integral.
"""

from __future__ import annotations

import numpy as np
from math import lgamma


def _as_array(value):
    return np.asarray(value, dtype=float)


def validate_gamma(gamma):
    """Return gamma as an array after checking 0 < gamma < 1."""
    gamma_arr = _as_array(gamma)
    if np.any((gamma_arr <= 0.0) | (gamma_arr >= 1.0)):
        raise ValueError("gamma must satisfy 0 < gamma < 1")
    return gamma_arr


def validate_positive(name, value):
    """Return value as an array after checking strict positivity."""
    arr = _as_array(value)
    if np.any(arr <= 0.0):
        raise ValueError(f"{name} must be strictly positive")
    return arr


def f_low_z(gamma):
    """Low-z response approximation.

    F_gamma(z) ~ tan(pi gamma / 2) / (2 (1 - gamma)), z << 1.
    """
    gamma_arr = validate_gamma(gamma)
    return np.tan(np.pi * gamma_arr / 2.0) / (2.0 * (1.0 - gamma_arr))


def k_gamma_0(gamma):
    """High-z prefactor K_gamma^(0)."""
    gamma_arr = validate_gamma(gamma)
    gammaln = np.vectorize(lgamma)
    log_value = (
        gammaln(1.0 - gamma_arr)
        + np.log(np.sin(np.pi * gamma_arr / 2.0))
        + gammaln(gamma_arr / 2.0)
        + gammaln((1.0 - gamma_arr) / 2.0)
        - np.log(2.0)
        - 1.5 * np.log(np.pi)
    )
    return np.exp(log_value)


def f_high_z(gamma, z):
    """High-z response approximation.

    F_gamma(z) ~ K_gamma^(0) z^(gamma - 1), z >> 1.
    """
    gamma_arr = validate_gamma(gamma)
    z_arr = validate_positive("z", z)
    return k_gamma_0(gamma_arr) * np.power(z_arr, gamma_arr - 1.0)


def response_factor(regime, gamma, z):
    """Evaluate the selected response regime."""
    if regime == "low_z":
        return f_low_z(gamma)
    if regime == "high_z":
        return f_high_z(gamma, z)
    raise ValueError("regime must be 'low_z' or 'high_z'")


def response_regime_table():
    """Return table rows describing the implemented response regimes."""
    return [
        {
            "regime": "low_z",
            "condition": "z = nu Delta << 1",
            "formula": "tan(pi gamma / 2) / (2 (1 - gamma))",
            "depends_on_z": False,
        },
        {
            "regime": "high_z",
            "condition": "z = nu Delta >> 1",
            "formula": "K_gamma_0(gamma) z^(gamma - 1)",
            "depends_on_z": True,
        },
    ]
