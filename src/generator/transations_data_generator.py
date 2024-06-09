import random

def generate_transaction(intro_mode=False) -> dict:
    user_id = random.randint(1, 10)
    card_id = random.randint(1,3)
    locations = {
        1: ('Warszawa', 50, 53, 19, 22),
        2: ('Los Angeles', 35, 38, -118, -120),
        3: ('Berlin', 50, 52, 12, 14),
        4: ('Paryż', 46, 48, 2, 4),
        5: ('Madryt', 39, 41, -3, -5),
        6: ('Rzym', 42, 43, 12, 13),
        7: ('Toronto', 41, 43, -78, -79),
        8: ('São Paulo', -21, -23, -44, -46),
        9: ('Sydney', -32, -34, 149, 151),
        10: ('Tokio', 35, 37, 139, 140)
    }

    city, lat_min, lat_max, lon_min, lon_max = locations[user_id]

    amount = round(random.uniform(50, 12000), 2)
    latitude = round(random.uniform(lat_min, lat_max), 6)
    longitude = round(random.uniform(lon_min, lon_max), 6)
    trans_limit = random.randint(5000, 10000)
    
    if not intro_mode:
        rand = random.random()
        if rand <= 0.2:
            amount = random.randint(0, 5000)
        elif rand > 0.2 and rand <= 0.4:
            latitude = round(random.uniform(-90, 90), 6)
            longitude = round(random.uniform(-180, 180), 6)
        
    return {
        'user_id': user_id,
        'card_id': card_id,
        'amount': amount,
        'latitude': latitude,
        'longitude': longitude,
        'trans_limit': trans_limit
    }
