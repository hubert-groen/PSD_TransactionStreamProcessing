import matplotlib.pyplot as plt

# Data
data = [
    {'user_id': 'user1', 'amount': 285, 'latitude': 52.032262, 'longitude': 19.302731, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 282, 'latitude': 50.168333, 'longitude': 21.281105, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 302, 'latitude': 52.250931, 'longitude': 18.730569, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 0, 'latitude': 1.315932, 'longitude': 2.938237, 'anomaly': 1},
    {'user_id': 'user1', 'amount': 0, 'latitude': 1.903203, 'longitude': 2.090614, 'anomaly': 1},
    {'user_id': 'user1', 'amount': 337, 'latitude': 51.650756, 'longitude': 21.635358, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 449, 'latitude': 52.300402, 'longitude': 19.905958, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 161, 'latitude': 52.827596, 'longitude': 17.795394, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 237, 'latitude': 50.022722, 'longitude': 21.227491, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 0, 'latitude': 1.432825, 'longitude': 2.43188, 'anomaly': 1},
]

# Extracting coordinates and anomaly status
latitudes = [entry['latitude'] for entry in data]
longitudes = [entry['longitude'] for entry in data]
anomalies = [entry['anomaly'] for entry in data]

# Plotting
plt.figure(figsize=(10, 6))
for lat, lon, anomaly in zip(latitudes, longitudes, anomalies):
    color = 'green' if anomaly == 0 else 'red'
    plt.scatter(lon, lat, color=color)

# Adding titles and labels
plt.title('Geographical Data Points')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Adding a legend
plt.scatter([], [], color='green', label='Non-anomalous')
plt.scatter([], [], color='red', label='Anomalous')
plt.legend()

# Displaying the plot
plt.show()
