from pyflink.common import WatermarkStrategy, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaTopicPartition, KafkaSink,  KafkaRecordSerializationSchema
from pyflink.datastream.connectors import KafkaSource
import json
import joblib
import os
import numpy as np

MODEL = joblib.load(os.path.abspath(os.path.dirname(__file__))+'/models/20240525_132030_my_model.pkl')

def is_anomalous_transaction(user_id, amount, latitude, longitude, model):
    # Nowa transakcja
    new_transaction = np.array([[amount, latitude, longitude]])
    
    # Wykrywanie anomalii
    is_anomaly = model.predict(new_transaction)[0] == 1
    
    #return is_anomaly
    if is_anomaly:
        return 1
    return 0


def verify_transaction(transaction_string: str):
    transaction_json = json.loads(transaction_string)
    user_id = transaction_json['user_id']
    amount = transaction_json['amount']
    latitude = transaction_json['latitude']
    longitude = transaction_json['longitude']
    
    return is_anomalous_transaction(user_id, amount, latitude, longitude, MODEL)
    #return 0    


if __name__ == '__main__':
    # Create a StreamExecutionEnvironment
    env = StreamExecutionEnvironment.get_execution_environment()


    properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '1',
    }

    env.set_parallelism(1)


    deserialization_schema = SimpleStringSchema()
    # deserialization_schema = DeserializationSchema()

    deserialization_schema = JsonRowDeserializationSchema.builder() \
        .type_info(type_info=Types.ROW([Types.STRING(), Types.INT(), Types.FLOAT(), Types.FLOAT()])).build()


    earliest = False
    offset = KafkaOffsetsInitializer.earliest() if earliest else KafkaOffsetsInitializer.latest()

    source = KafkaSource.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('TOPIC-Q1') \
        .set_group_id("test_group") \
        .set_starting_offsets(offset) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    record_serializer = KafkaRecordSerializationSchema.builder() \
        .set_topic('TOPIC-Q2') \
        .set_value_serialization_schema(SimpleStringSchema()) \
        .build()

    sink = KafkaSink.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_record_serializer(record_serializer) \
        .build()

    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    ds.print()

    ds.map(lambda x: "\n " + 'Transaction ' + x +' is anomalous: ' + str(verify_transaction(x)), output_type=Types.STRING()).print()
    #ds = ds.map(lambda x: "\n " + 'Transaction ' + x +' is anomalous: ' + str(verify_transaction(x)), output_type=Types.STRING())

    ds = ds.map(lambda x: "\n " + str(x[:-1]) + ', "anomaly": ' + str(verify_transaction(x)) + '}', output_type=Types.STRING())


    ds.sink_to(sink)

    # Print line for readablity in the console
    print("start reading data from kafka")



    env.execute("Detect anomalous transaction")
