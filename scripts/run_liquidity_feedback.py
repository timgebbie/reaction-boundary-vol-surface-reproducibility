"""Compute finite-rate, continuum and fast-shell comparisons in operational time."""

from itertools import product
from pathlib import Path
import sys

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions.liquidity_feedback import (
    continuum_root, modal_response, rate_grid, shell_response, step_velocity, velocity_transfer,
)
from functions.translating_front import aligned_gain
from scripts.run_frozen_response import write_csv

GAIN = aligned_gain()
FEEDBACK = 1.


def frequency_rows():
    rows = []
    for theta, floor, ceiling, count in product((.25, 1/3, .4), (1e-4, 1e-7),
                                               (1e3, 1e6), (48, 96)):
        rates, weights = rate_grid(theta, floor, ceiling, count)
        dc = velocity_transfer(0., rates, weights, GAIN, FEEDBACK)
        for omega in np.geomspace(.01, 1., 17):
            s = 1j * omega
            value = velocity_transfer(s, rates, weights, GAIN, FEEDBACK)
            def integrand(x):
                return np.exp((1-theta)*x) / (s + np.exp(x))
            clipped, _ = quad(integrand, np.log(floor), np.log(ceiling), complex_func=True,
                              epsabs=1e-12, epsrel=1e-12)
            reference = GAIN / (1 + FEEDBACK*np.sin(np.pi*theta)/np.pi*clipped)
            infinite = GAIN * s**theta / (s**theta + FEEDBACK)
            rows.append(dict(theta=theta, floor=floor, ceiling=ceiling, count=count,
                             omega=omega, H_real=value.real, H_imag=value.imag, dc=dc,
                             quadrature_error=abs(value/reference-1),
                             cutoff_error=abs(reference/infinite-1),
                             continuum_error=abs(value/infinite-1)))
    return rows


def time_rows():
    rates, weights = rate_grid(1/3, 1e-6, 1e5, 64)
    times = np.geomspace(.1, 10., 25)
    coarse = step_velocity(times, rates, weights, GAIN, FEEDBACK, .2)
    fine = step_velocity(times, rates, weights, GAIN, FEEDBACK, .1)
    modal = modal_response(times, rates, weights, GAIN, FEEDBACK)
    return [dict(u=u, G_ode=y, G_modal=m, G_continuum=continuum_root(u, 1/3, GAIN, FEEDBACK),
                 step_difference=abs(y-c)) for u, c, y, m in zip(times, coarse, fine, modal)]


def shell_rows():
    rates, weights = rate_grid(1/3, 1e-6, 1e5, 64)
    rows = []
    for cutoff, omega in product((2., 5., 20.), np.geomspace(.001, .2, 25)):
        s = 1j * omega
        full = velocity_transfer(s, rates, weights, GAIN, FEEDBACK)
        result = shell_response(s, rates, weights, GAIN, FEEDBACK, cutoff)
        row = dict(cutoff=cutoff, omega=omega, fast=result['fast'], M0=result['M0'],
                   M1=result['M1'], M2=result['M2'], bound=result['bound'])
        for label in ('exact', 'dropped', 'static', 'linear'):
            row[label+'_error'] = abs(result[label]/full-1)
        rows.append(row)
    return rows


def figure(time, shell):
    with mpl.rc_context({'svg.hashsalt':'reaction-boundary-feedback', 'font.size':9}):
        fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3.35), layout='constrained')
        t = [r['u'] for r in time]
        left.semilogx(t, [r['G_continuum'] for r in time], color='black', label='Continuum')
        left.semilogx(t, [r['G_ode'] for r in time], 'o', ms=3, fillstyle='none', label='Finite rates')
        left.set(xlabel='Operational lag', ylabel='Integrated root response')
        subset = [r for r in shell if r['cutoff'] == 5]
        for key, label in [('dropped', 'Drop fast modes'), ('static','Static memory'),
                           ('linear','First derivative')]:
            right.loglog([r['omega'] for r in subset], [r[key+'_error'] for r in subset], label=label)
        right.set(xlabel='Operational angular frequency', ylabel='Relative transfer error')
        for ax in (left, right):
            ax.grid(alpha=.2)
            ax.legend(frameon=False)
        fig.savefig(ROOT/'figures/v2/liquidity-feedback.svg', metadata={'Date':None})
        plt.close(fig)


if __name__ == '__main__':
    freq, time, shell = frequency_rows(), time_rows(), shell_rows()
    for name, rows in [('feedback-frequency.csv',freq),('feedback-time.csv',time),
                       ('feedback-shell.csv',shell)]:
        write_csv(name, rows)
    figure(time, shell)
