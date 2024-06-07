import random
from geopy.distance import geodesic
from transactions_history import TransactionHistory

history = TransactionHistory()

def add_transaction(user_id, amount, latitude, longitude, anomaly):
    history.add_transaction(user_id, amount, latitude, longitude, anomaly)

def generate_random_transactions(num_transactions, user, anomaly_distance_threshold=100):
    transactions = []
    base_location = (52.2296756, 21.0122287)  # Baza lokalizacji (np. Warszawa)
    
    for _ in range(num_transactions):
        amount = round(random.uniform(50, 500), 2)  # Losowa kwota transakcji między 1 a 500
        lat = round(random.uniform(50, 54), 6)    # Losowa szerokość geograficzna w Polsce
        lon = round(random.uniform(19, 23), 6)    # Losowa długość geograficzna w Polsce
        
        transaction_location = (lat, lon)
        distance = geodesic(base_location, transaction_location).km

        anomaly = 0

        rand = random.random()
        if rand <= 0.3:
            amount = random.randint(1, 9)
            anomaly = 1
        elif rand > 0.3 and rand < 0.4:
            latitude = round(random.uniform(-90, 90), 6)
            longitude = round(random.uniform(-180, 180), 6)
            anomaly = 1
        
        transactions.append((user, amount, lat, lon, anomaly))
    
    return transactions


transactions = generate_random_transactions(1000, "user1")

for transaction in transactions:
    add_transaction(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4])