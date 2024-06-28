from menu import menu
from utils import deposit, withdraw, show_statement, create_client, create_account, list_accounts

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