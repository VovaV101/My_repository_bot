from typing import Generator


class FormatStr:
    """
    Class for formatting text output in bot module.
    """

    @staticmethod
    def get_formatted_headers() -> str:
        """
        Method generate formatted headers string.
        :return: Formatted headers string.
        """
        s = "{:^50}".format("***Clients phone numbers***")
        s += "\n{:<10} | {:<20} | {:<70} |\n".format("Number", "User name", "Phone number")
        return s

    @staticmethod
    def show_address_book(records: Generator) -> str:
        """
        Method shows information about records from Address Book. The data is formatted in a
        string with headers.
        :param records: Generator that stores data about Address Book rows.
        :return: Formatted string.
        """
        s = FormatStr.get_formatted_headers()
        counter = 1
        for record_list in records:
            for record in record_list:
                phones_str = ",".join([phone_num for phone_num in record[1]["phones"]])
                s += '{:<10} | {:<20} | {:<70} |\n'.format(counter, record[0],
                                                           phones_str)
                counter += 1
            s += "---------------------------+++------------------------------------\n"
        return s
