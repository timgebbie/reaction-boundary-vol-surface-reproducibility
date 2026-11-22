"""Stationary frozen tangent response on the operational clock (arXiv:2607.05011v4)."""

from functools import lru_cache
from math import ceil, exp, hypot, isfinite, log, pi, sin, sqrt

import numpy as np
from scipy.integrate import quad
from scipy.special import beta, betainc, betaincc, erfcx, gamma as gamma_fn, hyp1f1, roots_genlaguerre


def _check(gamma, *positive):
    if not 0 < gamma < 1 or not all(isfinite(v) and v > 0 for v in positive):
        raise ValueError("Require 0 < gamma < 1 and positive finite model scales.")


def _segments(start, stop, scales):
    """Resolve each crossover and subdivide widely separated positive scales."""
    edges = sorted({start, stop, *(v for v in scales if start < v < stop)})
    for a, b in zip(edges, edges[1:]):
        if a == 0:
            yield a, b
        else:
            n = max(1, ceil(log(b / a) / log(8)))
            points = np.geomspace(a, b, n + 1)
            yield from zip(points, points[1:])


def _increment_integral(density, scales, mean_tail, tol):
    # Below the split use the cancellation-free increment filter directly.
    split = 8.0
    direct = sum(quad(lambda x: 2 * sin(x / 2)**2 * density(x), a, b,
                      epsabs=0, epsrel=tol)[0]
                 for a, b in _segments(0, split, scales))
    scale = density(split)
    cosine = quad(lambda x: density(x) / scale, split, np.inf,
                  weight="cos", wvar=1, epsabs=tol, limlst=160)[0]
    return direct + mean_tail - scale * cosine


def crossover(gamma, z, *, tol=1e-8):
    """Full zero-cutoff dimensionless response F_gamma(z), Eq. (21)."""
    _check(gamma, z, tol)
    def density(x):
        return x**(gamma - 1) / hypot(z, x)

    a, b = (1 - gamma) / 2, gamma / 2
    if z <= 8:
        fraction = betainc(a, b, (z / hypot(z, 8))**2)
    else:
        fraction = betaincc(b, a, (8 / hypot(z, 8))**2)
    tail = z**(gamma - 1) * beta(a, b) * fraction / 2
    factor = gamma_fn(1 - gamma) * sin(pi * gamma / 2) / pi
    return factor * _increment_integral(density, (z,), tail, tol)


@lru_cache(maxsize=32)
def _rate_rule(gamma, order):
    return roots_genlaguerre(order, gamma)


def _forcing_factor(gamma, q, order):
    """Spectrum divided by A_m * |omega|^(gamma-1), q=|omega|*tau0."""
    a = 1 - gamma
    if q < 1:
        # Fourier transform after shifting t -> t+tau0.
        shifted = gamma_fn(a) * np.exp(-0.5j * pi * a)
        lower = q**a * hyp1f1(a, a + 1, -1j * q) / a
        return 2 * (np.exp(1j * q) * (shifted - lower)).real
    rates, weights = _rate_rule(gamma, order)
    # Positive Laplace mixture of exponentials, integrated in rate*tau0.
    return 2 * q**(-1 - gamma) * np.dot(weights, 1 / (1 + (rates / q)**2)) / gamma_fn(gamma)


def frozen_variance(gamma, nu, tau0, delta, *, forcing=1., diffusion=1., liquidity=1., tol=1e-8, rate_order=64):
    """Unconditional increment variance V; the coefficient in Eq. (47) is V/delta.

    forcing is the covariance amplitude A_m, diffusion is D, and liquidity is L.
    """
    _check(gamma, nu, tau0, delta, diffusion, liquidity, tol)
    if not isfinite(forcing) or forcing < 0:
        raise ValueError("Forcing covariance amplitude must be nonnegative and finite.")
    if not isinstance(rate_order, int) or rate_order < 2:
        raise ValueError("rate_order must be an integer of at least two.")
    if forcing == 0:
        return 0.
    z, ratio = nu * delta, tau0 / delta
    def density(x):
        response = erfcx(np.sqrt(complex(z, x) * ratio))
        return x**(gamma - 1) * _forcing_factor(gamma, x * ratio, rate_order) * abs(response)**2 / hypot(z, x)

    # Integrate the nonoscillatory tail through both physical crossovers.
    end = max(8., z, 1 / ratio)
    tail = sum(quad(density, a, b, epsabs=0, epsrel=tol)[0]
               for a, b in _segments(8., end, (z, 1 / ratio)))
    tail += quad(lambda u: end * density(end / u) / u**2,
                 0, 1, epsabs=0, epsrel=tol)[0]
    value = _increment_integral(density, (z, 1 / ratio), tail, tol)
    scale = forcing * delta**(1 - gamma) / (diffusion * liquidity**2)
    return scale * exp(-2 * nu * tau0) * value / (2 * pi)


def time_covariance_check(gamma, nu, tau0, delta, *, forcing=1., diffusion=1., liquidity=1., tol=1e-7):
    """Independent time-domain (increment variance, level variance) for Eq. (47).

    Quadrature of the kernel autocorrelation against the forcing covariance,
    splitting at its lag cusp. Time variables are in units of 1/nu.
    """
    _check(gamma, nu, tau0, delta, diffusion, liquidity, tol)
    if not isfinite(forcing) or forcing < 0:
        raise ValueError("Forcing covariance amplitude must be nonnegative and finite.")
    e, lag = nu * tau0, nu * delta
    # Exponential truncation; repeat at stricter tolerance for convergence checks.
    end = max(45., -2 * log(tol))
    umax = np.log1p(end / e)

    def weight(h):
        def integrand(u):
            shifted = e * exp(u)
            return exp(-2 * e * np.expm1(u)) * sqrt(shifted / (shifted + h))
        return exp(-h) * quad(integrand, 0, umax, epsabs=0, epsrel=tol)[0]

    def difference(h):
        # Factor out C(h) before differencing for short lags.
        base = h + e
        # For h >= lag use the symmetric second difference as a series
        # when cancellation would erase the quadratic term.
        if h >= lag and lag / base < 1e-3:
            ratio = lag / base
            return -base**(-gamma) * gamma * (gamma + 1) * ratio**2 * (
                1 + (gamma + 2) * (gamma + 3) * ratio**2 / 12)
        left = abs(h - lag) + e
        return -base**(-gamma) * (np.expm1(-gamma * log(left / base))
                                  + np.expm1(-gamma * np.log1p(lag / base)))

    # At lag, |h-lag| develops a narrow peak of width e.
    scales = [e, 1., lag]
    distance = e
    while distance < min(lag, end) and lag < 2 * end:
        scales.extend((lag - distance, lag + distance))
        distance *= 4
    def integrate(fn):
        return sum(quad(lambda h: weight(h) * fn(h), a, b, epsabs=0, epsrel=tol)[0]
                   for a, b in _segments(0, end, scales))
    scale = forcing * nu**(gamma - 1) * exp(-2 * e) / (2 * pi * diffusion * liquidity**2)
    return scale * integrate(difference), scale * integrate(lambda h: (h + e)**(-gamma))
