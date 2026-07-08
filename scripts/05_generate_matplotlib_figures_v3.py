"""Generate Matplotlib v3 figures with boxed 3D surfaces and line contours."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / ".deps"))
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / "diagnostics" / "mpl-cache"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from functions.structural_profiles import PROFILE_NAMES
from functions.vol_surface_kernel import projected_variance_surface, projected_volatility_surface


CONFIG_PATH = PROJECT_ROOT / "config" / "profile-definitions-v1.json"
FIGURES_DIR = PROJECT_ROOT / "figures"
CAPTIONS_DIR = PROJECT_ROOT / "captions"

PROFILE_LABELS = {
    "liquidity_only": "Liquidity-only",
    "resilience_response_only": "Resilience-response-only",
    "combined_structural": "Combined structural",
}

REGIME_LABELS = {
    "low_z": "low-z response",
    "high_z": "high-z response",
}


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def planned_grid(config):
    state = config["state_axis"]
    maturity = config["maturity_axis"]
    m = np.linspace(state["range"][0], state["range"][1], state["num_points"])
    T = np.linspace(maturity["range"][0], maturity["range"][1], maturity["num_points"])
    return m, T


def surface_id(profile, regime):
    return f"{profile}-{regime}".replace("_", "-")


def style_3d_axes(ax):
    ax.view_init(elev=24, azim=-58)
    ax.set_box_aspect((1.25, 1.0, 0.72))
    ax.grid(True, linewidth=0.45, alpha=0.65)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 1))
        axis.pane.set_edgecolor((0, 0, 0, 1))
        axis.line.set_linewidth(1.0)
        axis.line.set_color("black")
    ax.tick_params(axis="both", which="major", labelsize=8, pad=2)
    ax.zaxis.set_tick_params(labelsize=8, pad=2)


def save_surface(profile, regime, m, T, vol):
    sid = surface_id(profile, regime)
    M, TT = np.meshgrid(m, T)
    fig = plt.figure(figsize=(7.0, 5.4))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(
        M,
        TT,
        vol,
        cmap="viridis",
        linewidth=0.18,
        edgecolor=(0.93, 0.93, 0.93, 0.55),
        antialiased=True,
        rcount=70,
        ccount=70,
    )
    style_3d_axes(ax)
    ax.set_title(f"{PROFILE_LABELS[profile]} surface: {REGIME_LABELS[regime]}", fontsize=11, pad=12)
    ax.set_xlabel(r"log-moneyness $m=\ln(x/x_0)$", labelpad=8)
    ax.set_ylabel(r"maturity $T$ (years)", labelpad=8)
    ax.set_zlabel(r"projected local volatility $\sigma_{\mathrm{loc}}$", labelpad=8)
    cbar = fig.colorbar(surf, ax=ax, shrink=0.68, pad=0.08)
    cbar.set_label(r"$\sigma_{\mathrm{loc}}$", fontsize=9)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        path = FIGURES_DIR / f"mpl-surface3d-{sid}-v3.{ext}"
        fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_contour(profile, regime, m, T, vol):
    sid = surface_id(profile, regime)
    M, TT = np.meshgrid(m, T)
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    levels = np.linspace(float(vol.min()), float(vol.max()), 12)
    contours = ax.contour(M, TT, vol, levels=levels, colors="black", linewidths=0.85)
    ax.clabel(contours, inline=True, fontsize=7, fmt="%.2f")
    ax.set_title(f"{PROFILE_LABELS[profile]} contour: {REGIME_LABELS[regime]}", fontsize=11)
    ax.set_xlabel(r"log-moneyness $m=\ln(x/x_0)$")
    ax.set_ylabel(r"maturity $T$ (years)")
    ax.grid(True, color="0.86", linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color("black")
    ax.text(
        0.01,
        0.98,
        r"contours of projected local volatility $\sigma_{\mathrm{loc}}$",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85},
    )
    fig.tight_layout()
    for ext in ("pdf", "png"):
        path = FIGURES_DIR / f"mpl-contour-lines-{sid}-v3.{ext}"
        fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_caption(profile, regime):
    sid = surface_id(profile, regime)
    path = CAPTIONS_DIR / f"caption-mpl-{sid}-v3.md"
    path.write_text(
        f"# Caption: Matplotlib v3 {PROFILE_LABELS[profile]}, {REGIME_LABELS[regime]}\n\n"
        "Artefact status: standalone caption draft\n\n"
        f"Surface files: `figures/mpl-surface3d-{sid}-v3.pdf`, `figures/mpl-surface3d-{sid}-v3.png`\n\n"
        f"Contour files: `figures/mpl-contour-lines-{sid}-v3.pdf`, `figures/mpl-contour-lines-{sid}-v3.png`\n\n"
        "The surface subfigure shows projected local volatility in a boxed 3D axes view. "
        "The contour subfigure shows true black line contours of the same projected local-volatility "
        "surface. The state coordinate is log-moneyness `m = ln(x/x0)` and the time coordinate is "
        "maturity `T` in years. The figure is a simulation of the reaction-boundary closure, not "
        "an empirical calibration.\n",
        encoding="utf-8",
    )


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    CAPTIONS_DIR.mkdir(exist_ok=True)
    config = load_config()
    params = config["baseline"]
    m, T = planned_grid(config)
    manifest_rows = []

    for profile in PROFILE_NAMES:
        for regime in ("low_z", "high_z"):
            sid = surface_id(profile, regime)
            vol = projected_volatility_surface(m, T, params, profile, regime)
            save_surface(profile, regime, m, T, vol)
            save_contour(profile, regime, m, T, vol)
            write_caption(profile, regime)
            for kind, stem in (
                ("surface", f"mpl-surface3d-{sid}-v3"),
                ("contour", f"mpl-contour-lines-{sid}-v3"),
            ):
                for ext in ("pdf", "png"):
                    manifest_rows.append(
                        {
                            "output_id": f"{kind}-{sid}-v3-{ext}",
                            "filename": f"figures/{stem}.{ext}",
                            "caption": f"captions/caption-mpl-{sid}-v3.md",
                        }
                    )

    manifest_path = PROJECT_ROOT / "figure-table-manifest-v3-addendum.md"
    with manifest_path.open("w", encoding="utf-8") as fh:
        fh.write("# Figure-Table Manifest v3 Addendum\n\n")
        fh.write("Artefact status: Matplotlib refined figure manifest draft\n\n")
        fh.write("| Output ID | Filename | Script | Caption | Status |\n")
        fh.write("|---|---|---|---|---|\n")
        for row in manifest_rows:
            fh.write(
                f"| {row['output_id']} | {row['filename']} | "
                f"scripts/05_generate_matplotlib_figures_v3.py | {row['caption']} | refined figure draft |\n"
            )
    print("Generated Matplotlib v3 boxed surfaces and line contours.")


if __name__ == "__main__":
    main()

