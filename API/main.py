# necessary imports
from flask import Flask
import withdraw_dep

app = Flask(__name__)

@app.route('/')
def main():
    return "Mainting database"


@app.route('/bal=<id>')
def bal(id: str):
    return withdraw_dep.bal(id)


@app.route('/dep=<id>+<amount>')
def dep(id: str, amount: str):
    return withdraw_dep.dep(id, amount)


@app.route('/with=<id>+<amount>')
def withdraw(id: str, amount: str):
    return withdraw_dep.wit(id, amount)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969, debug=True)
