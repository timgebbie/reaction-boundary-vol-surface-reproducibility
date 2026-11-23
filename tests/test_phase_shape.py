import unittest
import numpy as np
from scipy.integrate import quad
from functions.phase_shape import increment_covariance,projected_transfers,abel_shape_filter
from functions.liquidity_feedback import memory,rate_grid

class PhaseShapeTests(unittest.TestCase):
    def test_direct_signed_products(self):
        rng=np.random.default_rng(92)
        q=rng.normal(size=137);x=-q+.2*rng.normal(size=137)
        for lag in (1.,3.4,36.7):
            j=int(lag); f=lag-j
            def inc(z):
                return (1-f)*np.roll(z,-j)+f*np.roll(z,-j-1)-z
            self.assertAlmostEqual(increment_covariance(q,x,np.array([lag]),1.)[0],
                                   np.mean(inc(q)*inc(x)))

    def test_projected_gains_against_spatial_integrals(self):
        omega=np.array([0.,.012,.3,1.,5.])
        rates,w=rate_grid(.3,1e-7,100.,128)
        for eps in (-.2,0.,.2):
            q,x,y=projected_transfers(omega,.3,eps)
            def h(t):
                return .5*((1-eps)*np.exp(-t)+eps*np.exp(-2*t))
            projection=2*quad(lambda t:np.exp(-t)*h(t),0,np.inf)[0]
            for j,f in enumerate(omega[1:-1],1):
                s=1j*f;k=np.sqrt(1+s)
                mob=(k+1)*quad(lambda t:np.exp(-k*t)*h(t),0,np.inf,complex_func=True)[0]
                den=1+8*mob*memory(s,rates,w)
                np.testing.assert_allclose([q[j],y[j],q[j]+x[j]],
                                           [projection/(s*den),mob/(s*den),mob/(s*den)],rtol=2e-11)

    def test_abel_transfer_against_causal_time_kernel(self):
        for f in (.001,.08):
            def kernel(t):
                return .1*np.exp(-1e-4*(t+.25))/(2*np.sqrt(np.pi*(t+.25)))
            real=quad(kernel,0,np.inf,weight="cos",wvar=f)[0]
            imag=-quad(kernel,0,np.inf,weight="sin",wvar=f)[0]
            self.assertAlmostEqual(abs(abel_shape_filter(f)-(real+1j*imag)),0,places=8)
