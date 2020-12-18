"""Autorzy: Przemysław Scharmach i Michał Zaremba

Instrukcja przygotowania środowiska (dla systemów operacyjnych Windows)
W wierszu poleceń należy wpisać kolejno: 
    
    1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    2. python get-pip.py
    3. pip install numpy
    4. należy pobrać plik ratings.json i umiescic go w folderze z programem
  
Problem: 
Stworzenie prostego programu do rekomendacji filmów i seriali na podstawie ocen
członków grupy ćwiczeniowej oraz prowadzącego w 2 tygodnie z wykorzystaniem 
współczynnika Pearsona oraz pliku .json z danymi o osobach i ich ocenach filmów.

"""

import json
import numpy as np

# Metoda oblicza wynik korelacji Pearsona między użytkownikami
def pearson_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Użytkownik ' + user1 + ' nie istnieje w bazie')

    if user2 not in dataset:
        raise TypeError('Użytkownik ' + user2 + ' nie istnieje w bazie')

    # Sprawdza jakie z filmów zostały ocenione przez obu użytkowników
    rated_by_both = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            rated_by_both[item] = 1

    num_ratings = len(rated_by_both) 

    # Jesli nie ma filmow obejrzanych przez obu, wynik jest równy 0
    if num_ratings == 0:
        return 0

    # Liczy sumę ocen dla wszystkich częsci wspolnych
    
    user1_sum = np.sum([dataset[user1][item] for item in rated_by_both])
    user2_sum = np.sum([dataset[user2][item] for item in rated_by_both])

    # Podnosi do kwadratu oceny częci wspólnych
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in rated_by_both])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in rated_by_both])

    # Wylicza sumę częci wspólnych 
    product_sum = np.sum([dataset[user1][item] * dataset[user2][item] for item in rated_by_both])

    # Przypisuje wyniki do zmiennych i zwraca wartosc ostateczną
    Sxy = product_sum - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings
    
    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


# Szuka wskazanej ilosci użytkowników która jest podobna
def find_similar_users(dataset, user, num_users):
    if user not in dataset:
        raise TypeError('Użytkownik ' + user + ' nie istnieje w bazie')

    # Oblicza współczynnik pearsona dla wszystkich użytkowników
    scores = np.array([[x, pearson_score(dataset, user, x)] for x in dataset if user != x])

    # Sortuje bazując na drugiej kolumnie
    scores_sorted = np.argsort(scores[:, 1])

    # Sortuje malajeco (najwyższy wynik najpierw) 
    scored_sorted_dec = scores_sorted[::-1]

    # Zwraca najwyższe
    top_k = scored_sorted_dec[0:num_users] 

    return scores[top_k] 


 
# Metoda generująca rekomendacje dla użytkownika
def generate_recommendations(dataset, user, similar_users):
    if user not in dataset:
        raise TypeError('Użytkownik ' + user + ' nie istnieje w bazie')

    total_scores = {}
    similarity_sums = {}

    for u in similar_users:
        user2 = u[0]
        similarity_score = pearson_score(dataset, user, user2)

        if similarity_score <= 0:
            continue

        for item in [x for x in dataset[user2] if x not in dataset[user] or dataset[user][x] == 0]:
            total_scores.update({item: dataset[user2][item] * similarity_score})
            similarity_sums.update({item: similarity_score})

    if len(total_scores) == 0:
        return ['Brak możliwych rekomendacji']

    # Tworzy znormalizowaną listę
    movie_ranks = np.array([[total/similarity_sums[item], item] 
            for item, total in total_scores.items()])

    # Sortuje malejąco bazując na pierwszej kolumnie
    movie_ranks = movie_ranks[np.argsort(movie_ranks[:, 0].astype(np.float))][::-1]
    
    # Zwraca proponwane filmy
    recommendations = [movie for _, movie in movie_ranks]
    
            
    return recommendations
 
if __name__=='__main__':
    data_file = 'ratings.json'
    
    #Ustalamy dla kogo chcemy sprawdzić rekomendacje filmów

    user = input("Wskaż imię i nazwisko (bez polskich znaków) aby przedstawić rekomendacje: ")


    #Otwieramy Jsona z danymi o użytkownikach i ich filmach
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    
    
    #Szukamy innych użytkowników o podobnych gustach
    similar_users = find_similar_users(data, user, 7)
    print ("\nDla użytkownika " + user + " polecamy:")
    movies = generate_recommendations(data, user, similar_users) 
    for i, movie in enumerate(movies[:7]):
        print (movie)
        
    print ("\nPod żadnym pozorem proszę nie oglądać: ")
    for i, movie in enumerate(movies[-7:]):
        print (movie)
