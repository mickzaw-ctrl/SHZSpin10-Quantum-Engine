# Sektor Ciemny: Ciemna Materia i Ciemna Energia
### Status problemu, dane obserwacyjne i miejsce modelu SHZSpin10 w tym kontekście

> **Uwaga o statusie tego dokumentu:** Ciemna materia i ciemna energia to **wciąż otwarte problemy fizyki** —
> nie ma dziś ani jednego eksperymentu, obserwacji ani teorii, która by je „rozwiązała” w sensie wskazania
> mechanizmu potwierdzonego niezależnymi pomiarami. Ten dokument (1) rzetelnie opisuje, co obecnie wiemy,
> (2) wskazuje, czego nie wiemy, i (3) opisuje, w jaki sposób moduł `spin10_dark_sector.py` w tym repozytorium
> *modeluje* pewne aspekty sektora ciemnego jako fenomenologiczny toy-model oparty na strukturze grafowej
> Spin(10) — **nie jako wyprowadzenie z pierwszych zasad**. Jakiekolwiek stwierdzenie w stylu „SHZSpin10
> rozwiązuje problem ciemnej materii/energii” byłoby nieuczciwe naukowo i nie jest tu formułowane.

---

## 1. Co wiemy z obserwacji

### 1.1 Budżet energetyczny Wszechświata (Planck 2018, PDG 2024)
Z pomiarów mikrofalowego promieniowania tła (CMB) przez satelitę Planck oraz niezależnie z baryonowych
oscylacji akustycznych (BAO) i supernowych Ia, standardowy model kosmologiczny **ΛCDM** daje:

| Składnik | Udział Ω | Gęstość Ω·h² |
|---|---|---|
| Materia barionowa (zwykła) | Ω_b ≈ 0.049 | Ω_b h² = 0.0224 ± 0.0001 |
| Ciemna materia (zimna, CDM) | Ω_c ≈ 0.265 | Ω_c h² = 0.120 ± 0.001 |
| Ciemna energia (Λ) | Ω_Λ ≈ 0.685 | — |
| **Materia całkowita** | Ω_m = 0.315 ± 0.007 | — |

Źródło: Planck Collaboration 2018, *Cosmological Parameters* (A&A 641, A6). H₀ = 67.4 ± 0.5 km/s/Mpc,
w₀ = −1.03 ± 0.03 (zgodne ze stałą kosmologiczną w granicach błędu Planck+SNe).

**Wniosek:** ok. 95% budżetu energii Wszechświata to substancje, których natury nie znamy bezpośrednio —
znamy tylko ich efekty grawitacyjne/kosmologiczne.

### 1.2 Dowody na istnienie ciemnej materii
Ciemna materia nie jest hipotezą ad hoc — wynika z **wielu niezależnych** linii dowodowych:
- **Krzywe rotacji galaktyk** (Rubin, Ford, lata 70.) — gwiazdy na obrzeżach galaktyk krążą za szybko,
  by utrzymać je grawitacja samej widocznej materii.
- **Soczewkowanie grawitacyjne** gromad galaktyk (np. Kolizja Pocisku — Bullet Cluster) — masa wyznaczona
  z soczewkowania jest przesunięta względem gorącego gazu (widocznego w rentgenie), co pokazuje, że
  większość masy jest niebarionowa i słabo oddziałuje.
- **Widmo mocy CMB** — położenie i wysokość pików akustycznych wymaga obecności dodatkowej, bezciśnieniowej
  materii nieoddziałującej elektromagnetycznie.
- **Formowanie struktur wielkoskalowych** — symulacje N-ciałowe (np. Millennium) odtwarzają obserwowaną
  sieć kosmiczną tylko przy założeniu dominacji zimnej ciemnej materii.
- **Nukleosynteza Wielkiego Wybuchu (BBN)** — niezależnie ogranicza ilość materii barionowej do Ω_b ≈ 0.05,
  co jest dużo mniej niż całkowita materia grawitująca (Ω_m ≈ 0.315).

### 1.3 Czym ciemna materia *nie jest* (wykluczone/ograniczone eksperymentalnie)
- Bezpośrednie eksperymenty poszukujące WIMP-ów (LUX-ZEPLIN, XENONnT, PandaX) nie znalazły sygnału i
  wykluczyły duże obszary przestrzeni parametrów przekroju czynnego WIMP-nukleon.
