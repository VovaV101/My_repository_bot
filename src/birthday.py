from datetime import datetime

from src.field import Field

DATE_FORMAT = "%d-%m-%Y"


class Birthday(Field):
    """
    This class is a derived class from Field and needed for storing birthday of the
    client.
    """

    def __init__(self, birthday: str = None):
        self.value = birthday
        super().__init__(value=self.value)

    @property
    def value(self) -> datetime.date:
        """
        Getter method to return birthday value.
        :return: Birthday value.
        """
        return self.__value

    @value.setter
    def value(self, birthday: str) -> None:
        """
        Setter for birthday value.
        :param birthday: Birthday value.
        :return: None.
        """
        if birthday is None:
            self.__value = birthday
            return
        try:
            birthday_dt: datetime.date = datetime.strptime(birthday,
                                                           DATE_FORMAT).date()
            self.__value = birthday_dt
        except Exception:
            raise ValueError(f"Client birthday '{birthday}' or date format is "
                             f"incorrect. Expected date format is '{DATE_FORMAT}'."
                             f"Check it, please.")
