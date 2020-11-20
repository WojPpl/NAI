"""
Autorzy: Przemysław Scharmach, Michał Zaremba
Zasady: pl.wikipedia.org/wiki/Czwórki
Skorzystano z dokumentacji: https://zulko.github.io/easyAI/ref.html

Instrukcja przygotowania środowiska (dla systemów operacyjnych Windows)
W wierszu poleceń należy wpisać kolejno: 
    
    1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    2. python get-pip.py
    3. install numpy
    4. pip install easyAI
    
    W przypadku posiadania pip (instalator pakietów) pozycje 3. oraz 4. można wpisać również
    w terminalu IDE.
"""

import numpy as np

import time


from easyAI import TwoPlayersGame


class Connect4(TwoPlayersGame):
    
    """Klasa należąca do easyAI przeznaczona do tworzenia gier dwuosobowych. 
    Definiujemy w niej naszą grę. 
    
    Konieczne jest utworzenie metod: 
    __init__(self, players, ...), possible_moves(self), make_move(self, move),
    is_over(self).
    
    My do utworzenia Connect Four będziemy dodatkowo potrzebować metod scoring
    oraz show(self) - lose(self) korzysta z innej metody.
    """

    def __init__(self, players, board = None):
        
        """Metoda nadająca naszej grze stany początkowe. Okresla kolejno iż
        będzie w niej dwóch graczy, plansza posiada wielkosc 7 x 6
        (tablica dwuwymiarowa), a pierwszy ruch należeć będzie
        do gracza pierwszego.
        """
        self.players = players
        self.board = board if (board != None) else (
            np.array([[0 for i in range(7)] for j in range(6)]))
        self.nplayer = 1

    def possible_moves(self):
        
        """Metoda okreslajaca mozliwe zagrania gracza
        do którego należy obecny ruch. Składają się na nią kilka metod, których
        nie należy nadpisywać aby program działał poprawnie, a są to:
        
        self.player - aktualny gracz
        self.opponent - przeciwnik aktualnego gracza
        self.opponent - numer (1 lub 2) aktualnego gracza
        self.nopponent - numer (1 lub 2) przeciwnika
        self.nmove - wskazuje jak wiele ruchów wykonano do tej chwili
        
        Wskazujemy tutaj jakie sa mozliwe zagrania - mamy 7 stosów, więc 
        7 możliwych ruchów (pod warunkiem, że dana kolumna tablicy nie została
        w całosci wypelniona - wypełnienie oznaczać będzie że stos o danym 
        indeksie się przepełnił i dołożenie do niego żetonu nie jest ruchem 
        dozwolonym więc nie zostanie to umożliwione - pętla nie przekaże wartosci
        do metody
        
        """
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        
        """Metoda transofrmująca obecny stan gry zgodnie z ostatnio wykonanym ruchem"""
        
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.nplayer
    

    def show(self):
        
        """Metoda wyswietlajaca aktualną planszę w konsoli po każdym zagraniu, okresla typy żetonów"""
        
        print('\n' + '\n'.join(
                        ['0 1 2 3 4 5 6', 13 * '_'] +
                        [' '.join([['.', 'O', 'X'][self.board[5 - j][i]]
                        for i in range(7)]) for j in range(6)]))

    def lose(self):
        
        """Metoda przekazująca informację czy którys z graczy przegrał, korzysta z poniżej 
        zdefiniowanej metody find_four (referencja), która z kolei sprawdza czy spełniono warunek zwycięstwa 
        - a więc czy połączono przez gracza 4 żetony"""
        
        return find_four(self.board, self.nopponent)

    def is_over(self):
        
        """Metoda przekazująca informację czy gra zakończyła się tj. czy zapełniono wszystkie stosy i 
        nie ma już możliwych ruchów lub czy gracz przegrał, ponieważ przeciwnik połączył
        4 żetony"""
        
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        
        """Metoda zwracająca jeden z dwóch wyników dla AI. Z jego wartosci korzysta algorytm Negamax
        z którego korzysta easyAI"""
       
        return -100 if self.lose() else 0


def find_four(board, nplayer):
    
    """
    Zwraca wartosc True gdy gracz połączy 4 żetony w pionie, poziomie lub po skosie.
    """
    
    #Algorytm przeszukujący znaleziony w książce Aritificial Intelligence with Python Prateek Joshi
    
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == nplayer:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False


POS_DIR = np.array([[[i, 0], [0, 1]] for i in range(6)] +
                   [[[0, i], [1, 0]] for i in range(7)] +
                   [[[i, 0], [1, 1]] for i in range(1, 3)] +
                   [[[0, i], [1, 1]] for i in range(4)] +
                   [[[i, 6], [1, -1]] for i in range(1, 3)] +
                   [[[0, i], [1, -1]] for i in range(3, 7)])

if __name__ == '__main__':
    # Pętla zostanie wykonana tylko jesli skrypt zostanie uruchomiony: 
    # https://docs.python.org/3/library/__main__.html

    from easyAI import Human_Player, AI_Player, Negamax
    
    """
    Negamax to populary sposób implementacji algorytmu minimax, z tym że zamiast
    stosowania dwóch osobnych podprogramów dla gracza Min oraz gracza Max, algorytm Negmax
    przekazuje zanegowany wynik zgodnie z poniższym wzorem:
    max(a, b) == -min(-a, -b)
    """

    ai_alg = Negamax(5) #AI będzie myslec na 5 ruchów do przodu
    game = Connect4([Human_Player(), AI_Player(ai_alg)])
    history = game.play()
    if game.lose():
        print("Gracz %d wygrał." % (game.nopponent))
        time.sleep(5)
    else:
        print("Remis!")
        time.sleep(5)
    
