from pyflink.common import WatermarkStrategy, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaTopicPartition, KafkaSink,  KafkaRecordSerializationSchema
from pyflink.datastream.connectors import KafkaSource

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()


properties = {
'bootstrap.servers': '3W0CWL3.emrsn.org:9092',
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
    .set_topics('SOMETHING') \
    .set_group_id("test_group") \
    .set_starting_offsets(offset) \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

# record_serializer = KafkaRecordSerializationSchema.builder() \
#     .set_topic('SOMETHING_ELSE') \
#     .set_value_serialization_schema(SimpleStringSchema()) \
#     .build()

# sink = KafkaSink.builder() \
#     .set_bootstrap_servers('localhost:9092') \
#     .set_record_serializer(record_serializer) \
#     .build()

ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
ds.print()

# ds.add_sink(sink)

# Print line for readablity in the console
print("start reading data from kafka")

ds.map(lambda x: "\n " + str(x), output_type=Types.STRING()).print()

env.execute("Kafka Source Example")
