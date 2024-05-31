import json
import logging
import sys
import joblib
from pyflink.common import SimpleStringSchema, Types
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.datastream.functions import MapFunction
from pyflink.datastream.connectors import SerializationSchema

# Import the anomaly detection function and model
from anomaly_detection import is_anomalous_transaction

# Load the pre-trained model
model = joblib.load('20240525_132030_my_model.pkl')

class AnomalyDetectionMapFunction(MapFunction):
    def map(self, value):
        transaction_data = json.loads(value)
        user_id = transaction_data['user_id']
        amount = transaction_data['amount']
        latitude = transaction_data['latitude']
        longitude = transaction_data['longitude']
        
        if is_anomalous_transaction(user_id, amount, latitude, longitude, model) or amount < 3:
            result = {
                'user_id': user_id,
                'amount': amount,
                'latitude': latitude,
                'longitude': longitude
            }
            return json.dumps(result)
        else:
            return None

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    
    # Kafka source
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('TOPIC-A') \
        .set_group_id('flink-group') \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .build()
    
    # Kafka sink
    kafka_sink = KafkaSink.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_record_serializer(KafkaRecordSerializationSchema.builder()
                               .set_topic('TOPIC-B')
                               .set_value_serialization_schema(SerializationSchema(SimpleStringSchema()))
                               .build()) \
        .build()
    
    # Define the Flink pipeline
    ds = env.from_source(source=kafka_source, watermark_strategy=None, source_name="Kafka Source") \
            .map(AnomalyDetectionMapFunction(), output_type=Types.STRING()) \
            .filter(lambda x: x is not None) \
            .sink_to(kafka_sink)

    # Execute the Flink job
    env.execute("Kafka Flink Anomaly Detection Job")

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    main()
