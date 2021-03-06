import json


URL = "http://0.0.0.0:8080/"
CURRENCY = "⏣"


def to_int(**args) -> dict:
    """Converts the args into a float"""
    new_dict = {}
    for key, i in zip(args.keys(), args.values()):
        if i.isdigit():
            new_dict[key] = float(i)
        else:
            new_dict[key] = i

    return new_dict


def check(function):
    """Checks whether the account of the user already exists or not"""

    def check_account_exists(self: object, *, user_id: str, **args):
        data = {}
        if not user_id in self.data:
            data[user_id] = {
                "wallet": 100,
                "bank": 500,
                "inventory": {}
            }
        args = to_int(user_id=user_id, **args)
        args["user_id"] = int(user_id)

        new_data = {}
        if data:
            previous_data = load_data("user_data")
            new_data = dict(list(data.items()) + list(previous_data.items()))
            save_data(new_data)

        if new_data:
            self.data = new_data
        
        save_data(self.data)
        self.data = load_data("user_data")
        return function(self, **args)
    return check_account_exists


def save_data(data: dict):
    """Stores the data in the file"""
    with open("API/user_db.json", "w") as file:
        json.dump(data, file, indent=4)


def load_data(which_data: str) -> dict:
    """
    Loads the database
    :return: Dictionary
    """
    if which_data == "user_data":
        with open("API/user_db.json", "r") as file:
            data = json.load(file)
            data_keys = map(int, list(data.keys()))
            
            for old_data, new_data in zip(list(data.keys()), data_keys):
                old_info_ = data[old_data]
                data.pop(old_data)  # remove the old keys
                # add the new key
                data[new_data] = old_info_
            return data
    else:
        with open("API/shop_db.json", "r") as file:
            return json.load(file)

    raise FileNotFoundError("Please enter the name of a valid Database ")
