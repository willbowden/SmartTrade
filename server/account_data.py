######################################################
#    Module to manage data about a user's account.   #
######################################################

from datetime import datetime
import pandas as pd
from SmartTrade.server import constants, dbmanager, conversions
import time

def get_account_value(user, balances=None, atTime=None) -> dict: # Calculate and return user's total account value in USD
    totalValue = 0.0
    if atTime is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        date = atTime
    if balances is None:
        balances = get_account_balances(user)

    for key in balances.keys(): # Iterate through non-zero balances
        if key not in ['USDT', 'BUSD', 'USDC', 'GBP']:
            value = get_asset_value(user, key, balances[key], date)
        else:
            value = balances[key]
        totalValue += value
    result = {'date': date, 'value': totalValue}

    return result

def get_account_value_over_time(user, startDate=None):
    currentTime = conversions.date_to_unix(datetime.now())
    if startDate is None:
        startDate = currentTime - (30 * 86400000)
    dayDifference = ((currentTime - startDate) // 86400000) - 1
    results = []
    if dayDifference > 0:
        for day in range(dayDifference):
            value = get_account_value(user, atTime=startDate+(day*86400000))
            newRow = {'time': (startDate+(day*86400000))/10e3, 'value': value}
            results.append(newRow)

    return results
    

def get_account_holdings(user) -> dict: # Return a dictionary of the user's cryptocurrency balances and their individual value
    balances = get_account_balances(user)
    result = {}
    for key in balances.keys():
        value = get_asset_value(user, key, balances[key])
        result[key] = {'asset': key, 'balance': balances[key], 'value': value}

    totalValue = get_account_value(user, balances)
    result['totalValue'] = totalValue

    return result

def get_asset_value(user, asset:str, quantity:float, atTime=None) -> float: # Calculates the value of a given asset based on its most recent price
    if asset == 'USDT':
        value = quantity
    elif asset in constants.BLACKLISTED_COINS:
        value = 0
    else:
        if atTime is not None:
            price = user.exchange.fetch_price_at_time(asset, atTime)
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

def __get_fiat_deposits_and_withdrawals(user): # Get all fiat deposits and withdrawals made by a user.
    df = pd.DataFrame()
    deposits = pd.DataFrame(user.exchange.fetch_fiat_deposits()) # Collect data from exchange
    deposits['type'] = 'deposit' # Set the type to 'deposit
    df = df.append(deposits) # Append to dataframe
    withdrawals = pd.DataFrame(user.exchange.fetch_fiat_withdrawals()) # Get withdrawals
    withdrawals['type'] = 'withdrawal' # Set the type to 'withdrawal'
    df = df.append(withdrawals) # Append to dataframe
    df = df.rename(columns={'updateTime': 'timestamp', 'fiatCurrency': 'coin'}) # Rename some columns to conform with other data
    df = df[df['status'] == 'Successful'] # Only consider successful transactions
    df = df.drop(columns=[col for col in df if col not in ['timestamp', 'amount', 'type', 'coin']]) # Filter out only the needed info
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') # Change timestamp column to datetime type
    df.reset_index(inplace=True, drop=True) # Reset the index

    return df

def __get_crypto_deposits_and_withdrawals(user): # Get all crypto deposits and withdrawals made by a user.
    df = pd.DataFrame()
    df = df.append(user.exchange.fetch_crypto_deposits()) # Collect data from exchange
    df = df.append(user.exchange.fetch_crypto_withdrawals())
    df = df.drop(columns=[col for col in df if col not in ['info', 'timestamp', 'amount', 'type']]) # Filter out only the needed info
    df['coin'] = [row['info']['coin'] for index, row in df.iterrows()] # Extract the 'coin' info from the 'info' dict.
    df = df.drop(columns=['info']) # Get rid of the info dict, as we don't need anything more from it.
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') # Change timestamp column to datetime type
    df.reset_index(inplace=True, drop=True) # Reset the index

    return df

def __get_all_deposits_and_withdrawals(user):
    crypto = __get_crypto_deposits_and_withdrawals(user)
    fiat = __get_fiat_deposits_and_withdrawals(user)
    final = crypto.append(fiat)
    final.reset_index(inplace=True, drop=True) # Reset the index

    return final

def assemble_transactions(user, tradedPairs, trades=None, since=None):
    # 'txns' is short for 'transactions'. Just quicker to type.
    if trades is None: # If not provided a user's trades, download a new set from exchange.
        trades = pd.DataFrame()
        for pair in tradedPairs: # Get all the user's crypto trades
            print(f"Getting {pair}")
            if since is not None:
                pairTrades = user.exchange.fetch_crypto_trades(pair, since=since)
            else:
                pairTrades = user.exchange.fetch_crypto_trades(pair)
            trades = trades.append(pd.DataFrame(pairTrades)) # Append to dataframe

        trades = trades.drop(columns=[col for col in trades if col not in ['timestamp', 'symbol', 'side', 'price', 'amount', 'cost', 'fee', 'type']]) # Extract needed info
        trades = trades.rename(columns={"side": "type"}) # Rename column to conform with deposits & withdrawals
        trades['coin'] = ''

        trades.reset_index(inplace=True, drop=True)
        if since is not None:
            fiatTrades = user.exchange.fetch_fiat_trades(since=since)
        else:
            fiatTrades = user.exchange.fetch_fiat_trades()
        print(fiatTrades)
        print(trades)
        trades = trades.append(fiatTrades, ignore_index=True) # Get their fiat trades.


    if 'timestamp' not in str(type(trades['timestamp'].iat[0])):
        trades['timestamp'] = pd.to_datetime(trades['timestamp'], unit='ms') # Make sure all timestamps are in the right format, for sorting.

    txns = trades.append(__get_all_deposits_and_withdrawals(user)) # Combine with deposits and withdrawals.
    txns = txns.astype({'timestamp': 'datetime64[ms]', 'symbol': 'str', 'price': 'float64', 'amount': 'float64', 'cost': 'float64', 'fee': 'object', 'type': 'str', 'coin': 'str'}) # Convert columns to correct datatypes
 
    txns = txns.sort_values(by='timestamp') # Order data chronologically
    txns.reset_index(inplace=True, drop=True) # Reset index

    return txns