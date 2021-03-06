#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import common

import numpy as np
import unittest

from exact_solution import *


class TestExact(unittest.TestCase):
    def test_quadratic_jac(self):
        d = 2
        k = 3
        n_it = 100

        for _ in range(n_it):
            x = np.random.randn(d * k, 1).flatten()
            anchor = np.random.randn(d, 1)
            basis = np.random.randn(k, 1)
            distance = 3

            eps = 1e-5
            fun = quadratic_constraint(x, anchor, distance, basis)
            jac = quadratic_constraint_jac(x, anchor, distance, basis)
            jac_approx = []
            for i in range(len(x)):
                x_delta = x.copy()
                x_delta[i] += eps

                fun_delta = quadratic_constraint(x_delta, anchor, distance, basis)
                jac_approx.append((fun_delta - fun) / eps)

            np.testing.assert_almost_equal(jac, jac_approx, eps)
        print('ok')

    def test_f_multidim(self):
        from trajectory import Trajectory
        from measurements import get_measurements, create_anchors
        anchors = create_anchors(dim=2, n_anchors=5)
        trajectory = Trajectory(n_complexity=4, dim=2)
        basis, D_topright = get_measurements(trajectory, anchors, n_samples=10)

        eps = 1e-10
        self.assertTrue(np.all(abs(f_multidim(anchors, basis, D_topright, trajectory.coeffs)) < eps))
        self.assertTrue(abs(f_onedim(anchors, basis, D_topright, trajectory.coeffs)) < eps)
        coeffs_hat = np.squeeze(compute_exact(D_topright, anchors, basis))
        np.testing.assert_allclose(coeffs_hat, trajectory.coeffs)


if __name__ == "__main__":
    unittest.main()
