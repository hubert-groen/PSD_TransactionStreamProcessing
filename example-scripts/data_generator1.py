import random
import string

user_ids = list(range(1, 101))

def generate_message1() -> dict:
    random_user_id = random.choice(user_ids)
    # Generate a random message
    temp=str(random.randint(-15,30))
    message = ''.join(temp)
    return {
        'user_id': random_user_id,
        'message': message
        }