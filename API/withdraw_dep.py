import json


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


def bal(id: str) -> {str: [], str: float, str: float}:
    """
    Gets the balance of the user
    :return {inv: List, wallet: Real, bank: Real}:
    """
    return get_data(id)


@check
def dep(id, amount) -> str:
    """
    Allows user to deposit money 
    :return STRING:
    """

    data = get_data(id)
    if data["wallet"] < amount:
        return "Not enough money"

    data["wallet"] -= amount
    data["bank"] += amount
    save_data(id, data)

    return f"{amount} has been deposited"


@check
def wit(id, amount) -> str:
    """
    Allows user to withdraw money 
    :return STRING:
    """

    data = get_data(id)
    if data["bank"] < amount:
        return "Not enough money"

    data["bank"] -= amount
    data["wallet"] += amount
    save_data(id, data)

    return f"{amount} has been withdrawn"
