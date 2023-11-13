from typing import Any


class Field:
    """
    Base class that describes the logic for all types of fields.
    """

    def __init__(self, value: Any):
        self.__value = value

    def __str__(self):
        return str(self.__value)
