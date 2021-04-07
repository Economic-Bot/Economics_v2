import json
from API import utils, save_data


class Transaction:
    def __init__(self):
        """
        Loads the database
        """
        with open("API/db.json", "r") as file:
            self.data = json.load(file)

    @utils.check
    def withdraw(self, user_id: str, amount: str) -> bool:
        """
        Allows users to withdraw money from the bank.
        Bank amount decreases
        Wallet amount increases
        :return: Boolean
        """
        if self.data[user_id]["bank"] > amount:
            self.data[user_id]["bank"] -= amount
            self.data[user_id]["wallet"] += amount
            save_data(self.data)
            return True
        return False

    @utils.check
    def dep(self, user_id: str, amount: str) -> bool:
        """
        Allows users to deposit money from the bank.
        Bank amount increases
        Wallet amount decreases
        :return: Boolean
        """
        if self.data[user_id]["wallet"] < amount:
            self.data[user_id]["bank"] += amount
            self.data[user_id]["wallet"] -= amount
            save_data(self.data)
            return True
        return False

    @utils.check
    def balance(self, user_id: str) -> [float, float]:
        """
        Allows users to check there balance.
        :return: [Float, Float]
        """
        return [self.data[user_id]["wallet"], self.data[user_id]["bank"]]
