import json
from kafka import KafkaConsumer

if __name__ == '__main__':
# Kafka Consumer
    consumer = KafkaConsumer(
        'TOPIC-A2',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
        )
    for message in consumer:
        print('transaction after processing:')
        value = message.value
        corrected_message_value = value.decode('utf-8').replace("'", '"')
        print(json.loads(corrected_message_value))
        

