import random
import json

# Przykładowa lista ID użytkowników
user_ids = list(range(1, 101))

# Zakres dostępnych limitów na kartach kredytowych
credit_limits = list(range(500, 10001, 500))

# Lista ID kart kredytowych
card_ids = list(range(1000, 1100))

# Przykładowe centra lokalizacji dla użytkowników
user_locations = {
    1: (52.2297, 21.0122),  # Warsaw, Poland
    2: (48.8566, 2.3522),   # Paris, France
    3: (40.7128, -74.0060), # New York, USA
    # Dodaj więcej użytkowników i ich główne lokalizacje
}

def generate_random_location(center):
    latitude = round(center[0] + random.uniform(-0.1, 0.1), 4)
    longitude = round(center[1] + random.uniform(-0.1, 0.1), 4)
    return (latitude, longitude)

def generate_credit_card_transaction(user_id) -> dict:
    card_id = random.choice(card_ids)
    center_location = user_locations[user_id]
    location = generate_random_location(center_location)
    transaction_value = round(random.uniform(50, 1000), 2)
    credit_limit = random.choice(credit_limits)
    
    # Okazjonalna anomalia
    anomaly = None
    if random.random() < 0.1:  # 10% szansa na anomalię
        anomaly = random.choice(['location_change', 'low_amount'])
        if anomaly == 'location_change':
            location = generate_random_location((random.uniform(-90, 90), random.uniform(-180, 180)))
        elif anomaly == 'low_amount':
            transaction_value = round(random.uniform(1, 10), 2)
    
    transaction = {
        'user_id': user_id,
        'card_id': card_id,
        'location': location,
        'transaction_value': transaction_value,
        'credit_limit': credit_limit,
        'anomaly': anomaly                          # ta zmienna bedzie uzywana zeby sprawdzic czy wykrycie anomalii bylo prawidlowe
    }
    
    return transaction

# Generowanie przykładowych danych transakcji dla każdego użytkownika
transactions = []
for user_id in user_ids:
    if user_id in user_locations:
        num_transactions = random.randint(3, 10)  # Przykładowa liczba transakcji na użytkownika
        for _ in range(num_transactions):
            transactions.append(generate_credit_card_transaction(user_id))

print(json.dumps(transactions, indent=4))
