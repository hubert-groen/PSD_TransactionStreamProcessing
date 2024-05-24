from transactions_history import TransactionHistory
from anomaly_detection import is_anomalous_transaction

history = TransactionHistory()

def process_transaction(user_id, amount, latitude, longitude):
    if is_anomalous_transaction(user_id, amount, latitude, longitude, history):
        print("Anomalous transaction detected!")
    else:
        print("Transaction is normal.")
        history.add_transaction(user_id, amount, latitude, longitude)

# Dodawanie i analiza transakcji
process_transaction("user1", 50.0, 52.2296756, 21.0122287)
process_transaction("user1", 100.0, 52.2296756, 21.0122287)
process_transaction("user1", 50.0, 52.2296756, 21.0122287)
process_transaction("user1", 100.0, 52.406374, 16.9251681)
process_transaction("user1", 20.0, 50.0646501, 19.9449799)
process_transaction("user1", 150.0, 51.1078852, 17.0385376)
process_transaction("user1", 75.0, 53.1324886, 23.1688403)
process_transaction("user1", 200.0, 50.0411867, 21.9991196)
process_transaction("user1", 30.0, 51.7592485, 19.4559833)
process_transaction("user1", 500.0, 52.2296756, 21.0122287)
process_transaction("user1", 10.0, 52.406374, 16.9251681)
process_transaction("user1", 125.0, 50.0646501, 19.9449799)
process_transaction("user1", 60.0, 51.1078852, 17.0385376)
process_transaction("user1", 300.0, 53.1324886, 23.1688403)
process_transaction("user1", 85.0, 50.0411867, 21.9991196)
process_transaction("user1", 20.0, 51.7592485, 19.4559833)
process_transaction("user1", 450.0, 52.2296756, 21.0122287)
# Dodaj więcej transakcji do testów
