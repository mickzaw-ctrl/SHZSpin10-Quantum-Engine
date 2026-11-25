# Zakres techniczny i ograniczenia prototypu

Niniejszy dokument opisuje faktyczny zakres tej gałęzi; nie jest pełnym
wyprowadzeniem fizycznym teorii Spin(10).

## Elementy kodu

1. `spin10_core_fast.cpp` liczy deterministyczną sumę cosinusów na siatce faz.
   Parametr `n_sweeps` skaluje jedną sumę, ale nie powoduje wykonania sweepów.
   Kod nie realizuje działania na trójkątach, relaksacji Monte Carlo ani macierzy
   holonomii Spin(10).
2. `spin10_optimized.py` tworzy graf Barabási–Albert, wyznacza pomocnicze
   nachylenie prawdopodobieństwa powrotu oraz całkuje 1-loop RGE z założoną
   unifikacją i pojedynczym progiem. Nie szacuje niepewności. Nachylenie w
   stałym oknie nie jest wykazanym plateau IR; jawnie oznaczono je jako
   niewiarygodne w tej roli.
3. `graph_dirac.py` implementuje samosprzężony operator incydencji i jego
   indeks `|V|-|E|`. Nie jest 4D chiralnym operatorem Spin(10), a jego indeks
   nie wyznacza liczby generacji Modelu Standardowego.
4. `scientific_checks.py` odtwarza wybrane rachunki i ustalone benchmarki z
   zewnętrznej dokumentacji. To kontrole arytmetyczne, nie solver kwantowej
   grawitacji ani analiza eksperymentalnego likelihoodu.

## Niewykazane wcześniejsze deklaracje

W tym repozytorium brak implementacji wyprowadzającej stałą struktury subtelnej
1/137,036, symulacji przejścia Big Bounce, integracji z procesorem kwantowym,
wyprowadzenia korekcji kwantowej grawitacji oraz pomiaru 191 GigaOPS. Brak też
implementacji pełnego działania grafowego zapisanego w starszej wersji tego
pliku. Nie należy traktować tych deklaracji jako wyników kodu.

Szczegółowy zakres audytu, źródła oraz nierozwiązane problemy znajdują się w
[docs/AUDYT-I-STATUS.md](docs/AUDYT-I-STATUS.md). Dwa warunkowe benchmarki z
porównaniem do publikacji Planck i BICEP/Keck opisano w
[docs/PREDYKCJE-I-DANE.md](docs/PREDYKCJE-I-DANE.md).
