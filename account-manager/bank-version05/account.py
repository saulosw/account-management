from transaction import TransactionHistory, Withdrawal

class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = TransactionHistory()
        self._daily_deposit_count = 0

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def branch(self):
        return self._branch

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        if amount <= 0:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False

        if amount > self.balance:
            print("\n@@@ Operation failed! Insufficient balance. @@@")
            return False

        self._balance -= amount
        print("\n=== Withdrawal successful! ===")
        return True

    def deposit(self, amount):
        if amount <= 0:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False

        if self._daily_deposit_count >= 10:
            print("\n@@@ Operation failed! Maximum daily deposit limit reached. @@@")
            return False

        self._daily_deposit_count += 1

        self._balance += amount
        print(f"\n=== {amount} Deposit successful! ===")
        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        if amount > self._limit:
            print("\n@@@ Operation failed! Withdrawal amount exceeds limit. @@@")
            return False

        num_withdrawals = len(
            [transaction for transaction in self.history.transactions if isinstance(transaction, Withdrawal)]
        )

        if num_withdrawals >= self._withdrawal_limit:
            print("\n@@@ Operation failed! Maximum withdrawal limit reached. @@@")
            return False

        return super().withdraw(amount)

    def __str__(self):
        return f"""\
            Branch:\t\t{self.branch}
            Account:\t{self.number}
            Holder:\t\t{self.client.name}
        """