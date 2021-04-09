import json
from API import Client_Transactions


def to_int(*args, **kwargs) -> tuple:
    """Converts the args into a float"""
    new_args = []
    for i in args:
        if i.isdigit():
            new_args.append(int(i))
        else:
            new_args.append(i)

    new_kargs = {}
    for i in kwargs.keys():
        if kwargs[i].isdigit():
            new_kargs[i] = int(kwargs[i])
        else:
            new_kargs[i] = kwargs[i]

    return new_args, new_kargs


def check(function):
    """Checks whether the account of the user already exists or not"""

    def check_account_exists(self, user_id: str, *args, **kwargs):
        if not user_id in self.data:
            self.data[user_id] = {
                "wallet": 100,
                "bank": 500,
                "inventory": {}
            }
        args, kwargs = to_int(*args, **kwargs)
        return function(self, user_id, *args, **kwargs)
    return check_account_exists


def save_data(data: dict):
    """Stores the data in the file"""
    with open("API/user_db.json", "w") as file:
        json.dump(data, file, indent=4)
