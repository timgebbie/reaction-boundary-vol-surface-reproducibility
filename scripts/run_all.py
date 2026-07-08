"""Run the active v1.0 reproducibility route.

This helper executes the four active scripts in the order documented in README.md.
Each script can also be run separately.
"""

from __future__ import annotations

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    "scripts/03_run_diagnostics.py",
    "scripts/01_make_tables.py",
    "scripts/05_generate_matplotlib_figures_v3.py",
    "scripts/06_run_sensitivity_checks.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n>>> python {script}", flush=True)
        runpy.run_path(str(PROJECT_ROOT / script), run_name="__main__")
    print("\nActive v1.0 reproducibility route completed successfully.", flush=True)


if __name__ == "__main__":
    main()
