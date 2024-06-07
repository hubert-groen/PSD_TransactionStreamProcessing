import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer

time_to_sleep = 5

def serializer(message):
    return json.dumps(message).encode('utf-8')

def generate_temp():
    return {
        'id':1,
        'time':str(datetime.now()),
        'temp':random.randint(-20, 50)
    }


producer_1 = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
    )

if __name__ == '__main__':
    while True:
        mess = generate_temp()
        print(f'Producing message: {str(mess)}')
        producer_1.send('TEMP', mess)
        time.sleep(time_to_sleep)