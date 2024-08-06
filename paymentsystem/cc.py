# The Credit Card class stores credit card details that the user provides.
#
#
# @author (Maddie Hirschfeld)
# @version (May 24, 2024)

from blockchain.cryptograph import Cryptograph

class CC:
    def __init__ (self, cc_number, expiration, cvv, cryptograph):
        self.cryptograph = cryptograph
        self.cc_number = cc_number
        self.expiration = expiration
        self.cvv = cvv
    
    def get_decrypted_data(self):
        return {
            "cc_number": self.cryptograph.decrypt_data(self.cc_number),
            "expiration": self.cryptograph.decrypt_data(self.expiration),
            "cvv": self.cryptograph.decrypt_data(self.cvv)
        }