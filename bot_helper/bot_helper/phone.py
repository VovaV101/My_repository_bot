from __future__ import annotations

from re import Match
import re

from .field import Field


class Phone(Field):
    """
    This class is a derived class from Field and needed for storing phone of the client.
    """

    def __init__(self, phone: str):
        self.value = phone
        super().__init__(value=self.value)

    @property
    def value(self) -> str:
        """
        Getter method for getting phone number value.
        :return: Phone value.
        """
        return self.__value

    @value.setter
    def value(self, phone: str):
        match: Match[bytes] | None = re.search('\d+', phone)
        numbers = match.group() if match else ""
        phone_number_len: int = len(phone)
        if phone_number_len != 10 or len(numbers) != phone_number_len:
            raise ValueError(f"Phone number must have only digits with length "
                             f"10, but number: '{phone}' was given with the "
                             f"length {phone_number_len}")
        self.__value = phone
