# Module to retrieve data from exchange about a user's account.
from server import dbmanager
from datetime import datetime
import pandas as pd
import exchange_data

def update_account_value(userID: int, exchange) -> None: # Calculate user's total account value in USD and save as a new record
    totalValue = 0
    freeBalance = get_account_balances(exchange)
    for key in freeBalance.keys(): # Iterate only through freely available balances
        price = exchange_data.get_current_price(exchange, f"{key}/USDT")
        value = freeBalance[key] * price
        totalValue += value
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.f")
    dbmanager.add_account_value(userID, date, totalValue, 'USDT')

def get_account_balances(exchange) -> dict: # Get dict of free balances for every coin
    balanceJSON = exchange.fetch_balance()
    return balanceJSON['free']