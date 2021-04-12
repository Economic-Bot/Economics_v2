from API import utils
import json
import logging as log

log.basicConfig(
    format='Business API => %(levelname)s: %(name)s: %(message)s',
    level=log.INFO
)


class Business:
    def __init__(self):
        """
        Loads the database
        """
        with open("API/user_db.json", "r") as file:
            self.data = json.load(file)

        with open("API/shop_db.json", "r") as file:
            self.shop = json.load(file)

        log.info("Loaded database(s)")

    @utils.check
    def buy(self, user_id: str, item: str, amount: int) -> (bool, float, None):
        log.info(f"Received info: {user_id}, {item}, {amount}")

        if item in self.shop.keys():
            cost = amount*self.shop[item]["cost"]
            log.info(f"Cost: {cost}")

            # check whether the person has enough funds
            if self.data[user_id]["wallet"] >= cost:
                self.data[user_id]["wallet"] -= cost
                log.info(f"Deducted {cost} from {user_id}'s wallet balance")

                # store that in the `inventory`
                if self.data[user_id]["inventory"][item].get("amount", 0):
                    self.data[user_id]["inventory"][item]["amount"] += amount
                    log.info("Increased the number of {item} by {amount}")
                else:
                    self.data[user_id]["inventory"][item]["amount"] = amount
                    log.info("Added {item} to the inventory")

                log.info(f"Sending info: {True}, {cost}, {None}")
                return (True, cost, utils.save_data(self.data))

            log.info(f"The user doesnt have enough funds")
            log.info(f"Sending info: {False} {0.00} {None}")
            return (False, 0.00, utils.save_data(self.data))

        log.info(f"{item} doesn't exist in the shop")
        log.info(f"Sending info: {False} {0.00} {None}")
        return (False, 0.00, utils.save_data(self.data))

    @utils.check
    def sell(self, user_id: str, item: str, amount: int) -> (bool, float, None):
        log.info(f"Received info: {user_id}, {item}, {amount}")

        if item in self.data[user_id]["inventory"].keys():
            cost = amount*self.shop[item]["sell"]

            # check whether the person has enough items
            if amount <= self.data[user_id]["inventory"][item]["amount"]:
                self.data[user_id]["wallet"] += cost
                # remove that item from the `inventory`
                self.data[user_id]["inventory"][item]["amount"] -= amount
                log.info(f"Removed {amount} {item} from the inventory")
                log.info(f"Sending info: {True}, {cost}, {None}")
                return (True, cost, utils.save_data(self.data))

            log.info(f"The user doesnt have {amount} {items}")
            log.info(f"Sending info: {False} {0.00} {None}")
            return (False, 0.00, utils.save_data(self.data))

        log.info(f"The user doesn't have {items} in his/her inventory")
        log.info(f"Sending info: {False} {0.00} {None}")
        return (False, 0.00, utils.save_data(self.data))