- Poszukiwania aksjonów (ADMX i inne) systematycznie zawężają dozwolone masy/sprzężenia, bez detekcji.
- MACHO (masywne zwarte obiekty halo, np. czarne dziury pierwotne) w dużej mierze wykluczone przez
  mikrosoczewkowanie w większości zakresów mas jako dominujący składnik ciemnej materii.

**Stan na 2025/2026:** brak potwierdzonej detekcji cząstki ciemnej materii. To wciąż otwarty problem.

### 1.4 Dowody na przyspieszoną ekspansję i „ciemną energię”
- Supernowe Ia (Riess, Perlmutter, Schmidt — Nobel 2011) pokazały, że ekspansja Wszechświata **przyspiesza**,
  a nie zwalnia — sprzeczne z czystą grawitacją materii.
- Model ΛCDM opisuje to stałą kosmologiczną Λ o gęstości energii ρ_Λ ≈ 6×10⁻²⁷ kg/m³, ze stanem równania
  w = p/ρ = −1.

### 1.5 Problem stałej kosmologicznej — największa niezgodność teorii z eksperymentem
Naiwne oszacowanie gęstości energii próżni z Kwantowej Teorii Pola (sumowanie energii punktu zerowego pól
do obcięcia na skali Plancka) daje wartość **50–120 rzędów wielkości większą** niż obserwowana ciemna
energia. Nazywane bywa to „najgorszą przepowiednią teoretyczną w historii fizyki”. Żadna znana symetria
(w tym niezłamana supersymetria) nie tłumaczy naturalnie, dlaczego suma wkładów akurat się kasuje do
tak małej wartości resztkowej. To jest **fundamentalny, nierozwiązany problem** łączący kosmologię
z fizyką cząstek i grawitacją kwantową.

### 1.6 Nowość: dane DESI DR1/DR2 (2024–2025) sugerujące dynamiczną ciemną energię
Najnowsze pomiary BAO z **Dark Energy Spectroscopic Instrument (DESI)**:
- DESI DR1 (2024) wykazał odchylenia od czystego ΛCDM na poziomie 2.5–3.9σ (w zależności od zestawu
  danych supernowych: Pantheon+, Union3, DES-SN5YR) w kierunku modelu w₀wₐCDM, gdzie stan równania
  ciemnej energii **ewoluuje w czasie** zamiast być stałym w = −1.
- DESI DR2 (marzec 2025) wzmocnił te odchylenia do 2.8–4.2σ w zależności od kombinacji danych, preferując
  scenariusz, w którym w₀ > −1 i wₐ < 0 (tzw. „phantom crossing” — w przeszłości w < −1, dziś w > −1).
- Analizy Lyman-α z DESI DR2 (2026) oraz niezależne prace bayesowskie łączące DESI+CMB+SNIa potwierdzają
  ten trend, choć część rekonstrukcji non-parametrycznych (np. flexknot, MNRAS 2025) wskazuje, że siła
  dowodu zależy silnie od wybranej metody i zestawu supernowych — **nie jest to jeszcze konsensus 5σ**.

**Wniosek:** Jeśli te wyniki się potwierdzą (potrzeba niezależnej replikacji, np. przez Euclid, Rubin/LSST),
prosta stała kosmologiczna Λ może wymagać zastąpienia dynamicznym polem (kwintesencja, model fantomowy,
lub oddziałująca ciemna energia-materia). To wciąż przedmiot aktywnych badań w 2025–2026, nie rozstrzygnięty problem.

---

## 2. Główne kierunki teoretyczne (skrót)

| Podejście | Idea | Status |
|---|---|---|
| WIMP (słabo oddziałujące masywne cząstki) | Nowa cząstka spoza Modelu Standardowego, np. neutralino z SUSY | Coraz mocniej ograniczone eksperymentalnie |
| Aksjony | Lekkie pseudoskalarne cząstki z rozwiązania problemu silnego CP | Aktywne poszukiwania, brak detekcji |
| Sterylne neutrina | Neutrina niesprzężone ze słabym oddziaływaniem | Ograniczone przez obserwacje X-ray/kosmologię |
| MOND / zmodyfikowana grawitacja | Zmiana praw grawitacji zamiast nowej materii | Trudności z gromadami galaktyk (Bullet Cluster), CMB |
| Kwintesencja / dynamiczne pole skalarne (ciemna energia) | Pole φ o wolno zmieniającym się potencjale | Wspierane częściowo przez DESI DR1/DR2 |
| Stała kosmologiczna (Λ) | Energia próżni, w = −1 na stałe | Wciąż zgodna z większością danych, ale coraz bardziej kwestionowana przez DESI |
| Emergentna grawitacja / modele entropowe | Grawitacja i „ciemne” efekty jako zjawiska termodynamiczne/informacyjne | Spekulacyjne, brak ilościowej zgodności na poziomie precyzji ΛCDM |

