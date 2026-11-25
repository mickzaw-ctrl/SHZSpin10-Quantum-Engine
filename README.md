# SHZSpin10 — eksperymentalny silnik grafowy

Repozytorium zawiera prototypowe narzędzia numeryczne i kontrolne inspirowane
modelem grafowym Spin(10). **Nie stanowi obecnie potwierdzonej teorii
wszystkiego** ani dowodu emergencji czasoprzestrzeni, trzech generacji lub
stałych fizycznych. Bieżący kod jest narzędziem eksploracyjnym; jego wyniki i
założenia należy rozróżniać od danych eksperymentalnych.

## Audyt i dokumentacja

- [Audyt, pochodzenie liczb i status REMEDIA](docs/AUDYT-I-STATUS.md)
- [Dwa zamrożone benchmarki i porównanie z analizami eksperymentów](docs/PREDYKCJE-I-DANE.md)
- [Odtwarzalny przykład operatora Diraca na grafie](docs/OPERATOR-DIRACA.md)
- [Zakres i ograniczenia implementacji](whitepaper.md)

Poprzednio analizowane dokumenty `REMEDIA`, manifesty i `FIXES.md` znajdują się
w **innym** repozytorium, [spin10-toe](https://github.com/mickzaw-ctrl/spin10-toe).
Lokalny audyt odsyła do jego konkretnego commitu. Nie zmodyfikowano tam oryginałów.

## Instalacja i uruchomienie

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scientific_checks.py
python graph_dirac.py
python -m unittest discover -s tests -v
```

Opcjonalny kod C++:

```sh
g++ -O2 -shared -fPIC -fopenmp -o libspin10_fast.so spin10_core_fast.cpp
python spin10_optimized.py
python spin10_benchmark_hpc.py
```

Biblioteka C++ liczy deterministyczną sumę faz: **nie** aktualizuje ogniw
Spin(10), nie wykonuje 100 przemiatanych iteracji ani nie jest obliczeniem
Wilson loop. Benchmark mierzy liczbę odwiedzonych elementów na sekundę, nie
GigaFLOPS/GigaOPS. Brak biblioteki jest jawnie raportowany jako brak, nie jako
zerowy pomiar. Diagnostyka silnika zwraca `Performance` i `Diagnostics`, nie
poprzednie niezweryfikowane pola `Physics`.

## Ograniczenia

RGE jest ilustracyjnym jednopętlowym przepływem SM/MSSM z założonym równym
sprzężeniem na skali GUT. Użyty graf Barabási–Albert ma parametr m=4, co nie
oznacza średniego stopnia 4. Nachylenie błądzenia losowego w stałym oknie nie
jest potwierdzonym wymiarem spektralnym IR. Operator w `graph_dirac.py` ma
indeks grafowej charakterystyki Eulera i nie jest chiralnym operatorem 4D
Spin(10). Niepewności fizyczne nie zostały wyznaczone.

## Licencja

Treść licencji i dodatkowych warunków znajduje się w [LICENSE](LICENSE).
