"""Generate Stage 8 surface figures, raw outputs, captions, and provenance.

The runtime does not assume Matplotlib. Figures are rendered directly as
vector PDFs with ReportLab.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from functions.structural_profiles import PROFILE_NAMES
from functions.vol_surface_kernel import projected_variance_surface, projected_volatility_surface


CONFIG_PATH = PROJECT_ROOT / "config" / "profile-definitions-v1.json"
FIGURES_DIR = PROJECT_ROOT / "figures"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
RAW_OUTPUTS_DIR = PROJECT_ROOT / "raw-outputs"
CAPTIONS_DIR = PROJECT_ROOT / "captions"
DIAGNOSTICS_DIR = PROJECT_ROOT / "diagnostics"


PROFILE_LABELS = {
    "liquidity_only": "Liquidity-only",
    "resilience_response_only": "Resilience-response-only",
    "combined_structural": "Combined structural",
}

REGIME_LABELS = {
    "low_z": "low-z response",
    "high_z": "high-z response",
}

VIRIDIS_STOPS = [
    (68, 1, 84),
    (59, 82, 139),
    (33, 145, 140),
    (94, 201, 98),
    (253, 231, 37),
]

FONT_REGULAR = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"
pdfmetrics.registerFont(TTFont(FONT_REGULAR, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BOLD, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


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


def color_for(value, vmin, vmax):
    if vmax <= vmin:
        t = 0.5
    else:
        t = float(np.clip((value - vmin) / (vmax - vmin), 0.0, 1.0))
    scaled = t * (len(VIRIDIS_STOPS) - 1)
    idx = min(int(np.floor(scaled)), len(VIRIDIS_STOPS) - 2)
    frac = scaled - idx
    c0 = np.array(VIRIDIS_STOPS[idx], dtype=float)
    c1 = np.array(VIRIDIS_STOPS[idx + 1], dtype=float)
    rgb = np.round((1.0 - frac) * c0 + frac * c1).astype(int)
    return colors.Color(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def draw_text(c, x, y, text, size=9, bold=False):
    c.setFont(FONT_BOLD if bold else FONT_REGULAR, size)
    c.setFillColor(colors.black)
    c.drawString(x, y, text)


def draw_colorbar(c, x, y, height, vmin, vmax):
    steps = 40
    for i in range(steps):
        val = vmin + (vmax - vmin) * i / max(1, steps - 1)
        c.setFillColor(color_for(val, vmin, vmax))
        c.setStrokeColor(color_for(val, vmin, vmax))
        c.rect(x, y + height * i / steps, 10, height / steps + 0.5, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.rect(x, y, 10, height, fill=0, stroke=1)
    draw_text(c, x + 15, y - 1, f"{vmin:.3g}", 7)
    draw_text(c, x + 15, y + height - 4, f"{vmax:.3g}", 7)


def render_surface_panel(c, x0, y0, width, height, m, T, vol, vmin, vmax):
    m_idx = np.linspace(0, len(m) - 1, 34).astype(int)
    t_idx = np.linspace(0, len(T) - 1, 28).astype(int)
    M = m[m_idx]
    TT = T[t_idx]
    Z = vol[np.ix_(t_idx, m_idx)]
    mn, mx = M.min(), M.max()
    tn, tx = TT.min(), TT.max()

    def project(mi, ti, zi):
        m_norm = (mi - mn) / (mx - mn)
        t_norm = (ti - tn) / (tx - tn)
        z_norm = (zi - vmin) / (vmax - vmin)
        px = x0 + 28 + m_norm * (width * 0.62) + t_norm * (width * 0.26)
        py = y0 + 35 + t_norm * (height * 0.24) + z_norm * (height * 0.48)
        return px, py

    cells = []
    for i in range(len(t_idx) - 1):
        for j in range(len(m_idx) - 1):
            pts = [
                project(M[j], TT[i], Z[i, j]),
                project(M[j + 1], TT[i], Z[i, j + 1]),
                project(M[j + 1], TT[i + 1], Z[i + 1, j + 1]),
                project(M[j], TT[i + 1], Z[i + 1, j]),
            ]
            value = float(np.mean(Z[i : i + 2, j : j + 2]))
            cells.append((i + j, value, pts))
    cells.sort(key=lambda item: item[0])
    for _, value, pts in cells:
        c.setFillColor(color_for(value, vmin, vmax))
        c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.18))
        c.setLineWidth(0.15)
        path = c.beginPath()
        path.moveTo(*pts[0])
        for pt in pts[1:]:
            path.lineTo(*pt)
        path.close()
        c.drawPath(path, fill=1, stroke=1)

    c.setStrokeColor(colors.black)
    c.setLineWidth(0.6)
    c.rect(x0, y0, width, height, fill=0, stroke=1)
    draw_text(c, x0 + 8, y0 + height - 15, "Surface panel", 9, True)
    draw_text(c, x0 + 8, y0 + 8, "m = ln(x/x0)", 7)
    draw_text(c, x0 + width - 58, y0 + 8, "T", 7)
    draw_text(c, x0 + width - 70, y0 + height - 18, "projected vol", 7)


def render_contour_panel(c, x0, y0, width, height, m, T, vol, vmin, vmax):
    m_idx = np.linspace(0, len(m) - 1, 70).astype(int)
    t_idx = np.linspace(0, len(T) - 1, 54).astype(int)
    Z = vol[np.ix_(t_idx, m_idx)]
    cell_w = width / (len(m_idx) - 1)
    cell_h = height / (len(t_idx) - 1)
    for i in range(len(t_idx) - 1):
        for j in range(len(m_idx) - 1):
            value = float(np.mean(Z[i : i + 2, j : j + 2]))
            c.setFillColor(color_for(value, vmin, vmax))
            c.setStrokeColor(color_for(value, vmin, vmax))
            c.rect(x0 + j * cell_w, y0 + i * cell_h, cell_w + 0.2, cell_h + 0.2, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.6)
    c.rect(x0, y0, width, height, fill=0, stroke=1)
    draw_text(c, x0 + 8, y0 + height - 15, "Filled contour projection", 9, True)
    draw_text(c, x0 + width / 2 - 30, y0 - 14, "ln-moneyness m", 8)
    draw_text(c, x0 - 24, y0 + height / 2, "T", 8)


def caption_text(profile, regime, figure_file, output_file):
    profile_label = PROFILE_LABELS[profile]
    regime_label = REGIME_LABELS[regime]
    return (
        f"# Caption: {profile_label}, {regime_label}\n\n"
        "Artefact status: standalone caption draft\n\n"
        f"Figure file: `{figure_file}`\n\n"
        f"Raw output file: `{output_file}`\n\n"
        f"This figure shows the simulated local-volatility surface for the "
        f"`{profile}` structural profile under the `{regime}` asymptotic "
        "response regime. The left panel is a surface-style projection over "
        "log-moneyness `m = log(x/x0)` and maturity `T`; the right panel is "
        "the filled contour projection of the same simulated surface. The "
        "plotted quantity is local volatility, obtained by taking the square "
        "root of the projected local variance generated from the main "
        "reaction-boundary closure. The surface is a mechanism illustration, "
        "not an empirical calibration or validation.\n"
    )


def write_npz_and_summary(profile, regime, m, T, variance, volatility):
    sid = surface_id(profile, regime)
    npz_path = RAW_OUTPUTS_DIR / f"surface-{sid}-v1.npz"
    summary_path = OUTPUTS_DIR / f"surface-{sid}-summary-v1.csv"
    np.savez_compressed(
        npz_path,
        m=m,
        T=T,
        variance=variance,
        volatility=volatility,
        profile=profile,
        regime=regime,
    )
    with summary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "profile",
                "regime",
                "vol_min",
                "vol_max",
                "var_min",
                "var_max",
                "m_points",
                "T_points",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "profile": profile,
                "regime": regime,
                "vol_min": f"{volatility.min():.10g}",
                "vol_max": f"{volatility.max():.10g}",
                "var_min": f"{variance.min():.10g}",
                "var_max": f"{variance.max():.10g}",
                "m_points": len(m),
                "T_points": len(T),
            }
        )
    return npz_path, summary_path


def make_figure(profile, regime, m, T, volatility):
    sid = surface_id(profile, regime)
    fig_path = FIGURES_DIR / f"surface-{sid}-v1.pdf"
    page_w, page_h = landscape(letter)
    c = canvas.Canvas(str(fig_path), pagesize=(page_w, page_h))
    c.setTitle(f"{PROFILE_LABELS[profile]} {REGIME_LABELS[regime]}")

    vmin = float(np.min(volatility))
    vmax = float(np.max(volatility))
    draw_text(c, 36, page_h - 32, f"{PROFILE_LABELS[profile]}: {REGIME_LABELS[regime]}", 13, True)
    draw_text(c, 36, page_h - 49, "Simulated projected vol from the reaction-boundary closure", 9)

    render_surface_panel(c, 38, 85, 330, 240, m, T, volatility, vmin, vmax)
    render_contour_panel(c, 420, 105, 265, 205, m, T, volatility, vmin, vmax)
    draw_colorbar(c, 705, 120, 170, vmin, vmax)
    draw_text(c, 692, 300, "projected vol", 7)

    c.showPage()
    c.save()
    return fig_path


def main():
    for directory in (FIGURES_DIR, OUTPUTS_DIR, RAW_OUTPUTS_DIR, CAPTIONS_DIR, DIAGNOSTICS_DIR):
        directory.mkdir(exist_ok=True)

    config = load_config()
    params = config["baseline"]
    m, T = planned_grid(config)
    manifest_rows = [
        {
            "output_id": "parameter-ranges-v1",
            "type": "table",
            "final_filename": "tables/parameter-ranges-v1.tex",
            "script": "scripts/01_make_tables.py",
            "config": "config/parameter-ranges-v1.csv",
            "run_command": "python scripts/01_make_tables.py",
            "caption": "embedded in standalone table",
            "status": "table draft",
        },
        {
            "output_id": "response-regimes-v1",
            "type": "table",
            "final_filename": "tables/response-regimes-v1.tex",
            "script": "scripts/01_make_tables.py",
            "config": "functions/response_regimes.py",
            "run_command": "python scripts/01_make_tables.py",
            "caption": "embedded in standalone table",
            "status": "table draft",
        },
        {
            "output_id": "profile-definitions-v1",
            "type": "table",
            "final_filename": "tables/profile-definitions-v1.tex",
            "script": "scripts/01_make_tables.py",
            "config": "config/profile-definitions-v1.json",
            "run_command": "python scripts/01_make_tables.py",
            "caption": "embedded in standalone table",
            "status": "table draft",
        },
    ]
    provenance_rows = []

    for profile in PROFILE_NAMES:
        for regime in ("low_z", "high_z"):
            sid = surface_id(profile, regime)
            variance = projected_variance_surface(m, T, params, profile, regime)
            volatility = projected_volatility_surface(m, T, params, profile, regime)
            npz_path, summary_path = write_npz_and_summary(profile, regime, m, T, variance, volatility)
            figure_path = make_figure(profile, regime, m, T, volatility)
            caption_path = CAPTIONS_DIR / f"caption-surface-{sid}-v1.md"
            caption_path.write_text(
                caption_text(
                    profile,
                    regime,
                    figure_path.relative_to(PROJECT_ROOT),
                    npz_path.relative_to(PROJECT_ROOT),
                ),
                encoding="utf-8",
            )

            manifest_rows.append(
                {
                    "output_id": sid,
                    "type": "figure",
                    "final_filename": str(figure_path.relative_to(PROJECT_ROOT)),
                    "script": "scripts/02_generate_surfaces.py",
                    "config": "config/profile-definitions-v1.json",
                    "run_command": "python scripts/02_generate_surfaces.py",
                    "caption": str(caption_path.relative_to(PROJECT_ROOT)),
                    "status": "figure draft",
                }
            )
            provenance_rows.append(
                {
                    "output_id": sid,
                    "profile": profile,
                    "regime": regime,
                    "figure": str(figure_path.relative_to(PROJECT_ROOT)),
                    "raw_output": str(npz_path.relative_to(PROJECT_ROOT)),
                    "summary_output": str(summary_path.relative_to(PROJECT_ROOT)),
                    "caption": str(caption_path.relative_to(PROJECT_ROOT)),
                    "diagnostic_status": "Stage 7 diagnostics verified",
                    "interpretation_status": "not interpreted",
                }
            )

    manifest_path = PROJECT_ROOT / "figure-table-manifest.md"
    with manifest_path.open("w", encoding="utf-8") as fh:
        fh.write("# Figure-Table Manifest\n\n")
        fh.write("Artefact status: figure/table manifest draft\n\n")
        fh.write("| Output ID | Type | Filename | Script | Config | Run Command | Caption | Status |\n")
        fh.write("|---|---|---|---|---|---|---|---|\n")
        for row in manifest_rows:
            fh.write(
                f"| {row['output_id']} | {row['type']} | {row['final_filename']} | "
                f"{row['script']} | {row['config']} | `{row['run_command']}` | "
                f"{row['caption']} | {row['status']} |\n"
            )

    provenance_path = PROJECT_ROOT / "figure-table-provenance-register.csv"
    with provenance_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "output_id",
                "profile",
                "regime",
                "figure",
                "raw_output",
                "summary_output",
                "caption",
                "diagnostic_status",
                "interpretation_status",
            ],
        )
        writer.writeheader()
        writer.writerows(provenance_rows)

    print("Generated Stage 8 surfaces, raw outputs, captions, manifest, and provenance.")


if __name__ == "__main__":
    main()
