"""Variance of observed zeros on the exactly aligned translating family."""

import numpy as np
from scipy.stats import t as student

from functions.response_balance import slope
from functions.translating_front import front_profile


def field_zeros(phase, dx):
    """Measure sign-bracketed zeros on an origin-anchored spatial grid."""
    left = dx*np.floor(phase/dx)
    a = front_profile(left-phase)
    b = front_profile(left+dx-phase)
    valid = (a >= 0) & (b <= 0) & (a > b)
    safe_width = np.where(valid, a-b, 1.)
    zeros = np.where(valid, left+dx*a/safe_width, np.nan)
    return zeros, (a-b)/dx, int(np.count_nonzero(~valid))


def global_bracket_check(phase, dx):
    """Search from a common spatial box; no per-observation cell guess."""
    lo = np.full(phase.shape, int(np.floor(phase.min()/dx))-2, dtype=int)
    hi = np.full(phase.shape, int(np.ceil(phase.max()/dx))+2, dtype=int)
    while np.any(hi-lo>1):
        mid = (lo+hi)//2
        positive = front_profile(mid*dx-phase)>=0
        lo,hi = np.where(positive,mid,lo),np.where(positive,hi,mid)
    a = front_profile(lo*dx-phase)
    b = front_profile(hi*dx-phase)
    return lo*dx+dx*a/(a-b)


def periodic_variances(zeros, lags, step):
    """All-start increments with linear interpolation at fractional terminal times."""
    centred = zeros-zeros.mean()
    spectrum = np.fft.rfft(centred)
    corr = np.fft.irfft(np.abs(spectrum)**2, n=len(zeros))/len(zeros)
    variogram = 2*(corr[0]-corr)
    x = lags/step
    j = x.astype(int)
    r = x-j
    return (1-r)*variogram[j]+r*variogram[j+1]-r*(1-r)*variogram[1]


def predicted_variance(power, omega, step, n, lags):
    """Exact ensemble prediction for linearly interpolated phase increments.

    power contains the two-sided continuous-input spectral weights after
    velocity filtering and integration. DC and Nyquist are both excluded.
    """
    out = []
    for lag in lags:
        x = lag/step
        j = int(x)
        r = x-j
        multiplier = np.expm1(1j*omega*j*step) + r*np.exp(1j*omega*j*step)*np.expm1(1j*omega*step)
        out.append(2*np.dot(power[1:-1], np.abs(multiplier[1:-1])**2)/(n*step))
    return np.array(out)


def variance_statistics(means, lags, offsets):
    """Transform an ensemble mean, including a possible leave-one-path-out axis."""
    rate = means[...,len(offsets)//2] / lags
    rate_ratio = rate / rate[..., :1]
    exponent = slope(offsets, np.log(means))
    return np.stack((exponent,rate,rate_ratio),axis=-1)


def variance_intervals(paths, lags, offsets, family_size):
    n = len(paths)
    average = paths.mean(axis=0)
    point = variance_statistics(average,lags,offsets)
    leave = (n*average-paths)/(n-1)
    values = variance_statistics(leave,lags,offsets)
    stderr = np.sqrt((n-1)/n*np.sum((values-values.mean(axis=0))**2,axis=0))
    half = student.ppf(1-.05/(2*family_size),n-1)*stderr
    return point,point-half,point+half
