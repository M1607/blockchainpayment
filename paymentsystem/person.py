# The Person Class stores personal information about the user.
#
#
# @author (Maddie Hirschfeld)
# @version (May 24, 2024)

from paymentsystem.address import Address
from paymentsystem.cc import CC

class Person:
    def __init__(self, name, email, address, cc):
        self.name = name
        self.email = email
        self.address = address
        self.cc = cc