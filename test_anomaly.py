data = [
    {'user_id': 2, 'amount': 429.89, 'latitude': -17.952513, 'longitude': -152.997144},
    {'user_id': 5, 'amount': 8, 'latitude': 37.568524, 'longitude': -0.701222},
    {'user_id': 7, 'amount': 251.98, 'latitude': 80.006709, 'longitude': -103.271888},
    {'user_id': 7, 'amount': 0, 'latitude': 54.044809, 'longitude': -123.445968},
    {'user_id': 8, 'amount': 57.54, 'latitude': -45.88939, 'longitude': -2.115805},
    {'user_id': 2, 'amount': 0, 'latitude': 34.032527, 'longitude': -117.881451},
    {'user_id': 7, 'amount': 484.67, 'latitude': -46.527032, 'longitude': -155.566774},
    {'user_id': 6, 'amount': 166.76, 'latitude': 46.785413, 'longitude': 9.385204},
    {'user_id': 7, 'amount': 7, 'latitude': 42.672592, 'longitude': -77.870346},
    {'user_id': 5, 'amount': 56.12, 'latitude': 42.99705, 'longitude': -8.554843},
    # Więcej danych
]


import numpy as np

def is_anomaly(user_id, new_transaction, data, n=10, threshold=3):
    # Filtrujemy dane dla danego użytkownika
    user_data = [d['amount'] for d in data if d['user_id'] == user_id]
    
    # Jeśli użytkownik ma mniej niż n transakcji, bierzemy wszystkie
    if len(user_data) < n:
        n = len(user_data)
    
    # Pobieramy ostatnie n transakcji
    last_n_transactions = user_data[-n:]
    
    # Obliczamy średnią i odchylenie standardowe
    mean = np.mean(last_n_transactions)
    std = np.std(last_n_transactions)
    
    # Nowa kwota transakcji
    new_amount = new_transaction['amount']
    
    # Sprawdzamy, czy nowa transakcja jest anomalią
    if std == 0:
        # Jeśli odchylenie standardowe jest 0, każda różnica jest anomalią
        return new_amount != mean
    else:
        z_score = (new_amount - mean) / std
        return abs(z_score) > threshold

# Przykład użycia funkcji
new_transaction = {'user_id': 7, 'amount': 500, 'latitude': 42.672592, 'longitude': -77.870346}
print(is_anomaly(7, new_transaction, data))




def is_anomaly_iqr(user_id, new_transaction, data, n=10):
    # Filtrujemy dane dla danego użytkownika
    user_data = [d['amount'] for d in data if d['user_id'] == user_id]
    
    # Jeśli użytkownik ma mniej niż n transakcji, bierzemy wszystkie
    if len(user_data) < n:
        n = len(user_data)
    
    # Pobieramy ostatnie n transakcji
    last_n_transactions = user_data[-n:]
    
    # Obliczamy kwartyle
    q1 = np.percentile(last_n_transactions, 25)
    q3 = np.percentile(last_n_transactions, 75)
    iqr = q3 - q1
    
    # Definiujemy granice anomalii
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Nowa kwota transakcji
    new_amount = new_transaction['amount']
    
    # Sprawdzamy, czy nowa transakcja jest anomalią
    return new_amount < lower_bound or new_amount > upper_bound

# Przykład użycia funkcji
new_transaction = {'user_id': 7, 'amount': 500, 'latitude': 42.672592, 'longitude': -77.870346}
print(is_anomaly_iqr(7, new_transaction, data))



from sklearn.svm import OneClassSVM
import numpy as np

def is_anomaly_svm(user_id, new_transaction, data, n=10):
    # Filtrujemy dane dla danego użytkownika
    user_data = [d for d in data if d['user_id'] == user_id]
    
    # Jeśli użytkownik ma mniej niż n transakcji, bierzemy wszystkie
    if len(user_data) < n:
        n = len(user_data)
    
    # Pobieramy ostatnie n transakcji
    last_n_transactions = user_data[-n:]
    
    # Przygotowujemy dane do modelu SVM (używamy tylko kwoty transakcji)
    X = np.array([[d['amount']] for d in last_n_transactions])
    
    # Inicjalizujemy model OneClassSVM
    model = OneClassSVM(gamma='auto', nu=0.1)
    model.fit(X)
    
    # Nowa transakcja
    new_amount = [[new_transaction['amount']]]
    
    # Przewidujemy, czy nowa transakcja jest anomalią
    is_anomaly = model.predict(new_amount)
    
    # OneClassSVM zwraca -1 dla anomalii i 1 dla normalnych danych
    return is_anomaly[0] == -1

# Przykład użycia funkcji
new_transaction = {'user_id': 7, 'amount': 500, 'latitude': 42.672592, 'longitude': -77.870346}
print(is_anomaly_svm(7, new_transaction, data))



from sklearn.cluster import KMeans
import numpy as np

def is_anomaly_kmeans(user_id, new_transaction, data, n=10, k=2, threshold=3):
    # Filtrujemy dane dla danego użytkownika
    user_data = [d for d in data if d['user_id'] == user_id]
    
    # Jeśli użytkownik ma mniej niż n transakcji, bierzemy wszystkie
    if len(user_data) < n:
        n = len(user_data)
    
    # Pobieramy ostatnie n transakcji
    last_n_transactions = user_data[-n:]
    
    # Przygotowujemy dane do modelu k-means (używamy tylko kwoty transakcji)
    X = np.array([[d['amount']] for d in last_n_transactions])
    
    # Inicjalizujemy model KMeans
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    
    # Przypisujemy każdej transakcji odległość do najbliższego centroidu
    distances = kmeans.transform(X).min(axis=1)
    
    # Definiujemy granice anomalii na podstawie średniej i odchylenia standardowego odległości
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)
    
    # Nowa transakcja
    new_amount = [[new_transaction['amount']]]
    new_distance = kmeans.transform(new_amount).min(axis=1)[0]
    
    # Sprawdzamy, czy nowa transakcja jest anomalią
    return abs(new_distance - mean_distance) > threshold * std_distance

# Przykład użycia funkcji
new_transaction = {'user_id': 7, 'amount': 500, 'latitude': 42.672592, 'longitude': -77.870346}
print(is_anomaly_kmeans(7, new_transaction, data))
