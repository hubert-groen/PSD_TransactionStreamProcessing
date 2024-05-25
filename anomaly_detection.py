import numpy as np

# FIXME: wszystko jest dla jednego usera tylko
def is_anomalous_transaction(user_id, amount, latitude, longitude, model):
    # Nowa transakcja
    new_transaction = np.array([[amount, latitude, longitude]])
    
    # Wykrywanie anomalii
    is_anomaly = model.predict(new_transaction)[0] == 1
    
    return is_anomaly

