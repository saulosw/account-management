import textwrap

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