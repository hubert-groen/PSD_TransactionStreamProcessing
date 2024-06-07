import random

def generate_transaction() -> dict:
    user_id = random.randint(1, 10)
    
    locations = {
        1: ('Warszawa', 52.2297, 52.2297, 21.0122, 21.0122),
        2: ('Los Angeles', 34.0522, 34.0522, -118.2437, -118.2437),
        3: ('Berlin', 52.5200, 52.5200, 13.4050, 13.4050),
        4: ('Paryż', 48.8566, 48.8566, 2.3522, 2.3522),
        5: ('Madryt', 40.4168, 40.4168, -3.7038, -3.7038),
        6: ('Rzym', 41.9028, 41.9028, 12.4964, 12.4964),
        7: ('Toronto', 43.6510, 43.6510, -79.3470, -79.3470),
        8: ('São Paulo', -23.5505, -23.5505, -46.6333, -46.6333),
        9: ('Sydney', -33.8688, -33.8688, 151.2093, 151.2093),
        10: ('Tokio', 35.6895, 35.6895, 139.6917, 139.6917)
    }

    city, lat_min, lat_max, lon_min, lon_max = locations[user_id]

    amount = round(random.uniform(50, 500), 2)
    latitude = round(random.uniform(lat_min, lat_max), 6)
    longitude = round(random.uniform(lon_min, lon_max), 6)
    
    # rand = random.random()
    # if rand <= 0.2:
    #     amount = random.randint(0, 9)
    # elif rand > 0.2 and rand <= 0.4:
    #     latitude = round(random.uniform(-90, 90), 6)
    #     longitude = round(random.uniform(-180, 180), 6)
        
    return {
        'user_id': user_id,
        'amount': amount,
        'latitude': latitude,
        'longitude': longitude
    }

for _ in range(10):
    print(generate_transaction())