# Figure-Table Manifest

Artefact status: active figure/table manifest

This active manifest lists the preferred current outputs. Superseded v1 and
v2 generated figure artefacts were pruned from the active workspace after
the Matplotlib v3 refinement was accepted.

## Tables

| Output ID | Type | Filename | Script | Config | Run Command | Status |
|---|---|---|---|---|---|---|
| parameter-ranges-v1 | table | tables/parameter-ranges-v1.tex | scripts/01_make_tables.py | config/parameter-ranges-v1.csv | `python scripts/01_make_tables.py` | table draft |
| response-regimes-v1 | table | tables/response-regimes-v1.tex | scripts/01_make_tables.py | functions/response_regimes.py | `python scripts/01_make_tables.py` | table draft |
| profile-definitions-v1 | table | tables/profile-definitions-v1.tex | scripts/01_make_tables.py | config/profile-definitions-v1.json | `python scripts/01_make_tables.py` | table draft |

## Preferred Figures

| Output ID | Type | Filename | Script | Config | Caption | Status |
|---|---|---|---|---|---|---|
| surface-liquidity-only-low-z-v3-pdf | figure | figures/mpl-surface3d-liquidity-only-low-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-low-z-v3.md | preferred figure draft |
| surface-liquidity-only-low-z-v3-png | figure | figures/mpl-surface3d-liquidity-only-low-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-low-z-v3.md | fallback PNG |
| contour-liquidity-only-low-z-v3-pdf | figure | figures/mpl-contour-lines-liquidity-only-low-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-low-z-v3.md | preferred figure draft |
| contour-liquidity-only-low-z-v3-png | figure | figures/mpl-contour-lines-liquidity-only-low-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-low-z-v3.md | fallback PNG |
| surface-liquidity-only-high-z-v3-pdf | figure | figures/mpl-surface3d-liquidity-only-high-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-high-z-v3.md | preferred figure draft |
| surface-liquidity-only-high-z-v3-png | figure | figures/mpl-surface3d-liquidity-only-high-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-high-z-v3.md | fallback PNG |
| contour-liquidity-only-high-z-v3-pdf | figure | figures/mpl-contour-lines-liquidity-only-high-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-high-z-v3.md | preferred figure draft |
| contour-liquidity-only-high-z-v3-png | figure | figures/mpl-contour-lines-liquidity-only-high-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-liquidity-only-high-z-v3.md | fallback PNG |
| surface-resilience-response-only-low-z-v3-pdf | figure | figures/mpl-surface3d-resilience-response-only-low-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-low-z-v3.md | preferred figure draft |
| surface-resilience-response-only-low-z-v3-png | figure | figures/mpl-surface3d-resilience-response-only-low-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-low-z-v3.md | fallback PNG |
| contour-resilience-response-only-low-z-v3-pdf | figure | figures/mpl-contour-lines-resilience-response-only-low-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-low-z-v3.md | preferred figure draft |
| contour-resilience-response-only-low-z-v3-png | figure | figures/mpl-contour-lines-resilience-response-only-low-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-low-z-v3.md | fallback PNG |
| surface-resilience-response-only-high-z-v3-pdf | figure | figures/mpl-surface3d-resilience-response-only-high-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-high-z-v3.md | preferred figure draft |
| surface-resilience-response-only-high-z-v3-png | figure | figures/mpl-surface3d-resilience-response-only-high-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-high-z-v3.md | fallback PNG |
| contour-resilience-response-only-high-z-v3-pdf | figure | figures/mpl-contour-lines-resilience-response-only-high-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-high-z-v3.md | preferred figure draft |
| contour-resilience-response-only-high-z-v3-png | figure | figures/mpl-contour-lines-resilience-response-only-high-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-resilience-response-only-high-z-v3.md | fallback PNG |
| surface-combined-structural-low-z-v3-pdf | figure | figures/mpl-surface3d-combined-structural-low-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-low-z-v3.md | preferred figure draft |
| surface-combined-structural-low-z-v3-png | figure | figures/mpl-surface3d-combined-structural-low-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-low-z-v3.md | fallback PNG |
| contour-combined-structural-low-z-v3-pdf | figure | figures/mpl-contour-lines-combined-structural-low-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-low-z-v3.md | preferred figure draft |
| contour-combined-structural-low-z-v3-png | figure | figures/mpl-contour-lines-combined-structural-low-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-low-z-v3.md | fallback PNG |
| surface-combined-structural-high-z-v3-pdf | figure | figures/mpl-surface3d-combined-structural-high-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-high-z-v3.md | preferred figure draft |
| surface-combined-structural-high-z-v3-png | figure | figures/mpl-surface3d-combined-structural-high-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-high-z-v3.md | fallback PNG |
| contour-combined-structural-high-z-v3-pdf | figure | figures/mpl-contour-lines-combined-structural-high-z-v3.pdf | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-high-z-v3.md | preferred figure draft |
| contour-combined-structural-high-z-v3-png | figure | figures/mpl-contour-lines-combined-structural-high-z-v3.png | scripts/05_generate_matplotlib_figures_v3.py | config/profile-definitions-v1.json | captions/caption-mpl-combined-structural-high-z-v3.md | fallback PNG |

