"""Measure the input and response exponents independently on a fixed lag window."""

from itertools import product
from pathlib import Path
import sys

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t as student

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions.liquidity_feedback import rate_grid, modal_response
from functions.response_balance import forcing_estimates, response_slopes, root_response
from scripts.run_frozen_response import write_csv
from scripts.run_liquidity_feedback import GAIN

LAGS = np.geomspace(32, 320, 17)
OFFSETS = np.linspace(-np.log(2)/2, np.log(2)/2, 17)
TIMES = (LAGS[:, None] * np.exp(OFFSETS)).ravel()
INVERSION = [(24, 40, 30), (28, 52, 36)]
CASES = {
    "primary": (4., 1e-7, 100., 0.),
    "weaker": (1., 1e-7, 100., 0.),
    "off": (0., 1e-7, 100., 0.),
    "raised_floor": (4., .02, 100., 0.),
    "raised_ceiling": (4., 1e-7, 1000., 0.),
    "linear_shape": (4., 1e-7, 100., .2),
}


def estimate_input(gamma):
    paths, summaries = [], []
    for step in (1., .5):
        estimates = np.array([forcing_estimates(gamma, step, r) for r in range(32)])
        for col, stride in enumerate((1, 2)):
            vals = estimates[:, col]
            paths.extend(dict(gamma_input=gamma, step=step, stride=stride, replicate=r,
                              gamma_hat=v) for r, v in enumerate(vals))
            mean = vals.mean()
            half = student.ppf(1-.05/16, 31)*vals.std(ddof=1)/np.sqrt(32)
            summaries.append(dict(gamma_input=gamma, step=step, stride=stride,
                                  estimate=mean, lo=mean-half, hi=mean+half))
    return paths, summaries


def sweep(gamma, theta, case, forcing):
    g, floor, ceiling, mix = CASES[case]
    refinements = []
    max_modal_error = 0.
    for count, inv in product((64, 128), INVERSION):
        rates, weights = rate_grid(theta, floor, ceiling, count)
        values = root_response(TIMES, rates, weights, GAIN, g, mix, inv)
        if mix == 0:
            exact = modal_response(TIMES, rates, weights, GAIN, g)
            max_modal_error = max(max_modal_error, float(np.max(np.abs(values-exact))))
        grid = values.reshape(len(LAGS), -1)
        for stride in (2, 1):
            refinements.append(response_slopes(grid[:, ::stride], OFFSETS[::stride]))
    all_beta = np.array(refinements)
    beta = all_beta[-1]
    lower = 2*all_beta.min(axis=0) + min(row["lo"] for row in forcing) - 1
    upper = 2*all_beta.max(axis=0) + max(row["hi"] for row in forcing) - 1
    gamma_hat = forcing[2]["estimate"]  # Refined sampling, all band frequencies
    balance = 2*beta+gamma_hat-1
    if not np.all(np.isfinite(all_beta)):
        outcome = "invalid response"
    elif np.all((lower>=-.1) & (upper<=.1)):
        outcome = "compatible"
    elif np.all(lower>.1):
        outcome = "positive offset"
    elif np.all(upper<-.1):
        outcome = "negative offset"
    else:
        outcome = "inconclusive"
    return [dict(gamma_input=gamma, theta=theta, case=case, feedback=g, floor=floor,
                 ceiling=ceiling, shape_weight=mix, lag=lag, root_response=grid[j, 8],
                 beta=beta[j], beta_min=all_beta[:,j].min(), beta_max=all_beta[:,j].max(),
                 gamma_hat=gamma_hat, balance=balance[j], lower=lower[j], upper=upper[j],
                 modal_abs_error=max_modal_error if mix==0 else "", window_result=outcome)
            for j, lag in enumerate(LAGS)]


def make_figure(rows):
    with mpl.rc_context({"svg.hashsalt":"root-response-balance-v140","font.size":9}):
        fig,axes = plt.subplots(1,2,figsize=(8,3.25),layout="constrained", sharey=True)
        for ax, gamma in zip(axes,(.4,.6)):
            ax.axhspan(-.1,.1,color="0.90")
            ax.axhline(0,color="0.45",lw=.7)
            for offset,colour in zip((-.08,0,.08),("#2166ac","black","#b2182b")):
                theta=(1-gamma)/2+offset
                group=[r for r in rows if r["gamma_input"]==gamma and r["theta"]==theta and r["case"]=="primary"]
                ax.semilogx(LAGS,[r["balance"] for r in group],color=colour,label=f"θ = {theta:.2f}")
                ax.fill_between(LAGS,[r["lower"] for r in group],[r["upper"] for r in group],
                                color=colour,alpha=.15)
            ax.set(title=f"Input γ = {gamma:.1f}",xlabel="Operational lag")
            ax.legend(frameon=False)
        axes[0].set_ylabel("Response-balance residual")
        fig.savefig(ROOT/"figures/v2/response-balance.svg",metadata={"Date":None})
        plt.close(fig)


if __name__ == "__main__":
    paths, means, rows = [], [], []
    for gamma in (.4,.6):
        reps, summary = estimate_input(gamma)
        paths.extend(reps)
        means.extend(summary)
        for offset, case in product((-.08,0.,.08),CASES):
            rows.extend(sweep(gamma,(1-gamma)/2+offset,case,summary))
    write_csv("balance-forcing-paths.csv",paths)
    write_csv("balance-forcing-estimates.csv",means)
    write_csv("balance-window.csv",rows)
    make_figure(rows)
