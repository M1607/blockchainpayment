# The Test_Crypt helps test the encyption and decryption of credit
# cards utilizing the Cryptograph class.
#
#
# @author (Maddie Hirschfeld)
# @version (June 7, 2024)

import sqlite3
import logging
from blockchain.cryptograph import Cryptograph

# Configures logging
logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Initialize Cryptograph with the same key used in the application
key = '4a5QWiMoGiinE43Q4PLYPR9e-0nyLhNcFkU4bTgM060='
cryptograph = Cryptograph(key=key)

#Tests the encyrption and decryption of credit card number
def test_encryption_decryption():
    original_cc = "5678987612345432"
    encrypted_cc = cryptograph.encrypt_data(original_cc)
    decrypted_cc = cryptograph.decrypt_data(encrypted_cc)
    assert original_cc == decrypted_cc, f"Decryption failed: {decrypted_cc} != {original_cc}"
    logging.debug(f"Original: {original_cc}, Encrypted: {encrypted_cc}, Decrypted: {decrypted_cc}")
    print(f"Original: {original_cc}, Encrypted: {encrypted_cc}, Decrypted: {decrypted_cc}")

#Test the storage of encrypted credit card numbers
def test_database_storage():
    original_cc = "5678987612345432"
    encrypted_cc = cryptograph.encrypt_data(original_cc)
    logging.debug(f"Original: {original_cc}, Encrypted: {encrypted_cc}")

    # Simulates database storage
    conn = sqlite3.connect('test_transactions.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS transactions (cc_number TEXT)')
    cursor.execute('INSERT INTO transactions (cc_number) VALUES (?)', (encrypted_cc,))
    conn.commit()

    # Retrieves from database
    cursor.execute('SELECT cc_number FROM transactions')
    retrieved_encrypted_cc = cursor.fetchone()[0]
    logging.debug(f"Retrieved Encrypted: {retrieved_encrypted_cc}")
    decrypted_cc = cryptograph.decrypt_data(retrieved_encrypted_cc)
    conn.close()

    assert original_cc == decrypted_cc, f"Decryption failed: {decrypted_cc} != {original_cc}"
    logging.debug(f"Original: {original_cc}, Encrypted: {encrypted_cc}, Retrieved Encrypted: {retrieved_encrypted_cc}, Decrypted: {decrypted_cc}")
    print(f"Original: {original_cc}, Encrypted: {encrypted_cc}, Retrieved Encrypted: {retrieved_encrypted_cc}, Decrypted: {decrypted_cc}")

# Checks to make sure the encyption key remains consistent
def check_key_consistency():
    logging.debug(f"Key: {cryptograph.get_key()}")
    print(f"Key: {cryptograph.get_key()}")

# Executes the test
if __name__ == '__main__':
    test_encryption_decryption()
    test_database_storage()
    check_key_consistency()