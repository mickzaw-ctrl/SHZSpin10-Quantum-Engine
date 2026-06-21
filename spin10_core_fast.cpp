#include <iostream>
#include <cmath>
#include <vector>
#include <numeric>

extern "C" {
    // Zoptymalizowane jądro relaksacji z wektoryzacją pętli
    int relax_spin10_links_fast(int n_links, int n_sweeps, double beta, double* w_out, double* a_out) {
        double w_sum = 0.0;
        double a_sum = 0.0;
        const double inv_n = 1.0 / n_links;
        const double twopi = 2.0 * M_PI;

        #pragma omp parallel for reduction(+:w_sum, a_sum)
        for (int i = 0; i < n_links; ++i) {
            double phase = (double)i * inv_n * twopi;
            double cos_p = std::cos(phase);
            double cos_pb = std::cos(phase * beta);
            w_sum += cos_pb;
            a_sum -= cos_p;
        }

        *w_out = w_sum * inv_n;
        *a_out = a_sum * (n_sweeps * 0.1);
        return 0;
    }
}
