import unittest
import numpy as np
from functions.nonlinear_field import decreasing_root,evolve,phase_observation,travelling_speed
from functions.translating_front import front_profile
from scripts.run_nonlinear_field import increment_stats


class NonlinearFieldTests(unittest.TestCase):
    def test_reject_multiple_and_plateau(self):
        x=np.arange(-2,3,dtype=float)
        a=np.array([[1,.4,0,-.2,-1],[1,-.1,.2,-.2,-1],[1,0,0,-.3,-1]])
        root,mag,_,valid=decreasing_root(a,x)
        self.assertEqual(list(valid),[True,False,False]);self.assertEqual(root[0],0.)

    def test_orbit_phase_and_covariance(self):
        x=np.linspace(-10,10,401);q=np.array([.137,-.381])
        p,valid=phase_observation(front_profile(x[None,:]-q[:,None]),x,np.zeros(2))
        self.assertTrue(valid.all());np.testing.assert_allclose(p,q,atol=1e-8)
        t=np.arange(65.);q=np.sin(t);xi=.2*np.cos(t/2)
        v=increment_stats(np.column_stack([q+xi,q,xi]),[2.,4.27])
        np.testing.assert_allclose(v[:,0],v[:,1]+v[:,2]+2*v[:,3])

    def test_static_field_and_speed_law(self):
        out,failed,*_=evolve(np.zeros((1,33)),np.array([.3]),np.array([0.]),np.array([1e-7]),
                              half_width=8,dx=.2,dt=.25,nodes=32,burn=0)
        self.assertTrue(np.isnan(failed).all());self.assertLess(np.max(abs(out)),1e-10)
        self.assertAlmostEqual(travelling_speed(.1,0),.05)
