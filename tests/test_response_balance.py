import unittest
import numpy as np

from functions.liquidity_feedback import modal_response, rate_grid
from functions.response_balance import root_response, response_slopes


class ResponseBalanceTests(unittest.TestCase):
    def test_slope_and_invalid_response(self):
        x = np.linspace(-.35,.35,17)
        grid = np.array([3*np.exp(-.31*x), np.ones_like(x), np.zeros_like(x)])
        slopes = response_slopes(grid,x)
        np.testing.assert_allclose(slopes[:2],[.31,0],atol=1e-13)
        self.assertTrue(np.isnan(slopes[2]))

    def test_zero_feedback_and_independent_modal_inversion(self):
        r,w = rate_grid(.3,1e-7,100.,64)
        t = np.array([20.,50.,320.])
        for g in (0.,4.):
            actual = root_response(t,r,w,.5,g,0.,(24,40,30))
            np.testing.assert_allclose(actual,modal_response(t,r,w,.5,g),rtol=2e-8)

    def test_linear_shape_feedback_off_against_real_time_kernel(self):
        from scipy.integrate import quad
        from scipy.special import erfcx
        # L^{-1}[1/(sqrt(s+1)+2)] is integrable at zero; integrate in sqrt(t).
        r,w = rate_grid(.3,1e-7,100.,64)
        times = np.array([.05,1.,20.])
        def kernel(x):
            return np.exp(-x*x)*(2/np.sqrt(np.pi)-4*x*erfcx(2*x))
        ref = [.5*(1-.2*quad(kernel,0,np.sqrt(t))[0]) for t in times]
        np.testing.assert_allclose(root_response(times,r,w,.5,0.,.2,(24,40,30)),ref,rtol=1e-8)
