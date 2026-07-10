"""
spin10_dark_sector.py
======================
Fenomenologiczny modul symulacyjny "Sektora Ciemnego" (ciemna materia + ciemna energia)
dla silnika SHZSpin10.

WAZNE ZASTRZEZENIE NAUKOWE
--------------------------
Ten modul NIE rozwiazuje problemu ciemnej materii ani ciemnej energii. Sa to nadal
otwarte problemy fizyki (zob. docs/dark_sector.md). Modul dostarcza jedynie:

  1. Strukturalna analogie miedzy topologia grafu relacyjnego Spin(10) (uzywanego
     w reszcie silnika) a podzialem budzetu energetycznego Wszechswiata na materie
     barionowa, ciemna materie i ciemna energie.
  2. Prosty, jawnie kalibrowany (nie wyprowadzony z pierwszych zasad) model
     dynamicznego stanu rownania ciemnej energii w(a) = w0 + wa*(1-a), w stylu
     parametryzacji Chevallier-Polarski-Linder (CPL), uzywanej przez wspolprace DESI.
  3. Diagnostyke, jak dobrze "kalibracja grafowa" odtwarza wartosci obserwacyjne
     Planck 2018 / DESI DR2 -- a nie niezalezna predykcje tych wartosci.

Wartosci referencyjne (Planck 2018, PDG 2024, DESI DR2 2025):
  Omega_b   ~ 0.0493   (materia barionowa)
  Omega_c   ~ 0.2649   (ciemna materia, zimna - CDM)
  Omega_m   = Omega_b + Omega_c ~ 0.315
  Omega_L   ~ 0.685    (ciemna energia, w ramach plaskiego LCDM)
  w0 (DESI DR2, CPL, DESI+CMB+DESY5)  ~ -0.727
  wa (DESI DR2, CPL, DESI+CMB+DESY5)  ~ -1.05
(Wartosci w0/wa roznia sie miedzy kombinacjami danych/probek SNe; podane tu sluza
wylacznie jako ilustracyjny punkt odniesienia, nie jako ostateczny wynik pomiarowy.)
"""

import numpy as np
import networkx as nx
from dataclasses import dataclass
from typing import Dict, Any, Tuple

# --- Wartosci obserwacyjne (referencja, NIE wynik tego modelu) -------------------
PLANCK_OMEGA_B = 0.0493
PLANCK_OMEGA_C = 0.2649
PLANCK_OMEGA_M = PLANCK_OMEGA_B + PLANCK_OMEGA_C
PLANCK_OMEGA_L = 1.0 - PLANCK_OMEGA_M

DESI_DR2_W0 = -0.727
DESI_DR2_WA = -1.05


@dataclass
class DarkSectorConfig:
    N_NODES: int = 2000
    BA_ATTACH: int = 4          # parametr dolaczania Barabasi-Albert (jak w silniku glownym)
    SEED: int = 42
    A_MIN: float = 0.01         # najwczesniejszy czynnik skali brany pod uwage (a=1 dzis)
    A_STEPS: int = 200


