from training.transactions_history import TransactionHistory

history = TransactionHistory()

def add_transaction(user_id, amount, latitude, longitude, anomaly):
    history.add_transaction(user_id, amount, latitude, longitude, anomaly)

add_transaction("user1", 50.0, 52.2296756, 21.0122287, 0)
add_transaction("user1", 100.0, 52.2296756, 21.0122287, 0)
add_transaction("user1", 50.0, 52.2296756, 21.0122287, 0)
add_transaction("user1", 100.0, 52.406374, 16.9251681, 0)
add_transaction("user1", 20.0, 50.0646501, 19.9449799, 0)
add_transaction("user1", 150.0, 51.1078852, 17.0385376, 0)
add_transaction("user1", 75.0, 53.1324886, 23.1688403, 0)
add_transaction("user1", 200.0, 50.0411867, 21.9991196, 0)
add_transaction("user1", 30.0, 51.7592485, 19.4559833, 0)
add_transaction("user1", 500.0, 52.2296756, 21.0122287, 0)
add_transaction("user1", 10.0, 52.406374, 16.9251681, 0)
add_transaction("user1", 125.0, 50.0646501, 19.9449799, 0)
add_transaction("user1", 60.0, 51.1078852, 17.0385376, 0)
add_transaction("user1", 300.0, 53.1324886, 23.1688403, 0)
add_transaction("user1", 85.0, 50.0411867, 21.9991196, 0)
add_transaction("user1", 20.0, 51.7592485, 19.4559833, 0)
add_transaction("user1", 450.0, 52.2296756, 21.0122287, 0)
add_transaction("user1", 1.0, 52.2296756, 21.0122287, 1)
add_transaction("user1", 2.0, 52.2296756, 21.0122287, 1)
add_transaction("user1", 1.0, 52.2296756, 21.0122287, 1)