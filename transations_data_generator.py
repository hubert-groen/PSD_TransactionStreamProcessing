import random

def generate_transaction() -> dict:
    user_id = "user1"

    amount = round(random.uniform(50, 500), 2)
    latitude = round(random.uniform(50, 54), 6)
    longitude = round(random.uniform(19, 23), 6)
    
    rand = random.random()
    if rand <= 0.2:
        amount = random.randint(0, 9)

    elif rand > 0.2 and rand <= 0.4:
        # latitude = round(random.uniform(20, 24), 6)
        # longitude = round(random.uniform(11, 13), 6)
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        
    return {
        'user_id': user_id,
        'amount': amount,
        'latitude': latitude,
        'longitude': longitude
    }

        

