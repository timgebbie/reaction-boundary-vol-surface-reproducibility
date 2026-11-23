"""Signed phase–shape increments and linearised phase projection."""

import numpy as np
from scipy.special import erfcx

from functions.liquidity_feedback import memory, rate_grid
from functions.response_balance import slope


def abel_shape_filter(omega):
    """Finite-cutoff local Abel filter with prescribed amplitude 0.1."""
    nu, tau = 1e-4, .25
    z = nu + 1j*omega
    return .1*np.exp(-nu*tau)*erfcx(np.sqrt(z*tau))/(2*np.sqrt(z))


def projected_transfers(omega, theta, epsilon, nodes=128):
    """Return the neutral phase, stable shape and full first-variation root."""
    rates, weights = rate_grid(theta,1e-7,100.,nodes)
    out = np.zeros((3,len(omega)), dtype=complex)
    for i in range(1,len(omega)-1,2048):
        j = min(i+2048,len(omega)-1)
        s = 1j*omega[i:j]
        k = np.sqrt(1+s)
        a = 1-epsilon/(k+2)
        denominator = 1+4*a*memory(s,rates,weights)
        out[0,i:j] = .5*(1-epsilon/3)/(s*denominator)
        out[1,i:j] = .5*epsilon/(3*(k+1)*(k+2)*denominator)
        out[2,i:j] = .5*a/(s*denominator)
    return out


def increment_covariance(q, shape, lags, step):
    """Measured covariance of same-lag, same-origin periodic increments."""
    qhat = np.fft.rfft(q-q.mean())
    xhat = np.fft.rfft(shape-shape.mean())
    symmetric = np.fft.irfft((qhat*xhat.conj()).real,n=len(q))/len(q)
    cross = 2*(symmetric[0]-symmetric)
    indices = lags/step
    j = indices.astype(int)
    f = indices-j
    return (1-f)*cross[j]+f*cross[j+1]-f*(1-f)*cross[1]


def component_statistics(means,lags,offsets,has_shape):
    """means has axes [..., component, lag, regression offset]."""
    q, shape, total, cov = np.moveaxis(means,-3,0)
    mid = len(offsets)//2
    twice = 2*cov[...,mid]
    rate = total[...,mid]/lags
    shape_slope = slope(offsets,np.log(shape)) if has_shape else np.full_like(rate,np.nan)
    return np.stack((twice,twice/total[...,mid],slope(offsets,np.log(q)),
                     shape_slope,slope(offsets,np.log(total)),rate,rate/rate[...,:1]),axis=-1)
