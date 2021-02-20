"""
If account doesn't exists,
Then, make a new one,
Else, don't do antthing
"""

import json
import random

DB_PATH = "Json\db.json"


class MainChecks():
    current_balance: str = "Current balance:"
    coin_3 = "<:coin_3:811329630803066921>"
    
    reaction_coin = coin = "🪙"
    
    coin_4 = "<:Coin_4:811627460642603039>"
    coin_2 = "<:coin_2:811329629847027733>"
    bank = "<:BANK:811626657680982088>"

    currency = "✪"
    danker_meme = "⏣"

    def __init__(self, *_):
        self._ = _

    def shop_items(self):
        # TODO: Add more items
        shop = {
            "Laptop": f"Price: {random.randint(50, 51)}",
            "Telephone": f"Price: {random.randint(50, 51)}",
            "Phone": f"Price: {random.randint(50, 51)}"
        }
        return shop

    def load_data(self) -> dict:
        """Loads data"""
        with open(DB_PATH, "r") as file:
            return json.load(file)

    def account_exist(self, user_id: str):
        """Checks whether the account exist"""
        data = self.load_data()
        if str(user_id) not in data:
            return self.open_account(str(user_id))

    def open_account(self, user_id: str) -> None:
        """A new account is being made"""
        data = self.load_data()

        data[user_id] = {}
        data[user_id]["bank"] = 200.00
        data[user_id]["wallet"] = 300.00
        data[user_id]["inventory"] = {}
        data[user_id]["inventory"]["items"] = []
        data[user_id]["inventory"]["amount"] = []
        data[user_id]["inventory"]["cost"] = []


        return self.save_data(data)

    def save_data(self, data) -> None:
        """Saving the current state of the account"""
        with open(DB_PATH, "w") as file:
            json.dump(data, file, indent=4)
