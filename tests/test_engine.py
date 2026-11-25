import math
import unittest
from unittest.mock import patch

import networkx as nx
import numpy as np

from spin10_optimized import (FastHPCKernel, OptimizedEngine, OptimizedSpectralDim,
                              PhysicsConfig, run_one_loop_rge)


class EngineTests(unittest.TestCase):
    def test_rge_piecewise_matches_analytic_one_loop(self):
        mg, ms, mz, ag = 2.1e16, 5000., 91.18, 0.0381
        b_hi = np.array([33/5, 1, -3])
        b_lo = np.array([41/10, -19/6, -7])
        expected = 1/(1/ag - b_hi/(2*math.pi)*math.log(ms/mg)
                      - b_lo/(2*math.pi)*math.log(mz/ms))
        np.testing.assert_allclose(run_one_loop_rge(mg, ms, mz, ag), expected, rtol=1e-7)
        with self.assertRaises(ValueError):
            run_one_loop_rge(mg, mz)

    def test_fallback_does_not_fabricate_zero_measurements(self):
        with patch.object(FastHPCKernel, '__init__', lambda self: setattr(self, 'lib', None)):
            kernel = FastHPCKernel()
            self.assertEqual(kernel.run_relaxation(10, 1, 2.5), (None, None, False))
            config = PhysicsConfig(N_NODES=10, N_LINKS=10, WALKERS=30, MAX_STEPS=101)
            report = OptimizedEngine(config).run_full_stack()
            self.assertFalse(report['Performance']['Kernel_Available'])
            self.assertIsNone(report['Diagnostics']['Phase_Mean'])
            self.assertFalse(report['Diagnostics']['Spectral_IR_Reliable'])
            self.assertIn('assumed', report['Diagnostics']['Unification'])

    def test_walk_reproducible_with_noninteger_labels(self):
        graph = nx.relabel_nodes(nx.cycle_graph(8), lambda n: f'n{n}')
        x = OptimizedSpectralDim.compute(graph, max_steps=101, walkers=100, seed=5)
        y = OptimizedSpectralDim.compute(graph, max_steps=101, walkers=100, seed=5)
        self.assertEqual(x, y)
        with self.assertRaises(ValueError):
            OptimizedSpectralDim.compute(nx.empty_graph(2))

    def test_kernel_deterministic_sum_when_available(self):
        kernel = FastHPCKernel()
        if kernel.lib is None:
            self.skipTest('compile optional C++ library to exercise kernel')
        n, beta = 1000, 2.5
        w, a, ok = kernel.run_relaxation(n, 4, beta)
        phases = np.arange(n)*2*math.pi/n
        self.assertTrue(ok)
        self.assertAlmostEqual(w, np.cos(phases*beta).mean(), places=12)
        self.assertAlmostEqual(a, -np.cos(phases).sum()*0.4, places=10)
        with self.assertRaises(ValueError):
            kernel.run_relaxation(0, 4, beta)


if __name__ == '__main__':
    unittest.main()
