# The Generate_Key class generates a new encryption key
# utilizing the cyptography.fernet module.
#
#
# @author (Maddie Hirschfeld)
# @version (June 6, 2024)

from cryptography.fernet import Fernet

# Generate a new Fernet key
key = Fernet.generate_key()
# Decodes the generated key to a string
print(key.decode())