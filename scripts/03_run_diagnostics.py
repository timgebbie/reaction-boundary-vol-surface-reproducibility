"""Run Stage 7 diagnostics for the reaction-boundary surface helpers."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from functions.response_regimes import f_high_z, f_low_z
from functions.structural_profiles import PROFILE_NAMES, profile_components
from functions.vol_surface_kernel import (
    projected_variance_surface,
    projected_volatility_surface,
)


CONFIG_PATH = PROJECT_ROOT / "config" / "profile-definitions-v1.json"
DIAGNOSTICS_DIR = PROJECT_ROOT / "diagnostics"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def planned_grid(config):
    state = config["state_axis"]
    maturity = config["maturity_axis"]
    m = np.linspace(state["range"][0], state["range"][1], state["num_points"])
    T = np.linspace(maturity["range"][0], maturity["range"][1], maturity["num_points"])
    return m, T


def status_row(check, status, detail):
    return {"check": check, "status": status, "detail": detail}


def is_positive_finite(name, values):
    arr = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(arr)):
        return status_row(name, "failed", "non-finite values detected")
    if not np.all(arr > 0.0):
        return status_row(name, "failed", "non-positive values detected")
    return status_row(name, "verified", f"min={arr.min():.6g}, max={arr.max():.6g}")


def main():
    config = load_config()
    params = config["baseline"]
    m, T = planned_grid(config)
    rows = []

    gamma = params["gamma"]
    z_probe = np.array([0.01, 0.05, 0.1, 5.0, 10.0, 25.0])

    rows.append(is_positive_finite("low-z response positive finite", f_low_z(gamma)))
    rows.append(is_positive_finite("high-z response positive finite", f_high_z(gamma, z_probe)))

    low_a = f_low_z(gamma)
    low_b = f_low_z(gamma)
    if np.allclose(low_a, low_b):
        rows.append(status_row("low-z branch independent of z", "verified", "low-z helper takes gamma only"))
    else:
        rows.append(status_row("low-z branch independent of z", "failed", "unexpected low-z variation"))

    high_values = f_high_z(gamma, z_probe)
    if np.all(np.diff(high_values) < 0.0):
        rows.append(
            status_row(
                "high-z response decreases with z",
                "verified",
                f"first={high_values[0]:.6g}, last={high_values[-1]:.6g}",
            )
        )
    else:
        rows.append(status_row("high-z response decreases with z", "failed", "not monotone decreasing"))

    regimes = ("low_z", "high_z")
    for profile_name in PROFILE_NAMES:
        for regime in regimes:
            components = profile_components(profile_name, m, params, regime)
            for component_name, values in components.items():
                rows.append(
                    is_positive_finite(
                        f"{profile_name}/{regime}/{component_name} positive finite",
                        values,
                    )
                )

            variance = projected_variance_surface(m, T, params, profile_name, regime)
            volatility = projected_volatility_surface(m, T, params, profile_name, regime)
            rows.append(is_positive_finite(f"{profile_name}/{regime} variance positive finite", variance))
            rows.append(is_positive_finite(f"{profile_name}/{regime} volatility positive finite", volatility))

            if variance.shape == (len(T), len(m)):
                rows.append(
                    status_row(
                        f"{profile_name}/{regime} variance shape",
                        "verified",
                        f"shape={variance.shape}",
                    )
                )
            else:
                rows.append(
                    status_row(
                        f"{profile_name}/{regime} variance shape",
                        "failed",
                        f"shape={variance.shape}",
                    )
                )

    flat_params = dict(params)
    flat_params.update({"L_skew": 0.0, "L_smile": 0.0, "nu_skew": 0.0, "A_stress": 0.0})
    flat_variance = projected_variance_surface(m, T, flat_params, "combined_structural", "high_z")
    max_state_spread = np.max(np.ptp(flat_variance, axis=1))
    if max_state_spread < 1e-12:
        rows.append(
            status_row(
                "homogeneous baseline state-flat",
                "verified",
                f"max_state_spread={max_state_spread:.3g}",
            )
        )
    else:
        rows.append(
            status_row(
                "homogeneous baseline state-flat",
                "failed",
                f"max_state_spread={max_state_spread:.6g}",
            )
        )

    resilience_low = projected_variance_surface(m, T, params, "resilience_response_only", "low_z")
    resilience_high = projected_variance_surface(m, T, params, "resilience_response_only", "high_z")
    low_spread = np.max(np.ptp(resilience_low, axis=1))
    high_spread = np.max(np.ptp(resilience_high, axis=1))
    if low_spread < 1e-12 and high_spread > 1e-8:
        rows.append(
            status_row(
                "resilience-only low/high contrast",
                "verified",
                f"low_spread={low_spread:.3g}, high_spread={high_spread:.6g}",
            )
        )
    else:
        rows.append(
            status_row(
                "resilience-only low/high contrast",
                "failed",
                f"low_spread={low_spread:.6g}, high_spread={high_spread:.6g}",
            )
        )

    DIAGNOSTICS_DIR.mkdir(exist_ok=True)
    csv_path = DIAGNOSTICS_DIR / "stage07-diagnostics-v1.csv"
    md_path = DIAGNOSTICS_DIR / "stage07-diagnostics-v1.md"

    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)

    failed = [row for row in rows if row["status"] != "verified"]
    with md_path.open("w", encoding="utf-8") as fh:
        fh.write("# Stage 07 Diagnostics v1\n\n")
        fh.write("Artefact status: diagnostic output\n\n")
        fh.write(f"Total checks: {len(rows)}\n\n")
        fh.write(f"Verified checks: {len(rows) - len(failed)}\n\n")
        fh.write(f"Failed checks: {len(failed)}\n\n")
        fh.write("| Check | Status | Detail |\n")
        fh.write("|---|---|---|\n")
        for row in rows:
            fh.write(f"| {row['check']} | {row['status']} | {row['detail']} |\n")

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
