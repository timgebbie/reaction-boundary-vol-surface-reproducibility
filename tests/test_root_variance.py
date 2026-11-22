import unittest
import numpy as np
from functions.root_variance import (field_zeros,global_bracket_check,periodic_variances,
                                     predicted_variance,variance_statistics)


class RootVarianceTests(unittest.TestCase):
    def test_field_measurement_and_refinement(self):
        q=np.array([-2.75,-.031,0.,.312,3.123])
        for dx in (.125,.0625):
            y,mag,failed=field_zeros(q,dx)
            self.assertEqual(failed,0)
            self.assertTrue(np.all(mag>0))
            np.testing.assert_allclose(y,global_bracket_check(q,dx),atol=1e-14)
            self.assertLess(max(abs(y-q)),dx*dx/8)
        self.assertNotEqual(y[-1],q[-1])

    def test_fractional_lags_against_direct_zero_increments(self):
        y=np.random.default_rng(180).normal(size=257)
        for t in (2.,3.21,19.63):
            k=int(t);r=t-k
            direct=(1-r)*np.roll(y,-k)+r*np.roll(y,-k-1)-y
            self.assertAlmostEqual(periodic_variances(y,np.array([t]),1)[0],np.mean(direct**2))

    def test_spectral_normalisation_and_slope(self):
        n=128;h=.5;omega=2*np.pi*np.fft.rfftfreq(n,h);power=np.zeros(len(omega))
        power[7]=n*h/4
        lags=np.array([1.25,3.,7.5])
        y=np.cos(omega[7]*np.arange(n)*h)
        np.testing.assert_allclose(predicted_variance(power,omega,h,n,lags),
                                   periodic_variances(y,lags,h))
        offsets=np.linspace(-.3,.3,9)
        v=3*lags[:,None]*np.exp(offsets)
        res=variance_statistics(v,lags,offsets)
        np.testing.assert_allclose(res,np.tile([1.,3.,1.],(3,1)))
