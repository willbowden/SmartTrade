######################################################
#    Module to manage data about a user's account.   #
######################################################

from SmartTrade.server import dbmanager
from datetime import datetime
from SmartTrade.server import constants
from SmartTrade.server import exchange_data

def get_account_value(user) -> dict: # Calculate and return user's total account value in USD
    totalValue = 0.0
    balances = get_account_balances(user)
    for key in balances.keys(): # Iterate through non-zero balances
        if key != 'USDT':
            value = get_asset_value(user, key, balances[key])
        else:
            value = balances[key]
        totalValue += value
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {'date': date, 'value': totalValue}
    return result

def get_account_holdings(user) ->  list: # Return a list of the user's cryptocurrency balances and their individual value
    balances = get_account_balances(user.exchange)
    result = []
    for key in balances.keys():
        value = get_asset_value(user.exchange, key, balances[key])
        holding = {'asset': key, 'balance': balances[key], 'value': value}
        result.append(holding)

    return result

def get_asset_value(user, asset:str, quantity:float) -> float: # Calculates the value of a given asset based on its most recent price
    if asset == 'USDT':
        value = quantity
    elif asset in constants.BLACKLISTED_COINS:
        value = 0
    else:
        price = exchange_data.get_current_price(user.exchange, f"{asset}/USDT")
        value = quantity * price
    return round(value, 2)

def get_account_balances(user) -> dict: # Get dict of total balances for every coin
    balanceJSON = user.exchange.fetch_balance()
    balances = {x:y for x,y in balanceJSON['total'].items() if y!=0}  # See coursework document
    return balances
