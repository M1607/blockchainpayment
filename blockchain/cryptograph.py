# The Cryptograph class provides methods for encyrpting and decrypting data.
#
#
# @author (Maddie Hirschfeld)
# @version (June 6, 2024)


from cryptography.fernet import Fernet, InvalidToken
import logging

class Cryptograph:
    def __init__(self, key):
        # Converts the key into bytes if it is a string
        self.key = key.encode() if isinstance(key, str) else key
        #C reates Fernet cipher suite using the key provided
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data):
        # Data is converted into bytes if it is a string
        if isinstance(data, str):
            data = data.encode()
        # Data is encypted and decoded to a string
        encrypted_data = self.cipher_suite.encrypt(data).decode()
        # Logs encypted data for debugging
        logging.debug(f"Encrypted data: {encrypted_data}")
        # Returns encyrpted data
        return encrypted_data

    def decrypt_data(self, data):
        try:
            # Converts data to bytes if it is a string
            if isinstance(data, str):
                data = data.encode()
            # Decrypts the data and decodes it into a string
            decrypted_data = self.cipher_suite.decrypt(data).decode()
            # Logs decrypted data for debugging
            logging.debug(f"Decrypted data: {decrypted_data}")
            # Returns decrypted data
            return decrypted_data
        except InvalidToken as e:
            # Logs error message if decryption fails
            logging.error(f"Decryption error: {e}")
            # Value error with a message
            raise ValueError("Invalid Token or incorrect key.") from e

    def get_key(self):
        # Returns key as a decoded string
        return self.key.decode()
