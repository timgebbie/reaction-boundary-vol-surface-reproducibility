import unittest

import numpy as np

from functions.liquidity_feedback import modal_response, rate_grid, velocity_transfer
from functions.scale_window import beta_curve, conditional_history
from scripts.run_matched_refinement import history_scores


class ScaleWindowTests(unittest.TestCase):
    def test_local_response_derivative(self):
        lags = np.geomspace(.001, 1e6, 47)
        grid = rate_grid(.3, .02, 100., 128)
        h = 1e-5
        def log_response(shift):
            return np.log(modal_response(lags*np.exp(shift), *grid, .5, 4.))
        expected = (log_response(-h)-log_response(h))/(2*h)
        np.testing.assert_allclose(beta_curve(lags,.02,128), expected, atol=1e-8)

    def test_gaussian_history(self):
        times = np.arange(2000.)
        for gaps in ((80,32,160), (320,80,32)):
            rho, ratio = conditional_history(*gaps, 2*times)
            self.assertAlmostEqual(rho, 0.)
            self.assertAlmostEqual(ratio, 1.)
            rho, ratio = conditional_history(*gaps, times**1.6)
            self.assertLess(rho, -.02)
            self.assertLess(ratio, 1.)

    def test_relative_clock_equivalence(self):
        c, theta = 4., .3
        rates, weights = rate_grid(theta, 1e-7, 100., 128)
        new_rates, new_weights = rate_grid(theta, c*1e-7, c*100., 128)
        s = 1j*np.geomspace(1e-9, 1e4, 100)
        a = velocity_transfer(s, c*rates, weights, .5, 4.)
        b = velocity_transfer(s, new_rates, new_weights, .5, 4.*c**(theta-1))
        np.testing.assert_allclose(a,b,rtol=5e-14)

    def test_path_holdout_is_invariant_to_level(self):
        rng = np.random.default_rng(410)
        paths = np.cumsum(rng.standard_normal((4,300)),axis=1)
        shifts = np.array([1.,-2.,3.,4.])[:,None]
        a = history_scores(paths,32,80,32)
        b = history_scores(paths+shifts,32,80,32)
        np.testing.assert_allclose(a,b)
