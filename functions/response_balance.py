"""Forcing-memory and causal root-response estimators on the operational clock."""

from math import comb
import numpy as np

from functions.liquidity_feedback import memory


def slope(x, y):
    """OLS slope with intercept along the final dimension."""
    centred = x - x.mean()
    return np.sum(y * centred, axis=-1) / np.sum(centred**2)


def forcing_estimates(gamma, step, replicate, duration=262144):
    """Measure the forcing exponent from a realized stationary periodic Gaussian path."""
    n = int(duration / step)
    seed = np.random.SeedSequence([1400, round(100*gamma), round(2*step), replicate])
    rng = np.random.default_rng(seed)
    omega = 2*np.pi*np.fft.rfftfreq(n, d=step)
    coeff = np.fft.rfft(rng.standard_normal(n))
    coeff[0] = 0
    coeff[1:] *= (2*np.sin(omega[1:]*step/2)/step)**((gamma-1)/2)
    path = np.fft.irfft(coeff, n=n)
    band = (omega >= 1/320) & (omega <= 1/32)
    x = np.log(omega[band])
    y = np.log(np.abs(np.fft.rfft(path)[band])**2 * step/n)
    return [1+slope(x[::stride], y[::stride]) for stride in (1, 2)]


def root_response(times, rates, weights, gain, feedback, shape_weight, inversion):
    """Invert H(s)/s on a vertical Bromwich contour with Euler summation."""
    a, n, m = inversion
    k = np.arange(n+m+1)
    euler = np.array([comb(m,j)/2**m for j in range(m+1)])
    result = np.empty(len(times))
    # Bound the size of the time x frequency x rate array.
    for i in range(0, len(times), 16):
        t = times[i:i+16, None]
        s = (a/2 + 1j*np.pi*k)/t
        wave = np.sqrt(1+s)
        shape = 1 - shape_weight/(wave+2)
        transform = gain*shape/(s*(1+feedback*shape*memory(s, rates, weights)))
        terms = transform.real * (-1.)**k
        terms[:, 0] /= 2
        sums = np.cumsum(terms, axis=1)[:, n:]
        result[i:i+len(t)] = np.exp(a/2)*(sums @ euler)/t[:, 0]
    return result


def response_slopes(samples, offsets):
    """Use every sample in a centred local log regression; preserve invalid rows."""
    valid = np.all(np.isfinite(samples) & (samples > 0), axis=1)
    beta = np.full(samples.shape[0], np.nan)
    beta[valid] = -slope(offsets, np.log(samples[valid]))
    return beta
