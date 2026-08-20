import pytest
from app.main import app, accounts
from app.account import BankAccount


@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Reset sample accounts state before each test
    accounts["ACC001"] = BankAccount("ACC001", 1000.0)
    accounts["ACC002"] = BankAccount("ACC002", 500.0)
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Fintech Transaction API is running"


def test_get_balance_api(client):
    response = client.get("/api/account/ACC001")
    assert response.status_code == 200
    assert response.json["balance"] == 1000.0


def test_deposit_api_success(client):
    response = client.post("/api/deposit", json={"account_id": "ACC001", "amount": 200.0})
    assert response.status_code == 200
    assert response.json["balance"] == 1200.0


def test_withdraw_api_success(client):
    response = client.post("/api/withdraw", json={"account_id": "ACC001", "amount": 100.0})
    assert response.status_code == 200
    assert response.json["balance"] == 900.0


def test_transfer_api_success(client):
    response = client.post("/api/transfer", json={"source_id": "ACC001", "target_id": "ACC002", "amount": 300.0})
    assert response.status_code == 200
    assert response.json["source_balance"] == 700.0
    assert response.json["target_balance"] == 800.0


def test_withdraw_api_insufficient_funds(client):
    response = client.post("/api/withdraw", json={"account_id": "ACC001", "amount": 5000.0})
    assert response.status_code == 400
    assert "error" in response.json
