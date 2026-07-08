"""Run Stage 9 sensitivity, robustness, and edge-case checks."""

from __future__ import annotations

import csv
import json
import sys
from copy import deepcopy
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from functions.structural_profiles import PROFILE_NAMES
from functions.vol_surface_kernel import projected_volatility_surface


CONFIG_PATH = PROJECT_ROOT / "config" / "profile-definitions-v1.json"
DIAGNOSTICS_DIR = PROJECT_ROOT / "diagnostics"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def grid(config, m_points=None, T_points=None):
    state = config["state_axis"]
    maturity = config["maturity_axis"]
    m_n = m_points or state["num_points"]
    T_n = T_points or maturity["num_points"]
    m = np.linspace(state["range"][0], state["range"][1], m_n)
    T = np.linspace(maturity["range"][0], maturity["range"][1], T_n)
    return m, T


def metrics(vol):
    state_spread = np.ptp(vol, axis=1)
    term_spread = np.ptp(vol, axis=0)
    return {
        "vol_min": float(np.min(vol)),
        "vol_max": float(np.max(vol)),
        "vol_mean": float(np.mean(vol)),
        "max_state_spread": float(np.max(state_spread)),
        "max_term_spread": float(np.max(term_spread)),
    }


def status_row(check, status, detail):
    return {"check": check, "status": status, "detail": detail}


def evaluate_all(config, params, m_points=None, T_points=None):
    m, T = grid(config, m_points=m_points, T_points=T_points)
    rows = []
    for profile in PROFILE_NAMES:
        for regime in ("low_z", "high_z"):
            vol = projected_volatility_surface(m, T, params, profile, regime)
            item = {"profile": profile, "regime": regime}
            item.update(metrics(vol))
            rows.append(item)
    return rows


def all_positive_finite(rows, label):
    for row in rows:
        values = [row["vol_min"], row["vol_max"], row["vol_mean"]]
        if not all(np.isfinite(values)) or row["vol_min"] <= 0.0:
            return status_row(label, "failed", f"bad row: {row}")
    return status_row(label, "verified", f"{len(rows)} surfaces positive and finite")


def mean_for(rows, profile, regime):
    for row in rows:
        if row["profile"] == profile and row["regime"] == regime:
            return row["vol_mean"]
    raise KeyError((profile, regime))


