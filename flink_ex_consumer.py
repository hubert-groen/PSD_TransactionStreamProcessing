from pyflink.common import WatermarkStrategy, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaTopicPartition, KafkaSink,  KafkaRecordSerializationSchema
from pyflink.datastream.connectors import KafkaSource
import json
from anomaly_detection import is_anomalous_transaction
import joblib
import os

# MODEL = joblib.load(os.path.abspath(os.path.dirname(__file__))+'/models/20240525_132030_my_model.pkl')

def verify_transaction(transaction_string: str):
    transaction_json = json.loads(transaction_string)
    user_id = transaction_json['user_id']
    amount = transaction_json['amount']
    latitude = transaction_json['latitude']
    longitude = transaction_json['longitude']
    
    # return is_anomalous_transaction(user_id, amount, latitude, longitude, MODEL)
    return False    


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
        .set_topics('TOPICA') \
        .set_group_id("test_group") \
        .set_starting_offsets(offset) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    record_serializer = KafkaRecordSerializationSchema.builder() \
        .set_topic('OUTPUT') \
        .set_value_serialization_schema(SimpleStringSchema()) \
        .build()

    sink = KafkaSink.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_record_serializer(record_serializer) \
        .build()

    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    ds.print()

    ds.map(lambda x: "\n " + 'Transaction ' + x +' is anomalous: ' + str(verify_transaction(x)), output_type=Types.STRING()).print()
    ds = ds.map(lambda x: "\n " + 'Transaction ' + x +' is anomalous: ' + str(verify_transaction(x)), output_type=Types.STRING())

    ds.sink_to(sink)

    # Print line for readablity in the console
    print("start reading data from kafka")



    env.execute("Detect anomalous transaction")
