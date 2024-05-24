import numpy as np
from geopy.distance import geodesic


def is_anomalous_transaction(user_id, amount, latitude, longitude, history, threshold=2):
    transactions = history.get_recent_transactions()
    
    if len(transactions) < 10:
        return False  # Początkowo zbieramy dane
    
    amounts = [t[1] for t in transactions]
    latitudes = [t[2] for t in transactions]
    longitudes = [t[3] for t in transactions]
    
    mean_amount = np.mean(amounts)
    std_amount = np.std(amounts)
    
    if abs(amount - mean_amount) > threshold * std_amount:
        return True  # Anomalia w wartości transakcji
    
    mean_location = (np.mean(latitudes), np.mean(longitudes))
    distance = geodesic(mean_location, (latitude, longitude)).km
    
    if distance > threshold * np.std([geodesic((lat, lon), mean_location).km for lat, lon in zip(latitudes, longitudes)]):
        return True  # Anomalia w lokalizacji
    
    return False