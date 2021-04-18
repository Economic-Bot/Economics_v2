import json
from API import utils, Business_Transactions
import logging as log

log.basicConfig(
    format='Client API => %(levelname)s: %(name)s: %(message)s',
    level=log.INFO
)


class Transaction(Business_Transactions.Business):
    def __init__(self):
        """
        Loads the database
        """
        super(Transaction, self).__init__()
        self.data = utils.load_data("user_data")

        log.info("Loaded database")

    @utils.check
    def withdraw(self, *, user_id: str, amount: int) -> {str: bool, str: None}:
        """
        Allows users to withdraw money from the bank.
        Bank amount decreases
        Wallet amount increases
        :return: Boolean
        """
        if self.data[user_id]["bank"] > amount:
            self.data[user_id]["bank"] -= amount
            self.data[user_id]["wallet"] += amount
            return {"flag": True, "None": utils.save_data(self.data)}
        return {"flag": False, "None": utils.save_data(self.data)}

    @utils.check
    def dep(self, *, user_id: str, amount: int) -> {str: bool, str: None}:
        """
        Allows users to deposit money from the bank.
        Bank amount increases
        Wallet amount decreases
        :return: Boolean
        """
        if self.data[user_id]["wallet"] > amount:
            self.data[user_id]["bank"] += amount
            self.data[user_id]["wallet"] -= amount
            return {"flag": True, "None": utils.save_data(self.data)}
        return {"flag": False, "None": utils.save_data(self.data)}

    @utils.check
    def balance(self, *, user_id: str) -> {str: float, str: float, str: float}:
        """
        Allows users to check there balance.
        :return: [Float, Float]
        """
        inv: float = 0.00
        for i in self.data[user_id]["inventory"]:
            inv += self.data[user_id]["inventory"][i]["amount"]

        return {
            "wallet": self.data[user_id]["wallet"],
            "bank": self.data[user_id]["bank"],
            "inventory": inv
        }
