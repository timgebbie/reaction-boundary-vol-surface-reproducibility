"""Prescribed causal liquidity reassessment on a single operational clock."""

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import eigh


def rate_grid(theta, floor, ceiling, count):
    """Positive midpoint rule for rho(r) dr on a uniform grid in log(r)."""
    if not 0 < theta < .5 or not 0 < floor < ceiling or not np.isfinite(ceiling):
        raise ValueError("Require 0 < theta < 1/2 and finite positive ordered endpoints.")
    if not isinstance(count, int) or count < 1:
        raise ValueError("The number of rate cells must be a positive integer.")
    edges = np.linspace(np.log(floor), np.log(ceiling), count + 1)
    rates = np.exp((edges[1:] + edges[:-1]) / 2)
    weights = np.sin(np.pi * theta) / np.pi * rates**(1-theta) * np.diff(edges)
    return rates, weights


def memory(s, rates, weights):
    """Finite Stieltjes transform, with frequency axes preceding the rate axis."""
    return np.sum(weights / (np.asarray(s)[..., None] + rates), axis=-1)


def velocity_transfer(s, rates, weights, gain, feedback):
    if not np.isfinite(feedback) or feedback < 0 or not np.isfinite(gain):
        raise ValueError("Require a finite gain and nonnegative finite feedback.")
    return gain / (1 + feedback * memory(s, rates, weights))


def step_velocity(times, rates, weights, gain, feedback, max_step):
    """Causal mode ODE under unit step forcing. Equals the root impulse response."""
    t = np.asarray(times, dtype=float)
    if t.ndim != 1 or t.size == 0 or not np.all(np.isfinite(t)) or np.any(np.diff(t) <= 0):
        raise ValueError("Supply finite, strictly increasing operational times.")
    velocity_transfer(0., rates, weights, gain, feedback)
    result = np.zeros_like(t)
    result[t == 0] = gain
    positive = t[t > 0]
    if positive.size:
        jacobian = -np.diag(rates) - feedback * np.broadcast_to(weights, (len(rates), len(rates)))
        solution = solve_ivp(lambda u, z: gain - rates*z - feedback*np.dot(weights,z),
                             (0., positive[-1]), np.zeros(len(rates)), t_eval=positive,
                             method="Radau", jac=jacobian, rtol=2e-9, atol=1e-12, max_step=max_step)
        if not solution.success:
            raise RuntimeError(solution.message)
        result[t > 0] = gain - feedback * (weights @ solution.y)
    return result


def modal_response(times, rates, weights, gain, feedback):
    """Invert H(s)/s using the poles of the symmetric finite-rate realization."""
    dc = velocity_transfer(0., rates, weights, gain, feedback)
    b = np.sqrt(weights)
    poles, vectors = eigh(np.diag(rates) + feedback*np.outer(b, b))
    residues = gain * feedback * (vectors.T @ b)**2 / poles
    t = np.asarray(times)
    return np.where(t >= 0, dc + np.exp(-np.maximum(t, 0)[..., None]*poles) @ residues, 0.)


def continuum_root(time, theta, gain, feedback):
    """Mittag-Leffler root response via its positive relaxation spectrum."""
    if not (0 < theta < .5 and np.isfinite(time) and np.isfinite(gain)
            and np.isfinite(feedback) and feedback >= 0):
        raise ValueError("Invalid continuum time, exponent or gain.")
    if time < 0:
        return 0.
    if time == 0 or feedback == 0:
        return gain
    # x = r^theta / g, then y = x/(1+x). The rational measure is regular at both ends.
    c = np.cos(np.pi*theta)
    def density(y):
        x = y/(1-y)
        log_rt = (np.log(x) + np.log(feedback))/theta + np.log(time)
        if log_rt > 7:
            return 0.
        return np.exp(-np.exp(log_rt)) / (y*y + 2*c*y*(1-y) + (1-y)**2)
    value, _ = quad(density, 0., 1., epsabs=1e-11, epsrel=1e-11)
    return gain*np.sin(np.pi*theta)/(np.pi*theta)*value


def shell_response(s, rates, weights, gain, feedback, cutoff):
    """Eliminate fast states, retaining exact memory or its first two moments."""
    fast = rates >= cutoff
    if not np.any(fast) or np.all(fast):
        raise ValueError("The cutoff must leave at least one mode in each sector.")
    r, w = rates[fast], weights[fast]
    slow = memory(s, rates[~fast], weights[~fast])
    moments = [np.sum(w/r**n) for n in (1,2,3)]
    def transfer(shell):
        return gain / (1 + feedback*(slow + shell))
    linear = moments[0] - s*moments[1]
    bound = feedback * abs(s)**2 * moments[2] / abs(1 + feedback*(slow + linear))
    return dict(exact=transfer(memory(s,r,w)), dropped=transfer(0.),
                static=transfer(moments[0]), linear=transfer(linear), bound=bound,
                M0=moments[0], M1=moments[1], M2=moments[2], fast=int(fast.sum()))
