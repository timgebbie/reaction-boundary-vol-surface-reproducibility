"""Reproduce the W01 frozen-response comparison and crossover figure."""

import csv
from itertools import product
from pathlib import Path
import sys

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions.frozen_response import crossover, frozen_variance, time_covariance_check
from functions.response_regimes import f_high_z, f_low_z


def write_csv(name, rows):
    path = ROOT / "outputs" / "v2" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def compare_domains():
    rows = []
    for gamma, nu, tau0 in product((.3, .55, .8), (.25, 2.), (.001, .08)):
        for delta in (.01 * tau0, .02 / nu, 1 / nu, 50 / nu):
            args = (gamma, nu, tau0, delta)
            spectral = frozen_variance(*args)
            refined = frozen_variance(*args, tol=1e-10, rate_order=128)
            direct, level = time_covariance_check(*args)
            direct_fine, level_fine = time_covariance_check(*args, tol=1e-10)
            rows.append(dict(gamma=gamma, nu=nu, tau0=tau0, delta=delta, z=nu*delta,
                             V_spectral=spectral, V_time=direct, V_level=level,
                             variance_rate=spectral/delta,
                             relative_domain_error=abs(spectral/direct-1),
                             spectral_refinement=abs(spectral/refined-1),
                             time_refinement=abs(direct/direct_fine-1),
                             level_refinement=abs(level/level_fine-1),
                             conditional_ratio_at_y0=1-spectral/(4*level),
                             conditional_ratio_at_y2sd=1+3*spectral/(4*level)))
    return rows


def crossover_figure():
    gamma = .5
    z = np.logspace(-6, 6, 121)
    curves = {"F_zero_cutoff": np.array([crossover(gamma, x) for x in z])}
    for label, tau0 in (("F_cutoff_1e-8", 1e-8), ("F_cutoff_1e-2", 1e-2)):
        curves[label] = np.array([frozen_variance(gamma, 1., tau0, x) / x**(1-gamma)
                                  for x in z])
    curves["F_low_asymptote"] = np.full_like(z, f_low_z(gamma))
    curves["F_high_asymptote"] = f_high_z(gamma, z)
    # Central log differences on the fine grid; export every second sample.
    fine_z = np.logspace(-6, 6, 241)
    fine_f = np.array([crossover(gamma, x) for x in fine_z])
    chi = gamma - np.gradient(np.log(fine_f), np.log(fine_z), edge_order=2)[::2]
    coarse_chi = gamma - np.gradient(np.log(curves["F_zero_cutoff"]), np.log(z), edge_order=2)
    curves["chi_zero_cutoff"] = chi
    curves["chi_grid_difference"] = abs(chi - coarse_chi)
    write_csv("response-crossover.csv",
              [dict(z=x, **{k: v[i] for k, v in curves.items()}) for i, x in enumerate(z)])
    with mpl.rc_context({"svg.hashsalt": "reaction-boundary-W01", "font.size": 10}):
        fig, (ax, slope_ax) = plt.subplots(2, 1, sharex=True, figsize=(7.1, 6.2),
                                          height_ratios=(2, 1), layout="constrained")
        ax.loglog(z, curves["F_zero_cutoff"], color="#24334a", lw=2, label="Zero-cutoff crossover")
        for label, color, expn in (("F_cutoff_1e-8", "#167a74", -8), ("F_cutoff_1e-2", "#ba542e", -2)):
            ax.loglog(z, curves[label], color=color, label=rf"Finite cutoff, $\nu\tau_0=10^{{{expn}}}$")
        ax.loglog(z[z<=1], curves["F_low_asymptote"][z<=1], "--", color="#626573", label="Low- and high-$z$ asymptotes")
        ax.loglog(z[z>=1], curves["F_high_asymptote"][z>=1], "--", color="#626573")
        ax.set(ylabel=r"Scaled variance $V_\Delta / \Delta^{1-\gamma}$",
               title=r"Frozen tangent response, $\gamma=1/2$")
        ax.legend(frameon=False)
        ax.grid(which="major", alpha=.18)
        slope_ax.semilogx(z, chi, color="#24334a")
        slope_ax.set(xlabel=r"Operational lag $z=\nu\Delta$", ylabel=r"Rate exponent $\chi_\gamma$",
                     yticks=(.5, .75, 1.))
        slope_ax.grid(which="major", alpha=.18)
        path = ROOT / "figures/v2/response-crossover.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, metadata={"Date": None})
        plt.close(fig)


if __name__ == "__main__":
    comparison = compare_domains()
    write_csv("frozen-variance-checks.csv", comparison)
    for field in ("relative_domain_error", "spectral_refinement", "time_refinement", "level_refinement"):
        print(f"{field}: {max(row[field] for row in comparison):.3g}")
    crossover_figure()
