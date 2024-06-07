import random

def generate_transaction() -> dict:
    user_id = random.randint(1, 10)
    
    # Mapping user_id to their typical location range
    locations = {
        1: ('Warsaw', 50, 54, 19, 23),
        2: ('Los Angeles', 33.5, 34.5, -118.5, -117.5),
        3: ('Berlin', 47, 55, 5, 15),
        4: ('Paris', 41, 51, -5, 8),
        5: ('Madryt', 36, 43, -9, 4),
        6: ('Rome', 36, 47, 6, 19),
        7: ('Toronto', 42, 83, -141, -52),
        8: ('São Paulo', -34, 5, -74, -35),
        9: ('Sydney', -44, -10, 113, 154),
        10: ('Tokio', 24, 46, 123, 146)
    }

    city, lat_min, lat_max, lon_min, lon_max = locations[user_id]

    amount = round(random.uniform(50, 500), 2)
    latitude = round(random.uniform(lat_min, lat_max), 6)
    longitude = round(random.uniform(lon_min, lon_max), 6)
    
    rand = random.random()
    if rand <= 0.2:
        amount = random.randint(0, 9)
    elif rand > 0.2 and rand <= 0.4:
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        
    return {
        'user_id': user_id,
        'amount': amount,
        'latitude': latitude,
        'longitude': longitude
    }

for _ in range(10):
    print(generate_transaction())