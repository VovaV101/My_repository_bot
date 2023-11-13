import json

from src.field import Field

class Address(Field):

    """
    This class is a derived class from Field and needed for storing address of the client.
    """

    def __init__(self, address: list):
        self.value = address
        self.country, self.city, self.street, self.house, self.apartment = address
        super().__init__(value=self.value)

    @property
    def value(self) -> list:
        """
        Getter method for getting address.
        :return: Address.
        """
        return self.__value

    @value.setter
    def value(self, address: list) -> None:
        self.__value = address
        if len(address) < 5:
            self.__value = self.__value.extend([None] * (5 - len(address)))

    def __str__(self) -> str:
        return (f'country: {self.country}, city: {self.city}, street: {self.street}, '
                f'house: {self.house}, apartment: {self.apartment}')

    def get_addr_dict(self) -> dict:
        """
        Method returns the address in as the dictionary.
        :return: Address as a dictionary.
        """
        return {
                "country": self.country,
                "city": self.city,
                "street": self.street,
                "house": self.house,
                "apartment": self.apartment
        }
