import random
from geopy.distance import geodesic
from transactions_history import TransactionHistory

history = TransactionHistory()

def add_transaction(user_id, amount, latitude, longitude, anomaly):
    history.add_transaction(user_id, amount, latitude, longitude, anomaly)


def generate_random_transactions(num_transactions, user):
    transactions = []
    base_location = (52.2296756, 21.0122287) 
    
    for _ in range(num_transactions):

        amount = round(random.uniform(50, 500), 2) 
        latitude = round(random.uniform(50, 54), 6)
        longitude = round(random.uniform(19, 23), 6)

        anomaly = 0

        rand = random.random()
        if rand <= 0.3:
            amount = random.randint(1, 9)
            anomaly = 1
        elif rand > 0.3 and rand < 0.4:
            latitude = round(random.uniform(-90, 90), 6)
            longitude = round(random.uniform(-180, 180), 6)
            while 50 <= latitude <= 54 and 19 <= longitude <= 23:
                latitude = round(random.uniform(-90, 90), 6)
                longitude = round(random.uniform(-180, 180), 6)
            anomaly = 1

        transactions.append((user, amount, latitude, longitude, anomaly))
    
    return transactions

transactions = generate_random_transactions(1000, "user1")

for transaction in transactions:
    add_transaction(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4])


