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
