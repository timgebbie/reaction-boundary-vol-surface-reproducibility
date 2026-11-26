"""Finite-rate moving-root response and conditional Gaussian price diagnostics."""
import numpy as np
from scipy.linalg import eigh

from functions.liquidity_feedback import rate_grid, velocity_transfer


def beta_curve(lags, floor, count, theta=.3, gain=.5, feedback=4.):
    """Exact logarithmic derivative of the finite positive modal sum at each lag."""
    rates, weights = rate_grid(theta, floor, 100., count)
    b = np.sqrt(weights)
    poles, basis = eigh(np.diag(rates) + feedback * np.outer(b, b))
    amplitudes = gain * feedback * (basis.T @ b)**2 / poles
    dc = velocity_transfer(0., rates, weights, gain, feedback)
    terms = np.exp(-lags[:, None] * poles) * amplitudes
    return lags * (terms @ poles) / (dc + terms.sum(axis=1))


def conditional_history(age, first_gap, last_gap, variance):
    """Earlier/future partial correlation and present-conditioned variance ratio."""
    times = np.array([age, age + first_gap, age + first_gap + last_gap])
    v = variance[times]
    cov = (v[:, None] + v[None, :] - variance[abs(times[:, None] - times)]) / 2
    residual = cov - np.outer(cov[:, 1], cov[1, :]) / cov[1, 1]
    rho = residual[0, 2] / np.sqrt(residual[0, 0] * residual[2, 2])
    return rho, residual[2, 2] / variance[last_gap]


def variogram(gamma, theta, floor, duration, step, feedback=4., clock=1.):
    """Expected centred, origin-relative increment variance at integer time gaps."""
    n = round(duration / step)
    omega = 2 * np.pi * np.fft.rfftfreq(n, step)
    rates, weights = rate_grid(theta, floor, 100., 128)
    power = np.zeros_like(omega)
    for first in range(1, len(omega)-1, 2048):
        band = slice(first, min(first+2048, len(omega)-1))
        w = omega[band]
        signed_input = (2*np.sin(w*step/2)/step)**(gamma-1)
        response = velocity_transfer(1j*w, clock*rates, weights, .5, feedback)
        power[band] = signed_input * abs(response/w)**2
    cov = np.fft.irfft(power, n=n) / step
    return 2*(cov[0] - cov[::round(1/step)])
