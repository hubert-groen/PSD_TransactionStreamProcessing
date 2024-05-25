import numpy as np
import joblib

from anomaly_detection import is_anomalous_transaction


new_transaction = ("user1", 1.0, 52.2296756, 21.0122287)   # TODO: to będzie pobrane z kafki TOPIC-A, zamiast wygenerowane tutaj


model = joblib.load('20240525_132030_my_model.pkl')

if is_anomalous_transaction(*new_transaction, model):
    print("Anomalous transaction detected!")
else:
    print("Transaction is normal.")


# TODO: nadanie na kafkę TOPIC-B