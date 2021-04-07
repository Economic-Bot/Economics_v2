import json


def check(function):
    """Checks whether the account of the user already exists or not"""

    def check_account_exists(self, user_id: str, *args, **kwargs):
        if not user_id in self.data:
            self.data[user_id] = {
                "wallet": 100,
                "bank": 500,
                "inventory": {}
            }

        return function(user_id, *args, **kwargs)
    return check_account_exists


def save_data(data: dict):
    """Stores the data in the file"""
    with open("API/db.json", "w") as file:
        json.dump(data, file, indent=4)
