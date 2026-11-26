"""Plot the finite-rate response surface, variance envelopes and conditional history."""
import csv
from itertools import product
from pathlib import Path
import sys

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from functions.scale_window import beta_curve, conditional_history, variogram
from scripts.run_frozen_response import write_csv
from scripts.run_root_variance import DESIGNS

GAMMA, THETA = .4, .3
FLOORS = [1e-7, .02]
COLORS = ["#215d87", "#ad4c28"]
NAMES = ["reference floor", "raised floor"]

def accepted(filename, case):
    with (ROOT/'outputs/v2'/filename).open() as f:
        return [r for r in csv.DictReader(f) if r['case']==case and
                float(r.get('gamma',r.get('gamma_input')))==GAMMA and
                np.isclose(float(r['theta']),THETA)]

def plot_surface():
    z = np.geomspace(1e-5,1e9,375)
    floors = np.geomspace(1e-8,.1,92)
    surface = np.array([beta_curve(z, f, 128) for f in floors])
    coarse = np.array([beta_curve(z, f, 64) for f in floors])
    print("surface refinement, max absolute 64-to-128 change",abs(surface-coarse).max())
    write_csv("response-surface.csv",[dict(z=x,rate_floor_over_nu=f,beta_eff=b)
              for f,curve in zip(floors,surface) for x,b in zip(z,curve)])
    mpl.rcParams.update({"font.family":"DejaVu Sans","font.size":9,
                          "axes.spines.top":False,"axes.spines.right":False,
                          "pdf.fonttype":42, "svg.hashsalt":"beta-window"})
    fig=plt.figure(figsize=(9.3,7.4),layout="constrained")
    gs=fig.add_gridspec(2,2,height_ratios=[1.14,1])
    ax=fig.add_subplot(gs[0,:])
    im=ax.pcolormesh(z,floors,surface,shading="auto",cmap="viridis",rasterized=True)
    ax.contour(z,floors,surface,levels=[.25],colors="white",linewidths=.8)
    ax.plot(1/floors,floors,color="#f3a3c8",lw=1.55,ls=(0,(2,2)))
    ax.text(.52,.10,r"$\beta_{\rm eff}\simeq0.30$",transform=ax.transAxes,ha="center",color="#16352e")
    ax.text(.76,.68,r"$r_{\min}\Delta=1$",transform=ax.transAxes,color="#f3a3c8")
    ax.axvspan(32,320,color="white",alpha=.14)
    for x in [32,320]:ax.axvline(x,color="white",lw=.8,ls="--")
    for f,m in zip(FLOORS,["o","s"]): ax.scatter([np.sqrt(32*320)],[f],c="white",edgecolors="black",marker=m,s=37,zorder=4)
    ax.set(xscale="log",yscale="log",xlabel=r"Operational lag in resilience units  $z=\nu\Delta$",
           ylabel=r"Slowest reassessment rate  $r_{\min}/\nu$")
    ax.set_title(r"A   Running response exponent  $\beta_{\rm eff}=-d\log G/d\log\Delta$",loc="left",weight="bold")
    fig.colorbar(im,ax=ax,pad=.012,label=r"$\beta_{\rm eff}$")
    ax.text(.012,.035,"short lag / UV",transform=ax.transAxes,color="white")
    ax.text(.988,.035,"long lag / IR",transform=ax.transAxes,color="white",ha="right")
    vax=fig.add_subplot(gs[1,0])
    vax.axhspan(.9,1.1,color="#ddddda",alpha=.65)
    vax.axhline(1,color="0.4",lw=1)
    hax=fig.add_subplot(gs[1,1])
    hax.axhline(0,color=".6",lw=.8)
    hrows=[]
    for f,case,col,name in zip(FLOORS,["primary","raised_floor"],COLORS,NAMES):
        r=accepted("root-variance-window.csv",case)
        lags=np.array([float(i["lag"]) for i in r])
        lo,hi=([float(i[k]) for i in r] for k in ["slope_lo","slope_hi"])
        vax.fill_between(lags,lo,hi,color=col,alpha=.27)
        vax.plot(lags,lo,color=col,lw=1,label=name)
        vax.plot(lags,hi,color=col,lw=1)
        b=accepted("balance-window.csv",case)
        print(case,"beta range from accepted regressions",min(float(i['beta']) for i in b),max(float(i['beta']) for i in b))
        print(case,"response derivative discrepancy vs local regression",max(abs(beta_curve(lags,f,128)-[float(i['beta']) for i in b])))
        designs=[]
        d=np.unique(np.rint(np.geomspace(32,320,40)).astype(int))
        for duration,h in [(duration, h) for duration, h, _ in DESIGNS]:
            v=variogram(GAMMA, THETA, f, duration, h)
            table=accepted("root-variance-designs.csv",case)
            control=next(float(i["spectral_variance"]) for i in table if float(i['lag'])==32 and int(i['duration'])==duration and float(i['step'])==h)
            assert np.isclose(v[32],control,rtol=1e-9)
            line=[]
            for lag in d:
                rho, ratio=conditional_history(lag,lag,lag,v)
                line.append(rho)
                hrows.append(dict(rate_floor=f,duration=duration,step=h,lag=int(lag),partial_correlation=rho,
                                  conditional_variance_to_increment_variance=ratio,
                                  extra_fraction_of_residual_variance_explained=rho**2))
            designs.append(line)
        hax.fill_between(d,np.min(designs,axis=0),np.max(designs,axis=0),color=col,alpha=.3)
        hax.plot(d,designs[-1],color=col,label=name)
        print(case,"Gaussian equal-step rho envelope",np.min(designs),np.max(designs),"max rho squared",np.max(np.square(designs)))
    for panel in [vax,hax]:
        panel.set_xscale("log");panel.set_xticks([32,64,128,320],["32","64","128","320"])
        panel.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        panel.set_xlabel(r"Operational lag $\Delta$"); panel.grid(axis="y",alpha=.2)
    vax.legend(frameon=False,fontsize=8)
    vax.set_ylabel(r"Measured slope  $d\log V_y/d\log\Delta$")
    vax.set_title("B   Moving-zero variance",loc="left",weight="bold")
    hax.set_ylabel(r"Partial correlation  $\rho_{13\mid2}$")
    hax.set_title("C   Memory of an earlier price",loc="left",weight="bold")
    fig.supxlabel("γ = 0.4, θ = 0.30, ν = 1.    Dashed lines: tested decade.    White contour: β = 0.25.    ○ reference floor    □ raised floor", fontsize=9)
    fig.savefig(ROOT/"figures/v2/scale-window.pdf",dpi=210,metadata={"CreationDate":None,"ModDate":None})
    fig.savefig(ROOT/"figures/v2/scale-window.png",dpi=165)
    plt.close(fig)
    write_csv("conditional-history.csv",hrows)


def unequal_history():
    rows = []
    for gamma in (.4, .6):
        matched = (1-gamma)/2
        cases = [("matched", matched, 1e-7, 4., 1.),
                 ("low_theta", matched-.08, 1e-7, 4., 1.),
                 ("high_theta", matched+.08, 1e-7, 4., 1.),
                 ("raised_floor", matched, .02, 4., 1.),
                 ("off", matched, 1e-7, 0., 1.),
                 ("faster_clock", matched, 1e-7, 4., 4.)]
        for (case, theta, floor, feedback, clock), (duration, step, _) in product(cases, DESIGNS):
            v = variogram(gamma, theta, floor, duration, step, feedback, clock)
            for age, first, last in product((32,80,160,320), repeat=3):
                rho, ratio = conditional_history(age, first, last, v)
                rows.append(dict(gamma=gamma, theta=theta, case=case, floor=floor,
                                 clock=clock, feedback=feedback, duration=duration, step=step,
                                 age=age, gap1=first, gap2=last, rho=rho, gain=rho**2,
                                 conditional_ratio=ratio, variance_rate=v[last]/last))
    write_csv("unequal-history.csv", rows)


if __name__ == "__main__":
    plot_surface()
    unequal_history()
