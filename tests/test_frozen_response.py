"""W01 scientific acceptance tests. Run with unittest discovery from the repo root."""

import math
import unittest

from functions.frozen_response import crossover, frozen_variance, time_covariance_check
from functions.response_regimes import f_high_z, f_low_z
from scripts.run_frozen_response import compare_domains


def slope(first, second, ratio):
    return math.log(second / first) / math.log(ratio)


class FrozenResponseTests(unittest.TestCase):
    def test_independent_quadrature_and_refinement(self):
        for row in compare_domains():
            with self.subTest(gamma=row["gamma"], nu=row["nu"], tau0=row["tau0"], delta=row["delta"]):
                for key in ("relative_domain_error", "spectral_refinement", "time_refinement", "level_refinement"):
                    self.assertLess(row[key], 1e-6, key)

    def test_zero_cutoff_asymptotes(self):
        for gamma in (.3, .55, .8):
            self.assertAlmostEqual(crossover(gamma, 1e-5)/f_low_z(gamma), 1., delta=1e-5)
            self.assertAlmostEqual(crossover(gamma, 1e8)/f_high_z(gamma, 1e8), 1., delta=.01)
            high_slope = slope(crossover(gamma, 1e6), crossover(gamma, 1e8), 100)
            self.assertAlmostEqual(high_slope, gamma-1, delta=.01)

    def test_short_mesoscopic_and_plateau_slopes(self):
        g = .5
        def variance(tau, lag):
            return frozen_variance(g, 1., tau, lag)
        self.assertAlmostEqual(slope(variance(.1, 1e-5), variance(.1, 1e-4), 10), 2, delta=.01)
        self.assertAlmostEqual(slope(variance(1e-12, 1e-4), variance(1e-12, .01), 100),
                               1-g, delta=.01)
        for lag in (1e-4, .01):
            self.assertAlmostEqual(variance(1e-12, lag) / (lag**(1-g) * crossover(g, lag)),
                                   1., delta=.01)
        _, level = time_covariance_check(g, 1., .1, 1.)
        self.assertAlmostEqual(variance(.1, 1e6)/(2*level), 1., delta=.005)
        self.assertAlmostEqual(slope(variance(.1, 1e4), variance(.1, 1e6), 100), 0., delta=.01)
        high_prefactor = f_high_z(g, 1e6) * (1e6)**(1-g)
        self.assertAlmostEqual(variance(1e-12, 1e6)/high_prefactor, 1., delta=.005)
        self.assertLess(variance(.1, 1e6)/high_prefactor, .8)

    def test_conditioning_in_frozen_gaussian_model(self):
        for lag in (.001, 1e6):
            var = frozen_variance(.5, 1., .1, lag)
            direct, level = time_covariance_check(.5, 1., .1, lag)
            covariance = level - direct/2
            # Condition the future level on the present one, then form its increment.
            for sd in (0, 1, 2):
                cond_mean = (covariance/level - 1) * sd * math.sqrt(level)
                moment = level - covariance**2/level + cond_mean**2
                ratio = 1 + var / (4*level) * (sd**2 - 1)
                self.assertAlmostEqual(moment/var, ratio, delta=1e-6)
                if lag < 1:
                    self.assertAlmostEqual(ratio, 1., delta=.001)
                else:
                    self.assertAlmostEqual(ratio, (1+sd**2)/2, delta=.005)

    def test_units_and_domain(self):
        base = frozen_variance(.5, 2., .05, 1.)
        self.assertAlmostEqual(frozen_variance(.5, 2., .05, 1., forcing=6., diffusion=2., liquidity=3.),
                               base/3.)
        self.assertEqual(frozen_variance(.5, 2., .05, 1., forcing=0), 0.)
        for args in ((1,1,1,1), (.5,0,1,1), (.5,1,0,1), (.5,1,1,-1)):
            with self.assertRaises(ValueError):
                frozen_variance(*args)
