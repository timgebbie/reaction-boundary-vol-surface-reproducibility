"""W02 translation/shape and aligned-root scientific acceptance tests."""

import unittest
import numpy as np
from scipy.integrate import trapezoid
from scripts.run_translating_front import aligned_check, spectrum_box

from functions.translating_front import (
    aligned_gain, aligned_placement, aligned_root_path, front_profile,
    grid_root, lattice_bound_eigenvalue, moving_profile_pde_residual,
    point_interaction_spectrum, root_slope, translation_mode, zero_phase_shape,
)


class TranslatingFrontTests(unittest.TestCase):
    def test_simple_root_and_grid_interpolation(self):
        for D, nu, lam, q in ((1., 1., 1., .223), (2., .5, 1.4, -.18)):
            self.assertAlmostEqual(front_profile(q, q, diffusion=D,
                                                   resilience=nu, deposition=lam), 0)
            h = 1e-5
            derivative = (front_profile(q+h, q, diffusion=D, resilience=nu, deposition=lam)
                          - front_profile(q-h, q, diffusion=D, resilience=nu, deposition=lam))/(2*h)
            self.assertAlmostEqual(-derivative, root_slope(diffusion=D, resilience=nu,
                                                             deposition=lam), delta=3e-5)
            errors = []
            for spacing in (.08, .04):
                x = np.arange(-5, 5+spacing/2, spacing)
                yhat = grid_root(front_profile(x,q,diffusion=D,resilience=nu,deposition=lam),x)
                errors.append(abs(yhat-q))
            self.assertLess(errors[1], errors[0] / 2.5)

    def test_translation_eigenvalue_and_shape_gap(self):
        errors = []
        for dx, half in ((.08, 125), (.04, 250)):
            result = point_interaction_spectrum(half, dx)
            ev = result['eigenvalues']
            self.assertLess(abs(ev[-1]-result['infinite_lattice_prediction']), 2e-6)
            self.assertLess(ev[-2], -1.)
            self.assertLess(abs(ev[-1]), .002)
            self.assertLess(result['mode_l2_error'], .002)
            errors.append(abs(ev[-1]))
        self.assertLess(errors[1], errors[0] / 3.5)
        for dx in (.04, .1):
            self.assertLess(lattice_bound_eigenvalue(dx), 0.)

    def test_aligned_source_and_phase_root_identity(self):
        x = np.linspace(-35, 35, 100001)
        self.assertAlmostEqual(trapezoid(aligned_placement(x), x), 1., delta=1e-7)
        self.assertLess(np.max(np.abs(aligned_placement(x)-aligned_gain()*translation_mode(x))), 1e-14)
        t = np.linspace(0, 4, 101)
        b = .8 + .5*np.sin(t)
        q = aligned_root_path(t,b,q0=.18)
        self.assertAlmostEqual(q[0], .18)
        self.assertAlmostEqual(q[-1], .18+aligned_gain()*(.8*4+.5*(1-np.cos(4))), delta=1e-4)
        for value in q[::10]:
            self.assertAlmostEqual(front_profile(value, value), 0., delta=1e-14)

    def test_phase_not_identical_to_observed_root_for_transverse_shape(self):
        x = np.linspace(-40,40,100001)
        psi = translation_mode(x)
        f = zero_phase_shape(x)
        phase = trapezoid(psi*f,x)/trapezoid(psi**2,x)
        root_variation = f[len(f)//2]/root_slope()
        self.assertAlmostEqual(phase, 0, delta=3e-7)
        self.assertAlmostEqual(root_variation, 1/3, delta=1e-12)
        self.assertGreater(abs(root_variation - phase), .3)
        # Linearised root displacement is seen in a small perturbed field.
        field = front_profile(x) + .001*f
        root = grid_root(field,x)
        self.assertAlmostEqual(root, .001 * root_variation, delta=2e-6)

    def test_exact_nonlinear_pde_ansatz_locally_converges(self):
        q, b = .137, -.7
        errors=[]
        for dx in (.04, .02):
            x=np.arange(-5,5+dx/2,dx)
            errors.append(moving_profile_pde_residual(x,q,b,dx))
        self.assertLess(errors[1], errors[0] / 3.0)

    def test_pinned_and_moving_box(self):
        # Largest pinned mode has wave number pi/(2W), first odd shape has pi/W.
        for width in (6, 12, 24):
            row = spectrum_box(width, 32)
            self.assertAlmostEqual(row['pinned'], -1 - (np.pi/(2*width))**2, delta=1e-5)
            self.assertAlmostEqual(row['stable'], row['odd_box_prediction'], delta=1e-5)
            self.assertLess(row['pinned'], -1)
            self.assertGreater(row['neutral'], -.001)

    def test_interface_weak_residual_and_shifted_source(self):
        coarse = aligned_check(.08, .04)
        fine = aligned_check(.01, .005)
        shifted = aligned_check(.01, .005, forcing_offset=.4)
        self.assertLess(fine['weak_residual'], coarse['weak_residual'] / 50)
        self.assertLess(fine['root_error'], 5e-6)
        self.assertGreater(shifted['weak_residual'], .1)

    def test_reject_non_unique_root(self):
        x=np.linspace(-2,2,401)
        with self.assertRaises(ValueError):
            grid_root(np.sin(4*x),x)
        with self.assertRaises(ValueError):
            point_interaction_spectrum(n_half=1)
        with self.assertRaises(ValueError):
            aligned_root_path([0,1,1],[1,1,1])


if __name__ == '__main__':
    unittest.main()
