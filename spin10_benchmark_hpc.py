"""Measure deterministic kernel wall time and link visits, not FLOPS/GigaOPS."""
import time
from spin10_optimized import FastHPCKernel


def main():
    kernel = FastHPCKernel()
    if kernel.lib is None:
        raise SystemExit('Compile libspin10_fast.so first; no Python kernel fallback is implemented.')
    print('Deterministic phase sum; sweeps scale an output, not loop iterations.')
    print(f'{"links":>12} {"mean seconds":>14} {"million link visits/s":>24}')
    for n in [100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]:
        kernel.run_relaxation(n, 100, 2.5)
        times = []
        for _ in range(3):
            start = time.perf_counter()
            kernel.run_relaxation(n, 100, 2.5)
            times.append(time.perf_counter() - start)
        mean = sum(times)/len(times)
        print(f'{n:12,d} {mean:14.6f} {n/mean/1e6:24.3f}')


if __name__ == '__main__':
    main()
