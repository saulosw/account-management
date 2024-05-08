from datetime import datetime

def deposit(account_balance, statement, deposits):
    deposit_amount = float(input("Enter the deposit amount: "))
    if deposit_amount > 0:
        current_date_time = datetime.now()
        current_date = current_date_time.strftime('%m/%d/%Y %H:%M')
        deposits += 1
        account_balance += deposit_amount
        statement += f"Deposit of ${deposit_amount:.2f} made on {current_date}\n"
        print(f"Deposit of ${deposit_amount:.2f} successful")
    else:
        print("Operation failed. Please enter a valid amount.")
    return account_balance, statement, deposits

def withdraw(account_balance, statement, withdrawals):
    withdrawal_limit = 500
    WITHDRAWALS_PER_DAY = 3
    if withdrawals < WITHDRAWALS_PER_DAY:
        withdrawal_amount = float(input("Enter the withdrawal amount: "))
        if withdrawal_amount <= withdrawal_limit and withdrawal_amount <= account_balance:
            current_date_time = datetime.now()
            current_date = current_date_time.strftime('%m/%d/%Y %H:%M')
            withdrawals += 1
            account_balance -= withdrawal_amount
            statement += f"Withdrawal of ${withdrawal_amount:.2f} made on {current_date}\n"
            print(f"Withdrawal of ${withdrawal_amount:.2f} successful.")
        elif withdrawal_amount > withdrawal_limit:
            print(f"Withdrawal amount exceeds daily limit of ${withdrawal_limit}.")
        else:
            print(f"Insufficient balance. You have ${account_balance:.2f}")
    else:
        print("Daily withdrawal limit reached.")
    return account_balance, statement, withdrawals

def view_statement(account_balance, statement, deposits, withdrawals):
    print(f'============= STATEMENT =============')
    print(f"Current balance: ${account_balance}")
    print("============ Activities ============")
    print(f"You made {deposits} deposit(s) and {withdrawals} withdrawal(s).")
    print("No activities were performed." if not statement else statement)

def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None

def create_user(users):
    cpf = int(input("Enter your CPF (numbers only): "))
    user = filter_user(cpf, users)

    if user:
        print("\n===== User with this CPF already exists! ====")
        return
    username = str(input("Enter your username: "))
    user_birth = str(input("Enter your birth date (MM/DD/YYYY): "))
    user_address = str(input("Enter your address: "))

    users.append({"name": username, "user_birth": user_birth, "user_address": user_address, "cpf": cpf})

    print("==== User created successfully! ====")

def create_account(agency, account_num, users):
    cpf = int(input("Enter your CPF (numbers only): "))
    user = filter_user(cpf, users)

    if user:
        print("==== Account created successfully! ====")
        return {"agency": agency, "account_num": account_num, "user": user}
    print("==== User not found, please insert an existing CPF! ====")

def list_account(accounts):
    for account in accounts:
        print(f"""
==================================================
                Agency: {account['agency']}
                Account Number: {account['account_num']}
                Username: {account['user']['name']}
==================================================
        """)

menu = """
[ d ] Deposit
[ w ] Withdraw
[ v ] View Statement
[ nu ] New User
[ na ] New Account
[ la ] List All Accounts
[ q ] Quit

=> """

account_balance = 0
statement = ""
deposits = 0
withdrawals = 0
users = []
accounts = []
account_num = 0
AGENCY = "0001"

while True:
    option = input(menu).lower()
    
    if option == "d":
        account_balance, statement, deposits = deposit(account_balance, statement, deposits)
        
    elif option == "w":
        account_balance, statement, withdrawals = withdraw(account_balance, statement, withdrawals)
        
    elif option == "v":
        view_statement(account_balance, statement, deposits, withdrawals)

    elif option == "nu":
        create_user(users)

    elif option == "na":
        account_num = len(accounts) + 1
        account = create_account(AGENCY, account_num, users)

        if account:
            accounts.append(account)

    elif option == "la":
        list_account(accounts)
        
    elif option == "q":
        break

    else:
        print("========= Invalid operation, please try again! =========")