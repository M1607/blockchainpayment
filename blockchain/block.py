# The Block class represents a block in a blockchain. A block 
# is where transcation data is permanently stored.
#
#
# @author (Maddie Hirschfeld)
# @version (May 19, 2024)

import hashlib

class Block():
    # Initializes the block with transaction data and the hash
    # of the previous block. Additionally it sets the inital none
    # to zero.
    def __init__(self, transaction, previous_hash):
        self.hash = None
        self.previous_hash = previous_hash
        #Number incremented in order to generate hash based on needs.
        self.nonce = 0
        self.transaction = transaction
    
    # Function that mines the block by finding a has that meets the 
    # difficult requirement
    def mine(self, difficulty):
        while True:
            self.hash = hashlib.sha256()
            self.hash.update(str(self).encode('utf-8'))
            hash_int = int(self.hash.hexdigest(), 16)
            if hash_int < 2**(256 - difficulty):
                break
            self.nonce += 1
        
        
    # String method that represents the block, including the previous
    # one is returned.
    def __str__(self):
        return "{}{}{}".format(self.previous_hash.hexdigest(), self.transaction, self.nonce)