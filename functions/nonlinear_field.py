"""Root-coupled reaction diffusion at unit field scales, on a fixed Eulerian grid."""

import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from functions.liquidity_feedback import rate_grid


def decreasing_root(field, x):
    """Rows are independent fields. A plateau, touch or reversed crossing is invalid."""
    a,b=field[:,:-1],field[:,1:]
    cross=(a>=0)&(b<0)
    cell=np.argmax(cross,axis=1)
    row=np.arange(len(field)); left=a[row,cell]; right=b[row,cell]
    dx=x[1]-x[0]
    width=left-right
    valid=((cross.sum(1)==1)&(field[:,0]>0)&(field[:,-1]<0)&
           ~np.any((a<=0)&(b>=0),axis=1)&np.isfinite(field).all(1)&(width>0))
    fraction=left/np.where(width>0,width,1.)
    return x[cell]+dx*fraction,width/dx,cell,valid


def phase_observation(field,x,root):
    """Translate the neutral mode until the residual field is orthogonal."""
    phase=root.copy()
    for _ in range(6):
        xi=x[None,:]-phase[:,None]
        psi=np.exp(-np.abs(xi))
        psi[:,[0,-1]]*=.5  # trapezoidal endpoint weights
        residual=field-np.sign(xi)*np.expm1(-np.abs(xi))
        score=np.sum(psi*residual,axis=1)
        derivative=np.sum(psi*(np.sign(xi)*residual-np.exp(-np.abs(xi))),axis=1)
        if np.all(abs(score)*(x[1]-x[0])<1e-11):
            break
        phase-=score/np.where(abs(derivative)>1e-12,derivative,np.nan)
    xi=x[None,:]-phase[:,None]
    score=np.trapezoid(np.exp(-np.abs(xi))*(field-np.sign(xi)*np.expm1(-abs(xi))),x,axis=1)
    return phase,(np.isfinite(phase)&(abs(score)<1e-8)&(abs(phase)<x[-1]))


def travelling_speed(b,epsilon):
    """Whole-line constant-forcing speed from the root value of the Green solution."""
    def residual(v):
        k=np.sqrt(1+v*v/4)
        left,right=k-v/2,k+v/2
        return -v + b/2*((1-epsilon)*(1/(1+left)+1/(1+right))
                         +epsilon*(1/(2+left)+1/(2+right)))
    return brentq(residual,-2.,2.)


