"""Generate refined, subfigure-ready Stage 8 v2 figures.

This script keeps the v1 combined figures intact and creates separate
surface and contour files for LaTeX subfigures. It writes both PDF and PNG.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
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
RAW_OUTPUTS_DIR = PROJECT_ROOT / "raw-outputs"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CAPTIONS_DIR = PROJECT_ROOT / "captions"
DIAGNOSTICS_DIR = PROJECT_ROOT / "diagnostics" / "render-checks"

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"
pdfmetrics.registerFont(TTFont(FONT_REGULAR, FONT_PATH))
pdfmetrics.registerFont(TTFont(FONT_BOLD, FONT_BOLD_PATH))

PROFILE_LABELS = {
    "liquidity_only": "Liquidity-only",
    "resilience_response_only": "Resilience-response-only",
    "combined_structural": "Combined structural",
}

REGIME_LABELS = {
    "low_z": "low-z response",
    "high_z": "high-z response",
}

SURFACE_STOPS = [
    (68, 1, 84),
    (59, 82, 139),
    (33, 145, 140),
    (94, 201, 98),
    (253, 231, 37),
]


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


def interp_rgb(value, vmin, vmax, stops=SURFACE_STOPS):
    if vmax <= vmin:
        t = 0.5
    else:
        t = float(np.clip((value - vmin) / (vmax - vmin), 0.0, 1.0))
    scaled = t * (len(stops) - 1)
    idx = min(int(np.floor(scaled)), len(stops) - 2)
    frac = scaled - idx
    c0 = np.array(stops[idx], dtype=float)
    c1 = np.array(stops[idx + 1], dtype=float)
    return tuple(np.round((1.0 - frac) * c0 + frac * c1).astype(int))


def gray_rgb(value, vmin, vmax):
    if vmax <= vmin:
        t = 0.5
    else:
        t = float(np.clip((value - vmin) / (vmax - vmin), 0.0, 1.0))
    shade = int(round(245 - 205 * t))
    return shade, shade, shade


def reportlab_color(rgb):
    return colors.Color(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def draw_pdf_text(c, x, y, text, size=9, bold=False):
    c.setFont(FONT_BOLD if bold else FONT_REGULAR, size)
    c.setFillColor(colors.black)
    c.drawString(x, y, text)


def pil_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD_PATH, 28),
        "bold": ImageFont.truetype(FONT_BOLD_PATH, 18),
        "body": ImageFont.truetype(FONT_PATH, 16),
        "small": ImageFont.truetype(FONT_PATH, 13),
    }


def surface_cells(m, T, vol, x0, y0, width, height, vmin, vmax, nx=42, ny=34):
    m_idx = np.linspace(0, len(m) - 1, nx).astype(int)
    t_idx = np.linspace(0, len(T) - 1, ny).astype(int)
    M = m[m_idx]
    TT = T[t_idx]
    Z = vol[np.ix_(t_idx, m_idx)]
    mn, mx = M.min(), M.max()
    tn, tx = TT.min(), TT.max()

    def project(mi, ti, zi):
        m_norm = (mi - mn) / (mx - mn)
        t_norm = (ti - tn) / (tx - tn)
        z_norm = (zi - vmin) / (vmax - vmin)
        px = x0 + 40 + m_norm * (width * 0.60) + t_norm * (width * 0.26)
        py = y0 + 45 + t_norm * (height * 0.22) + z_norm * (height * 0.52)
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
    return cells


def draw_pdf_surface(path, profile, regime, m, T, vol):
    page_w, page_h = landscape(letter)
    c = canvas.Canvas(str(path), pagesize=(page_w, page_h))
    c.setTitle(f"{PROFILE_LABELS[profile]} {REGIME_LABELS[regime]} surface")
    vmin, vmax = float(vol.min()), float(vol.max())
    draw_pdf_text(c, 42, page_h - 38, f"{PROFILE_LABELS[profile]} surface: {REGIME_LABELS[regime]}", 15, True)
    draw_pdf_text(c, 42, page_h - 58, "Projected local volatility; m = log-moneyness ln(x/x0); T = maturity in years", 9)

    x0, y0, width, height = 70, 80, 660, 420
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.1)
    c.rect(x0, y0, width, height, fill=0, stroke=1)
    for _, value, pts in surface_cells(m, T, vol, x0, y0, width, height, vmin, vmax):
        c.setFillColor(reportlab_color(interp_rgb(value, vmin, vmax)))
        c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.20))
        c.setLineWidth(0.12)
        path_obj = c.beginPath()
        path_obj.moveTo(*pts[0])
        for pt in pts[1:]:
            path_obj.lineTo(*pt)
        path_obj.close()
        c.drawPath(path_obj, fill=1, stroke=1)
    draw_pdf_text(c, x0 + 18, y0 + 15, "log-moneyness m = ln(x/x0)", 9)
    draw_pdf_text(c, x0 + width - 95, y0 + 15, "maturity T", 9)
    draw_pdf_text(c, x0 + width - 140, y0 + height - 22, "projected local volatility", 9)
    c.showPage()
    c.save()


def draw_pdf_contour(path, profile, regime, m, T, vol):
    page_w, page_h = landscape(letter)
    c = canvas.Canvas(str(path), pagesize=(page_w, page_h))
    c.setTitle(f"{PROFILE_LABELS[profile]} {REGIME_LABELS[regime]} contour")
    vmin, vmax = float(vol.min()), float(vol.max())
    draw_pdf_text(c, 42, page_h - 38, f"{PROFILE_LABELS[profile]} contour: {REGIME_LABELS[regime]}", 15, True)
    draw_pdf_text(c, 42, page_h - 58, "Black-and-white projection of projected local volatility", 9)

    x0, y0, width, height = 80, 78, 620, 420
    m_idx = np.linspace(0, len(m) - 1, 95).astype(int)
    t_idx = np.linspace(0, len(T) - 1, 72).astype(int)
    Z = vol[np.ix_(t_idx, m_idx)]
    cell_w = width / (len(m_idx) - 1)
    cell_h = height / (len(t_idx) - 1)
    for i in range(len(t_idx) - 1):
        for j in range(len(m_idx) - 1):
            value = float(np.mean(Z[i : i + 2, j : j + 2]))
            col = reportlab_color(gray_rgb(value, vmin, vmax))
            c.setFillColor(col)
            c.setStrokeColor(col)
            c.rect(x0 + j * cell_w, y0 + i * cell_h, cell_w + 0.2, cell_h + 0.2, fill=1, stroke=0)

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.1)
    c.rect(x0, y0, width, height, fill=0, stroke=1)
    draw_pdf_text(c, x0 + width / 2 - 65, y0 - 24, "log-moneyness m = ln(x/x0)", 9)
    draw_pdf_text(c, x0 - 48, y0 + height / 2, "maturity T", 9)
    draw_pdf_text(c, x0 + width + 16, y0 + height - 5, "high", 8)
    draw_pdf_text(c, x0 + width + 16, y0, "low", 8)
    for i in range(32):
        value = vmin + (vmax - vmin) * i / 31
        col = reportlab_color(gray_rgb(value, vmin, vmax))
        c.setFillColor(col)
        c.setStrokeColor(col)
        c.rect(x0 + width + 45, y0 + i * height / 32, 12, height / 32 + 0.4, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.rect(x0 + width + 45, y0, 12, height, fill=0, stroke=1)
    draw_pdf_text(c, x0 + width + 64, y0 + height - 4, f"{vmax:.3g}", 8)
    draw_pdf_text(c, x0 + width + 64, y0 - 2, f"{vmin:.3g}", 8)
    c.showPage()
    c.save()


def draw_png_surface(path, profile, regime, m, T, vol):
    fonts = pil_fonts()
    W, H = 1400, 900
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    draw.text((55, 38), f"{PROFILE_LABELS[profile]} surface: {REGIME_LABELS[regime]}", fill="black", font=fonts["title"])
    draw.text((55, 78), "Projected local volatility; m = log-moneyness ln(x/x0); T = maturity in years", fill="black", font=fonts["body"])
    x0, y0, width, height = 110, 170, 1160, 610
    vmin, vmax = float(vol.min()), float(vol.max())
    draw.rectangle([x0, y0, x0 + width, y0 + height], outline="black", width=3)
    for _, value, pts in surface_cells(m, T, vol, x0, y0, width, height, vmin, vmax, nx=52, ny=42):
        pts_i = [(int(round(x)), int(round(H - y))) for x, y in pts]
        draw.polygon(pts_i, fill=interp_rgb(value, vmin, vmax), outline=(235, 235, 235))
    draw.text((x0 + 20, y0 + height - 28), "log-moneyness m = ln(x/x0)", fill="black", font=fonts["small"])
    draw.text((x0 + width - 120, y0 + height - 28), "maturity T", fill="black", font=fonts["small"])
    draw.text((x0 + width - 225, y0 + 24), "projected local volatility", fill="black", font=fonts["small"])
    img.save(path)


def draw_png_contour(path, profile, regime, m, T, vol):
    fonts = pil_fonts()
    W, H = 1400, 900
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    draw.text((55, 38), f"{PROFILE_LABELS[profile]} contour: {REGIME_LABELS[regime]}", fill="black", font=fonts["title"])
    draw.text((55, 78), "Black-and-white projection of projected local volatility", fill="black", font=fonts["body"])
    x0, y0, width, height = 130, 160, 1040, 610
    vmin, vmax = float(vol.min()), float(vol.max())
    m_idx = np.linspace(0, len(m) - 1, 120).astype(int)
    t_idx = np.linspace(0, len(T) - 1, 90).astype(int)
    Z = vol[np.ix_(t_idx, m_idx)]
    cell_w = width / (len(m_idx) - 1)
    cell_h = height / (len(t_idx) - 1)
    for i in range(len(t_idx) - 1):
        for j in range(len(m_idx) - 1):
            value = float(np.mean(Z[i : i + 2, j : j + 2]))
            x = x0 + j * cell_w
            y = y0 + height - (i + 1) * cell_h
            draw.rectangle([x, y, x + cell_w + 1, y + cell_h + 1], fill=gray_rgb(value, vmin, vmax))
    draw.rectangle([x0, y0, x0 + width, y0 + height], outline="black", width=3)
    draw.text((x0 + width / 2 - 110, y0 + height + 30), "log-moneyness m = ln(x/x0)", fill="black", font=fonts["body"])
    draw.text((x0 - 82, y0 + height / 2), "maturity T", fill="black", font=fonts["body"])
    bx, by, bh = x0 + width + 55, y0, height
    for i in range(70):
        value = vmin + (vmax - vmin) * (69 - i) / 69
        draw.rectangle([bx, by + i * bh / 70, bx + 24, by + (i + 1) * bh / 70 + 1], fill=gray_rgb(value, vmin, vmax))
    draw.rectangle([bx, by, bx + 24, by + bh], outline="black", width=2)
    draw.text((bx + 38, by - 5), f"{vmax:.3g}", fill="black", font=fonts["small"])
    draw.text((bx + 38, by + bh - 12), f"{vmin:.3g}", fill="black", font=fonts["small"])
    img.save(path)


def write_caption(profile, regime):
    sid = surface_id(profile, regime)
    path = CAPTIONS_DIR / f"caption-refined-{sid}-v2.md"
    path.write_text(
        f"# Caption: refined {PROFILE_LABELS[profile]}, {REGIME_LABELS[regime]}\n\n"
        "Artefact status: standalone caption draft\n\n"
        f"Surface files: `figures/surface3d-{sid}-v2.pdf`, `figures/surface3d-{sid}-v2.png`\n\n"
        f"Contour files: `figures/contour-{sid}-v2.pdf`, `figures/contour-{sid}-v2.png`\n\n"
        "These paired subfigure-ready files show the same simulated projected local-volatility "
        "surface. The surface view is boxed for geometric inspection; the contour view is "
        "black-and-white for print-friendly comparison. The state axis is log-moneyness "
        "`m = ln(x/x0)` and the time axis is maturity `T` in years. The figure is a "
        "simulation of the reaction-boundary closure, not an empirical calibration.\n",
        encoding="utf-8",
    )
    return path


def write_summary(profile, regime, m, T, variance, volatility):
    sid = surface_id(profile, regime)
    npz_path = RAW_OUTPUTS_DIR / f"surface-{sid}-v2.npz"
    np.savez_compressed(npz_path, m=m, T=T, variance=variance, volatility=volatility, profile=profile, regime=regime)
    summary_path = OUTPUTS_DIR / f"surface-{sid}-summary-v2.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["profile", "regime", "vol_min", "vol_max", "var_min", "var_max", "m_points", "T_points"],
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


def main():
    for directory in (FIGURES_DIR, RAW_OUTPUTS_DIR, OUTPUTS_DIR, CAPTIONS_DIR, DIAGNOSTICS_DIR):
        directory.mkdir(exist_ok=True)
    config = load_config()
    params = config["baseline"]
    m, T = planned_grid(config)
    manifest_rows = []

    for profile in PROFILE_NAMES:
        for regime in ("low_z", "high_z"):
            sid = surface_id(profile, regime)
            variance = projected_variance_surface(m, T, params, profile, regime)
            volatility = projected_volatility_surface(m, T, params, profile, regime)
            write_summary(profile, regime, m, T, variance, volatility)

            surface_pdf = FIGURES_DIR / f"surface3d-{sid}-v2.pdf"
            contour_pdf = FIGURES_DIR / f"contour-{sid}-v2.pdf"
            surface_png = FIGURES_DIR / f"surface3d-{sid}-v2.png"
            contour_png = FIGURES_DIR / f"contour-{sid}-v2.png"
            draw_pdf_surface(surface_pdf, profile, regime, m, T, volatility)
            draw_pdf_contour(contour_pdf, profile, regime, m, T, volatility)
            draw_png_surface(surface_png, profile, regime, m, T, volatility)
            draw_png_contour(contour_png, profile, regime, m, T, volatility)
            caption_path = write_caption(profile, regime)

            for kind, filename in (
                ("surface", surface_pdf),
                ("surface", surface_png),
                ("contour", contour_pdf),
                ("contour", contour_png),
            ):
                manifest_rows.append(
                    {
                        "output_id": f"{kind}-{sid}-v2",
                        "type": "figure",
                        "filename": str(filename.relative_to(PROJECT_ROOT)),
                        "script": "scripts/04_generate_refined_figures_v2.py",
                        "config": "config/profile-definitions-v1.json",
                        "caption": str(caption_path.relative_to(PROJECT_ROOT)),
                        "status": "refined figure draft",
                    }
                )

    manifest_path = PROJECT_ROOT / "figure-table-manifest-v2-addendum.md"
    with manifest_path.open("w", encoding="utf-8") as fh:
        fh.write("# Figure-Table Manifest v2 Addendum\n\n")
        fh.write("Artefact status: refined figure manifest draft\n\n")
        fh.write("| Output ID | Type | Filename | Script | Config | Caption | Status |\n")
        fh.write("|---|---|---|---|---|---|---|\n")
        for row in manifest_rows:
            fh.write(
                f"| {row['output_id']} | {row['type']} | {row['filename']} | {row['script']} | "
                f"{row['config']} | {row['caption']} | {row['status']} |\n"
            )

    print("Generated refined v2 surface and contour figures.")


if __name__ == "__main__":
    main()

