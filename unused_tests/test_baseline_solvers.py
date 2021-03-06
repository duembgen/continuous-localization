#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import common

import numpy as np
import unittest

from baseline_solvers import *
from trajectory import Trajectory
from measurements import get_measurements, create_anchors


class TestBaselineSolvers(unittest.TestCase):
    def setUp(self):
        self.traj = Trajectory(n_complexity=5, dim=2)
        self.n_anchors = 4
        self.basis = []
        self.D_topright = []

    def set_measurements(self, seed=None):
        #  random trajectory and anchors
        self.traj.set_coeffs(seed=seed)
        if seed is not None:
            np.random.seed(seed)
        self.anchors = create_anchors(self.traj.dim, self.n_anchors)

        # get measurements
        self.basis, self.D_topright = get_measurements(self.traj, self.anchors, seed=seed, n_samples=20)

    def improve_with_gradientDescent(self, coeffs_est):
        """ Make sure result gets better after running a few iters of grad descent. """
        err_raw = np.linalg.norm(coeffs_est - self.traj.coeffs)

        # For very small errors, the gradient steps to sometimes not refine the error.
        # I believe this is a precision and not algorithmic problem, so we do the
        # test only if the coeffs_est are not so close to the solution to start with.
        # note that if the first condition fails, err_refined > err_raw, so we only
        # have to check that err_refined < eps.
        if (abs(err_raw) < 1e-10):
            print("err_raw was already good enough.")
            return

        coeffs_grad, __ = gradientDescent(self.anchors, self.basis, coeffs_est, self.D_topright, maxIters=10)
        err_refined = np.linalg.norm(coeffs_grad - self.traj.coeffs)

        np.testing.assert_array_almost_equal(coeffs_grad, self.traj.coeffs, decimal=2)

        self.assertTrue((err_refined <= err_raw) or (abs(err_refined) < 1e-10))

    def test_customMDS(self):
        """ Check noiseless error. """

        for i in range(10):
            self.set_measurements(seed=i)

            # check noiseless methods.
            coeffs_est = customMDS(self.D_topright, self.basis, self.anchors)
            np.testing.assert_array_almost_equal(coeffs_est, self.traj.coeffs, decimal=2)

            self.improve_with_gradientDescent(coeffs_est)


if __name__ == "__main__":
    unittest.main()
