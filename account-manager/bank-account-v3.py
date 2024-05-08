import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def make_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class Person(Client):
    def __init__(self, name, date_of_birth, cpf, address):
        super().__init__(address)
        self.name = name
        self.date_of_birth = date_of_birth
        self.cpf = cpf


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = TransactionHistory()

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

        self._balance += amount
        print("\n=== Deposit successful! ===")
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


class TransactionHistory:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        transaction_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": transaction_time
            }
        )


class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success = account.withdraw(self.amount)
        if success:
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success = account.deposit(self.amount)
        if success:
            account.history.add_transaction(self)


def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [e]\tStatement
    [na]\tNew account
    [la]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu_text))


def find_client(cpf, clients):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None


def get_client_account(client):
    if not client.accounts:
        print("\n@@@ Client does not have any account! @@@")
        return
    return client.accounts[0]


def deposit(clients):
    cpf = input("Enter the CPF of the client: ")
    client = find_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    amount = float(input("Enter the deposit amount: "))
    transaction = Deposit(amount)

    account = get_client_account(client)
    if not account:
        return

    client.make_transaction(account, transaction)


def withdraw(clients):
    cpf = input("Enter the CPF of the client: ")
    client = find_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    amount = float(input("Enter the withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = get_client_account(client)
    if not account:
        return

    client.make_transaction(account, transaction)


def show_statement(clients):
    cpf = input("Enter the CPF of the client: ")
    client = find_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    account = get_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions have been made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\t$ {transaction['amount']:.2f} - Date: {transaction['date']}"

    print(statement)
    print(f"\nBalance:\n\t$ {account.balance:.2f}")
    print("==========================================")


def create_client(clients):
        cpf = input("Enter the CPF (numbers only): ")
        if not cpf.isdigit():
            print("\n@@@ Error: CPF must contain only numbers! @@@")
            main()
            return

        client = find_client(cpf, clients)

        if client:
            print("\n@@@ Client with this CPF already exists! @@@")
            return

        name = input("Enter the full name (Only text): ")
        date_of_birth = input("Enter the date of birth (Only Numbers) (ddmmyyyy): ")
        address = input("Enter the address (street, number - neighborhood - city/state) (Only text): ")
        
        if name.isdigit() or address.isdigit():
            print("\n@@@ Error: Name or Addres must contain only text! @@@")
            main()
            return
        
        if not date_of_birth.isdigit():
            print("\n@@@ Error: Your date of birth must contain only numbers! @@@")
            main()
            return

        client = Person(name=name, date_of_birth=date_of_birth, cpf=cpf, address=address)

        clients.append(client)

        print("\n=== Client created successfully! ===")

def create_account(account_number, clients, accounts):
    cpf = input("Enter the CPF of the client: ")
    client = find_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found, account creation process aborted! @@@")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\n=== Account created successfully! ===")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    clients = []
    accounts = []

    while True:
        option = menu().lower()

        if option == "d":
            deposit(clients)

        elif option == "w":
            withdraw(clients)

        elif option == "e":
            show_statement(clients)

        elif option == "nu":
            create_client(clients)

        elif option == "na":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\n@@@ Invalid operation, please select again. @@@")


if __name__ == "__main__":
    main()
