import pandas as pd
import joblib
import datetime

from transactions_history import TransactionHistory
from sklearn.ensemble import RandomForestClassifier


history = TransactionHistory()

def load_data(history):
    transactions = history.get_recent_transactions()
    df = pd.DataFrame(transactions, columns=['user_id', 'amount', 'latitude', 'longitude', 'anomaly'])
    return df

def train_isolation_forest(data):
    X = data[['amount', 'latitude', 'longitude']].values
    y = data['anomaly'].values
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model


data = load_data(history)

model = train_isolation_forest(data)


current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
model_path = f"{current_time}_my_model.pkl"
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")