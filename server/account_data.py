######################################################
#    Module to manage data about a user's account.   #
######################################################

from datetime import datetime
from SmartTrade.server import constants, dbmanager
import time

def get_account_value(user, balances=None) -> dict: # Calculate and return user's total account value in USD
    totalValue = 0.0
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if balances is None:
        balances = get_account_balances(user)

    for key in balances.keys(): # Iterate through non-zero balances
        if key != 'USDT':
            value = get_asset_value(user, key, balances[key])
        else:
            value = balances[key]
        totalValue += value
    result = {'date': date, 'value': totalValue}

    return result

def get_account_holdings(user) -> dict: # Return a dictionary of the user's cryptocurrency balances and their individual value
    balances = get_account_balances(user)
    result = {}
    for key in balances.keys():
        value = get_asset_value(user, key, balances[key])
        result[key] = {'asset': key, 'balance': balances[key], 'value': value}

    totalValue = get_account_value(user, balances)
    result['totalValue'] = totalValue

    return result

def get_asset_value(user, asset:str, quantity:float) -> float: # Calculates the value of a given asset based on its most recent price
    if asset == 'USDT':
        value = quantity
    elif asset in constants.BLACKLISTED_COINS:
        value = 0
    else:
        price = user.exchange.fetch_current_price(f"{asset}/USDT")
        value = quantity * price
    return round(value, 2)

def get_account_balances(user) -> dict: # Get dict of total balances for every coin
    balanceJSON = user.exchange.fetch_balances()
    balances = {x:y for x,y in balanceJSON['total'].items() if y!=0}  # See coursework document
    return balances

def get_traded_pairs(user):
    tradedPairs = []
    toCheck = list(user.exchange.markets.keys()) # Get all available trading pairs on the exchange.
    while toCheck != []:
        print(f"Checking {toCheck[0]}.")
        time.sleep(0.04) # Only allowed ~1200 requests per minute, so to avoid getting blocked from the API we will wait a bit.
        try:
            orders = user.exchange.fetch_orders(symbol=toCheck[0], limit=1) # Only request 1 trade to check if the user has interacted with this pair.
            if orders != []:
                tradedPairs.append(toCheck[0])
                print("Found.")
            
            toCheck.pop(0)
        except Exception as e:
            print(e)
            toBack = toCheck.pop(0) # If we get an error, move the symbol to the end of the queue to retry later.
            toCheck.append(toBack)

    return tradedPairs


