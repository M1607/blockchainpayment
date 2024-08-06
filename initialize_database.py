# Initialize_database is a script that initializes the SQLite database
# that is used for storing transcation data.
#
#
# @author (Maddie Hirschfeld)
# @version (May 25, 2024)

import sqlite3

# Connects to the database (transaction.db) and creates a cursor
def initialize_database():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    # Creation of transaction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            street TEXT NOT NULL,
            street2 TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zipcode TEXT NOT NULL,
            cc_number TEXT NOT NULL,
            expiration TEXT NOT NULL,
            cvv TEXT NOT NULL,
            transaction_hash TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Saves the changes and closes the connection.
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    initialize_database()