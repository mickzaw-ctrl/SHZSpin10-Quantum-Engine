"""Exploratory graph, deterministic kernel, and one-loop RGE diagnostics.

None of these routines establishes a Spin(10) quantum-gravity prediction.
"""
from dataclasses import dataclass
from pathlib import Path
import ctypes
import time

import networkx as nx
import numpy as np
from scipy.integrate import solve_ivp


@dataclass
class PhysicsConfig:
    M_GUT: float = 2.1e16  # GeV, assumed input
    M_SUSY: float = 5000.0  # GeV, assumed threshold
    GAMMA: float = 0.2739  # unused
    N_NODES: int = 500
    N_LINKS: int = 5000000
    SEED: int = 42
    WALKERS: int = 10000
    MAX_STEPS: int = 200


class FastHPCKernel:
    """Optional C++ deterministic phase sum; not a Monte Carlo simulation."""
    def __init__(self):
        self.lib = None
        path = Path(__file__).resolve().with_name('libspin10_fast.so')
        if path.exists():
            self.lib = ctypes.CDLL(str(path))
            self.lib.relax_spin10_links_fast.argtypes = [
                ctypes.c_int, ctypes.c_int, ctypes.c_double,
                ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
            self.lib.relax_spin10_links_fast.restype = ctypes.c_int

    def run_relaxation(self, n_links, sweeps, beta):
        if n_links <= 0 or sweeps < 0:
            raise ValueError('n_links must be positive and sweeps nonnegative')
        if self.lib is None:
            return None, None, False
        w, a = ctypes.c_double(), ctypes.c_double()
        status = self.lib.relax_spin10_links_fast(n_links, sweeps, beta,
                                                  ctypes.byref(w), ctypes.byref(a))
        if status != 0:
            raise RuntimeError(f'kernel failed with status {status}')
        return w.value, a.value, True


class OptimizedSpectralDim:
    """Finite random-walk slope; a slope alone does not establish an IR plateau."""
    @staticmethod
    def compute(G, max_steps=200, walkers=10000, seed=42):
        if max_steps < 101 or walkers <= 0 or not G or not nx.is_connected(G):
            raise ValueError('need a nonempty connected graph, >=101 steps and positive walkers')
        nodes = list(G.nodes())
        index = {node: i for i, node in enumerate(nodes)}
        adj = [np.array([index[n] for n in G.neighbors(node)], dtype=np.int32)
               for node in nodes]
        if any(len(neighbors) == 0 for neighbors in adj):
            raise ValueError('isolated nodes are unsupported')
        rng = np.random.default_rng(seed)
        pos = rng.integers(0, len(nodes), size=walkers, dtype=np.int32)
        start_pos = pos.copy()
        p_return = np.zeros(max_steps)
        for t in range(max_steps):
            for i in np.flatnonzero(rng.random(walkers) > 0.5):
                neighbors = adj[pos[i]]
                pos[i] = neighbors[rng.integers(len(neighbors))]
            p_return[t] = np.mean(pos == start_pos)
        if np.any(p_return[10:100] == 0):
            return None  # cannot fit logarithms of unobserved return probabilities
        slope = np.polyfit(np.log(np.arange(1, max_steps + 1))[10:100],
                           np.log(p_return[10:100]), 1)[0]
        return float(-2 * slope)


def run_one_loop_rge(m_gut, m_susy, m_z=91.18, alpha_gut=0.0381):
    """Integrate a toy one-loop SM/MSSM flow, with a continuous threshold.

    The high-scale equality and threshold are inputs, not tested unification;
    no threshold corrections, split spectrum, uncertainties or fitting.
    """
    if not (0 < m_z < m_susy < m_gut and alpha_gut > 0):
        raise ValueError('require 0 < M_Z < M_SUSY < M_GUT and positive alpha_GUT')
    g = np.full(3, np.sqrt(4*np.pi*alpha_gut))
    for start, end, coefficients in [
        (m_gut, m_susy, [33/5, 1, -3]),
        (m_susy, m_z, [41/10, -19/6, -7]),
    ]:
        b = np.array(coefficients)
        sol = solve_ivp(lambda t, y: b*y**3/(16*np.pi**2),
                        (np.log(start), np.log(end)), g, rtol=1e-9, atol=1e-11)
        if not sol.success or not np.all(np.isfinite(sol.y[:, -1])):
            raise RuntimeError(f'RGE integration failed: {sol.message}')
        g = sol.y[:, -1]
    return g**2 / (4*np.pi)


class OptimizedEngine:
    def __init__(self, config: PhysicsConfig):
        if config.N_NODES <= 4:
            raise ValueError('Barabasi-Albert m=4 requires N_NODES > 4')
        self.cfg = config
        self.hpc = FastHPCKernel()
        # BA parameter m=4 means roughly eight neighbours on average, not four.
        self.graph = nx.barabasi_albert_graph(config.N_NODES, 4, seed=config.SEED)

    def run_full_stack(self):
        t0 = time.perf_counter()
        phase_mean, phase_action, hpc_ok = self.hpc.run_relaxation(self.cfg.N_LINKS, 100, 2.5)
        slope = OptimizedSpectralDim.compute(self.graph, max_steps=self.cfg.MAX_STEPS,
                                             walkers=self.cfg.WALKERS, seed=self.cfg.SEED)
        couplings = run_one_loop_rge(self.cfg.M_GUT, self.cfg.M_SUSY)
        return {
            'Performance': {
                'Backend': 'C++ deterministic phase sum' if hpc_ok else 'unavailable',
                'Exec_Time_s': time.perf_counter() - t0,
                'Kernel_Available': hpc_ok,
            },
            'Diagnostics': {
                'Phase_Mean': phase_mean,
                'Phase_Action_Sum': phase_action,
                'Random_Walk_Slope_11_100': slope,
                'Spectral_IR_Reliable': False,
                'Spectral_IR_Reason': 'fixed late-time window is not validated against finite-size saturation',
                'Mean_Graph_Degree': 2*self.graph.number_of_edges()/self.graph.number_of_nodes(),
                'Alpha_s_MZ_One_Loop_Toy': float(couplings[2]),
                'Unification': 'assumed at M_GUT, not tested',
                'Uncertainty': 'not estimated',
            },
        }


if __name__ == '__main__':
    report = OptimizedEngine(PhysicsConfig()).run_full_stack()
    for section, data in report.items():
        print(f'\n[{section}]')
        for key, value in data.items():
            print(f'  {key}: {value}')
