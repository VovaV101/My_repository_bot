from src.field import Field


class Name(Field):
    """
    This class is a derived class from Field and needed for storing name of the client.
    """

    def __init__(self, client_name: str):
        self.value = client_name
        super().__init__(value=self.value)

    @property
    def value(self) -> str:
        """
        Getter for getting Name field value.
        :return: Name value.
        """
        return self.__value

    @value.setter
    def value(self, client_name: str) -> None:
        """
        Setter for setting Name value.
        :param client_name: Client name string.
        :return: None.
        """
        self.__value = client_name
