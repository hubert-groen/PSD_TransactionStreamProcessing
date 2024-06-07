from transations_data_generator import generate_transaction
import joblib
import os
import numpy as np

MODEL = joblib.load(os.path.abspath(os.path.dirname(__file__))+'/training/20240607_002028_my_model.pkl')

def is_anomalous_transaction(user_id, amount, latitude, longitude, model=MODEL):
    # Nowa transakcja
    new_transaction = np.array([[amount, latitude, longitude]])
    
    # Wykrywanie anomalii
    is_anomaly = model.predict(new_transaction)[0] == 1
    
    #return is_anomaly
    if is_anomaly:
        return 1
    return 0


tab = []
pred = []

for _ in range(10):
    transaction = generate_transaction()
    result = is_anomalous_transaction(transaction["user_id"], transaction["amount"], transaction["latitude"], transaction["longitude"])

    print(f"transaction: {transaction}\npredicion: {result}")
    print("---\n")

    tab.append(transaction)
    pred.append(result)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))

for i, transaction in enumerate(tab):
    color = 'green' if pred[i] == 0 else 'red'
    plt.scatter(transaction['longitude'], transaction['latitude'], c=color, label=f"Prediction: {pred[i]}")

# Add labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Transaction Locations and Anomaly Predictions')
plt.legend(["Non-anomalous (0)", "Anomalous (1)"], loc='upper right')

# Show the plot
plt.show()