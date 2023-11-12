from src.field import Field

class Email(Field):

    def __init__(self, email: str):
        self.value = email
        super().__init__(value=self.value)

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, email: str):
    
        self.__value = email
