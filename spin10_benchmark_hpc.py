import time
import numpy as np
import json
import matplotlib.pyplot as plt
from spin10_optimized import OptimizedEngine, PhysicsConfig

class Spin10HPCBenchmark:
    """
    Oficjalny pakiet benchmarkujący wydajność silnika SHZSpin10 v14.4.
    Przeznaczony do generowania raportów wydajnościowych dla NVIDIA HPC Team.
    """
    
    def __init__(self):
        self.results = []

    def run_benchmark_suite(self):
        # Definicja skali testów (od 100k do 10M połączeń)
        link_scales = [100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]
        
        print("="*80)
        print(f" STARTING HPC BENCHMARK: SHZSpin10 v14.4-OPTIMIZED")
        print(f" Platform: {np.show_config() or 'Standard Linux Cluster'}")
        print("="*80)
        print(f"{'N Links':<15} | {'Exec Time [s]':<15} | {'Giga-OPS':<15} | {'Alpha_s':<10}")
        print("-" * 80)

        for n_links in link_scales:
            # Konfiguracja pod konkretną skalę
            config = PhysicsConfig(N_LINKS=n_links, N_NODES=max(100, n_links // 10000))
            engine = OptimizedEngine(config)
            
            # Warm-up (pominiecie JIT / cache effects)
            engine.run_full_stack()
            
            # Rzeczywisty pomiar (średnia z 3 prób)
            times = []
            for _ in range(3):
                t_start = time.perf_counter()
                report = engine.run_full_stack()
                t_end = time.perf_counter()
                times.append(t_end - t_start)
            
            avg_time = np.mean(times)
            giga_ops = (n_links * 100) / (avg_time * 1e9) # 100 operacji na link
            
            res = {
                "n_links": n_links,
                "avg_time": avg_time,
                "giga_ops": giga_ops,
                "alpha_s": report['Physics']['Alpha_s_MZ']
            }
            self.results.append(res)
            
            print(f"{n_links:<15,} | {avg_time:<15.4f} | {giga_ops:<15.2f} | {res['alpha_s']:<10.4f}")

    def generate_report(self):
        # 1. Zapis wyników do JSON
        with open("hpc_benchmark_results.json", "w") as f:
            json.dump(self.results, f, indent=4)
        
        # 2. Generowanie wykresu skalowania
        n_links = [r['n_links'] for r in self.results]
        gops = [r['giga_ops'] for r in self.results]
        
        plt.figure(figsize=(10, 6))
        plt.plot(n_links, gops, 'o-', color='green', lw=2, markersize=8)
        plt.xscale('log')
        plt.title("HPC Performance Scaling: SHZSpin10 ToE Kernel")
        plt.xlabel("Number of Gravitational Links (N)")
        plt.ylabel("Performance [Giga-OPS]")
        plt.grid(True, which="both", ls="-", alpha=0.2)
        plt.savefig("hpc_performance_scaling.png")
        
        print("\n" + "="*80)
        print(" BENCHMARK COMPLETE")
        print(f" Peak Performance: {max(gops):.2f} Giga-OPS")
        print(" Files generated: hpc_benchmark_results.json, hpc_performance_scaling.png")
        print("="*80)

if __name__ == "__main__":
    bench = Spin10HPCBenchmark()
    bench.run_benchmark_suite()
    bench.generate_report()
