# Audyt naukowy: status, zakres i odtwarzalność

Data opracowania: 2026-11-25. Punktem odniesienia jest [spin10-toe, commit
`53ecbfd65436d51e6aa8c684612caef2951b7860`](https://github.com/mickzaw-ctrl/spin10-toe/tree/53ecbfd65436d51e6aa8c684612caef2951b7860).
To **inne repozytorium** niż bieżące `SHZSpin10-Quantum-Engine`. Plików
`REMEDIA`, manifestów i `FIXES.md` nie ma na bieżącej gałęzi; ich oryginały
nie zostały tu zmienione. Niniejsze pliki są **sprostowaniem**, nie nową wersją
tamtych dokumentów. Nie obejmuje to pełnego audytu publikacji PDF ani wszystkich
wartości numerycznych i symulacji w zewnętrznym repozytorium.

## Klasyfikacja twierdzeń

| Element i wartość | Kategoria / źródło | Zależność i niepewność | Weryfikacja/status |
|---|---|---|---|
| N=150, Var(k)=0,262, W=0,688 | [historyczne wartości raportu](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/wyprowadzenie-stalej-kosmologicznej.md#L21-L33) | Zależą od dynamiki, liczby kroków i ziarna; błędy MC, autokorelacja i zbieżność nie podane w tym zestawieniu | Nie reprodukowano tu; nie są dowodem emergentnej geometrii |
| N=60 e-foldów, α=3,75 | [założenia benchmarku inflacyjnego](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/publikacja-III-trylogia.md#L28-L56) | r=12α/N²; bez wyprowadzonej niepewności α, N i reheatingu | Warunkowy przykład, nie ustalona predykcja grafu; zob. `PREDYKCJE-I-DANE.md` |
| \(f_{NL}\): 45, 0,32, 0,1 | [wpisane parametry / wyrażenie](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/publikacja-IV-tetralogia.md#L154-L170) | Zapis w dokumencie daje 1,44; [kod](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/src/spin10_engine.py#L498-L505) traktuje 0,32 jako φ_rms i kwadratuje: 0,4608. Niepewność i uzasadnienie brak | Żadna interpretacja nie daje podanych 14,5189; żadna nie jest wyprowadzoną predykcją |
| θ₁₃ przy Var=0,262, k=4, W=0,688 | [wyrażenie w dokumencie](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/trzy-generacje-E8-predykcje.md#L109-L124) | θ=asin(√Var/k·W)=5,0508°, nie 8,8°; niepewność niewyznaczona | Poprawiony rachunek w `scientific_checks.py` |
| P_holografia(120), c=0,33 | [założony wzór](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/KLUCZOWE-REMEDIA.md#L156-L179) | 1−c/√N = 0,969875, nie 0,67; niepewność dopasowania brak | Sprzeczność z tabelą; wzór nie udowadnia holografii |
| d_S,IR(150), N_c=150 | ten sam dokument | 4(1−exp(−N/N_c))=2,52848, nie 3,3 ani 4; niepewność brak | Nie potwierdza tabeli; nowy audyt opisuje saturację skończonego grafu |
| 125 multipletów: −6,23+125·0,05 | [remedium](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/KLUCZOWE-REMEDIA.md#L111-L138) | +0,02 przy zaokrąglonych wejściach, nie 0; dokładności wkładów nie podano | Liczba pól jest całkowita; dokładne zerowanie i fizyczna konieczność nie zostały wykazane |
| Λ i G_N | [wyprowadzenie](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/docs/wyprowadzenie-stalej-kosmologicznej.md#L79-L102) | W jednostkach ħ=c=1: [G_N]=L², [ρ]=L⁻⁴, [Λ]=L⁻². Wzór G_N ∝ (N a²)⁻¹ ma wymiar L⁻². Klasyczny ślad YM w 4D wynosi zero | Wzór wymaga nowego wyprowadzenia; możliwa anomalia kwantowa nie wynika z klasycznego tensora. Nie udajemy jej obliczenia |
| Bazowy kod niniejszej gałęzi: M_GUT=2,1×10¹⁶ GeV, M_SUSY=5×10³ GeV, α_GUT=0,0381 | Wpisane założenia `PhysicsConfig` i `run_one_loop_rge` | Wynik zależy od obu skal, α_GUT i przyjętych β; brak błędu, korekt progowych i dopasowania | Jednopętlowy model zabawkowy. Równość sprzężeń na GUT to wejście, nie test unifikacji |
| Graf BA, m=4 | Implementacja `OptimizedEngine` | Średni stopień ≈ 2m przy dużym N, nie 4; zależy od N i ziarna | Stałe okno 11–100 daje tylko nachylenie diagnostyczne; brak wykazanego plateau IR |

## Aktualizacja statusu REMEDIA i manifestów

W miejsce mocnych stwierdzeń pierwotnych dokumentów obowiązuje tu następujący
status. Jest zgodny z zakresem ustaleń opublikowanego [FIXES.md](https://github.com/mickzaw-ctrl/spin10-toe/blob/53ecbfd/FIXES.md),
ale nie przyjmuje automatycznie jego pozostałych ocen jako niezależnie sprawdzonych:

1. **Baryogeneza — otwarta.** Czynnik wzmocnienia 3-flavour był kalibrowany;
   nie przedstawiono tu odtwarzalnego rozwiązania układu Boltzmanna ani bilansu
   niepewności. Dopasowania nie wolno nazywać przewidywaniem.
2. **Anomalia Weyla — otwarta.** Rachunek wkładów, zależność od tła i warunki
   anulowania wymagają osobnego wyprowadzenia; dokładne zero nie wynika z tabeli.
3. **Holografia i wymiar spektralny — otwarte.** Ekstrapolacje do N=10⁶ nie są
   wynikami zrealizowanej symulacji ani dowodem granicy ciągłej. Wymagane są
   wyniki na kilku rozmiarach, kontrola okien dyfuzji i niepewności.
4. **Split-SUSY — alternatywna hipoteza.** Zmiana parametru masy jest zmianą
   benchmarku, nie dowodem zgodności kompletnego modelu. Granice eksperymentów
   zależą od widma i kanału rozpadu.
5. **Manifesty testów — hipotezy warunkowe.** Wybranie wartości i porównanie
   jej z granicą nie dowodzi modelu; do istotności σ potrzebna jest analiza
   likelihood, tła, ekspozycji i niepewności. Brak sygnału testuje wyłącznie
   ściśle określony benchmark w granicach założeń eksperymentu.

## Weryfikacja lokalna

```sh
python -m pip install -r requirements.txt
python scientific_checks.py
python graph_dirac.py
python -m unittest discover -s tests -v
```

Testy sprawdzają arytmetykę, klasyczny ślad YM, przykładową konstrukcję Diraca,
RGE 1-loop i właściwości kodu. Nie dowodzą wyprowadzeń fizycznych ani nie
odtwarzają zewnętrznych symulacji. Opcjonalna biblioteka C++ wymaga kompilacji
opisanej w README; bez niej jej test jest pomijany.
