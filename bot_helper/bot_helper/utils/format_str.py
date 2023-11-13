from typing import Generator


class FormatStr:
    """
    Class for formatting text output in bot module.
    """

    ADDRESS_KEY_LIST = ["country", "city", "street", "house", "apartment"]

    @staticmethod
    def get_formatted_headers() -> str:
        """
        Method generate formatted headers string.
        :return: Formatted headers string.
        """
        s = "{:^131}".format("******Clients phone numbers******")
        s += "\n{:<10} | {:<20} | {:<12} | {:<11} | {:<35} | {:<26} |\n".format("Number",
                                                                          "User name",
                                                                          "Phone number",
                                                                          "Birthday",
                                                                          "Email",
                                                                          "Address")
        return s
    
    @staticmethod 
    def get_formatted_headers_birthdays() -> str: 
        """ Method generate formatted headers string. :return: Formatted headers string. """ 
        s = "{:^50}".format("***Clients birthdays***") 
        s += "\n{:<10} | {:<20} | {:<70} |\n".format("Name", "Info birthdays", "Days for birthday") 
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
                phones_list: list = record[1]["phones"] if record[1]["phones"] else ["None"]
                emails_list: list = record[1]["emails"] if record[1]["emails"] else ["None"]
                address_dic: dict = record[1]["address"]

                if len(phones_list) <= 5:
                    for _ in range(5 - len(phones_list)):
                        phones_list.append(" ")

                if len(emails_list) <= 5:
                    for _ in range(5 - len(emails_list)):
                        emails_list.append(" ")

                s += '{:<10} | {:<20} | {:<12} | {:<11} | {:<35} | {:<10} {:<15} |\n'.format(
                                                                        counter,
                                                                        record[0],
                                                                        phones_list[0],
                                                                        str(record[1]["birthday"]),
                                                                        emails_list[0],
                                                                        "country:",
                                                                        str(address_dic["country"])
                                                                        )

                for indx in range(1, 5):
                    s += '{:<10} | {:<20} | {:<12} | {:<11} | {:<35} | {:<10} {:<15} |\n'.format(
                                                        "",
                                                        "",
                                                        phones_list[indx],
                                                        "",
                                                        emails_list[indx],
                                                        f"{FormatStr.ADDRESS_KEY_LIST[indx]}:",
                                                        str(address_dic[FormatStr.ADDRESS_KEY_LIST[indx]])
                                                        )
                counter += 1
                s += "{:-<64}+++{:->64}\n".format("", "")
        return s
