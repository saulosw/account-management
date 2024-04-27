from datetime import datetime

def deposit(saldo, statement, deposits):
    deposit_amount = float(input("Enter the deposit amount: "))
    if deposit_amount > 0:
        current_date_time = datetime.now()
        current_date = current_date_time.strftime('%m/%d/%Y %H:%M')
        deposits += 1
        saldo += deposit_amount
        statement += f"Deposit of ${deposit_amount:.2f} made on {current_date}\n"
        print(f"Deposit of ${deposit_amount:.2f} successful")
    else:
        print("Operation failed. Please enter a valid amount.")
    return saldo, statement, deposits

def withdraw(saldo, statement, withdrawals):
    withdrawal_limit = 500
    WITHDRAWALS_PER_DAY = 3
    if withdrawals < WITHDRAWALS_PER_DAY:
        if saldo > 0:
            withdrawal_amount = float(input("Enter the withdrawal amount: "))
            if withdrawal_amount <= saldo:
                current_date_time = datetime.now()
                current_date = current_date_time.strftime('%m/%d/%Y %H:%M')
                withdrawals += 1
                saldo -= withdrawal_amount
                statement += f"Withdrawal of ${withdrawal_amount:.2f} made on {current_date}\n"
                print(f"Withdrawal of ${withdrawal_amount:.2f} successful.")
            else:
                print(f"Insufficient balance. You have ${saldo:.2f}")
        else:
            print("Zero balance.")
    else:
        print("Daily withdrawal limit reached.")
    return saldo, statement, withdrawals

def view_statement(saldo, statement, deposits, withdrawals):
    print(f'============= STATEMENT =============')
    print(f"Current balance: ${saldo}")
    print("============ Activities ============")
    print(f"You made {deposits} deposit(s) and {withdrawals} withdrawal(s).")
    print("No activities were performed." if not statement else statement)

menu = """
[d] Deposit
[w] Withdraw
[v] View Statement
[q] Quit

=> """

saldo = 0
statement = ""
deposits = 0
withdrawals = 0

while True:
    option = input(menu).lower()
    
    if option == "d":
        saldo, statement, deposits = deposit(saldo, statement, deposits)
        
    elif option == "w":
        saldo, statement, withdrawals = withdraw(saldo, statement, withdrawals)
        
    elif option == "v":
        view_statement(saldo, statement, deposits, withdrawals)
        
    elif option == "q":
        break
