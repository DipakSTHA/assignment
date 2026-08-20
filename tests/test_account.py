import pytest
from app.account import BankAccount


def test_successful_deposit():
    account = BankAccount("ACC001", 100.0)
    new_balance = account.deposit(50.0)
    assert new_balance == 150.0
    assert account.balance == 150.0


def test_successful_withdrawal():
    account = BankAccount("ACC001", 200.0)
    new_balance = account.withdraw(50.0)
    assert new_balance == 150.0
    assert account.balance == 150.0


def test_balance_calculation():
    account = BankAccount("ACC001", 500.0)
    account.deposit(200.0)
    account.withdraw(100.0)
    account.deposit(50.0)
    assert account.balance == 650.0


def test_valid_transaction():
    source = BankAccount("ACC001", 300.0)
    target = BankAccount("ACC002", 100.0)
    result = source.transfer(target, 150.0)
    assert result is True
    assert source.balance == 150.0
    assert target.balance == 250.0


def test_invalid_transaction():
    source = BankAccount("ACC001", 300.0)
    with pytest.raises(ValueError, match="Target account is required"):
        source.transfer(None, 50.0)


def test_insufficient_balance():
    account = BankAccount("ACC001", 50.0)
    with pytest.raises(ValueError, match="Insufficient balance"):
        account.withdraw(100.0)

    target = BankAccount("ACC002", 0.0)
    with pytest.raises(ValueError, match="Insufficient balance"):
        account.transfer(target, 100.0)


def test_invalid_amount():
    account = BankAccount("ACC001", 100.0)
    with pytest.raises(ValueError, match="greater than zero"):
        account.deposit(-20.0)

    with pytest.raises(ValueError, match="greater than zero"):
        account.withdraw(0.0)


def test_negative_initial_balance():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount("ACC001", -50.0)
