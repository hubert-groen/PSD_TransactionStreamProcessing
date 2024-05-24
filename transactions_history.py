import sqlite3


class TransactionHistory:
    def __init__(self, db_name='transactions.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        
    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    amount REAL,
                    latitude REAL,
                    longitude REAL
                )
            """)
    
    def add_transaction(self, user_id, amount, latitude, longitude):
        with self.conn:
            self.conn.execute("""
                INSERT INTO transactions (user_id, amount, latitude, longitude)
                VALUES (?, ?, ?, ?)
            """, (user_id, amount, latitude, longitude))
    
    def get_recent_transactions(self, limit=10):
        with self.conn:
            cursor = self.conn.execute("""
                SELECT user_id, amount, latitude, longitude
                FROM transactions
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
