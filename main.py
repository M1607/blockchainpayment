# The Main class is used for testing purpose and validation
# of various classes in the blockchain and payment processing system.
#
#
# @author (Maddie Hirschfeld)
# @version (May 24, 2024)

from blockchain.chain import Chain
from paymentsystem.address import Address
from paymentsystem.cc import CC
from paymentsystem.person import Person

if __name__ == "__main__":
    # Initializes the blockchain with the difficulty level of 20
    chain = Chain(20)

    # Creation of an Address, CC (Credit Card), and Person instance
    address = Address("747 Oak St.", "Unit 5", "Telluride", "CO", "81435")
    cc = CC("1234567812345678", "12/18", "123")
    person = Person("Maddie Hirsch", "mhirsch@gmail.com", address, cc)
    
    # Creates a transaction string from the person instance
    transaction = f"{person.name}, {person.email}, {person.address.street}, {person.address.street2} {person.address.city}, {person.address.state}, {person.address.zipcode}, {person.cc.cc_number}, {person.cc.expiration}, {person.cc.cvv}"
    
    # Adds the transaction to the blockchain's pool to be mined.
    chain.add_to_pool(transaction)
    chain.mine()