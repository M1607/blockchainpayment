# The Chain class represents the blockchain and manages the list
# of blocks. Additionally, it also mines and validates new blocks
#
#
# @author (Maddie Hirschfeld)
# @version (May 19, 2024)

import hashlib
from blockchain.block import Block

class Chain():
    # Initializes blockchain with a specified difficulty requirement
    def __init__(self, difficulty):
        #  The difficulty level of mining new blocks
        self.difficulty = difficulty
        # The list to store blocks on the chain
        self.blocks = []
        # Blocks are created out of the data from 
        # the pool. The pool is the lobby area of data to be mined.
        self.pool = []
        self.create_origin_block()
    
    # Validates the block by checking ithe block meets the
    # difficulty requirment correctly. It also ensures that the
    # previous block matches.
    def proof_of_work(self, block):
        hash = hashlib.sha256()
        hash.update(str(block).encode('utf-8'))
        return (block.hash.hexdigest() == hash.hexdigest() and 
                int(hash.hexdigest(), 16) < 2**(256 - self.difficulty) and 
                block.previous_hash == self.blocks[-1].hash)
    
    # Adds the block to the chain if it fulfills the requirements.
    def add_to_chain(self, block):
        if self.proof_of_work(block):
            self.blocks.append(block)
            
    # Adds transaction data to the pool of transactions that 
    # are qaiting to be mined.
    def add_to_pool (self, transaction):
        self.pool.append(transaction)
        
    # Creates the "Origin" block with predefined data, and
    # adds the origin block to the chain.
    def create_origin_block(self):
        h = hashlib.sha256()
        h.update(''.encode('utf-8'))
        origin = Block("Origin", h)
        origin.mine(self.difficulty)
        self.blocks.append(origin)
    
    # Mines blocks if they exist in the transaction pool. The oldest
    # transaction in the pool is mined and the new details of the block are
    # that is mined are printed
    def mine(self):
        if len(self.pool) > 0:
            # Removes the block from the pool
            data = self.pool.pop()
            # Creates a new block object
            block = Block(data, self.blocks[-1].hash)
            # The block is mined.
            block.mine(self.difficulty)
            # The mined block is added to the chain.
            self.add_to_chain(block)
            print("\n\n==============")
            print("Hash: ", block.hash.hexdigest())
            print ("Previous Hash:\t\t", block.previous_hash.hexdigest())
            print("Nonce:\t\t", block.nonce)
            print("Data:\t\t", block.transaction)
            print("\n\n================")