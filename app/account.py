class BankAccount:
    def __init__(self, account_id: str, balance: float = 0.0):
        self.account_id = account_id
        self.balance = float(balance)

    def deposit(self, amount: float) -> float:
        # Validate deposit amount
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        # Validate withdrawal amount
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError("Insufficient balance for withdrawal.")
        self.balance -= amount
        return self.balance

    def transfer(self, target_account: "BankAccount", amount: float) -> bool:
        # Validate transfer details
        if target_account is None:
            raise ValueError("Target account is required for transfer.")
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError("Insufficient balance for transfer.")
        
        self.balance -= amount
        target_account.balance += amount
        return True
