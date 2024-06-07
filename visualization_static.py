# from transations_data_generator import generate_transaction
# import joblib
# import os
# import numpy as np

# MODEL = joblib.load(os.path.abspath(os.path.dirname(__file__))+'/training/20240607_002028_my_model.pkl')

# def is_anomalous_transaction(user_id, amount, latitude, longitude, model=MODEL):
#     # Nowa transakcja
#     new_transaction = np.array([[amount, latitude, longitude]])
    
#     # Wykrywanie anomalii
#     is_anomaly = model.predict(new_transaction)[0] == 1
    
#     #return is_anomaly
#     if is_anomaly:
#         return 1
#     return 0


# tab = []
# pred = []

# for _ in range(10):
#     transaction = generate_transaction()
#     result = is_anomalous_transaction(transaction["user_id"], transaction["amount"], transaction["latitude"], transaction["longitude"])

#     print(f"transaction: {transaction}\npredicion: {result}")
#     print("---\n")

#     tab.append(transaction)
#     pred.append(result)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 6))

# for i, transaction in enumerate(tab):
#     color = 'green' if pred[i] == 0 else 'red'
#     plt.scatter(transaction['longitude'], transaction['latitude'], c=color, label=f"Prediction: {pred[i]}")

# # Add labels and title
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Transaction Locations and Anomaly Predictions')
# plt.legend(["Non-anomalous (0)", "Anomalous (1)"], loc='upper right')

# # Show the plot
# plt.show()


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

for _ in range(20):
    transaction = generate_transaction()
    result = is_anomalous_transaction(transaction["user_id"], transaction["amount"], transaction["latitude"], transaction["longitude"])

    print(f"transaction: {transaction}\npredicion: {result}")
    print("---\n")

    tab.append(transaction)
    pred.append(result)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 6))

# for i, transaction in enumerate(tab):
#     color = 'green' if pred[i] == 0 else 'red'
#     plt.scatter(transaction['longitude'], transaction['latitude'], c=color, label=f"Prediction: {pred[i]}")

# # Add labels and title
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Transaction Locations and Anomaly Predictions')
# plt.legend(["Non-anomalous (0)", "Anomalous (1)"], loc='upper right')

# # Show the plot
# plt.show()



import plotly.express as px
import pandas as pd

# Convert the transaction data to a DataFrame
df = pd.DataFrame(tab)

# Add the predictions to the DataFrame
df['Prediction'] = pred

# Map the predictions to colors
df['Color'] = df['Prediction'].map({0: '#ff0808', 1: '#2596b3'})

# Create a scatter geo plot with Plotly
fig = px.scatter_geo(
    df,
    lat='latitude',
    lon='longitude',
    color='Color',
    hover_name='user_id',
    hover_data={'amount': True, 'Prediction': True},
    title='Transaction Locations and Anomaly Predictions'
)

# Update the layout
fig.update_layout(
    geo=dict(
        projection_type='natural earth'
    ),
    legend_title='Anomaly Prediction'
)

# Show the plot
fig.show()






# import plotly.express as px
# import pandas as pd

# # Convert the transaction data to a DataFrame
# df = pd.DataFrame(tab)

# # Add the predictions to the DataFrame
# df['Prediction'] = pred

# # Map the predictions to colors
# df['Color'] = df['Prediction'].map({0: 'green', 1: 'red'})

# # Create a scatter plot with Plotly
# fig = px.scatter(
#     df,
#     x='longitude',
#     y='latitude',
#     color='Color',
#     hover_data=['amount', 'user_id', 'Prediction'],
#     title='Transaction Locations and Anomaly Predictions'
# )

# # Update the layout
# fig.update_layout(
#     xaxis_title='Longitude',
#     yaxis_title='Latitude',
#     legend_title='Anomaly Prediction'
# )

# # Show the plot
# fig.show()