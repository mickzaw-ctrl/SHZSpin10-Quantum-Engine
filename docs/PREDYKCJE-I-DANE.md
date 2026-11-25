# Zamrożone benchmarki i porównanie z danymi

Wersja porównania: 2026-11-25; źródłowa dokumentacja modelu przypięta do
[`53ecbfd`](https://github.com/mickzaw-ctrl/spin10-toe/tree/53ecbfd65436d51e6aa8c684612caef2951b7860).
Nie wykonano dopasowania ani skanowania parametrów. Poniższe benchmarki są
ustalone **po opublikowaniu** wyników eksperymentalnych: nie są ślepą,
przedrejestrowaną prognozą ani wykazanym następstwem dynamiki grafu. Niepewność
teoretyczna w obu przypadkach nie została wyznaczona.

## 1. Inflacyjny stosunek tensorowy r

- Zamrożone wejścia: α=3,75, N=60 e-foldów; wzór r=12α/N². Wynik **r=0,0125**.
- Źródło: [Publikacja III, sekcja 1](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/publikacja-III-trylogia.md#L28-L56).
  Wzór jest warunkowym przybliżeniem α-attractor, a identyfikacja α z wymiarem
  algebry nie została tu wyprowadzona. Wartość r zmienia się wraz z α i N.
- [BICEP/Keck XIII (2021)](https://arxiv.org/abs/2110.00483): r₀.₀₅ < 0,036
  przy 95% CL, przy opisanych w pracy założeniach analizy i skali odniesienia
  0,05 Mpc⁻¹. Zakładamy zgodność skali/modelu dla orientacyjnego porównania.
- **Wniosek:** benchmark znajduje się poniżej tej historycznej granicy; to
  zgodność z ograniczeniem, nie detekcja, dowód modelu ani obliczenie istotności.
  Nie twierdzimy, że jest to najnowsza dostępna granica.

## 2. Równoboczne f_NL

- Zamrożone wejścia według [Publikacji IV](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/publikacja-IV-tetralogia.md#L154-L170):
  liczba pól 45, wpisane 0,32 i czynnik 0,1. Dosłownie zapisane mnożenie daje
  **1,44**. Interpretacja [kodu](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/src/spin10_engine.py#L498-L505),
  w którym φ_rms=0,32 jest kwadratem w równaniu, daje **0,4608**. Sprzeczności
  nie rozstrzygnięto; ani jedna wartość nie wynika z pełnego rachunku bispektrum.
- [Planck Collaboration 2018, wyniki IX (2020)](https://doi.org/10.1051/0004-6361/201935891):
  f_NL^equil = −26 ± 47 (68% CL, statystyczne, temperatura + polaryzacja).
  To nie jest wartość −26 ± 117 z manifestu. Dla porównania szablonów i
  wieloskładnikowego kształtu wymagana jest właściwa projekcja i kowariancja.
- **Wniosek:** obie liczby są w przybliżeniu wewnątrz ±1σ od wartości centralnej
  dla uproszczonego porównania tego samego szablonu. To nie potwierdza modelu;
  przy nieznanej niepewności teorii nie wyznaczamy jej istotności ani nie
  prognozujemy przyszłego SNR.

Obliczenia arytmetyczne i niezmienność domyślnego zestawu wejść sprawdzają
`scientific_checks.py` i `tests/test_scientific_checks.py`. Test nie jest
analizą danych eksperymentalnych.
