"""Compare an independent Abel benchmark with common forcing and projected field response."""

from pathlib import Path
import sys

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t as student

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from functions.phase_shape import (abel_shape_filter, projected_transfers, increment_covariance,
                                   component_statistics)
from functions.root_variance import periodic_variances, predicted_variance
from scripts.run_root_variance import LAGS, OFFSETS, SUPPORT, DESIGNS, phase_filter
from scripts.run_frozen_response import write_csv

METRICS=("twice_cov","cross_fraction","phase_slope","shape_slope","total_slope","rate","relative_rate")
CASES=[("additive",0.),("additive",.75),("additive",-.75),
       ("projected",0.),("projected",.2),("projected",-.2)]
FAMILY=7*17*12*3


def analyse(gamma,model,coefficient,duration,step):
    theta=(1-gamma)/2
    n=int(duration/step)
    omega=2*np.pi*np.fft.rfftfreq(n,step)
    power=np.zeros(len(omega))
    power[1:-1]=(2*np.sin(omega[1:-1]*step/2)/step)**(gamma-1)
    if model=="additive":
        q_filter=phase_filter(omega,theta,4.,1e-7,128)
        x_filter=abel_shape_filter(omega)
        corr=coefficient
    else:
        q_filter,x_filter,y_filter=projected_transfers(omega,theta,coefficient)
        corr=1.
    theory=2*predicted_variance(corr*power*(q_filter*x_filter.conj()).real,omega,step,n,LAGS)
    sample=[]; paths=[]
    for rep in range(32):
        seed=[1600,round(100*gamma),round(2*step),duration,rep]
        rng=np.random.default_rng([*seed,0])
        m=np.fft.rfft(rng.standard_normal(n))*np.sqrt(power/step)
        q=np.fft.irfft(q_filter*m,n=n)
        if model=="additive":
            rng2=np.random.default_rng([*seed,1])
            m2=np.fft.rfft(rng2.standard_normal(n))*np.sqrt(power/step)
            xi=np.fft.irfft(x_filter*(corr*m+np.sqrt(1-corr**2)*m2),n=n)
            y=q+xi
        else:
            xi=np.fft.irfft(x_filter*m,n=n)
            y=np.fft.irfft(y_filter*m,n=n)
        vq=periodic_variances(q,SUPPORT,step)
        vx=periodic_variances(xi,SUPPORT,step)
        vy=periodic_variances(y,SUPPORT,step)
        c=increment_covariance(q,xi,SUPPORT,step)
        identity=np.max(abs(vy-vq-vx-2*c)/vy)
        displacement=np.max(abs(y-q-xi))/max(1.,np.max(abs(y)))
        sample.append(np.stack((vq,vx,vy,c)))
        for j,lag in enumerate(LAGS):
            paths.append(dict(gamma=gamma,model=model,coefficient=coefficient,duration=duration,
                              step=step,path=rep,lag=lag,Vq=vq[j,4],Vxi=vx[j,4],Vy=vy[j,4],
                              C=c[j,4],max_variance_error=identity,max_displacement_error=displacement))
    sample=np.asarray(sample)
    avg=sample.mean(axis=0)
    has_shape=(model=="additive" or coefficient!=0)
    vals=component_statistics(avg,LAGS,OFFSETS,has_shape)
    leave=component_statistics((32*avg-sample)/31,LAGS,OFFSETS,has_shape)
    se=np.sqrt(31/32*np.sum((leave-leave.mean(axis=0))**2,axis=0))
    radius=student.ppf(1-.05/(2*FAMILY),31)*se
    result=[]
    for j,lag in enumerate(LAGS):
        r=dict(gamma=gamma,theta=theta,model=model,coefficient=coefficient,duration=duration,
               step=step,lag=lag,Vq=avg[0,j,4],Vxi=avg[1,j,4],Vy=avg[2,j,4],
               expected_twice_cov=theory[j])
        for k,key in enumerate(METRICS):
            r[key]=vals[j,k]
            r[key+"_lo"]=vals[j,k]-radius[j,k]
            r[key+"_hi"]=vals[j,k]+radius[j,k]
        result.append(r)
    return result,paths


def classify(rows,gamma):
    window=[]
    for lag in LAGS:
        subset=[r for r in rows if r["lag"]==lag]
        r={k:subset[0][k] for k in ("gamma","model","coefficient","lag")}
        for key in METRICS:
            r[key+"_lo"]=min(t[key+"_lo"] for t in subset)
            r[key+"_hi"]=max(t[key+"_hi"] for t in subset)
        window.append(r)
    if all(r["twice_cov_lo"]>0 for r in window):
        sign="positive"
    elif all(r["twice_cov_hi"]<0 for r in window):
        sign="negative"
    elif all(r["twice_cov_lo"]==r["twice_cov_hi"]==0 for r in window):
        sign="identically zero"
    else:
        sign="unresolved"
    total=all(r["total_slope_lo"]>=.9 and r["total_slope_hi"]<=1.1 and
              r["rate_lo"]>0 and r["relative_rate_lo"]>=.8 and r["relative_rate_hi"]<=1.25
              for r in window)
    local=all(r["shape_slope_lo"]>0 and r["shape_slope_hi"]<.9 for r in window)
    target=all(r["shape_slope_lo"]>=1-gamma-.1 and r["shape_slope_hi"]<=1-gamma+.1
               for r in window)
    for r in window:
        r.update(cross_sign=sign,total_compatible=total,shape_subdiffusive=local,
                 shape_matches_abel_slope=target,coexistence=total and local)
    return window


def figure(window):
    with mpl.rc_context({"svg.hashsalt":"phase-shape-v160","font.size":9}):
        fig,axes=plt.subplots(1,2,figsize=(8.4,3.4),layout="constrained")
        for ax,model,title in zip(axes,("additive","projected"),("Additive local Abel response","Projected moving field")):
            for case,c in zip([v for m,v in CASES if m==model],("black","#2166ac","#b2182b")):
                rows=[r for r in window if r["model"]==model and r["coefficient"]==case and r["gamma"]==.4]
                lo=[100*r["cross_fraction_lo"] for r in rows];hi=[100*r["cross_fraction_hi"] for r in rows]
                ax.fill_between(LAGS,lo,hi,color=c,alpha=.16)
                ax.semilogx(LAGS,lo,color=c,lw=.9,label=("ρ" if model=="additive" else "ε")+f" = {case:g}")
                ax.semilogx(LAGS,hi,color=c,lw=.9)
            ax.axhline(0,color=".5",lw=.6)
            ax.set(title=title,xlabel="Operational lag",ylabel="Cross term / total variance (%)")
            ax.legend(frameon=False)
        fig.savefig(ROOT/"figures/v2/phase-shape.svg",metadata={"Date":None})
        plt.close(fig)


if __name__=="__main__":
    designs,paths,window=[],[],[]
    for gamma in (.4,.6):
        for model,coefficient in CASES:
            group=[]
            for duration,step,_ in DESIGNS:
                rows,rr=analyse(gamma,model,coefficient,duration,step)
                group.extend(rows); paths.extend(rr)
            designs.extend(group)
            window.extend(classify(group,gamma))
    for name,rows in (("designs",designs),("paths",paths),("window",window)):
        write_csv("phase-shape-"+name+".csv",rows)
    figure(window)
    if any(r["max_variance_error"]>1e-9 or r["max_displacement_error"]>1e-10 for r in paths):
        raise RuntimeError("Component reconstruction exceeded its recorded tolerance; inspect saved rows.")