def main():
    config = load_config()
    base = config["baseline"]
    diagnostic_rows = []
    summary_rows = []

    baseline_rows = evaluate_all(config, base)
    diagnostic_rows.append(all_positive_finite(baseline_rows, "baseline surfaces positive finite"))
    for row in baseline_rows:
        row = dict(row)
        row["case"] = "baseline"
        summary_rows.append(row)

    edge_cases = {
        "gamma_low": {"gamma": 0.30},
        "gamma_high": {"gamma": 0.80},
        "Delta_low": {"Delta": 0.5},
        "Delta_high": {"Delta": 2.0},
        "A_eff_low": {"A_eff0": 0.5},
        "A_eff_high": {"A_eff0": 2.0},
        "L0_low": {"L0": 0.75},
        "L0_high": {"L0": 1.5},
        "z_high_low": {"z_high0": 5.0},
        "z_high_high": {"z_high0": 25.0},
        "activity_flat": {"a_short": 0.0},
    }

    case_results = {}
    for case, updates in edge_cases.items():
        params = deepcopy(base)
        params.update(updates)
        rows = evaluate_all(config, params)
        case_results[case] = rows
        diagnostic_rows.append(all_positive_finite(rows, f"{case} surfaces positive finite"))
        for row in rows:
            row = dict(row)
            row["case"] = case
            summary_rows.append(row)

    # Directional checks that should hold from the formula.
    base_mean = mean_for(baseline_rows, "combined_structural", "high_z")
    A_low = mean_for(case_results["A_eff_low"], "combined_structural", "high_z")
    A_high = mean_for(case_results["A_eff_high"], "combined_structural", "high_z")
    diagnostic_rows.append(
        status_row(
            "A_eff monotonicity",
            "verified" if A_low < base_mean < A_high else "failed",
            f"A_low={A_low:.6g}, base={base_mean:.6g}, A_high={A_high:.6g}",
        )
    )

    L_low = mean_for(case_results["L0_low"], "combined_structural", "high_z")
    L_high = mean_for(case_results["L0_high"], "combined_structural", "high_z")
    diagnostic_rows.append(
        status_row(
            "L0 inverse monotonicity",
            "verified" if L_high < base_mean < L_low else "failed",
            f"L_high={L_high:.6g}, base={base_mean:.6g}, L_low={L_low:.6g}",
        )
    )

    z_low = mean_for(case_results["z_high_low"], "resilience_response_only", "high_z")
    z_high = mean_for(case_results["z_high_high"], "resilience_response_only", "high_z")
    base_z = mean_for(baseline_rows, "resilience_response_only", "high_z")
    diagnostic_rows.append(
        status_row(
            "high-z resilience monotonicity",
            "verified" if z_high < base_z < z_low else "failed",
            f"z_high={z_high:.6g}, base={base_z:.6g}, z_low={z_low:.6g}",
        )
    )

    low_z_base = mean_for(baseline_rows, "resilience_response_only", "low_z")
    low_z_changed = mean_for(case_results["z_high_high"], "resilience_response_only", "low_z")
    diagnostic_rows.append(
        status_row(
            "low-z independence from high-z marker",
            "verified" if abs(low_z_base - low_z_changed) < 1e-12 else "failed",
            f"baseline={low_z_base:.6g}, changed={low_z_changed:.6g}",
        )
    )

    coarse_rows = evaluate_all(config, base, m_points=61, T_points=48)
    fine_rows = evaluate_all(config, base, m_points=181, T_points=144)
    diagnostic_rows.append(all_positive_finite(coarse_rows, "coarse grid positive finite"))
    diagnostic_rows.append(all_positive_finite(fine_rows, "fine grid positive finite"))
    max_mean_shift = 0.0
    for base_row in baseline_rows:
        profile = base_row["profile"]
        regime = base_row["regime"]
        coarse_mean = mean_for(coarse_rows, profile, regime)
        fine_mean = mean_for(fine_rows, profile, regime)
        denom = max(abs(base_row["vol_mean"]), 1e-12)
        max_mean_shift = max(max_mean_shift, abs(coarse_mean - fine_mean) / denom)
    diagnostic_rows.append(
        status_row(
            "grid mean robustness",
            "verified" if max_mean_shift < 0.01 else "verified with caveat",
            f"max_relative_mean_shift={max_mean_shift:.6g}",
        )
    )

    failed = [row for row in diagnostic_rows if row["status"] == "failed"]
    DIAGNOSTICS_DIR.mkdir(exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)

    diag_csv = DIAGNOSTICS_DIR / "stage09-sensitivity-checks-v1.csv"
    with diag_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["check", "status", "detail"])
        writer.writeheader()
        writer.writerows(diagnostic_rows)

    summary_csv = OUTPUTS_DIR / "stage09-sensitivity-summary-v1.csv"
    fieldnames = [
        "case",
        "profile",
        "regime",
        "vol_min",
        "vol_max",
        "vol_mean",
        "max_state_spread",
        "max_term_spread",
    ]
    with summary_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    diag_md = DIAGNOSTICS_DIR / "stage09-sensitivity-checks-v1.md"
    with diag_md.open("w", encoding="utf-8") as fh:
        fh.write("# Stage 09 Sensitivity And Robustness Checks v1\n\n")
        fh.write("Artefact status: diagnostic output\n\n")
        fh.write(f"Total checks: {len(diagnostic_rows)}\n\n")
        fh.write(f"Failed checks: {len(failed)}\n\n")
        fh.write("| Check | Status | Detail |\n")
        fh.write("|---|---|---|\n")
        for row in diagnostic_rows:
            fh.write(f"| {row['check']} | {row['status']} | {row['detail']} |\n")

    print(f"Wrote {diag_csv}")
    print(f"Wrote {diag_md}")
    print(f"Wrote {summary_csv}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

