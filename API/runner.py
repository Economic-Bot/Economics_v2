from flask import Flask
from API import Client_Transactions
import logging as log

log.basicConfig(
    format='Runner => %(levelname)s: %(name)s: %(message)s',
    level=log.INFO
)

app = Flask(__name__)


user_transactions = Client_Transactions.Transaction()


@app.route('/')
def main():
    log.info("Received requests on main")
    return "Protecting the database"


@app.route("/with=<user_id>+<amount>")
@app.route("/withdraw=<user_id>+<amount>")
def withdraw(user_id: str, amount: int) ->{str: bool, str: str, str: float, str: str, str: None}:
    log.info(f"Received ID: {user_id}, Amount: {amount} in widthdraw")
    return user_transactions.withdraw(user_id=user_id, amount=amount)


@app.route("/dep=<user_id>+<amount>")
def deposit(user_id: str, amount: int) -> {str: bool, str: float, str: None}:
    log.info(f"Received ID: {user_id}, Amount: {amount} in deposit")
    return user_transactions.dep(user_id=user_id, amount=amount)


@app.route("/balance=<user_id>")
@app.route("/bal=<user_id>")
def balance(user_id: str) -> {str: bool, str: float, str: None}:
    log.info(f"Received ID: {user_id} in balance")
    return user_transactions.balance(user_id=user_id)


@app.route("/buy=<user_id>+<item>+<amount>")
def buy(user_id: str, item: str, amount: int) -> {str: bool, str: float, str: None}:
    log.info(f"Received ID: {user_id}, Amount: {amount}, Item: {item} in buy")
    return user_transactions.buy(user_id=user_id, item=item, amount=amount)


@app.route("/sell=<user_id>+<item>+<amount>")
def sell(user_id: str, item: str, amount: int) -> {str: bool, str: float, str: None}:
    log.info(f"Received ID: {user_id}, Amount: {amount}, Item: {item} in sell")
    return user_transactions.sell(user_id=user_id, item=item, amount=amount)


def run():
    log.critical("Started the host")
    app.run(host="0.0.0.0", port=8080)


def start():
    return run()


if __name__ == "__main__":
    start()
