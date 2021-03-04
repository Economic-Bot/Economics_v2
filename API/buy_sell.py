import json
import string

SHOP = [
    {

    }, {

    }, {

    }
]

def check(function) -> [str, ()]:
    """
    Checks whether the amount is a digit or not
    :return String:
    :return function(id, amount):
    """
    def number_check(id, amount):
        if amount.isdigit():
            amount = float(amount)
            return function(id, amount)

        return "Invalid data"
    return number_check


def save_data(id, data) -> None:
    with open("db.json", "w") as file:
        json.dump({id: data}, file, indent=4)


def get_data(id: str) -> {str: [], str: float, str: float}:
    """
    This is a helper function
    :return {inv: List, wallet: Real, bank: Real}:
    """
    with open("db.json", "r") as file:
        data = json.load(file).get(id, {"inv": [], "wallet": 500, "bank": 500})

    return data


@check
def buy(id, amount):
    ...
