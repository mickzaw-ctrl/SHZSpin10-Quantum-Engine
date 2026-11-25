import math
import unittest
from dataclasses import FrozenInstanceError

import numpy as np
import networkx as nx

from graph_dirac import incidence_dirac, incidence_index
from scientific_checks import (FrozenInflationBenchmark, theta13_degrees,
                               holography_probability, spectral_dimension_ir, lambda_length_dimensions)


class ArithmeticTests(unittest.TestCase):
    def test_theta13_and_formulae(self):
        self.assertAlmostEqual(theta13_degrees(), 5.0508, delta=0.0001)
        self.assertAlmostEqual(holography_probability(120), 0.969875, places=5)
        self.assertAlmostEqual(spectral_dimension_ir(150), 4*(1-math.exp(-1)))
        self.assertAlmostEqual(-6.23 + 125*0.05, 0.02)

    def test_frozen_benchmarks(self):
        b = FrozenInflationBenchmark()
        self.assertAlmostEqual(b.tensor_ratio, 0.0125)
        self.assertAlmostEqual(b.f_nl_document_expression, 1.44)
        self.assertAlmostEqual(b.f_nl_code_expression, 0.4608)
        self.assertLess(b.tensor_ratio, 0.036)  # published upper limit, not evidence
        with self.assertRaises(FrozenInstanceError):
            b.alpha = 4

    def test_lambda_dimensions_expose_external_inconsistency(self):
        dims = lambda_length_dimensions()
        self.assertEqual(dims, {'G_expression': -2, 'G_expected': 2,
                                'Lambda_expression': -6, 'Lambda_expected': -2})
        self.assertNotEqual(dims['G_expression'], dims['G_expected'])
        self.assertNotEqual(dims['Lambda_expression'], dims['Lambda_expected'])

    def test_yang_mills_classical_trace(self):
        # Euclidean antisymmetric field, flat metric: Tr(T)=F_ab F_ab - 4/4 F_ab F_ab.
        F = np.array([[0., 2., -1., 3.], [-2., 0., 4., 2.],
                      [1., -4., 0., -5.], [-3., -2., 5., 0.]])
        T = F @ F.T - np.eye(4) * np.sum(F*F)/4
        self.assertAlmostEqual(np.trace(T), 0)


class GraphDiracTests(unittest.TestCase):
    def test_dirac_properties_and_index(self):
        for G, expected in [(nx.path_graph(4), 1), (nx.cycle_graph(4), 0),
                            (nx.star_graph(4), 1), (nx.empty_graph(3), 3)]:
            with self.subTest(nodes=G.number_of_nodes(), edges=G.number_of_edges()):
                D, gamma, B = incidence_dirac(G)
                np.testing.assert_allclose(D, D.T)
                np.testing.assert_allclose(D @ gamma + gamma @ D, 0, atol=1e-14)
                result = incidence_index(G)
                self.assertEqual(result['index'], expected)
                self.assertEqual(result['positive_zero_modes'] - result['negative_zero_modes'], expected)
                self.assertEqual(expected, G.number_of_nodes()-G.number_of_edges())

    def test_invariance_under_relabeling(self):
        G = nx.cycle_graph(5)
        H = nx.relabel_nodes(G, {i: f'node-{4-i}' for i in G})
        self.assertEqual(incidence_index(G)['index'], incidence_index(H)['index'])

    def test_invalid_inputs(self):
        for G in [nx.DiGraph([(0, 1)]), nx.MultiGraph([(0, 1)]), nx.Graph([(0, 0)])]:
            with self.assertRaises(ValueError):
                incidence_index(G)
        with self.assertRaises(ValueError):
            incidence_index(nx.path_graph(2), tolerance=-1)


if __name__ == '__main__':
    unittest.main()
