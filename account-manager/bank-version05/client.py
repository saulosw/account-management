class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def make_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class Person(Client):
    def __init__(self, name, date_of_birth, cpf, address, email):
        super().__init__(address)
        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.cpf = cpf