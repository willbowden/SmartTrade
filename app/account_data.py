# Module to manage data about a user's account.
from SmartTrade.server import dbmanager
from datetime import datetime
from SmartTrade.app import constants
from SmartTrade.app import exchange_data
import asyncio

def get_account_value(userID: int, exchange) -> None: # Calculate user's total account value in USD and save as a new record
    totalValue = 0
    freeBalanceWithZeros = get_account_balances(exchange)
    freeBalance = {x:y for x,y in freeBalanceWithZeros.items() if y!=0} # See comments section in document
    for key in freeBalance.keys(): # Iterate only through freely available balances
        if key != 'USDT':
            price = exchange_data.get_current_price(exchange, f"{key}/USDT")
            value = freeBalance[key] * price
        else:
            value = freeBalance[key]
        totalValue += value
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    result = {'userID': userID, 'date': date, 'value': totalValue, 'currency': 'USDT'}
    return result

def save_account_value(value) -> None:
    dbmanager.add_account_value(value['userID'], value['date'], value['value'], value['currency'])

def load_account_value_data(userID: int) -> list:
    return dbmanager.load_account_values(userID)

def get_account_balances(exchange) -> dict: # Get dict of free balances for every coin
    balanceJSON = exchange.fetch_balance()
    return balanceJSON['free']