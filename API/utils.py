import json


URL = "http://0.0.0.0:8080/"
CURRENCY = "⏣"


def to_int(*args) -> list:
    """Converts the args into a float"""
    new_args = []
    for i in args:
        if i.isdigit():
            new_args.append(int(i))
        else:
            new_args.append(i)

    return new_args


def check(function):
    """Checks whether the account of the user already exists or not"""

    def check_account_exists(self, *, user_id: str, **args):
        if not user_id in self.data:
            self.data[user_id] = {
                "wallet": 100,
                "bank": 500,
                "inventory": {}
            }
        args = to_int(**args)
        return function(self, user_id, **args)
    return check_account_exists


def save_data(data: dict):
    """Stores the data in the file"""
    with open("API/user_db.json", "w") as file:
        json.dump(data, file, indent=4)
