import json
from kafka import KafkaConsumer

if __name__ == '__main__':
# Kafka Consumer
    consumer = KafkaConsumer(
        'TOPIC-B',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
        )
    for message in consumer:
        print('transaction after processing:')
        print(json.loads(message.value))