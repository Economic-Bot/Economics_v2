from flask import Flask
from API import Client_Transactions
import typing as t

app = Flask(__name__)


user_transactions = Client_Transactions.Transaction()


@app.route('/')
def main():
    return "Protecting the database"


@app.route("/with=<user_id>+<amount>")
@app.route("/withdraw=<user_id>+<amount>")
def withdraw(user_id: str, amount: int) -> t.Dict[t.str, bool, str, float, str, None]:
    user_transactions.withdraw()


@app.route("/dep=<user_id>+<amount>")
def deposit(user_id: str, amount: int) -> {str: bool, str: float, str: None}:
    user_transactions.withdraw()



@app.route("/balance=<user_id>")
@app.route("/bal=<user_id>")
def balance(user_id: str) -> {str: bool, str: float, str: None}:
    user_transactions.balance()


@app.route("/buy=<user_id>+<item>+<amount>")
def buy(user_id: str, item: str, amount: int) -> {str: bool, str: float, str: None}:
    user_transactions.buy()


@app.route("/sell=<user_id>+<item>+<amount>")
def sell(user_id: str, item: str, amount: int) -> {str: bool, str: float, str: None}:
    user_transactions.sell()


def run():
    app.run(host="0.0.0.0", port=8080)  # , debug=True)


def start():
    return run()


if __name__ == "__main__":
    start()
