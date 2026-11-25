# Jawny operator Diraca na grafie: przykład kontrolny

`graph_dirac.py` definiuje jawny skończony operator incydencji na prostym,
nieskierowanym grafie, **nie** operator chiralnych fermionów 4D Spin(10).
To odtwarzalny punkt kontrolny, nie dowód trzech generacji.

Dla dowolnej orientacji krawędzi tworzymy macierz incydencji B wymiaru |V|×|E|:
−1 w wierzchołku początkowym, +1 w końcowym. Na przestrzeni C^V ⊕ C^E:

```
D = [ 0   B ]     Γ = [ I_V   0  ]
    [ B†  0 ]         [  0  −I_E ]
```

D jest samosprzężony i {D,Γ}=0. Indeks z tym gradownikiem to
`dim ker(B†) − dim ker(B) = |V| − |E|`, obliczany przez SVD z podaną tolerancją.
Odwrócenie orientacji krawędzi zmienia tylko znak kolumny B, nie indeks.

| Graf | |V| | |E| | n₊ | n₋ | indeks |
|---|---:|---:|---:|---:|---:|
| Ścieżka o 4 wierzchołkach | 4 | 3 | 1 | 0 | 1 |
| Cykl o 4 wierzchołkach | 4 | 4 | 1 | 1 | 0 |
| Gwiazda o stopniu centralnym 4 | 5 | 4 | 1 | 0 | 1 |
| 3 izolowane wierzchołki | 3 | 0 | 3 | 0 | 3 |

Przykład indeksu 3 pokazuje tylko charakterystykę Eulera grafu. Nie identyfikuje
modów z generacjami; nawet graf ze stopniem 4 nie wymusza indeksu 3. Tensorowanie
tego operatora z dowolną przestrzenią wewnętrzną samo nie wprowadza chiralnych
fermionów Spin(10).

Aby podjąć rzeczywistą próbę wyprowadzenia generacji, trzeba określić: przestrzeń
spinorów 16, reprezentację połączeń Spin(10), operator i gradownik/chiralność,
warunki brzegowe, dozwolone topologie i granicę ciągłą, a następnie wykazać
stabilność indeksu i związek z fizycznym widmem. Tego w obecnym repozytorium
nie zrealizowano. `python graph_dirac.py` i testy pozwalają odtworzyć jedynie
powyższy przykład matematyczny.
