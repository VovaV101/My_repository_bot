from src.field import Field

class Address(Field):

    def __init__(self, address: list):

        self.value = address
        self.country = address[0] if address[0] else None
        self.city = address[1] if address[1] else None
        self.street = address[2] if address[2] else None
        self.house = address[3] if address[3] else None
        self.apartment = address[4] if address[4] else None


        super().__init__(value=self.value)

    @property
    def value(self) -> str:

        return self.__value

    @value.setter
    def value(self, address: str) -> None:
    
        self.__value = address

    
    def __str__(self):

        return f'Country: {self.country}, City: {self.city}, Street: {self.street}, House: {self.house}, Apartment: {self.apartment}'

        