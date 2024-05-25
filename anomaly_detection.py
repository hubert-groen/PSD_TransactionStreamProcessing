import numpy as np
import joblib


def is_anomalous_transaction(user_id, amount, latitude, longitude, model):
    # Nowa transakcja
    new_transaction = np.array([[amount, latitude, longitude]])
    
    # Wykrywanie anomalii
    is_anomaly = model.predict(new_transaction)[0] == 1
    
    return is_anomaly


model = joblib.load('20240525_132030_my_model.pkl')


new_transaction = ("user1", 1.0, 52.2296756, 21.0122287)   # to będzie pobrane z kafki zamiast wygenerowane tutaj
if is_anomalous_transaction(*new_transaction, model):
    print("Anomalous transaction detected!")
else:
    print("Transaction is normal.")


