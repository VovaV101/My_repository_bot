from prompt_toolkit.completion import NestedCompleter


def get_nested_completer() -> NestedCompleter:
    """
    Method that creates the dictionary with the instructions how to prompt commands
    in console for the bot.
    :return: NestedCompleter instance
    """
    return NestedCompleter.from_nested_dict({
        "help": None,
        "hello": None,
        "delete": None,
        "change": None,
        "update": {"birthday": None},
        "phone": None,
        "show": {"all": None, "days to birthday": None},
        "good bye": None,
        "close": None,
        "exit": None,
        "add": {
            "contact": None,
            "phone": None,
            "email": None,
            "address": None
        },
        "search": None,
        "upcoming birthdays": None
    })

