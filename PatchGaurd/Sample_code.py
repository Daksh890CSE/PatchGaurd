def withdraw(balance,amount):
    if amount<0:
        return balance
    
    if amount<=balance:
        return balance-amount
    
    return balance