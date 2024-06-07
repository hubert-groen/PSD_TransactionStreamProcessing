from transactions_history import TransactionHistory

history = TransactionHistory()

def add_transaction(user_id, amount, latitude, longitude, anomaly):
    history.add_transaction(user_id, amount, latitude, longitude, anomaly)

# add_transaction("user1", 50.0, 52.2296756, 21.0122287, 0)
# add_transaction("user1", 100.0, 52.2296756, 21.0122287, 0)
# add_transaction("user1", 50.0, 52.2296756, 21.0122287, 0)
# add_transaction("user1", 100.0, 52.406374, 16.9251681, 0)
# add_transaction("user1", 20.0, 50.0646501, 19.9449799, 0)
# add_transaction("user1", 150.0, 51.1078852, 17.0385376, 0)
# add_transaction("user1", 75.0, 53.1324886, 23.1688403, 0)
# add_transaction("user1", 200.0, 50.0411867, 21.9991196, 0)
# add_transaction("user1", 30.0, 51.7592485, 19.4559833, 0)
# add_transaction("user1", 500.0, 52.2296756, 21.0122287, 0)
# add_transaction("user1", 10.0, 52.406374, 16.9251681, 0)
# add_transaction("user1", 125.0, 50.0646501, 19.9449799, 0)
# add_transaction("user1", 60.0, 51.1078852, 17.0385376, 0)
# add_transaction("user1", 300.0, 53.1324886, 23.1688403, 0)
# add_transaction("user1", 85.0, 50.0411867, 21.9991196, 0)
# add_transaction("user1", 20.0, 51.7592485, 19.4559833, 0)
# add_transaction("user1", 450.0, 52.2296756, 21.0122287, 0)
# add_transaction("user1", 1.0, 52.2296756, 21.0122287, 1)
# add_transaction("user1", 2.0, 52.2296756, 21.0122287, 1)
# add_transaction("user1", 1.0, 52.2296756, 21.0122287, 1)



import random
from geopy.distance import geodesic

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
            lat = round(random.uniform(20, 24), 6)
            lon = round(random.uniform(11, 13), 6)
            anomaly = 1
        
        transactions.append((user, amount, lat, lon, anomaly))
    
    return transactions

# Generowanie 20 losowych transakcji
transactions = generate_random_transactions(1000, "user1")

# Wyświetlenie transakcji
for transaction in transactions:
    add_transaction(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4])
    #print(f"add_transaction(\"{transaction[0]}\", {transaction[1]}, {transaction[2]}, {transaction[3]}, {transaction[4]})")
