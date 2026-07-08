"""Structural profiles for the reaction-boundary surface simulation."""

from __future__ import annotations

import numpy as np


PROFILE_NAMES = (
    "liquidity_only",
    "resilience_response_only",
    "combined_structural",
)


def _as_array(value):
    return np.asarray(value, dtype=float)


def activity_profile(T, alpha0=1.0, a_short=0.25, tau_alpha=0.5):
    """Deterministic activity profile alpha(T)."""
    T_arr = _as_array(T)
    if np.any(T_arr < 0.0):
        raise ValueError("T must be nonnegative")
    if alpha0 <= 0.0 or tau_alpha <= 0.0:
        raise ValueError("alpha0 and tau_alpha must be positive")
    alpha = alpha0 * (1.0 + a_short * np.exp(-T_arr / tau_alpha))
    if np.any(alpha <= 0.0):
        raise ValueError("activity profile must remain positive")
    return alpha


def liquidity_profile(m, L0=1.0, L_skew=0.8, L_smile=1.5, L_floor=0.2):
    """State-dependent liquidity slope L(m)."""
    m_arr = _as_array(m)
    if L0 <= 0.0 or L_floor <= 0.0:
        raise ValueError("L0 and L_floor must be positive")
    shape = 1.0 + L_skew * m_arr + L_smile * np.square(m_arr)
    return L0 * np.maximum(L_floor, shape)


def z_profile(m, z_regime, nu_skew=1.0):
    """State-dependent z(m)=nu(m) Delta profile."""
    if z_regime <= 0.0:
        raise ValueError("z_regime must be positive")
    m_arr = _as_array(m)
    return z_regime * np.exp(nu_skew * m_arr)


def forcing_profile(m, A_eff0=1.0, A_stress=0.75):
    """State-dependent effective forcing A_eff(m)."""
    if A_eff0 <= 0.0:
        raise ValueError("A_eff0 must be positive")
    m_arr = _as_array(m)
    return A_eff0 * np.exp(-A_stress * m_arr)


def profile_components(profile_name, m, params, regime):
    """Return A_eff(m), L(m), and z(m) for a named simulation profile."""
    if profile_name not in PROFILE_NAMES:
        raise ValueError(f"unknown profile_name: {profile_name}")
    if regime not in ("low_z", "high_z"):
        raise ValueError("regime must be 'low_z' or 'high_z'")

    m_arr = _as_array(m)
    z_base = params["z_low"] if regime == "low_z" else params["z_high0"]

    A_eff = np.full_like(m_arr, float(params["A_eff0"]), dtype=float)
    L = np.full_like(m_arr, float(params["L0"]), dtype=float)
    z = np.full_like(m_arr, float(z_base), dtype=float)

    if profile_name == "liquidity_only":
        L = liquidity_profile(
            m_arr,
            L0=params["L0"],
            L_skew=params["L_skew"],
            L_smile=params["L_smile"],
            L_floor=params["L_floor"],
        )
    elif profile_name == "resilience_response_only":
        z = z_profile(m_arr, z_base, nu_skew=params["nu_skew"])
    elif profile_name == "combined_structural":
        L = liquidity_profile(
            m_arr,
            L0=params["L0"],
            L_skew=params["L_skew"],
            L_smile=params["L_smile"],
            L_floor=params["L_floor"],
        )
        z = z_profile(m_arr, z_base, nu_skew=params["nu_skew"])
        A_eff = forcing_profile(
            m_arr,
            A_eff0=params["A_eff0"],
            A_stress=params["A_stress"],
        )

    return {
        "A_eff": A_eff,
        "L": L,
        "z": z,
    }

