from threading import Thread
from flask import Flask
from API import Client_Transactions

app = Flask(__name__)


user_transactions = Client_Transactions.Transaction()


@app.route('/')
def main():
    return "Hmm"


@app.route("/with=<user_id:string>+<amount:string>")
@app.route("/withdraw=<user_id:string>+<amount:string>")
def withdraw(user_id: str, amount: str) -> bool:
    user_transactions.withdraw(user_id, amount)


@app.route("/dep=<user_id:string>+<amount:string>")
def deposit(user_id: str, amount: str) -> bool:
    user_transactions.dep(user_id, amount)


@app.route("/balance=<user_id:string>")
@app.route("/bal=<user_id:string>")
def balance(user_id: str) -> bool:
    user_transactions.balance(user_id)


def run():
    app.run(host="0.0.0.0", port=8080, debug=True)


def start():
    server = Thread(target=run)
    server.start()


if __name__ == "__main__":
    run()
