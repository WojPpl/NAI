"""
Autorzy: Przemysław Scharmach, Michał Zaremba
Skorzystano z dokumentacji: https://pythonhosted.org/scikit-fuzzy/

Opis problemu:
Algorytm szacujący ceny mieszkań na podstawie rozmiaru oraz subiektywnych ocen
wyposażenia i położenia (na podstawie odległosci od centrum). Z uwagi na
wysoki poziom skomplikowania w przypadku całej Polski (bardzo duże
zróżnicowanie cenowe mieszkań w różnych miastach) przyjmujemy iż reguły 
tworzymy dla miasta Gdańsk.


Instrukcja przygotowania środowiska (dla systemów operacyjnych Windows)
W wierszu poleceń należy wpisać kolejno: 
    
    1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    2. python get-pip.py
    3. pip install numpy
    4. pip install skfuzzy
    
    W przypadku posiadania pip (instalator pakietów) pozycje 3. oraz 4. można
    wpisać również w terminalu IDE.

Komentarz dodatkowy:
Napotkalismy następującą trudnosc: okazało się, że uzyskanie wartosci 
minimalnej jak i maksymalnej z przedziałów nie jest mozliwe mimo podania 
minimalnych jak i maksymalnych wartosci zmiennych. 
Znaleźlismy wytłumaczenie tutaj, natomiast niestety nie pomoglo ono 
skonstruowac programu tak, aby wartosci cenowe mialy zawsze pokrycie z 
rzeczywistoscią. Co ciekawe - w przypadku przykładu z tip 
problem sytuacja wygląda tak samo - nawet jesli jedzenie i obsluga byly naszym 
zdaniem "na dziesiątkę" to nie osiągniemy wartosci maksymalnej napiwku 
okreslonej w naszym universum, czyli 25%.
    
https://gitter.im/scikit-fuzzy/scikit-fuzzy?at=5772a252bb1de91c5494d205

"Great question. What you're finding is a general feature of classical fuzzy 
systems. Basically the actual response will not span the universe, the actual 
range of responses from the system will be a smaller range. This is because 
when generating the crisp output, the most extreme membership values are 
combined and then functionally the centroid value is found. Because membership
functions are not singletons/delta functions, the nonzero membership at values 
prior to the extrema of the universe will pull the maximum available value back
from the edge.This is nonintuitive but guaranteed by the underlying math. 
The solution is not to extend the membership functions outside the output 
universe(s). Instead, one solution is to extend the output universe(s) and the
membership functions with nonzero values at the extrema such that the 
centroid of the membership function now reaches the desired endpoint.
This is nonintuitive but guaranteed by the underlying math. The solution is not 
to extend the membership functions outside the output universe(s). 
Instead, one solution is to extend the output universe(s) and the membership 
functions with nonzero values at the extrema such that the centroid of the
membership function now reaches the desired endpoint.

Cytując klasyka: "it's not a bug, it's a feature"
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Zmienne
"""
W tej sekcji definiujemy zmienne które będziemy stosować w naszym universum
(Antecedent - wejsciowe, jak i Consequent - wyjsciowe) - tutaj są to trzy 
inputy oraz jeden output. Tworzymy tablice tworzące, które okreslaja 
przedzial w jakim przedziale wartosci tych zmiennych bedziemy się poruszać.
Przypinamy im etykiety, które widoczne będą później na wykresach.
"""
rozmiar = ctrl.Antecedent(np.arange(0, 121, 1), 'rozmiar')
odleglosc_od_centrum = ctrl.Antecedent(np.arange(0, 11, 1), 'odleglosc od centrum')
wyposazenie = ctrl.Antecedent(np.arange(0, 11, 1), 'wyposazenie')
cena =  ctrl.Consequent(np.arange(701, 6002, 1), 'cena')

#Funkcje Membership
"""
W tej sekcji okreslamy nasze funkcje przynaleznosci (Membership Functions).
Można robić to zarówno w sposób automatyczny (funkcja automf), tak jak w
w przypadku wyposazenia oraz odleglosci od centrum, ale
także możemy okreslic je ręcznie - tak jak w przypadku rozmiaru czy ceny.
Funkcje te przypinają do przedziałów wartosci słowną "etykietę".
Dla automf wybierając wartosc (3) będziemy otrzymywać zwrotnie wartosci "good", 
"average" lub "poor" zależnie od przedziału. W przypadku trójkąta (trimf) 
wskazujemy przedziały trzyczęsciowe, w przypadku funkcji trapmf rysujemy trapez 
i wskazujemy czteroczęsciowe przedziały.
"""

wyposazenie.automf(3)
odleglosc_od_centrum.automf(3)

rozmiar['small'] = fuzz.trimf(rozmiar.universe, [10, 30, 41])
rozmiar['decent'] = fuzz.trimf(rozmiar.universe, [41, 50, 61])
rozmiar['large'] = fuzz.trimf(rozmiar.universe, [61, 90, 121])

cena['low'] = fuzz.trapmf(cena.universe, [700, 800, 1000, 1500])
cena['medium'] = fuzz.trapmf(cena.universe, [1500, 2000, 2500, 3000])
cena['high'] = fuzz.trapmf(cena.universe, [3000, 4000, 5000, 6000])


#Wykresy
"""
W tej sekcji wywołujemy pythonowe funkcje odpowiedzialne za rysowanie wykresów.
"""

rozmiar.view()
odleglosc_od_centrum.view()
cena.view()

#Reguły
"""
W tej sekcji okreslamy reguły według których ma odbywać się liczenie
naszych wyników końcowych (cen) zależnie od wskazanych klasyfikacji wartoci 
zmiennych wejsciowych. Na podstawie tej klasyfikacji tworzona jest zmienna 
cena_ctrl łącząca reguły w jeden kontroler, następnie wyliczana jest cena przy 
użyciu funkcji ControlSystemSimulation.
"""

r1 = ctrl.Rule((rozmiar['large'] & odleglosc_od_centrum['good'] & wyposazenie['good']) |
(rozmiar['large'] & odleglosc_od_centrum['good'] & wyposazenie['poor']) |
(rozmiar['large'] & odleglosc_od_centrum['good'] & wyposazenie['average']), cena['high'])

r2 = ctrl.Rule((rozmiar['large'] & odleglosc_od_centrum['good'] & wyposazenie['good']) |
(rozmiar['large'] & odleglosc_od_centrum['average'] & wyposazenie['good']) |
(rozmiar['large'] & odleglosc_od_centrum['average'] & wyposazenie['average']), cena['high'])

r3 = ctrl.Rule((rozmiar['decent'] & odleglosc_od_centrum['good'] & wyposazenie['good']) |
(rozmiar['decent'] & odleglosc_od_centrum['good'] & wyposazenie['good']) |
(rozmiar['decent'] & odleglosc_od_centrum['good'] & wyposazenie['average']), cena['high'])

r4 = ctrl.Rule((rozmiar['decent'] & odleglosc_od_centrum['average'] & wyposazenie['good']) |
(rozmiar['decent'] & odleglosc_od_centrum['average'] & wyposazenie['good']), cena['high'])

r5 = ctrl.Rule((rozmiar['small'] & odleglosc_od_centrum['good'] & wyposazenie['good']), cena['high'])

r6 = ctrl.Rule((rozmiar['small'] & odleglosc_od_centrum['poor'] & wyposazenie['good'])|
(rozmiar['small'] & odleglosc_od_centrum['poor'] & wyposazenie['poor']), cena['low'])

r7 = ctrl.Rule((rozmiar['small'] & odleglosc_od_centrum['average'] & wyposazenie['poor'])|
(rozmiar['small'] & odleglosc_od_centrum['poor'] & wyposazenie['average']), cena['low'])

r8 = ctrl.Rule((rozmiar['small'] & odleglosc_od_centrum['good'] & wyposazenie['poor'])|
(rozmiar['small'] & odleglosc_od_centrum['good'] & wyposazenie['average']), cena['medium'])

r9 = ctrl.Rule((rozmiar['large'] & odleglosc_od_centrum['average'] & wyposazenie['poor'])|
(rozmiar['large'] & odleglosc_od_centrum['poor'] & wyposazenie['average']), cena['medium'])

r10 = ctrl.Rule((rozmiar['decent'] & odleglosc_od_centrum['average'] & wyposazenie['poor'])|
(rozmiar['decent'] & odleglosc_od_centrum['average'] & wyposazenie['poor']), cena['medium'])

r11 = ctrl.Rule((rozmiar['small'] & odleglosc_od_centrum['good'] & wyposazenie['poor'])|
(rozmiar['small'] & odleglosc_od_centrum['average'] & wyposazenie['good']), cena['medium'])

cena_ctrl = ctrl.ControlSystem(rules=[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11])
wynik_ceny = ctrl.ControlSystemSimulation(cena_ctrl)

#Dane wejsciowe
"""
W tej sekcji wpisujemy wartosci naszych zmiennych wejsciowych aby za chwilę
otrzymać wynik wyswietlony przy pomocy funkcji print. Rysujemy również finalny
wykres przedstawiający uzyskany wynik w formie graficznej w odniesieniu do 
podanego przedziału.
"""

wynik_ceny.input['rozmiar'] = int(input("Wskaż rozmiar mieszkania w metrach kwadratowych maksymalnie do 120 m: "))
wynik_ceny.input['odleglosc od centrum'] = int(input("Podaj ocenę położenia na podstawie odległosci od centrum (0-10): "))
wynik_ceny.input['wyposazenie'] = int(input("Wskaż ocenę wyposazenia mieszkania (0-10): "))
wynik_ceny.compute()
print("Szacunkowa miesięczna cena wynajmu wyniesie: ", round(wynik_ceny.output['cena']), "zł")
cena.view(sim=wynik_ceny)

