import unittest

import numpy as np
from scipy.special import gamma

from functions.liquidity_feedback import continuum_root, memory, rate_grid, step_velocity, velocity_transfer
from scripts.run_liquidity_feedback import GAIN, frequency_rows, time_rows, shell_rows


class LiquidityFeedbackTests(unittest.TestCase):
    def test_cutoff_against_continuum_and_refined_quadrature(self):
        rows = frequency_rows()
        self.assertLess(max(r['quadrature_error'] for r in rows if r['count']==96), .002)
        self.assertLess(max(r['continuum_error'] for r in rows
                            if r['floor']==1e-7 and r['ceiling']==1e6), .05)
        self.assertTrue(all(0 < r['dc'] < GAIN for r in rows))

    def test_time_domain_and_mittag_leffler(self):
        rows = time_rows()
        self.assertLess(max(abs(r['G_ode']-r['G_modal']) for r in rows), 1e-6*GAIN)
        self.assertLess(max(r['step_difference'] for r in rows), 1e-6*GAIN)
        self.assertLess(max(abs(r['G_ode']-r['G_continuum']) for r in rows), .04*GAIN)
        for theta in (.25, 1/3, .4):
            t = .1
            series = sum((-t**theta)**k/gamma(1+k*theta) for k in range(60))
            self.assertAlmostEqual(continuum_root(t,theta,GAIN,1), GAIN*series, places=10)

    def test_causality_stability_and_dc(self):
        r,w = rate_grid(1/3, 1e-6, 1e5, 64)
        values = step_velocity([-1., 0., .1, 1.],r,w,GAIN,0.,.1)
        np.testing.assert_allclose(values, [0.,GAIN,GAIN,GAIN])
        self.assertGreater(np.linalg.eigvalsh(np.diag(r)+np.outer(np.sqrt(w),np.sqrt(w)))[0],0)
        dc = velocity_transfer(0.,r,w,GAIN,1.)
        self.assertAlmostEqual(velocity_transfer(1e-12j,r,w,GAIN,1.).real, dc, places=11)

    def test_shell_error_and_composition(self):
        rows = shell_rows()
        self.assertLess(max(r['exact_error'] for r in rows), 1e-12)
        self.assertLess(max(r['linear_error'] for r in rows), .005)
        self.assertTrue(all(r['linear_error'] <= r['bound']+2e-14 for r in rows))
        rates,w = rate_grid(1/3,1e-6,1e5,64)
        fast = rates >= 2
        upper, middle = rates >= 20, (rates >= 2) & (rates < 20)
        for s in (.001j,.2j):
            staged = memory(s,rates[upper],w[upper])+memory(s,rates[middle],w[middle])
            self.assertAlmostEqual(abs(staged-memory(s,rates[fast],w[fast])),0.,places=13)
        for n in (1,2,3):
            pieces = sum(np.sum(w[m]/rates[m]**n) for m in (upper,middle))
            self.assertAlmostEqual(pieces,np.sum(w[fast]/rates[fast]**n),places=13)
