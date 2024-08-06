# The Address class stores the address details of the user.
# 
#
#
# @author (Maddie Hirschfeld)
# @version (May 24, 2024)

class Address:
    def __init__(self, street, street2, city, state, zipcode):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zipcode =zipcode