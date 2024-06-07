from pyflink.common import WatermarkStrategy, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream.functions import FilterFunction
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaTopicPartition, KafkaSink,  KafkaRecordSerializationSchema
from pyflink.datastream.connectors import KafkaSource
import json

if __name__ == '__main__':
    # Create a StreamExecutionEnvironment
    env = StreamExecutionEnvironment.get_execution_environment()


    properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '1',
    }

    env.set_parallelism(1)

    deserialization_schema = SimpleStringSchema()

    earliest = False
    offset = KafkaOffsetsInitializer.earliest() if earliest else KafkaOffsetsInitializer.latest()

    source = KafkaSource.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('TEMP') \
        .set_group_id("test_group") \
        .set_starting_offsets(offset) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    record_serializer = KafkaRecordSerializationSchema.builder() \
        .set_topic('ALARM_TEMP') \
        .set_value_serialization_schema(SimpleStringSchema()) \
        .build()

    sink = KafkaSink.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_record_serializer(record_serializer) \
        .build()

    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    ds.print()

    ds = ds.map(lambda x: json.loads(x))
    ds.print()
    ds = ds.filter(lambda x: x['temp']<0)
    ds = ds.map(lambda x: str(json.dumps(x).encode('utf-8')), output_type=Types.STRING())
    ds.sink_to(sink)

    # Print line for readablity in the console
    print("start reading data from kafka")

    env.execute("Detect temperature below 0")
