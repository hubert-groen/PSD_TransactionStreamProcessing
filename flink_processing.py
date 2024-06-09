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
import datetime
import math

ACCEPTED_TRANSACTION_FREQUENCY = 10
TRANSACTION_QUEUE_SIZE = 10

COUNTER_IDX = 0
TRANS_SUM_IDX = 1
PREV_TRANS_IDX = 2


class ProcessTransaction(FlatMapFunction):
    
    def __init__(self):
        self.state = None

    def open(self, runtime_context: RuntimeContext):
        descriptor = ValueStateDescriptor(
            "transaction_state",  # the state name
            Types.PICKLED_BYTE_ARRAY()  # type information
        )
        self.state = runtime_context.get_state(descriptor)

    def update_transaction_buffer(self, new_value, buffer):
        transaction = {
            'amount':new_value['amount'],
            'datetime':datetime.datetime.now(),
            'latitude':new_value['latitude'],
            'longitude':new_value['longitude']
        }
        buffer.append(transaction)
        if (len(buffer)>TRANSACTION_QUEUE_SIZE):
            buffer.pop(0)
        
    def detect_anomaly(self, curr_trans, state) -> str:
        if(curr_trans['amount']>curr_trans['trans_limit']):
            return 'Trans_limit'
        elif(self.is_amount_anomalous(curr_trans, state)):
            return 'Amount'
        elif(self.is_geolocation_anomalous(curr_trans, state)):
            return 'Geolocation'
        elif(self.is_frequency_anomalous(curr_trans, state[PREV_TRANS_IDX])):
            return 'Frequency'
        else:
            return 'None'
    
    def is_amount_anomalous(self, curr_trans, state):
        if len(state[PREV_TRANS_IDX]) < 4:       # 4 is some arbitrary number of min transactions
            return False
        avg_trans = state[TRANS_SUM_IDX]/len(state[PREV_TRANS_IDX])
        # some dummy method - to be improved
        return (curr_trans['amount']-avg_trans)>4*avg_trans


    def haversine_distance(self, lat1, lon1, lat2, lon2):
        '''
        - some common function to calculate distrance taking into acount flatness of the earth XD
        '''
        R = 6371.0

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

    def is_geolocation_anomalous(self, curr_trans, state):
        prev_transactions = state[PREV_TRANS_IDX]
        if len(prev_transactions) < 4:  # 4 is some arbitrary number of min transactions
            return False

        avg_latitude = sum(trans['latitude'] for trans in prev_transactions) / len(prev_transactions)
        avg_longitude = sum(trans['longitude'] for trans in prev_transactions) / len(prev_transactions)

        distance = self.haversine_distance(avg_latitude, avg_longitude,
                                    curr_trans['latitude'], curr_trans['longitude'])

        return distance > 200

    def is_frequency_anomalous(self, curr_trans, prev_trans_buffer):
        sum = 0
        if(len(prev_trans_buffer)<3):
            curr_trans['trans_freq'] = 0
            return False
        diff1 = datetime.datetime.now() - prev_trans_buffer[-1]['datetime']
        diff2 = prev_trans_buffer[-1]['datetime'] - prev_trans_buffer[-2]['datetime'] 
        diff3 = prev_trans_buffer[-2]['datetime'] - prev_trans_buffer[-3]['datetime'] 
        sum += diff1.seconds + diff2.seconds + diff3.seconds
        curr_trans['trans_freq'] = (sum/3)
        return (sum/3)< ACCEPTED_TRANSACTION_FREQUENCY
        
    def process_transaction(self, value) -> str:
        current_state = self.state.value()
        if current_state is None:
            current_state = (
                0,              # transaction counter
                0,              # sum of transactions
                []              # transaction buffer
                )
            
        alert = self.detect_anomaly(value, current_state)
        if alert != 'None':
            return alert
        # do not update state with anomalous transaction
        new_trans_sum = current_state[1]
        # update sum of buff transactions
        if(len(current_state[PREV_TRANS_IDX])==TRANSACTION_QUEUE_SIZE):
            # remove the amount of the transaction at the end of buffer
            new_trans_sum -= current_state[PREV_TRANS_IDX][0]['amount']
        new_trans_sum = value['amount']
            
        self.update_transaction_buffer(value, current_state[PREV_TRANS_IDX])
        # update the counter
        current_state = (
            current_state[COUNTER_IDX] + 1,
            new_trans_sum,
            current_state[PREV_TRANS_IDX]
        )
        self.state.update(current_state)
        value['average-amount'] = current_state[TRANS_SUM_IDX]/len(current_state[PREV_TRANS_IDX])
        return alert

    def flat_map(self, value):
        alert = self.process_transaction(value)
        current_state = self.state.value()
        value['alert'] = alert

        yield value

properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '1',
}


if __name__ == '__main__':
    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    earliest = False
    offset = KafkaOffsetsInitializer.earliest() if earliest else KafkaOffsetsInitializer.latest()

    source = KafkaSource.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('TOPIC-A3') \
        .set_group_id("test_group") \
        .set_starting_offsets(offset) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    record_serializer = KafkaRecordSerializationSchema.builder() \
        .set_topic('TOPIC-A4') \
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
        .flat_map(ProcessTransaction())

    ds.map(lambda x: "\n " + str(x), output_type=Types.STRING()).print()

    ds = ds.map(lambda x: str(x), output_type=Types.STRING())


    ds.sink_to(sink)

    print("start reading data from kafka")

    env.execute("Detect anomalous transaction")
