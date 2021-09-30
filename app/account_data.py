# Module to manage data about a user's account.
from SmartTrade.server import dbmanager
from datetime import datetime
from SmartTrade.app import constants
from SmartTrade.app import exchange_data
import asyncio

def get_account_value(userID: int, exchange) -> dict: # Calculate user's total account value in USD and save as a new record
    totalValue = 0
    balances = get_account_balances(exchange)
    for key in balances.keys(): # Iterate through non-zero balances
        if key != 'USDT':
            value = get_asset_value(exchange, key, balances[key])
        else:
            value = balances[key]
        totalValue += value
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {'userID': userID, 'date': date, 'value': totalValue}
    return result

def get_account_holdings(exchange) ->  list:
    balances = get_account_balances(exchange)
    result = []
    for key in balances.keys():
        value = get_asset_value(exchange, key, balances[key])
        holding = {'asset': key, 'balance': balances[key], 'value': value}
        result.append(holding)

    return result

def get_asset_value(exchange, asset:str, quantity:float) -> float:
    if asset == 'USDT':
        value = quantity
    else:
        price = exchange_data.get_current_price(exchange, f"{asset}/USDT")
        value = quantity * price
    return round(value, 2)

def save_account_value(userID: int, value) -> None:
    dbmanager.add_account_value(userID, value['date'], value['value'])

def load_account_value_data(userID: int) -> list:
    return dbmanager.load_account_values(userID)

def get_account_balances(exchange) -> dict: # Get dict of total balances for every coin
    balanceJSON = exchange.fetch_balance()
    balances = {x:y for x,y in balanceJSON['total'].items() if y!=0}  # See comments section in document
    return balances