def evolve(inputs, theta, epsilon, floor, *, half_width, dx, dt, nodes, feedback=4., burn=256):
    """Inputs have shape (paths, quarter-time nodes). Sample at integer times."""
    duration=(inputs.shape[1]-1)/4
    steps=round(duration/dt)
    stride=round(1/dt)
    if stride*dt!=1 or steps*dt!=duration:
        raise ValueError("The grids must resolve integer observations and the terminal time.")
    x=dx*np.arange(-round(half_width/dx),round(half_width/dx)+1)
    size=len(inputs)
    rates,weights=map(np.stack,zip(*(rate_grid(float(t),float(f),100.,nodes) for t,f in zip(theta,floor))))
    decay=np.exp(-dt*rates); load=-np.expm1(-dt*rates)/rates
    memory=np.zeros_like(rates); gain=2*feedback
    mu=dt/dx**2
    def band(diagonal,off):
        ab=np.zeros((3,len(x)-2));ab[1]=diagonal;ab[0,1:]=off;ab[2,:-1]=off
        return ab
    def solve(ab,rhs):
        return solve_banded((1,1),ab,rhs.T,check_finite=False).T
    step_matrix=band(1+dt+2*mu,-mu)
    init=-np.sign(x[1:-1]);init[[0,-1]] += np.array([1.,-1.])/dx**2
    field=np.empty((size,len(x)));field[:,0]=1;field[:,-1]=-1
    field[:,1:-1]=solve_banded((1,1),band(1+2/dx**2,-1/dx**2),init)
    y,_,_,valid=decreasing_root(field,x)
    arr=np.full((size,int(duration)+1,3),np.nan)
    phase,pvalid=phase_observation(field,x,y)
    arr[:,0,:]=np.stack((y,phase,y-phase),axis=1)
    valid &= pvalid
    failed=np.where(valid,np.nan,0.);reason=np.where(valid,'','initial root').astype('U40')
    min_slope=np.full(size,np.inf); weak_sum=np.zeros(size);weak_count=np.zeros(size,int)
    row=np.arange(size); interior=x[None,1:-1]
    def flag(mask,time,label):
        new=mask & np.isnan(failed)
        failed[new]=time;reason[new]=label
    for n in range(steps):
        time=(n+1)*dt; position=(time-dt/2)*4; i=int(position);frac=position-i
        forcing=(1-frac)*inputs[:,i]+frac*inputs[:,i+1]
        xi=interior-y[:,None]; e=np.exp(-abs(xi))
        shape=.5*((1-epsilon[:,None])*e+epsilon[:,None]*e*e)
        sign=-np.clip(2*xi/dx,-1.,1.)
        past=np.sum(weights*decay*memory,axis=1)
        b0=forcing-gain*past
        rhs=field[:,1:-1]+dt*(sign+b0[:,None]*shape)
        rhs[:,0]+=mu;rhs[:,-1]-=mu
        solved=solve(step_matrix,np.concatenate((rhs,shape),axis=0))
        F=field.copy(); F[:,1:-1]=solved[:size]
        U=np.zeros_like(F);U[:,1:-1]=(gain*np.sum(weights*load,axis=1))[:,None]*solved[size:]
        residual=F-U*(x[None,:]-y[:,None])
        trial,_,cell,ok=decreasing_root(residual,x)
        # Inside this cell both F and U are affine, so the scalar residual is quadratic.
        a=F[row,cell]; fd=(F[row,cell+1]-a)/dx
        u=U[row,cell]; ud=(U[row,cell+1]-u)/dx
        for _ in range(3):
            d=trial-x[cell]; du=trial-y
            derivative=fd-ud*du-(u+ud*d)
            trial-=((a+fd*d)-(u+ud*d)*du)/np.where(abs(derivative)>1e-13,derivative,np.nan)
        fresh=F-U*(trial-y)[:,None]
        measured,mag,_,root_ok=decreasing_root(fresh,x)
        flag(~ok,time,'ambiguous feedback bracket')
        flag(~root_ok,time,'invalid field zero or slope')
        flag(~np.isfinite(trial)|(abs(trial-measured)>1e-8),time,'feedback inconsistency')
        alive=np.isnan(failed)
        min_slope=np.where(alive,np.minimum(min_slope,mag),min_slope)
        velocity=(measured-y)/dt
        memory=decay*memory+load*velocity[:,None]
        if (n+1)%stride==0:
            phase,pok=phase_observation(fresh,x,measured)
            flag(~pok,time,'phase observation failure')
            alive=np.isnan(failed)
            arr[alive,int(time),:]=np.stack((measured,phase,measured-phase),axis=1)[alive]
            if time>burn:
                # Smooth compact test of radius 2 centred on the old zero.
                z=(x[None,:]-y[:,None])/2; z2=z*z
                test=np.where(abs(z)<1,(1-z2)**4,0)
                dd=np.where(abs(z)<1,-2*(1-z2)**3+12*z2*(1-z2)**2,0)
                b=forcing-gain*np.sum(weights*memory,axis=1)
                # Exact integral of the odd continuum sign against this even test is zero.
                source=.5*((1-epsilon[:,None])*np.exp(-2*abs(z))+epsilon[:,None]*np.exp(-4*abs(z)))
                weak=np.trapezoid(((fresh-field)/dt+fresh-b[:,None]*source)*test-fresh*dd,x,axis=1)
                inside=alive & (abs(y)+2<x[-1])
                weak_sum[inside]+=abs(weak[inside]);weak_count[inside]+=1
        # Failed trajectories have no later observations; keep other paths numerically isolated.
        alive=np.isnan(failed)
        field=np.where(alive[:,None],fresh,field)
        y=np.where(alive,measured,y);memory[~alive]=0
    return arr,failed,reason,min_slope,weak_sum/np.maximum(1,weak_count),weak_count
