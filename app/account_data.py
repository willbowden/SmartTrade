# Module to manage data about a user's account.
from SmartTrade.server import dbmanager
from datetime import datetime
from SmartTrade.app import constants
from SmartTrade.app import exchange_data
import asyncio

def get_account_value(userID: int, exchange) -> None: # Calculate user's total account value in USD and save as a new record
    totalValue = 0
    balancesWithZeros = get_account_balances(exchange)
    balances = {x:y for x,y in balancesWithZeros.items() if y!=0} # See comments section in document
    for key in balances.keys(): # Iterate only through freely available balances
        if key != 'USDT':
            price = exchange_data.get_current_price(exchange, f"{key}/USDT")
            value = balances[key] * price
        else:
            value = balances[key]
        totalValue += value
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    result = {'userID': userID, 'date': date, 'value': totalValue}
    return result

def save_account_value(userID: int, value) -> None:
    dbmanager.add_account_value(userID, value['date'], value['value'])

def load_account_value_data(userID: int) -> list:
    return dbmanager.load_account_values(userID)

def get_account_balances(exchange) -> dict: # Get dict of total balances for every coin
    balanceJSON = exchange.fetch_balance()
    return balanceJSON['total']
