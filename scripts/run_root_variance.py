"""Independent aligned-root variance at the response experiment's fixed lags."""

from pathlib import Path
import sys
import csv

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from functions.liquidity_feedback import rate_grid, velocity_transfer
from functions.root_variance import (field_zeros, global_bracket_check, periodic_variances,
                                     predicted_variance, variance_intervals)
from scripts.run_frozen_response import write_csv
from scripts.run_liquidity_feedback import GAIN
from scripts.run_response_balance import LAGS

OFFSETS = np.linspace(-np.log(2)/2,np.log(2)/2,9)
SUPPORT = LAGS[:,None]*np.exp(OFFSETS)
DESIGNS = [(65536,1.,.125),(65536,.5,.0625),(131072,1.,.0625)]
FAMILY_SIZE = 3*17*10*3


def phase_filter(omega,theta,feedback,floor,nodes):
    rates,weights = rate_grid(theta,floor,100.,nodes)
    z = np.zeros(omega.shape,dtype=complex)
    for start in range(1,len(omega)-1,2048):
        end = min(start+2048,len(omega)-1)
        s = 1j*omega[start:end]
        z[start:end] = velocity_transfer(s,rates,weights,GAIN,feedback)/s
    return z


def run_design(gamma,theta,case,design):
    duration,h,dx = design
    n = int(duration/h)
    omega = 2*np.pi*np.fft.rfftfreq(n,h)
    input_power = np.zeros_like(omega)
    input_power[1:-1] = (2*np.sin(omega[1:-1]*h/2)/h)**(gamma-1)
    feedback = 0. if case=="off" else 4.
    floor = .02 if case=="raised_floor" else 1e-7
    filt = phase_filter(omega,theta,feedback,floor,128)
    predicted = predicted_variance(input_power*abs(filt)**2,omega,h,n,LAGS)
    coarse_filter = phase_filter(omega,theta,feedback,floor,64)
    coarse = predicted_variance(input_power*abs(coarse_filter)**2,omega,h,n,LAGS)
    variance, audit, path_rows = [],[],[]
    for replicate in range(32):
        rng = np.random.default_rng([1500,round(100*gamma),round(2*h),duration,replicate])
        noise = np.fft.rfft(rng.standard_normal(n))
        phase = np.fft.irfft(noise*np.sqrt(input_power/h)*filt,n=n)
        y,root_slope,failures = field_zeros(phase,dx)
        check = global_bracket_check(phase[::256],dx)
        search_difference = np.max(abs(y[::256]-check))
        search_tolerance = 1e-12*(1+np.max(abs(check)))
        audit.append(dict(gamma=gamma,theta=theta,case=case,duration=duration,step=h,dx=dx,
                          path=replicate,failures=failures,min_slope=root_slope.min(),
                          max_root_error=np.max(abs(y-phase)),
                          search_difference=search_difference))
        if failures or not np.isfinite(search_difference) or search_difference>search_tolerance:
            # Retain the failed path; its missing observations invalidate the case.
            v = np.full(SUPPORT.shape,np.nan)
        else:
            v = periodic_variances(y,SUPPORT,h)
        variance.append(v)
        path_rows.extend(dict(gamma=gamma,theta=theta,case=case,duration=duration,step=h,
                              path=replicate,lag=lag,variance=v[i,4])
                         for i,lag in enumerate(LAGS))
    paths = np.asarray(variance)
    point,lo,hi = variance_intervals(paths,LAGS,OFFSETS,FAMILY_SIZE)
    details = []
    for j,lag in enumerate(LAGS):
        row = dict(gamma=gamma,theta=theta,case=case,duration=duration,step=h,dx=dx,
                   lag=lag,variance=point[j,1]*lag,spectral_variance=predicted[j],
                   rate_grid_change=abs(coarse[j]/predicted[j]-1))
        for k,name in enumerate(("slope","rate","rate_ratio")):
            row[name] = point[j,k]
            row[name+"_lo"],row[name+"_hi"] = lo[j,k],hi[j,k]
        details.append(row)
    return details,audit,path_rows


def classify(details, response_status):
    result = []
    for lag in LAGS:
        subset = [r for r in details if r["lag"] == lag]
        row = {k:subset[-1][k] for k in ("gamma","theta","case","lag")}
        for name in ("slope","rate","rate_ratio"):
            row[name+"_lo"] = np.min([r[name+"_lo"] for r in subset])
            row[name+"_hi"] = np.max([r[name+"_hi"] for r in subset])
        result.append(row)
    if not all(np.isfinite(r["slope_lo"]) for r in result):
        status = "invalid"
    elif all(r["slope_lo"]>=.9 and r["slope_hi"]<=1.1 and r["rate_lo"]>0
             and r["rate_ratio_lo"]>=.8 and r["rate_ratio_hi"]<=1.25 for r in result):
        status = "compatible"
    elif all(r["slope_hi"]<.9 for r in result):
        status = "below"
    elif all(r["slope_lo"]>1.1 for r in result):
        status = "above"
    else:
        status = "inconclusive"
    for row in result:
        row.update(variance_status=status,response_status=response_status,
                   joint_compatible=(status==response_status=="compatible"))
    return result


def figure(rows):
    with mpl.rc_context({"svg.hashsalt":"observed-root-v150","font.size":9}):
        fig, axes=plt.subplots(1,2,figsize=(8.2,3.4),layout="constrained",sharey=True)
        for gamma,ax in zip((.4,.6),axes):
            ax.axhspan(.9,1.1,color=".91")
            ax.axhline(1,color=".45",lw=.7)
            for off,c in zip((-.08,0,.08),("#2166ac","black","#b2182b")):
                theta=(1-gamma)/2+off
                rr=[r for r in rows if r["gamma"]==gamma and r["theta"]==theta and r["case"]=="primary"]
                lo=np.array([r["slope_lo"] for r in rr]);hi=np.array([r["slope_hi"] for r in rr])
                ax.fill_between(LAGS,lo,hi,color=c,alpha=.12)
                ax.semilogx(LAGS,lo,color=c,lw=.9,label=f"θ = {theta:.2f}")
                ax.semilogx(LAGS,hi,color=c,lw=.9)
            ax.set(xlabel="Operational lag",title=f"Input γ = {gamma:.1f}")
            ax.legend(frameon=False)
        axes[0].set_ylabel("Measured root-variance slope")
        fig.savefig(ROOT/"figures/v2/root-variance.svg",metadata={"Date":None})
        plt.close(fig)


if __name__ == "__main__":
    with (ROOT/"outputs/v2/balance-window.csv").open() as stream:
        prior={(float(r["gamma_input"]),float(r["theta"]),r["case"]):r["window_result"]
               for r in csv.DictReader(stream)}
    all_details,all_audit,all_paths,all_windows=[],[],[],[]
    for gamma in (.4,.6):
        for off,case in [(-.08,"primary"),(0.,"primary"),(.08,"primary"),(0.,"off"),(0.,"raised_floor")]:
            theta=(1-gamma)/2+off
            details=[]
            for design in DESIGNS:
                chunk,audit,paths=run_design(gamma,theta,case,design)
                details.extend(chunk);all_audit.extend(audit);all_paths.extend(paths)
            all_details.extend(details)
            all_windows.extend(classify(details,prior[gamma,theta,case]))
    for name,rows in [("designs",all_details),("roots",all_audit),("paths",all_paths),("window",all_windows)]:
        write_csv("root-variance-"+name+".csv",rows)
    figure(all_windows)
