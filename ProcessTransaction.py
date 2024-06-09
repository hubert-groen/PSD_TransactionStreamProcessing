from sklearn.svm import OneClassSVM
import datetime
import math
import numpy as np

ACCEPTED_TRANSACTION_FREQUENCY = 10
TRANSACTION_QUEUE_SIZE = 10

COUNTER_IDX = 0
TRANS_SUM_IDX = 1
PREV_TRANS_IDX = 2

class ProcessTransaction(FlatMapFunction):
    
    def __init__(self):
        self.state = None
        self.amount_svm = OneClassSVM(gamma='auto')
        self.geo_svm = OneClassSVM(gamma='auto')
        self.is_svm_trained = False

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
        
    def train_svms(self, state):
        transactions = state[PREV_TRANS_IDX]
        if len(transactions) >= 10:
            amount_data = np.array([trans['amount'] for trans in transactions]).reshape(-1, 1)
            geo_data = np.array([[trans['latitude'], trans['longitude']] for trans in transactions])
            self.amount_svm.fit(amount_data)
            self.geo_svm.fit(geo_data)
            self.is_svm_trained = True
 
    def is_amount_anomalous(self, curr_trans, state):
        if not self.is_svm_trained:
            self.train_svms(state)
        if len(state[PREV_TRANS_IDX]) < 10:
            return False
        amount_data = np.array([[curr_trans['amount']]])
        return self.amount_svm.predict(amount_data) == -1

    def haversine_distance(self, lat1, lon1, lat2, lon2):
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
        if not self.is_svm_trained:
            self.train_svms(state)
        if len(state[PREV_TRANS_IDX]) < 10:
            return False
        geo_data = np.array([[curr_trans['latitude'], curr_trans['longitude']]])
        return self.geo_svm.predict(geo_data) == -1

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
