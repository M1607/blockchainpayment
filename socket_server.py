# The Socket_server script listens for transaction data, processes it
# and adds the transaction data to the blockchain. Additionally, the
# transactiond details are stored in the SQLite database.
#
#
# @author (Maddie Hirschfeld)
# @version (June 6, 2024)

import socket
import sqlite3
from blockchain.chain import Chain
from blockchain.block import Block
from blockchain.cryptograph import Cryptograph
import logging

# Encytpion key
key = 'kTZ_RzqoJrKxHx2qcoQcdU-gKFR5yT2BxKg1Lkunqu4='
cryptograph = Cryptograph(key=key)

# Configures logging for app.log
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Stores transaction in the SQLite database.
def store_transaction(transaction, transaction_hash):
    try:
        # Connects to SQL database
        with sqlite3.connect('transactions.db') as conn:
            cursor = conn.cursor()
            # Encypts sensitive transaction data
            encrypted_cc_number = cryptograph.encrypt_data(transaction['cc_number'])
            encrypted_expiration = cryptograph.encrypt_data(transaction['expiration'])
            encrypted_cvv = cryptograph.encrypt_data(transaction['cvv'])
            # Transaction data added to database
            cursor.execute('''
                INSERT INTO transactions (
                    name, email, street, street2, city, state, zipcode,
                    cc_number, expiration, cvv, transaction_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction['name'], transaction['email'], transaction['street'], transaction['street2'],
                transaction['city'], transaction['state'], transaction['zipcode'],
                encrypted_cc_number, encrypted_expiration, encrypted_cvv, transaction_hash
            ))
            # Logs for debugging
            logging.debug(f"Encrypted CC Number stored in DB: {encrypted_cc_number}")
            # Commits the transaction
            conn.commit()
            # Logs for debugging
            logging.debug("Transaction successfully saved to database.")
    except sqlite3.Error as e:
        logging.error(f"Error saving transaction to database: {e}")

# Sets up the server to listen for transaction data process it, and
# store on the blockchain and database.
def server_program():
    # Gets the hostname
    host = socket.gethostname()
    # Intiates port 5000
    port = 5001

    # Initializes the server socket
    server_socket = socket.socket()
    # Binds host address and port together
    server_socket.bind((host, port))

    # Configures how many client the server can listen simultaneously
    server_socket.listen(2)
    print(f"Server is listening on {host}:{port}")
    # Accepts a new connection
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    
    # Initializes the blockcahin with difficulty of 20
    blockchain = Chain(20)
    
    while True:
        # Receives data stream. 
        # It won't accept a data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # Exits the loop if data is not received.
            break
        print("Received transaction data: " + str(data))
        
        # Parses the received transaction data
        transaction = dict(zip(
            ["name", "email", "street", "street2", "city", "state", "zipcode", "cc_number", "expiration", "cvv"],
            data.split(", ")
        ))
        # Logs for debugging
        logging.debug(f"Parsed transaction data: {transaction}")

        # Add transaction to the pool and mines it
        blockchain.add_to_pool(data)
        blockchain.mine()
        
        # Stores the transaction in the database
        store_transaction(transaction, blockchain.blocks[-1].hash.hexdigest())
        
        response = "Transaction logged on blockchain and stored in the database."
        # Sends response to the client
        conn.send(response.encode())
    
    # Closes the connection    
    conn.close()

# Runs the server program
if __name__ == '__main__':
    server_program()