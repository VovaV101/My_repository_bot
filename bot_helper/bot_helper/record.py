from __future__ import annotations

import json
from datetime import datetime
from typing import Tuple, Any

from bot_helper.birthday import Birthday, DATE_FORMAT
from bot_helper.name import Name
from bot_helper.phone import Phone
from bot_helper.address import Address
from bot_helper.email_address import Email


class RecordAlreadyExistsException(Exception):
    """
    A record which was operating already exists.
    """
    pass


class RecordWasNotFoundException(Exception):
    """
    Record was not found during operation.
    """
    pass


class Record:
    """
    This class describes the logic of storing data about the client and all his/her
    phones.
    """

    def __init__(self, name: str, birthday: str = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.address = Address([])
        self.emails = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones:" \
               f" {'; '.join(p.value for p in self.phones)}, address:" \
               f" {self.address}, emails:" \
               f" {'; '.join(em.value for em in self.emails)}"

    def __repr__(self) -> str:
        birthday: datetime = self.birthday.value
        birthday_str = None
        if birthday:
            birthday_str = birthday.strftime(DATE_FORMAT)

        address: dict = self.address.get_addr_dict()

        return json.dumps(
            {
                self.name.value:
                    {
                        "phones": [phone_num.value for phone_num in self.phones],
                        "birthday": birthday_str,
                        "address": address,
                        "emails": [email.value for email in self.emails]
                    }
            }
        )

    def days_to_birthday(self) -> int:
        """
        Method calculates the number of days to the next client's birthday. The method
        returns the number of days without fractional part.
        :return: Number of days.
        """
        if self.birthday.value:
            today = datetime.today()
            today_day, today_month, today_year = today.day, today.month, today.year
            birth_day, birth_month = self.birthday.value.day, self.birthday.value.month
            next_birthday_year = today_year

            if today_month > birth_month or (today_month == birth_month and today_day
                                             > birth_day):
                next_birthday_year = today_year + 1
            time_diff = datetime(next_birthday_year, birth_month, birth_day) - today
            days_to_next_birthday = time_diff.days
            return days_to_next_birthday
        else:
            raise ValueError("There is no information about the client birthday. Add "
                             "it first and call this method again.")

    def get_phone_by_number(self, phone_num: str) -> Tuple[Any, int] | Tuple[None, None]:
        """
        Method iterates through the list of phone objects and returns the object that
        has 'phone_num' as a phone value.
        :param phone_num: Phone number string.
        :return: Phone object and it's index in the list.
        """
        for idx, phone in enumerate(self.phones):
            if phone.value == phone_num:
                return phone, idx
        return None, None
 
    def get_email_by_number(self, email_num: str) -> Tuple[Any, int] | Tuple[None, None]:
        """
        Method iterates through the list of email objects and returns the object that
        has 'email_num' as an email value.
        :param email_num: Email number string.
        :return: Email object and it's index in the list.
        """
        for idx, email in enumerate(self.emails):
            if email.value == email_num:
                return email, idx
        return None, None

    def add_phone(self, phone_num: str) -> str:
        """
        Method adds Phone instances into the list of phones for a particular client.
        :param phone_num: Phone number as a string.
        :return: Notification with the information about adding phone.
        """
        self.phones.append(Phone(phone=phone_num))
        return f"Phone number '{phone_num}' was successfully added to the contact '" \
               f"{self.name.value}'"

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Method founds the phone number in a list of other client's numbers and edits
        it if the number was found.
        :param old_phone: The phone that must be changed.
        :param new_phone: The new phone number.
        :return: None.
        """
        found_phone, idx = self.get_phone_by_number(phone_num=old_phone)
        if found_phone:
            self.phones[idx].value = new_phone
        else:
            raise ValueError(
                f"Phone with the number '{old_phone}' was not found for the "
                f"user '{self.name.value}'")
  
    def edit_email(self, old_email: str, new_email: str) -> None:
        """
        Method founds the email number in a list of other client's emails and edits it if the number was found.
        :param old_email: The email that must be changed.
        :param new_email: The new email number.
        :return: None.
        """
        found_email, idx = self.get_email_by_number(email_num=old_email)
        if found_email:
            self.emails[idx].value = new_email
        else:
            raise ValueError(
                f"Email '{old_email}' was not found for the user '{self.name.value}'")

    def remove_phone(self, phone_num: str) -> None:
        """
        Method that removes phone number from the list of client's numbers.
        :param phone_num: Phone number that should be removed.
        :return: None.
        """
        _, idx = self.get_phone_by_number(phone_num=phone_num)
        self.phones.pop(idx)

    def find_phone(self, phone_num: str) -> Phone:
        """
        Method that searches for a phone number and returns a Phone object if the
        number was found.
        :param phone_num: Phone number that should be found.
        :return: The Phone object of found phone number or None.
        """
        found_phone, _ = self.get_phone_by_number(phone_num=phone_num)
        return found_phone

    def add_birthday(self, birthday: str) -> str:
        """
        Method adds Birthday instance to the field 'birthday' for the particular client.
        :param birthday: Birthday date as a string.
        :return: Notification with the information about adding birthday.
        """
        self.birthday = Birthday(birthday=birthday)
        return f"Birthday '{birthday}' was successfully added to the birthday '" \
               f"{self.name.value}'"

    def add_address(self, address: list):
        """
        Method adds Address instance to the field 'address' for the particular client.
        :param address: country, city, street, house, apartment.
        :return: Notification with the information about adding address.
        """
        self.address = Address(address)
        return f"Address '{address}' was successfully added to the address '" \
               f"{self.name.value}'"

    def add_email(self, email: str):
        """
        Method adds Email instances into the list of emails for a particular client.
        :param email: Email address as a string.
        :return: Notification with the information about adding email.
        """
        self.emails.append(Email(email))
        return f"Email '{email}' was successfully added to the contact '" \
               f"{self.name.value}'"