Modele oparte na grupach dużej unifikacji (GUT), w tym Spin(10), *mogą* dostarczać kandydatów na ciemną
materię (np. prawostronne neutrina, dodatkowe fermiony w reprezentacji **16** Spin(10) o masie chronionej
symetrią), ale są to **kandydaci koncepcyjni**, wymagający dopasowania mas i przekrojów czynnych do danych
— nie automatyczne przewidywania.

---

## 3. Co robi moduł `spin10_dark_sector.py` w tym repozytorium

Moduł jest **fenomenologicznym modelem symulacyjnym**, spójnym stylistycznie z resztą silnika SHZSpin10
(`spin10_optimized.py`), który:

1. Wykorzystuje ten sam graf Barabási–Albert (relacyjny model grafowy) co reszta silnika, traktując
   węzły o różnym stopniu połączeń (`k_i`) jako analogię „gęstości energii” w danym rejonie grafu.
2. Interpretuje **niskostopniowe, słabo połączone węzły** (peryferie grafu) jako sektor analogiczny do
   ciemnej materii — masywny, ale "słabo sprzężony" z gęsto połączonym rdzeniem (analogia do materii
   barionowej silnie oddziałującej elektromagnetycznie).
3. Wprowadza efektywny potencjał holonomii, którego wartość oczekiwana w granicy termodynamicznej grafu
   jest **kalibrowana** (nie wyprowadzana) tak, by odtworzyć znane z obserwacji proporcje
   Ω_b : Ω_c : Ω_Λ ≈ 0.049 : 0.265 : 0.685 (Planck 2018).
4. Implementuje prosty, jawnie oznaczony jako *toy-model*, przepływ w(a) w stylu CPL
   (w(a) = w₀ + wₐ(1−a)) do zilustrowania, jak wyglądałby scenariusz dynamicznej ciemnej energii
   sugerowany przez DESI DR2, **bez twierdzenia, że model to przewiduje**.
5. Na końcu każdego raportu jawnie wypisuje disclaimer o charakterze fenomenologicznym/kalibrowanym
   wyniku, aby uniknąć nieporozumienia, że problem sektora ciemnego został "rozwiązany".

### Czego moduł **nie robi**
- Nie wyprowadza mas ani sprzężeń cząstek ciemnej materii z pierwszych zasad Spin(10).
- Nie przewiduje niezależnie wartości Ω_Λ ani w₀, wₐ — te wartości są danymi wejściowymi (z Planck/DESI),
  używanymi do kalibracji, a wynik jest w dużej mierze odtworzeniem założeń.
- Nie zastępuje ani nie podważa ΛCDM jako obowiązującego modelu roboczego kosmologii.

---

## 4. Podsumowanie

Ciemna materia i ciemna energia razem stanowią ok. 95% budżetu energetycznego Wszechświata, a mimo to
ich mikroskopowa natura pozostaje nieznana. Dowody na ich *istnienie* są mocne i wielokrotnie
niezależnie potwierdzone; dowody na ich *naturę* — brak. Najnowsze dane (DESI DR1/DR2, 2024–2026)
wprowadzają dodatkową niepewność, sugerując że nawet stała kosmologiczna Λ może nie być ostatnim słowem.
Żaden istniejący model — w tym modele oparte na grupach GUT takich jak Spin(10) — nie „rozwiązuje” tego
problemu w sensie potwierdzonym eksperymentalnie. SHZSpin10 traktuje ten temat uczciwie: jako inspirację
do budowy kalibrowanych modeli fenomenologicznych, a nie jako rozwiązany problem fizyczny.

---

## Źródła
- Planck Collaboration (2018/2020), *Planck 2018 results. VI. Cosmological parameters*, A&A 641, A6.
- DESI Collaboration (2024), *DESI DR1 BAO and cosmological constraints*.
- DESI Collaboration (2025), *DESI DR2 Results* — https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/
- Adame et al. 2025, *DESI DR2 BAO*; Abdul Karim et al. 2025.
- A&A 2026 (aa57820-25): *Evidence of dynamical dark energy found via the DESI DR2 Lyman-α forest*.
- Wikipedia / HandWiki: *Cosmological constant problem* — przegląd rzędów wielkości niezgodności.
- Bertone, Hooper, Silk (2005), *Particle dark matter: evidence, candidates and constraints*, Phys. Rept.
