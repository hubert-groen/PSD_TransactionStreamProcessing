import json
import joblib
import argparse
import logging
import sys
import numpy as np

# KAFKA
from kafka import KafkaConsumer, KafkaProducer

# FLINK
from pyflink.common import WatermarkStrategy, Encoder, Types
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.functions import MapFunction, RuntimeContext


def serializer(message):
    return json.dumps(message).encode('utf-8')

def dict_to_tuple(transaction: dict) -> tuple:
    user_id = transaction['user_id']
    amount = float(transaction['amount'])
    latitude = transaction['latitude']
    longitude = transaction['longitude']
    return (user_id, amount, latitude, longitude)



model = joblib.load('/home/psd/kafka-producer-consumer/PSD_TransactionStreamProcessing/20240525_132030_my_model.pkl')



def is_anomalous_transaction(user_id, amount, latitude, longitude, model=model):
    new_transaction = np.array([[amount, latitude, longitude]])
    is_anomaly = model.predict(new_transaction)[0] == 1
    return is_anomaly

class AnomalyDetectionMapFunction(MapFunction):
    def open(self, runtime_context: RuntimeContext):
        self.model = model
    
    def map(self, transaction):
        user_id, amount, latitude, longitude = transaction
        if is_anomalous_transaction(user_id, amount, latitude, longitude, self.model):
            return transaction
        else:
            return 'normal'

# Przygotowanie środowiska wykonawczego Flink
env = StreamExecutionEnvironment.get_execution_environment()
env.set_runtime_mode(RuntimeExecutionMode.BATCH)
env.set_parallelism(1)

# Kafka Producer
producer_2 = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

def flink_processing(transaction):

    transaction_value_json = transaction.value.decode('utf-8')
    transaction_data = json.loads(transaction_value_json)
    transaction_tuple = dict_to_tuple(transaction_data)

    ds = env.from_collection([transaction_tuple])

    ds = ds.map(AnomalyDetectionMapFunction(), output_type=Types.TUPLE([Types.STRING(), Types.FLOAT(), Types.FLOAT(), Types.FLOAT()])) \
          .filter(lambda x: x is not None)

    ds.print()
    env.execute('Flink Anomaly Detection')

if __name__ == '__main__':
    # Kafka Consumer
    consumer = KafkaConsumer(
        'TOPIC-A',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--input',
    #     dest='input',
    #     required=False,
    #     help='Input file to process.')
    # parser.add_argument(
    #     '--output',
    #     dest='output',
    #     required=False,
    #     help='Output file to write results to.')

    # argv = sys.argv[1:]
    # known_args, _ = parser.parse_known_args(argv)

    print('here')

    for transaction in consumer:
        print('flink processing')
        # flink_processing(transaction)
        print(transaction)
