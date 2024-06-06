import random

def generate_transaction() -> dict:
    user_id = "user1"
    

    if random.random() < 0.2:  # 10% chance to get a value between 1 and 9
        amount = random.randint(0, 9)
        latitude = round(random.uniform(1, 2), 6)
        longitude = round(random.uniform(2, 3), 6)
    else:
        amount = random.randint(20, 500)
        latitude = round(random.uniform(50, 53), 6)
        longitude = round(random.uniform(17, 22), 6)
        
    return {
        'user_id': user_id,
        'amount': amount,
        'latitude': latitude,
        'longitude': longitude
    }
