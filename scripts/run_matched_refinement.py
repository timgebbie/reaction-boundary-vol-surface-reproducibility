"""Refine the nonlinear zero on common driving paths and measure prediction error."""
from pathlib import Path
from itertools import product
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions.nonlinear_field import evolve
from scripts.run_frozen_response import write_csv
from scripts.run_nonlinear_field import CASES, input_path, increment_stats
from scripts.run_root_variance import SUPPORT, LAGS, OFFSETS
from functions.response_balance import slope

GRIDS = {"previous": (.1, .125), "half_time": (.1, .0625),
         "quarter_time": (.1, .03125), "half_space_time": (.05, .0625),
         "joint": (.05, .03125)}


def history_scores(paths, age, first_gap, second_gap):
    """Predict a new increment on held-out paths from displacements since an origin."""
    a, b, c = age, age + first_gap, age + first_gap + second_gap
    size = paths.shape[1] - c
    origin = paths[:, :size]
    past = paths[:, a:a+size] - origin
    present = paths[:, b:b+size] - origin
    target = paths[:, c:c+size] - paths[:, b:b+size]
    data = np.stack([present, past], axis=-1)
    errors = np.zeros(3)
    for held in range(len(paths)):
        train = np.arange(len(paths)) != held
        features = data[train].reshape(-1, 2)
        centre = features.mean(axis=0)
        y = target[train].ravel()
        intercept = np.mean(y)
        for k in (0, 1, 2):
            coef = np.linalg.lstsq((features-centre)[:, :k], y-intercept, rcond=None)[0]
            pred = intercept + (data[held]-centre)[:, :k] @ coef
            errors[k] += np.sum((target[held]-pred)**2)
    return errors / target.size


def main():
    cfg = list(product((.4, .6), range(4), CASES))
    force = np.stack([input_path(g, path) for g, path, _ in cfg])
    theta = np.array([(1-g)/2 for g, _, _ in cfg])
    eps = np.array([case[1] for _, _, case in cfg])
    floor = np.array([case[2] for _, _, case in cfg])
    fields, rows, scores, variances = {}, [], [], []
    for grid, (dx, dt) in GRIDS.items():
        values, failure, reason, *_ = evolve(force, theta, eps, floor,
                         half_width=18, dx=dx, dt=dt, nodes=64)
        fields[grid] = values[:, :, 0]
        for g, case in product((.4,.6), CASES):
            ids = [i for i,(gamma,_,control) in enumerate(cfg) if gamma==g and control==case]
            valid = np.isnan(failure[ids]).all()
            moments = (np.mean([increment_stats(values[k,256:], SUPPORT) for k in ids], axis=0)
                       if valid else np.full((*SUPPORT.shape,4), np.nan))
            fitted = slope(OFFSETS, np.log(moments[:,:,0]))
            for j, lag in enumerate(LAGS):
                vy, vq, vx, cross = moments[j,len(OFFSETS)//2]
                variances.append(dict(grid=grid, gamma=g, case=case[0], lag=lag, complete=valid,
                                      Vy=vy, Vq=vq, Vxi=vx, C=cross, slope=fitted[j], rate=vy/lag,
                                      identity_error=abs(vy-vq-vx-2*cross)/vy))
        for k, (g, rep, case) in enumerate(cfg):
            rows.append(dict(grid=grid, gamma=g, path=rep, case=case[0],
                             failed_at=failure[k], reason=reason[k]))
    for i, row in enumerate(rows):
        k = i % len(cfg)
        grid = row["grid"]
        error = np.max(np.abs(fields[grid][k] - fields["joint"][k]))
        previous = {"half_time":"previous","quarter_time":"half_time",
                    "joint":"half_space_time"}.get(grid)
        row.update(error_to_joint=error, tolerance=.05 if grid=="previous" else .03,
                   previous_time_difference=(np.max(np.abs(fields[grid][k]-fields[previous][k]))
                                             if previous else np.nan))
    write_csv("matched-field-variance.csv", variances)
    write_csv("matched-field-refinement.csv", rows)
    for g, case in product((.4,.6), CASES):
        ids = [i for i,(gamma,_,control) in enumerate(cfg) if gamma==g and control==case]
        data = fields["joint"][ids,256:]
        for age, left, right in product((32,80,160), repeat=3):
            valid = np.isfinite(data).all()
            mse = history_scores(data, age, left, right) if valid else np.full(3,np.nan)
            scores.append(dict(gamma=g, case=case[0], age=age, gap1=left, gap2=right,
                               complete=valid, mse_mean=mse[0], mse_present=mse[1],
                               mse_history=mse[2], history_gain=1-mse[2]/mse[1]))
    write_csv("matched-field-history.csv", scores)


if __name__ == "__main__":
    main()
