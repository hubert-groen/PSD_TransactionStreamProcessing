from pyflink.common import WatermarkStrategy, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.datastream import StreamExecutionEnvironment

#state
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.datastream import StreamExecutionEnvironment, FlatMapFunction, RuntimeContext

from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaTopicPartition, KafkaSink,  KafkaRecordSerializationSchema
from pyflink.datastream.connectors import KafkaSource
import json
import joblib
import os
import numpy as np


properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '1',
} 

class CountWindowAverage(FlatMapFunction):

    def __init__(self):
        self.sum = None

    def open(self, runtime_context: RuntimeContext):
        descriptor = ValueStateDescriptor(
            "average",  # the state name
            Types.PICKLED_BYTE_ARRAY()  # type information
        )
        self.sum = runtime_context.get_state(descriptor)

    def flat_map(self, value):
        # access the state value
        current_avg = self.sum.value()
        if current_avg is None:
            current_avg = (0, 0, 0, 0)

        # update the count
        current_avg = (current_avg[0] + 1, 
                       current_avg[1] + value['amount'],
                       current_avg[1] + value['latitude'],
                       current_avg[1] + value['longitude'])
        
        current_avg = (current_avg[0], current_avg[1]/current_avg[0], 
                       current_avg[2]/current_avg[0], current_avg[3]/current_avg[0])

        # update the state
        self.sum.update(current_avg)
        value['average-amount'] = current_avg[1]
        value['average-latitude'] = current_avg[2]
        value['average-longitude'] = current_avg[3]
        

        yield value


if __name__ == '__main__':
    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)


    deserialization_schema = SimpleStringSchema()

    deserialization_schema = JsonRowDeserializationSchema.builder() \
        .type_info(type_info=Types.ROW([Types.STRING(), Types.INT(), Types.FLOAT(), Types.FLOAT()])).build()


    earliest = False
    offset = KafkaOffsetsInitializer.earliest() if earliest else KafkaOffsetsInitializer.latest()

    source = KafkaSource.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('TOPIC-Q3') \
        .set_group_id("test_group") \
        .set_starting_offsets(offset) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    record_serializer = KafkaRecordSerializationSchema.builder() \
        .set_topic('TOPIC-Q4') \
        .set_value_serialization_schema(SimpleStringSchema()) \
        .build()

    sink = KafkaSink.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_record_serializer(record_serializer) \
        .build()

    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    ds.print()
    ds = ds.map(lambda x: json.loads(x))
        
    ds = ds.key_by(lambda x:  x['user_id']) \
        .flat_map(CountWindowAverage())

    ds.map(lambda x: "\n " + str(x), output_type=Types.STRING()).print()

    ds = ds.map(lambda x: str(x), output_type=Types.STRING())


    ds.sink_to(sink)

    print("start reading data from kafka")

    env.execute("Detect anomalous transaction")
