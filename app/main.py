from flask import Flask, jsonify, request

try:
    from app.account import BankAccount
except ModuleNotFoundError:
    from account import BankAccount

app = Flask(__name__)

# In-memory account storage 
accounts = {
    "ACC001": BankAccount("ACC001", 1000.0),
    "ACC002": BankAccount("ACC002", 500.0)
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Fintech Transaction API is running"}), 200


@app.route("/api/account/<account_id>", methods=["GET"])
def get_balance(account_id):
    account = accounts.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "account_id": account.account_id,
        "balance": account.balance
    }), 200


@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.get_json() or {}
    account_id = data.get("account_id")
    amount = data.get("amount")

    if not account_id or amount is None:
        return jsonify({"error": "Missing account_id or amount"}), 400

    account = accounts.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    try:
        new_balance = account.deposit(float(amount))
        return jsonify({
            "message": "Deposit successful",
            "account_id": account.account_id,
            "balance": new_balance
        }), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json() or {}
    account_id = data.get("account_id")
    amount = data.get("amount")

    if not account_id or amount is None:
        return jsonify({"error": "Missing account_id or amount"}), 400

    account = accounts.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    try:
        new_balance = account.withdraw(float(amount))
        return jsonify({
            "message": "Withdrawal successful",
            "account_id": account.account_id,
            "balance": new_balance
        }), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@app.route("/api/transfer", methods=["POST"])
def transfer():
    data = request.get_json() or {}
    source_id = data.get("source_id")
    target_id = data.get("target_id")
    amount = data.get("amount")

    if not source_id or not target_id or amount is None:
        return jsonify({"error": "Missing source_id, target_id, or amount"}), 400

    source_account = accounts.get(source_id)
    target_account = accounts.get(target_id)

    if not source_account or not target_account:
        return jsonify({"error": "One or both accounts not found"}), 404

    try:
        source_account.transfer(target_account, float(amount))
        return jsonify({
            "message": "Transfer successful",
            "source_id": source_account.account_id,
            "source_balance": source_account.balance,
            "target_id": target_account.account_id,
            "target_balance": target_account.balance
        }), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
