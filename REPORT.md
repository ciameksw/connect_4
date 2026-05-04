# Raport Connect 4 -> AI

## 1. Opis zastosowanego algorytmu

W projekcie zastosowano algorytm **Minimax z alpha-beta pruning** do wyboru najlepszego ruchu.

### Minimax + Alpha-Beta

Algorytm:
- symuluje możliwe ruchy do określonej głębokości (`minimax_search_depth`)
- maksymalizuje wynik dla jednego gracza i minimalizuje dla drugiego
- wykorzystuje alpha-beta pruning w celu ograniczenia liczby analizowanych stanów

---

### Ocena stanów (heurystyka)

Ocena planszy odbywa się na dwa sposoby:

#### 1. Stany terminalne
Jeżeli gra się kończy:
- wygrana → `terminal_score_win`
- przegrana → `terminal_score_loss`
- remis → `0`

#### 2. Stany nieterminalne (heurystyka)

Dla stanów pośrednich stosowana jest funkcja heurystyczna, która zlicza wynik na podstawie paru składowych:

##### Preferencja środka

Środkowa kolumna daje dodatkowe punkty (`heuristic_score_center_column`)

##### Analiza "okien" 

Sprawdza wszystkie możliwe „okna” (ciągi pól o długości `win_length`) w czterech kierunkach:
- poziomo
- pionowo
- po skosie (2 kierunki)

Dla każdego okna:
- przyznawane są punkty za własne układy
- odejmowane są punkty za układy przeciwnika

##### Normalizacja wyniku

Wynik heurystyki dzielony jest przez liczbę pionków na planszy:

```
score = score / liczba_pionków
```

Zapobiega to nadmiernemu wzrostowi wartości w trakcie gry

##### Multiplier heurystyki

Końcowy wynik mnożony jest przez `heuristic_score_multiplier`

Pozwala regulować wpływ heurystyki względem stanów terminalnych

##### Discount względem głębokości

Wynik jest zmniejszany wraz z głębokością:

```
score *= (1 - heuristic_depth_discount_ratio * depth_fraction)
```

Dzięki temu:
- AI preferuje szybsze zwycięstwa
- opóźnia przegrane

---

## 2. Konfigurowalne parametry

### Parametry planszy
- `rows` – liczba wierszy
- `columns` – liczba kolumn
- `win_length` – długość ciągu potrzebnego do wygranej

---

### Parametry przeszukiwania
- `minimax_search_depth` – głębokość przeszukiwania drzewa

Większa wartość:
- poprawia jakość decyzji
- znacząco zwiększa czas obliczeń

---

### Heurystyki – własne układy
- `heuristic_score_exact_win_length`
- `heuristic_score_one_missing`
- `heuristic_score_two_missing`
- `heuristic_score_three_missing`

---

### Heurystyki – przeciwnik
- `heuristic_penalty_opponent_one_missing`
- `heuristic_penalty_opponent_two_missing`
- `heuristic_penalty_opponent_three_missing`

Odpowiadają za siłę blokowania przeciwnika.

---

### Parametry pozycyjne
- `heuristic_score_center_column` – bonus za środek planszy

---

### Skalowanie i balans
- `heuristic_score_multiplier` – wpływ heurystyki

---

### Discount głębokości
- `heuristic_depth_discount_ratio`

---

### Wyniki terminalne
- `terminal_score_win`
- `terminal_score_loss`

---

## 3. Predefiniowane poziomy trudności

### Easy
- `minimax_search_depth = 2`
- `heuristic_penalty_opponent_one_missing = -8`
- `heuristic_score_multiplier = 0.8`

Efekt:
- bardzo płytkie przeszukiwanie
- słabe reagowanie na zagrożenia przeciwnika
- mniejszy wpływ heurystyki na decyzje
- AI często nie blokuje oczywistych ruchów

---

### Medium
- `minimax_search_depth = 4`
- `heuristic_penalty_opponent_one_missing = -20`
- `heuristic_score_multiplier = 1.0`

Efekt:
- głębsze przeszukiwanie
- lepsze wykrywanie zagrożeń
- zbalansowana heurystyka
- AI podejmuje bardziej "przemyślane" decyzje

---

### Hard
- `minimax_search_depth = 6`
- `heuristic_penalty_opponent_one_missing = -40`
- `heuristic_score_multiplier = 1.5`

Efekt:
- najwyższa dostępna głębokość przeszukiwania
- pełna siła heurystyk
- silne reagowanie na zagrożenia przeciwnika
- AI trudne do pokonania, bardziej defensywne

---

## 4. Testy

Przeprowadzono testy manualne polegające na grze ze sztuczną inteligencją, z różną konfiguracją.
Sprawdzano "silę" przeciwnika, zdolność do blokowania wygrywających ruchów, czas odpowiedzi AI.

Na podstawie przeprowadzonych testów powstały predefiniowane poziomy trudności.

---

## 5. Wyniki i wnioski

- zwiększenie głębokości przeszukiwania (`minimax_search_depth`) poprawia jakość decyzji AI, ale znacząco wydłuża czas obliczeń

- przy większych planszach wysoka głębokość powoduje bardzo duży wzrost złożoności obliczeniowej, co może prowadzić do niegrywalności (zbyt długie czasy odpowiedzi AI)

- zmniejszenie kar za zagrożenia przeciwnika powoduje, że AI rzadziej blokuje i gra mniej defensywnie

- zwiększenie kar dla przeciwnika skutkuje bardziej ostrożną i defensywną strategią

- bonus za środkową kolumnę poprawia jakość ruchów, ponieważ zwiększa możliwości budowania układów

- normalizacja heurystyki (dzielenie przez liczbę pionków) stabilizuje ocenę planszy w trakcie gry

- discount względem głębokości powoduje preferowanie szybszych zwycięstw i opóźnianie przegranych

- odpowiedni dobór parametrów pozwala uzyskać różne poziomy trudności bez zmiany samego algorytmu

- zastosowanie alpha-beta pruning znacząco redukuje liczbę analizowanych stanów, co pozwala na użycie większej głębokości przeszukiwania niż przy samym minimax
