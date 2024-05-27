import json
import joblib

from anomaly_detection import is_anomalous_transaction
from kafka import KafkaConsumer
from kafka import KafkaProducer

def serializer(message):
    return json.dumps(message).encode('utf-8')

def dict_to_tuple(transaction: dict) -> tuple:
    user_id = transaction['user_id']
    amount = float(transaction['amount'])
    latitude = transaction['latitude']
    longitude = transaction['longitude']
    return (user_id, amount, latitude, longitude)


model = joblib.load('20240525_132030_my_model.pkl')

producer_2 = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
    )



if __name__ == '__main__':
# Kafka Consumer
    consumer = KafkaConsumer(
        'TOPIC-A',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
        )
    
    for transaction in consumer:

            # Decode the byte string to a JSON string
        transaction_value_json = transaction.value.decode('utf-8')

        # Parse the JSON string
        transaction_data = json.loads(transaction_value_json)

        # Extract the needed fields
        user_id = transaction_data['user_id']
        amount = transaction_data['amount']
        latitude = transaction_data['latitude']
        longitude = transaction_data['longitude']


        if is_anomalous_transaction(user_id, amount, latitude, longitude, model) or amount < 3:
            print("!!!!!!!!!!!!! Anomaly detected")
            print(json.loads(transaction.value))
            new = {'user_id': user_id,
                   'amount': amount,
                   'latitude': latitude,
                   'longitude': longitude}
            producer_2.send('TOPIC-B', new)
        else:
            print("Normal")
            print(json.loads(transaction.value))