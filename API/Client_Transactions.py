import json
from API import utils, save_data


class Transaction:
    def __init__(self):
        """
        Loads the database
        """
        with open("API/user_db.json", "r") as file:
            self.data = json.load(file)

    @utils.check
    def withdraw(self, user_id: str, amount: int) -> (bool, None):
        """
        Allows users to withdraw money from the bank.
        Bank amount decreases
        Wallet amount increases
        :return: Boolean
        """
        if self.data[user_id]["bank"] > amount:
            self.data[user_id]["bank"] -= amount
            self.data[user_id]["wallet"] += amount
            return (True, utils.save_data())
        return (False, utils.save_data())

    @utils.check
    def dep(self, user_id: str, amount: int) -> (bool, None):
        """
        Allows users to deposit money from the bank.
        Bank amount increases
        Wallet amount decreases
        :return: Boolean
        """
        if self.data[user_id]["wallet"] < amount:
            self.data[user_id]["bank"] += amount
            self.data[user_id]["wallet"] -= amount
            return (True, utils.save_data())
        return (False, utils.save_data())

    @utils.check
    def balance(self, user_id: str) -> [float, float]:
        """
        Allows users to check there balance.
        :return: [Float, Float]
        """
        return [self.data[user_id]["wallet"], self.data[user_id]["bank"]]
