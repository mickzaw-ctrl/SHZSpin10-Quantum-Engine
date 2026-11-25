"""A finite graph Dirac operator for reproducible mathematical checks.

This is the incidence (discrete de Rham) Dirac operator, NOT a four-dimensional
chiral Spin(10) fermion operator. Its index is the graph Euler characteristic,
not a prediction of the number of physical fermion generations.
"""
import numpy as np
import networkx as nx


def incidence_dirac(graph):
    """Return D, grading Gamma and incidence matrix B on C^V ⊕ C^E.

    Each undirected edge is oriented according to NetworkX's edge iteration;
    reversing an orientation changes a basis sign but not the index. B maps
    edges to vertices, D = [[0,B],[B†,0]], Gamma = diag(+I_V,-I_E).
    """
    if graph.is_directed() or graph.is_multigraph() or nx.number_of_selfloops(graph):
        raise ValueError('Expected an undirected simple graph without self-loops')
    nodes = list(graph.nodes())
    edges = list(graph.edges())
    row = {node: i for i, node in enumerate(nodes)}
    B = np.zeros((len(nodes), len(edges)), dtype=float)
    for j, (u, v) in enumerate(edges):
        B[row[u], j], B[row[v], j] = -1.0, 1.0
    D = np.block([[np.zeros((len(nodes), len(nodes))), B],
                  [B.T, np.zeros((len(edges), len(edges)))]])
    gamma = np.diag([1.0] * len(nodes) + [-1.0] * len(edges))
    return D, gamma, B


def incidence_index(graph, tolerance=None):
    """Numerically return dim ker(B†) - dim ker(B), with rank tolerance.

    The nonzero eigenvalues of the full D do not contribute to its graded
    index. For this rectangular B, the two graded kernels have dimensions
    |V|-rank(B) and |E|-rank(B). The finite-dimensional index is |V|-|E|.
    """
    _, _, B = incidence_dirac(graph)
    singular_values = np.linalg.svd(B, compute_uv=False)
    if tolerance is None:
        largest = float(singular_values[0]) if singular_values.size else 0.0
        tolerance = max(B.shape, default=0) * np.finfo(float).eps * largest
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError('tolerance must be finite and nonnegative')
    rank = int(np.count_nonzero(singular_values > tolerance))
    n_vertex, n_edge = B.shape
    return {'rank': rank, 'positive_zero_modes': n_vertex - rank,
            'negative_zero_modes': n_edge - rank,
            'index': (n_vertex - rank) - (n_edge - rank),
            'tolerance': float(tolerance)}


if __name__ == '__main__':
    for name, graph in [('path_4', nx.path_graph(4)), ('cycle_4', nx.cycle_graph(4)),
                        ('star_degree_4', nx.star_graph(4)),
                        ('three_disconnected_vertices', nx.empty_graph(3))]:
        print(name, incidence_index(graph))