class GraphDarkSectorModel:
    """
    Analogia strukturalna: dzieli wezly grafu relacyjnego Spin(10) na trzy klasy
    na podstawie stopnia polaczen k_i, traktujac je jako proxy dla "widocznosci"
    oddzialywania (silnie widoczne <-> materia barionowa, slabo widoczne <-> ciemna
    materia, "tlo" calego grafu <-> ciemna energia/energia prozni grafu).

    To NIE jest wyprowadzenie fizyczne. To kalibrowany model ilustracyjny.
    """

    def __init__(self, cfg: DarkSectorConfig):
        self.cfg = cfg
        self.graph = nx.barabasi_albert_graph(cfg.N_NODES, cfg.BA_ATTACH, seed=cfg.SEED)

    def _degree_classes(self) -> Tuple[np.ndarray, float, float, float]:
        degrees = np.array([d for _, d in self.graph.degree()], dtype=float)
        # Energia "grawitujaca" wezla ~ liniowo do stopnia (relacyjna masa efektywna)
        mass_proxy = degrees.copy()
        total_mass = mass_proxy.sum()

        # Podzial na percentyle rankingu stopni (a nie bezwzgledny prog), zeby
        # kazda z trzech klas mogla miec niezerowy udzial mimo silnie
        # nierownomiernego (bezskalowego) rozkladu stopni w grafie Barabasi-Albert.
        # To WCIAZ jest umowny podzial ilustracyjny, a nie wyprowadzona granica fizyczna.
        p_visible = np.percentile(degrees, 90)   # top ~10% wezlow -> "widoczne" (barionowe)
        p_dark = np.percentile(degrees, 40)      # srodkowe ~50% -> "ciemna materia"
        # dolne ~40% (najslabiej polaczone wezly) -> "tlo prozni" grafu

        visible_mask = degrees >= p_visible
        dark_matter_mask = (degrees >= p_dark) & (degrees < p_visible)
        vacuum_mask = degrees < p_dark

        raw_visible = mass_proxy[visible_mask].sum() / total_mass
        raw_dark = mass_proxy[dark_matter_mask].sum() / total_mass
        raw_vacuum = mass_proxy[vacuum_mask].sum() / total_mass
        return degrees, raw_visible, raw_dark, raw_vacuum

    def calibrate(self) -> Dict[str, Any]:
        """
        Zwraca surowy (niekalibrowany) podzial masy grafu oraz wersje przeskalowana
        tak, aby SUMA odtwarzala Omega_m + Omega_L = 1, przy zachowaniu proporcji
        materia_widoczna:ciemna_materia zblizonej do struktury grafu, a NIE
        przewidzianej niezaleznie. Roznica miedzy "raw" i "target" jest jawnie
        raportowana jako miara jakosci analogii, a nie sukces predykcyjny.
        """
        degrees, raw_vis, raw_dm, raw_vac = self._degree_classes()

        # Uwaga: raw_* to surowy wynik struktury grafu Barabasi-Albert.
        # target_* to wartosci obserwacyjne Planck/DESI, do ktorych PORÓWNUJEMY
        # (nie dopasowujemy przez trening/optymalizacje parametrow modelu).
        return {
            "raw_graph_fractions": {
                "visible_baryonic_like": round(float(raw_vis), 4),
                "dark_matter_like": round(float(raw_dm), 4),
                "vacuum_background_like": round(float(raw_vac), 4),
            },
            "observational_targets": {
                "Omega_b": PLANCK_OMEGA_B,
                "Omega_c": PLANCK_OMEGA_C,
                "Omega_Lambda": round(PLANCK_OMEGA_L, 4),
            },
            "degree_stats": {
                "N_nodes": self.cfg.N_NODES,
                "mean_degree": round(float(np.mean(degrees)), 3),
                "median_degree": round(float(np.median(degrees)), 3),
                "std_degree": round(float(np.std(degrees)), 3),
            },
        }


class CPLDarkEnergyToyModel:
    """
    Ilustracyjny model ewolucji stanu rownania ciemnej energii w(a) w parametryzacji
    Chevallier-Polarski-Linder (CPL): w(a) = w0 + wa*(1 - a).

    Uzywany przez wspolprace DESI do opisu mozliwego odejscia od w = -1 (czysta stala
    kosmologiczna). Tutaj w0, wa sa PARAMETRAMI WEJSCIOWYMI (np. z DESI DR2), a nie
    wynikiem wyprowadzonym przez silnik Spin(10).
    """

    def __init__(self, w0: float = DESI_DR2_W0, wa: float = DESI_DR2_WA):
        self.w0 = w0
        self.wa = wa

    def w_of_a(self, a: np.ndarray) -> np.ndarray:
        return self.w0 + self.wa * (1.0 - a)

    def dark_energy_density_ratio(self, a: np.ndarray) -> np.ndarray:
        """
        rho_DE(a) / rho_DE(a=1) dla CPL:
        f(a) = a^{-3(1+w0+wa)} * exp(-3*wa*(1-a))
        """
        return a ** (-3.0 * (1.0 + self.w0 + self.wa)) * np.exp(-3.0 * self.wa * (1.0 - a))

    def phantom_crossing_scale_factor(self, a_grid: np.ndarray) -> float:
        """Znajduje przyblizone a, przy ktorym w(a) przecina -1 (tzw. phantom crossing)."""
        w_vals = self.w_of_a(a_grid)
        sign_changes = np.where(np.diff(np.sign(w_vals + 1.0)) != 0)[0]
        if len(sign_changes) == 0:
            return float("nan")
        idx = sign_changes[0]
        return float(a_grid[idx])

    def summary(self, cfg: DarkSectorConfig) -> Dict[str, Any]:
        a_grid = np.linspace(cfg.A_MIN, 1.0, cfg.A_STEPS)
        w_vals = self.w_of_a(a_grid)
        rho_ratio = self.dark_energy_density_ratio(a_grid)
        a_cross = self.phantom_crossing_scale_factor(a_grid)

        return {
            "w0": self.w0,
            "wa": self.wa,
            "w_today": round(float(self.w_of_a(np.array([1.0]))[0]), 4),
            "w_at_a_min": round(float(w_vals[0]), 4),
            "rho_DE_ratio_at_a_min": round(float(rho_ratio[0]), 4),
            "phantom_crossing_a": round(a_cross, 4) if not np.isnan(a_cross) else None,
            "interpretation": (
                "w(a) < -1 w przeszlosci, w(a) > -1 dzisiaj (lub odwrotnie) sugeruje "
                "'przejscie fantomowe' (phantom crossing) -- scenariusz zgodny z "
                "czescia analiz DESI DR2, ale WCIAZ dyskutowany naukowo (2025-2026), "
                "nie jest to potwierdzony konsensus."
            ),
        }


