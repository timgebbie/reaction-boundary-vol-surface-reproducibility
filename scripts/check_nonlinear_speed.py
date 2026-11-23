"""Follow up the moving-profile control by refining time at fixed spatial resolution."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from functions.nonlinear_field import evolve, travelling_speed
from scripts.run_frozen_response import write_csv


def speed_refinement():
    forcing = 0.1
    epsilon = np.array([0.0, 0.2, -0.2])
    exact = [travelling_speed(forcing, value) for value in epsilon]
    rows = []
    for dx in (0.1, 0.05):
        for dt in (0.125, 0.0625, 0.03125, 0.015625):
            field, failed, reasons, *_ = evolve(
                np.full((3, 129), forcing),
                np.full(3, 0.3), epsilon, np.full(3, 1e-7),
                half_width=18, dx=dx, dt=dt, nodes=64, feedback=0, burn=0,
            )
            for index, value in enumerate(epsilon):
                speed = (field[index, 32, 0] - field[index, 8, 0]) / 24
                rows.append(dict(dx=dx, dt=dt, epsilon=value, speed=speed,
                                 exact=exact[index], error=speed-exact[index],
                                 failed_at=failed[index], reason=reasons[index]))
    return rows


if __name__ == "__main__":
    write_csv("nonlinear-speed-refinement.csv", speed_refinement())
