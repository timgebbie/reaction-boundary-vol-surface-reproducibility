"""Nonlinear finite-box trajectories, signed root observations and convergence checks."""
from pathlib import Path
import sys
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from functions.nonlinear_field import evolve,travelling_speed
from functions.response_balance import slope
from scripts.run_root_variance import LAGS, OFFSETS, SUPPORT
from scripts.run_frozen_response import write_csv

DESIGNS={"base":(12,.2,.25,32),"space":(12,.1,.25,32),"time":(12,.2,.125,32),
         "walls":(18,.2,.25,32),"rates":(12,.2,.25,64),"fine":(18,.1,.125,64)}
CASES=[("aligned",0.,1e-7),("narrow",.2,1e-7),("broad",-.2,1e-7),("floor",.2,.02)]


def input_path(gamma,rep):
    h=.25;n=16384
    omega=2*np.pi*np.fft.rfftfreq(n,h)
    coeff=np.fft.rfft(np.random.default_rng([1700,round(100*gamma),rep]).standard_normal(n))
    coeff[1:-1]*=(2*np.sin(omega[1:-1]*h/2)/h)**((gamma-1)/2)
    coeff[[0,-1]]=0
    return .1*np.fft.irfft(coeff,n=n)[:5121]/np.sqrt(h)


def increment_stats(path,lags):
    result=[]
    for lag in np.ravel(lags):
        j=int(np.floor(lag));f=lag-j
        count=len(path)-int(np.ceil(lag))
        end=(1-f)*path[j:j+count]
        if f: end=end+f*path[j+1:j+1+count]
        d=end-path[:count]; d-=d.mean(axis=0)
        vy,vq,vx=np.mean(d*d,axis=0);c=np.mean(d[:,1]*d[:,2])
        result.append([vy,vq,vx,c])
    return np.array(result).reshape((*np.shape(lags),4))


def simulate():
    config=[(g,rep,name,eps,floor) for g in (.4,.6) for rep in range(4) for name,eps,floor in CASES]
    forcing=np.array([input_path(g,r) for g,r,*_ in config])
    theta=np.array([(1-g)/2 for g,*_ in config]);eps=np.array([c[3] for c in config]);floor=np.array([c[4] for c in config])
    paths={}; audits=[];variances=[];series=[];controls=[]
    for key,(width,dx,dt,nodes) in DESIGNS.items():
        opts=dict(half_width=width,dx=dx,dt=dt,nodes=nodes)
        arr,fail,reason,mag,weak,count=evolve(forcing,theta,eps,floor,**opts)
        paths[key]=arr
        for k,(g,rep,name,_,_) in enumerate(config):
            audits.append(dict(design=key,gamma=g,path=rep,case=name,failed_at=fail[k],reason=reason[k],
                               min_slope_magnitude=mag[k],weak_mean=weak[k],weak_count=count[k]))
            if key in ("base","fine"):
                series.extend(dict(design=key,gamma=g,path=rep,case=name,time=t,y=y,q=q,xi=xi)
                              for t,(y,q,xi) in enumerate(arr[k]) if t%8==0)
        for g in (.4,.6):
            for name,_,_ in CASES:
                ids=[k for k,c in enumerate(config) if c[0]==g and c[2]==name]
                good=np.isnan(fail[ids]).all()
                vals=np.mean([increment_stats(arr[k,256:],SUPPORT) for k in ids],axis=0) if good else np.full((*SUPPORT.shape,4),np.nan)
                pp=slope(OFFSETS,np.log(vals[:,:,0]))
                for j,lag in enumerate(LAGS):
                    vy,vq,vx,c=vals[j,4]
                    variances.append(dict(design=key,gamma=g,case=name,lag=lag,complete=good,
                                          Vy=vy,Vq=vq,Vxi=vx,C=c,slope=pp[j],rate=vy/lag,
                                          identity_error=abs(vy-vq-vx-2*c)/vy))
        b=np.tile(np.array([0.,.1,.1,.1])[:,None],(1,129))
        es=np.array([0.,0.,.2,-.2])
        ar,failed,why,*_=evolve(b,np.full(4,.3),es,np.full(4,1e-7),feedback=0.,burn=0,**opts)
        for k,e in enumerate(es):
            speed=(ar[k,32,0]-ar[k,8,0])/24
            exact=travelling_speed(b[k,0],e)
            controls.append(dict(design=key,forcing=b[k,0],epsilon=e,speed=speed,exact=exact,
                                 abs_error=abs(speed-exact),failed_at=failed[k],reason=why[k]))
    for r in audits:
        k=config.index(next(c for c in config if (c[0],c[1],c[2])==(r["gamma"],r["path"],r["case"])))
        diff=paths[r["design"]][k,:,0]-paths["fine"][k,:,0]
        r["fine_error"]=np.max(np.abs(diff))
        r["ceiling"]=.05 if r["design"]=="base" else .03
        r["converged"]=np.isfinite(r["fine_error"]) and r["fine_error"]<=r["ceiling"]
    return audits,variances,series,controls


def figure(rows,audits):
    with mpl.rc_context({"svg.hashsalt":"nonlinear-root-v170","font.size":9}):
        fig,(ax,bx)=plt.subplots(1,2,figsize=(8.3,3.4),layout="constrained")
        for name,_,_ in CASES:
            r=[v for v in rows if v["design"]=="fine" and v["gamma"]==.4 and v["case"]==name]
            ax.semilogx(LAGS,[v["slope"] for v in r],label=name)
        ax.axhline(1,color=".6",lw=.7);ax.legend(frameon=False)
        ax.set(xlabel="Operational lag",ylabel="Exploratory root-variance slope")
        keys=list(DESIGNS)[:-1]
        bx.bar(keys,[max(a["fine_error"] for a in audits if a["design"]==k) for k in keys],color="#42687c")
        bx.set(ylabel="Maximum root error vs joint refinement")
        fig.savefig(ROOT/"figures/v2/nonlinear-field.svg",metadata={"Date":None})
        plt.close(fig)


if __name__=="__main__":
    audit,var,series,ctrl=simulate()
    for name,rows in (("audit",audit),("variance",var),("trajectories",series),("speed",ctrl)):
        write_csv("nonlinear-field-"+name+".csv",rows)
    figure(var,audit)
