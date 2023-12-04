import re
from .field import Field

class Email(Field):
    """
    This class is a derived class from Field and needed for storing email of the client.
    """

    def __init__(self, email: str):
        self.value = email
        super().__init__(value=self.value)

    @property
    def value(self) -> str:
        """
        Getter method for getting email address value.
        :return: Email address value.
        """
        return self.__value

    @value.setter
    def value(self, email: str):
        match = re.search(r"[A-Za-z]+[\w\.]+@\w+\.[a-zA-Z]{1,}[^\.-]", email)
        email_address = match.group() if match else "" 
        if len(email) != len(email_address):
            raise ValueError("The address must contain exactly one @ symbol."\
                            "The address must include the characters A-Za-z0-9 before and after the @ symbol."\
                            "The local name can contain the characters a-zA-z0-9 and the characters: ! #$%&'r; + - . = ? ^^ _ ` { } ½ ~."\
                            "The following characters cannot be used: < > ( ) [ ] @ , ; : \ /  * or space."\
                            "The domain name must contain two text lines separated by a dot."\
                            "The last character cannot be a minus sign, a hyphen, or a dot.")
        self.__value = email
