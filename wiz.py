import json
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx

# Dane wejściowe (przykładowe dane, które podałeś)
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
    {'user_id': 'user1', 'amount': 124, 'latitude': 52.862876, 'longitude': 17.228286, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 254, 'latitude': 52.657274, 'longitude': 19.581793, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 110, 'latitude': 51.488318, 'longitude': 20.790737, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 282, 'latitude': 51.793093, 'longitude': 17.945863, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 404, 'latitude': 52.928642, 'longitude': 21.721614, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 299, 'latitude': 51.584476, 'longitude': 21.251348, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 1, 'latitude': 1.659914, 'longitude': 2.57017, 'anomaly': 1},
    {'user_id': 'user1', 'amount': 136, 'latitude': 50.096094, 'longitude': 20.351613, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 395, 'latitude': 50.408041, 'longitude': 18.976698, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 54, 'latitude': 51.011778, 'longitude': 21.08628, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 259, 'latitude': 52.642649, 'longitude': 17.92613, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 145, 'latitude': 51.301024, 'longitude': 20.744694, 'anomaly': 0},
    {'user_id': 'user1', 'amount': 0, 'latitude': 1.087428, 'longitude': 2.228882, 'anomaly': 1}
]

# Przetwarzanie danych
points = [Point(d['longitude'], d['latitude']) for d in data]
gdf = gpd.GeoDataFrame(data, geometry=points)

# Ustawienie układu współrzędnych na WGS 84
gdf.set_crs(epsg=4326, inplace=True)

anomalies = gdf[gdf['anomaly'] == 1]
non_anomalies = gdf[gdf['anomaly'] == 0]

# Tworzenie wykresu mapy
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# Wykres punktów na mapie
non_anomalies.plot(ax=ax[0], color='green', markersize=10, label='Non-anomalies')
anomalies.plot(ax=ax[0], color='red', markersize=10, label='Anomalies')
ctx.add_basemap(ax[0], crs=gdf.crs, source=ctx.providers.Stamen.TonerLite)
ax[0].legend()
ax[0].set_title('Transactions Map')

# Wykres amount
ax[1].bar(range(len(data)), [d['amount'] for d in data], color=['red' if d['anomaly'] else 'green' for d in data])
ax[1].set_title('Transaction Amounts')
ax[1].set_xlabel('Transaction Index')
ax[1].set_ylabel('Amount')

# Procent anomalii
anomaly_percentage = (len(anomalies) / len(data)) * 100
anomaly_count = len(anomalies)
total_count = len(data)
print(f'Liczba anomalii: {anomaly_count} / {total_count}')
print(f'Procent anomalii: {anomaly_percentage:.2f}%')

# Wyświetlanie wykresów
plt.tight_layout()
plt.show()
