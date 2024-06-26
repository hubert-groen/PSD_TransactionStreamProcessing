import time
import json
import random
from datetime import datetime
from src.generator.transations_data_generator import generate_transaction
from kafka import KafkaProducer

# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer_1 = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
    )

if __name__ == '__main__':
    # Infinite loop - runs until you kill the program

    for i in range(20):
        transaction = generate_transaction(intro_mode=True)
        print(f'Producing INTRO message {datetime.now()} | Message = {str(transaction)}')
        producer_1.send('TOPIC-NA1', transaction)
        time_to_sleep = random.randint(1, 1)
        time.sleep(time_to_sleep)
        i += 1

    while True:
        # Generate a message
        transaction = generate_transaction()
        # Send it to our 'TOPIC-A' topic
        print(f'Producing message {datetime.now()} | Message = {str(transaction)}')
        producer_1.send('TOPIC-NA1', transaction)
        # Sleep for a random number of seconds
        time_to_sleep = random.randint(1, 1)
        time.sleep(time_to_sleep)