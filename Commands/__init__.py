from typing import Dict, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


USERNAME = "bot"
with open(".env") as file:
    PASSWORD = file.readlines()[1].split("=")[1]

client = MongoClient(
    f"mongodb+srv://{USERNAME}:{PASSWORD}"
    "@cluster0.uniku.mongodb.net/"
    "myFirstDatabase?retryWrites=true&w=majority"
)
db = client.get_database("economicbot")
USER_DATABASE: Collection = db.get("user_balance")


def check_user_exists(*, user_id: int):
    """Checks whether the user exists in the database or not.
    If it doesn't exists, then it is added to the database
    """
    try:
        data = {"_id": user_id, "coins": 100, "bank": 150}
        USER_DATABASE.insert_one(data)
    except DuplicateKeyError:  # the `user_id` already exists
        pass


def update_database(*, user_id: int, new_data: Dict[str, Any]):
    """Updates the database
    if there is a change in the total number of coins in the user's bank etc
    """
    query = {"_id": user_id}
    new_data = {"$set": new_data}
    USER_DATABASE.update_one(query, new_data)