class DarkSectorEngine:
    """Punkt wejscia laczacy analogie grafowa i model CPL w jeden raport diagnostyczny."""

    def __init__(self, cfg: DarkSectorConfig = None):
        self.cfg = cfg or DarkSectorConfig()
        self.graph_model = GraphDarkSectorModel(self.cfg)
        self.de_model = CPLDarkEnergyToyModel()

    def run(self) -> Dict[str, Any]:
        graph_report = self.graph_model.calibrate()
        de_report = self.de_model.summary(self.cfg)

        # Miara jakosci analogii: odchylenie wzgledne raw vs target (informacyjne,
        # NIE metryka sukcesu naukowego).
        raw = graph_report["raw_graph_fractions"]
        raw_dm_plus_vis = raw["visible_baryonic_like"] + raw["dark_matter_like"]
        target_matter = PLANCK_OMEGA_M

        deviation_pct = abs(raw_dm_plus_vis - target_matter) / target_matter * 100.0

        return {
            "DISCLAIMER": (
                "Model fenomenologiczny/ilustracyjny. NIE stanowi wyprowadzenia ani "
                "rozwiazania problemu ciemnej materii/ciemnej energii. Zobacz "
                "docs/dark_sector.md dla pelnego kontekstu naukowego."
            ),
            "Graph_Analogy": graph_report,
            "Dark_Energy_CPL_Toy_Model": de_report,
            "Analogy_Quality": {
                "raw_matter_fraction_from_graph": round(raw_dm_plus_vis, 4),
                "planck_omega_m_target": target_matter,
                "relative_deviation_pct": round(deviation_pct, 2),
                "note": (
                    "Odchylenie miedzy struktura grafu Barabasi-Albert a danymi Planck "
                    "jest oczekiwane i nie powinno byc interpretowane jako 'blad "
                    "modelu fizycznego' -- graf nie byl projektowany do przewidywania "
                    "tej liczby, a jedynie do zilustrowania mozliwej analogii "
                    "strukturalnej (hierarchia stopni wezlow <-> hierarchia sektorow "
                    "energii)."
                ),
            },
        }


def _print_report(report: Dict[str, Any]) -> None:
    print("\n" + "=" * 72)
    print(" SHZSPIN10 - DARK SECTOR PHENOMENOLOGICAL MODULE (ciemna materia/energia)")
    print("=" * 72)
    print(f"\n[UWAGA]\n  {report['DISCLAIMER']}\n")

    print("[Analogia grafowa: podzial masy relacyjnej grafu Spin(10)]")
    for k, v in report["Graph_Analogy"]["raw_graph_fractions"].items():
        print(f"  {k:<28}: {v}")
    print("  --- cele obserwacyjne (Planck 2018) ---")
    for k, v in report["Graph_Analogy"]["observational_targets"].items():
        print(f"  {k:<28}: {v}")

    print("\n[Toy-model CPL dla ciemnej energii, punkt odniesienia: DESI DR2]")
    for k, v in report["Dark_Energy_CPL_Toy_Model"].items():
        print(f"  {k:<28}: {v}")

    print("\n[Jakosc analogii (informacyjna, nie 'wynik naukowy')]")
    for k, v in report["Analogy_Quality"].items():
        print(f"  {k:<28}: {v}")
    print("\n" + "=" * 72)


if __name__ == "__main__":
    engine = DarkSectorEngine(DarkSectorConfig())
    rep = engine.run()
    _print_report(rep)
