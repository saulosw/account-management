import sys
import os
from date_birth_validate import age_validate
from cpf_validate import validate_cpf
from code_generator import generate_client_code
from pathlib import Path
from client import Person
from transaction import Deposit, Withdrawal
from account import CheckingAccount
import textwrap

ROOT_PATH_FOLDER_EMAIL = Path(__file__).parent / "email-sys"
ROOT_PATH_FOLDER_DB = Path(__file__).parent / "client-DB"

sys.path.append(str(ROOT_PATH_FOLDER_EMAIL))
sys.path.append(str(ROOT_PATH_FOLDER_DB))

from send_email import email_validate
from user_data import client_data
from client_management_data import save_client_infodb, initialize_db
from email_validate import check_structure_email

def save_account_statement(account):
    folder = "statementpip install python-dotes"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"{account.number}_statement.txt")
    with open(filename, 'w') as file:
        file.write("================ STATEMENT ================\n")
        transactions = account.history.transactions
        if not transactions:
            file.write("No transactions have been made.\n")
        else:
            for transaction in transactions:
                file.write(f"{transaction['type']}:\n\t$ {transaction['amount']:.2f} - Date: {transaction['date']}\n")
        file.write("==========================================\n")
        file.write(f"Balance: $ {account.balance:.2f}\n")
    print(f"\n=== Account statement saved successfully in {filename}! ===")


def save_account_info(account):
    folder = "accounts"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"{account.number}_info.txt")
    with open(filename, 'w') as file:
        file.write(f"Branch: {account.branch}\n")
        file.write(f"Account: {account.number}\n")
        file.write(f"Holder: {account.client.name}\n")
    print(f"\n=== Account information saved successfully in {filename}! ===")


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

    save_account_statement(account)


def create_client(clients):
    cpf = input("Enter the CPF (numbers only): ")
    if not cpf.isdigit():
        print("\n@@@ Error: CPF must contain only numbers! @@@")
        return

    client = find_client(cpf, clients)

    if client:
        print("\n@@@ Client with this CPF already exists! @@@")
        return
    
    if not validate_cpf(cpf):
        print("\n@@@ This cpf is not valid! @@@")
        return
    
    email = input("Enter your email: ")
    for existing_client in clients:
        if existing_client.email == email:
            print("\n@@@ Error: Email already in use! @@@")
            return
    
    if not check_structure_email(email):
        print("@@@ The email has errors in its structure! @@@")
        print("** Check if the email is a Gmail and if it was written correctly! **")
        return

    name = input("Enter the full name (Only text): ")
    date_of_birth = input("Enter the date of birth (Only Numbers) (ddmmyyyy): ")

    if not age_validate(date_of_birth):
        print("\n@@@ Error: This birth date is invalid! @@@")
        return
    
    address = input("Enter the address (street, number - neighborhood - city/state) (Only text): ")

    if name.isdigit() or address.isdigit():
        print("\n@@@ Error: Name or Address must contain only text! @@@")
        return

    if not date_of_birth.isdigit():
        print("\n@@@ Error: Your date of birth must contain only numbers! @@@")
        return
    
    client_code = generate_client_code()
    
    client_data["nome"] = name
    client_data["email"] = email

    email_validate(email, name, client_code)

    user_enter_code = input("Enter the code that was sent to your email:")

    if user_enter_code == client_code:
        client = Person(name=name, date_of_birth=date_of_birth, cpf=cpf, address=address, email=email)

        clients.append(client)
        initialize_db()
        save_client_infodb(name, email, date_of_birth, cpf, address)
        print("\n=== Client created successfully! ===")

    else: print("\n@@@ Error: Your code does not exist. @@@")

def create_account(account_number, clients, accounts):
    cpf = input("Enter the CPF of the client: ")
    client = find_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found, account creation process aborted! @@@")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    save_account_info(account)
    print("\n=== Account created successfully! ===")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))