# Merchant_flask provides a secure way to display transaction data from
# the transaction database for merchants on a web page.
#
#
# @author (Maddie Hirschfeld)
# @version (June 6, 2024)


from flask import Flask, render_template
import sqlite3
import logging
from blockchain.cryptograph import Cryptograph

app = Flask(__name__)

# Encryption key used for decryption
key = 'kTZ_RzqoJrKxHx2qcoQcdU-gKFR5yT2BxKg1Lkunqu4='
cryptograph = Cryptograph(key=key)

# Configures logging for the app.log
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def get_all_transactions():
    # Connects to the SQLite database (transactions.db)
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    # Executes query to retrieve transaction details that
    # are ordered by the timestamp
    cursor.execute('SELECT name, cc_number, transaction_hash FROM transactions ORDER BY timestamp DESC')
    transactions = cursor.fetchall()
    conn.close()

    # Logging for debugging
    logging.debug(f"Retrieved transactions from DB: {transactions}")

    # List that stores updated transactions
    updated_transactions = []

    for transaction in transactions:
        # Name from transaction
        name = transaction[0]
        # Encrypted Credit Card Number from the transaction
        encrypted_cc_number = transaction[1]
        # Transaction hash from the transaction
        transaction_hash = transaction[2]

        #Logs transaction
        logging.debug(f"Processing transaction for {name}, Encrypted CC: {encrypted_cc_number}")

        try:
            # Decrypts the encrypted credit card number
            decrypted_cc = cryptograph.decrypt_data(encrypted_cc_number)
            # Logs the decrypted number
            logging.debug(f"Decrypted CC Number for {name}: {decrypted_cc}")

            # Masks credit card to only show the last four digits
            if len(decrypted_cc) >= 4:
                masked_cc = '**** **** **** ' + decrypted_cc[-4:]
            else:
                masked_cc = 'Invalid CC Number'

            # Appends the transactiond details to the list
            updated_transactions.append((name, masked_cc, transaction_hash))
        except ValueError as e:
            logging.error(f"Decryption error for {name}: {e}")
            updated_transactions.append((name, '**** **** **** ****', transaction_hash))
        except Exception as e:
            logging.error(f"Unexpected error for {name}: {e}")
            updated_transactions.append((name, '**** **** **** ****', transaction_hash))

    logging.debug(f"Updated transactions: {updated_transactions}")
    # Returns the list of transactions
    return updated_transactions

@app.route('/transactions')
def transactions():
    # Gets all the transactions from the database
    all_transactions = get_all_transactions()
    # Renders the transactions template with all the data for the merchant
    return render_template('transactions.html', transactions=all_transactions)

if __name__ == '__main__':
    # Imports and initializes the database
    from initialize_database import initialize_database
    initialize_database()
     # Runs the app in debug mode and ensures that it is on port 5001
    app.run(debug=True, port=5001)