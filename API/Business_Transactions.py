from API import utils, save_data
import json


class Business:
    def __init__(self):
        """
        Loads the database
        """
        with open("API/user_db.json", "r") as file:
            self.data = json.load(file)

        with open("API/shop_db.json", "r") as file:
            self.shop = json.load(file)
    
    @utils.check()
    def buy(self, user_id: str, item: str, amount: int) -> bool:
        if item in self.shop.keys():
            cost = amount*self.shop[item]["cost"]
            # check whether the person has enough funds
            if self.data[user_id]["wallet"] >= cost:
                self.data[user_id]["wallet"] -= cost
                # store that in the `inventory`
                if self.data[user_id]["inventory"][item].get("amount", 0):
                    self.data[user_id]["inventory"][item]["amount"] += amount
                else:
                    self.data[user_id]["inventory"][item]["amount"] = amount
                return True
        return False
