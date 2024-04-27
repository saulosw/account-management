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

menu = """
[d] Deposit
[w] Withdraw
[v] View Statement
[q] Quit

=> """

account_balance = 0
statement = ""
deposits = 0
withdrawals = 0

while True:
    option = input(menu).lower()
    
    if option == "d":
        account_balance, statement, deposits = deposit(account_balance, statement, deposits)
        
    elif option == "w":
        account_balance, statement, withdrawals = withdraw(account_balance, statement, withdrawals)
        
    elif option == "v":
        view_statement(account_balance, statement, deposits, withdrawals)
        
    elif option == "q":
        break
