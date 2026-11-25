"""Reproducible checks of selected claims from the pinned external documents.

Frozen benchmarks are illustrative conditional formulae, not demonstrated
predictions of this repository. Observational inputs are historical published
results, not an assertion that no newer result exists.
"""
from dataclasses import dataclass
from math import asin, degrees, exp, sqrt


@dataclass(frozen=True)
class FrozenInflationBenchmark:
    alpha: float = 3.75
    e_folds: float = 60.0
    gauge_fields: int = 45
    phi_squared_document: float = 0.32
    coefficient: float = 0.1

    @property
    def tensor_ratio(self):
        return 12 * self.alpha / self.e_folds**2

    @property
    def f_nl_document_expression(self):
        return self.gauge_fields * self.phi_squared_document * self.coefficient

    @property
    def f_nl_code_expression(self):
        # The referenced code instead names 0.32 phi_rms and squares it.
        return self.gauge_fields * self.phi_squared_document**2 * self.coefficient


def theta13_degrees(variance=0.262, mean_degree=4.0, wilson=0.688):
    sine = sqrt(variance) / mean_degree * wilson
    return degrees(asin(sine))


def holography_probability(n, c=0.33):
    return 1 - c / sqrt(n)


def spectral_dimension_ir(n, n_critical=150.0):
    return 4 * (1 - exp(-n / n_critical))


def lambda_length_dimensions():
    """Length exponents for the external Lambda derivation in natural units.

    N and the square bracket are dimensionless, [a] = L, and the cited
    expression is G=3/(2*pi*N*a**2), Lambda=8*pi*G/a**4*[...].
    Return both expression exponents and the expected physical dimensions.
    """
    g_expression = -2
    return {'G_expression': g_expression, 'G_expected': 2,
            'Lambda_expression': g_expression - 4, 'Lambda_expected': -2}


def main():
    bench = FrozenInflationBenchmark()
    print(f'r = {bench.tensor_ratio:.6g}; BK18 limit r_0.05 < 0.036 (95% CL)')
    print(f'f_NL = {bench.f_nl_document_expression:.6g} (written expression); '
          f'{bench.f_nl_code_expression:.6g} (code interpretation)')
    print('Planck 2018 f_NL^equil = -26 ± 47 (68% CL, statistical)')
    print(f'theta13 = {theta13_degrees():.4f} degrees')
    print(f'P_holography(120) = {holography_probability(120):.6f}')
    print(f'd_s_IR(150) = {spectral_dimension_ir(150):.6f}')
    print(f'Lambda dimensional audit (length exponents): {lambda_length_dimensions()}')
    print('These are arithmetic checks, not validated physical predictions.')


if __name__ == '__main__':
    main()
