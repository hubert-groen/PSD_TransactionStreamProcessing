from transations_data_generator_2 import generate_transaction
import joblib
import os
import numpy as np
import plotly.express as px
import pandas as pd


MODEL = joblib.load(os.path.abspath(os.path.dirname(__file__))+'/training/20240607_125558_my_model.pkl')

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

for _ in range(40):
    transaction = generate_transaction()
    result = is_anomalous_transaction(transaction["user_id"], transaction["amount"], transaction["latitude"], transaction["longitude"])

    print(f"transaction: {transaction}\npredicion: {result}")
    print("---\n")

    tab.append(transaction)
    pred.append(result)


df = pd.DataFrame(tab)
df['Prediction'] = pred
df['Color'] = df['Prediction'].map({0: '#ff0808', 1: '#2596b3'})

fig = px.scatter_geo(
    df,
    lat='latitude',
    lon='longitude',
    color='Color',
    hover_name='user_id',
    hover_data={'amount': True, 'Prediction': True},
    title='Transaction Locations and Anomaly Predictions'
)

fig.update_layout(
    geo=dict(
        projection_type='natural earth'
    ),
    legend_title='Anomaly Prediction'
)

fig.show()
