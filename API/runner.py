from threading import Thread
from flask import Flask
from API import Client_Transactions

app = Flask(__name__)


user_transactions = Client_Transactions.Transaction()


@app.route('/')
def main():
    return "Protecting the database"


@app.route("/with=<user_id>+<amount>")
@app.route("/withdraw=<user_id>+<amount>")
def withdraw(user_id: str, amount: int) -> {str: bool, str: float}:
    return {str: user_transactions.withdraw(user_id, amount)[0]}


@app.route("/dep=<user_id>+<amount>")
def deposit(user_id: str, amount: int) -> {str: bool, str: float}:
    return {str: user_transactions.dep(user_id, amount)[0]}


@app.route("/balance=<user_id>")
@app.route("/bal=<user_id>")
def balance(user_id: str) -> {str: bool, str: float}:
    return {str: user_transactions.balance(user_id)[0]}


@app.route("/buy=<user_id>+<item>+<amount>")
def but(user_id: str, item: str, amount: int) -> {str: bool, str: float}:
    return {str: user_transactions.buy(user_id, item, amount)[0]}


@app.route("/sell=<user_id>+<item>+<amount>")
def sell(user_id: str, item: str, amount: int) -> {str: bool, str: float}:
    return {str: user_transactions.sell(user_id, item, amount)[0]}


def run():
    app.run(host="0.0.0.0", port=8080)  # , debug=True)


def start():
    return run()


if __name__ == "__main__":
    start()
