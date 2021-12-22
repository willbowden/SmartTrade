import json
from SmartTrade.server.user import User
import time
from SmartTrade.server import dbmanager, exchange_data
import pandas as pd

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

def __get_by_pagination(function, params, since, end):
    total = pd.DataFrame()
    while since < end:
        total = total.append(function(*params))
        since = total['timestamp'][-1]

def __get_deposits_and_withdrawals(user): # Get all deposits and withdrawals made by a user.
    df = pd.DataFrame()
    df = df.append(user.exchange.exchange.fetch_deposits()) # Collect data from exchange
    # df = df.append(user.exchange.fetch_withdrawals())
    # df = df.drop(columns=[col for col in df if col not in ['info', 'timestamp', 'amount', 'type']]) # Filter out only the needed info
    # df['coin'] = [row['info']['coin'] for index, row in df.iterrows()] # Extract the 'coin' info from the 'info' dict.
    # df = df.drop(columns=['info']) # Get rid of the info dict, as we don't need anything more from it.
    # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') # Make sure all timestamps are in the right format, for sorting.
    # df.reset_index(inplace=True, drop=True) # Reset the index

    return df

def track_transactions(user, tradedPairs, trades=None): # Track a user's trading history and use it to populate the database.
    # 'txns' is short for 'transactions'. Just quicker to type.
    balances = {}
    downloadTrades = False
    if trades is None: # If not provided a user's trades, download a new set from exchange.
        trades = pd.DataFrame()
        downloadTrades = True

    for pair in tradedPairs:
        coins = pair.split("/") # Separate trading pairs into base and quote currency
        for coin in coins:
            if coin not in balances: # Add records for the balance of each coin.
                balances[coin] = pd.DataFrame(columns=['timestamp', 'type', 'price', 'amount'])

        if downloadTrades: # Download trades from exchange if necessary
            print(f"Getting {pair}")
            pairTrades = user.exchange.fetch_trades(pair)
            trades = trades.append(pd.DataFrame(pairTrades))

    trades = trades.drop(columns=[col for col in trades if col not in ['timestamp', 'symbol', 'side', 'price', 'amount', 'cost', 'fee']]) # Extract needed info
    trades = trades.rename(columns={"side": "type"}) # Rename column to conform with deposits & withdrawals
    
    txns = trades.append(__get_deposits_and_withdrawals(user)) # Combine with deposits and withdrawals.
    txns = txns.sort_values(by=['timestamp']) # Order data chronologically
    txns.reset_index(inplace=True, drop=True) # Reset index

    print(txns)

    for index, txn in txns.iterrows():
        if type(txn['symbol']) == str: # If we're working with a trading pair..
            base, quote = txn['symbol'].split("/") # .. separate into base and quote currencies.
        if txn['type'] == 'buy':
            pass
            



# with open('tradedPairs.json', 'r') as infile:
#     tradedPairs = json.load(infile)

# trades = pd.read_json('trades.json')
# track_transactions(u, tradedPairs, trades)


u = User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
ex = u.exchange
with open('test.json', 'w') as outfile:
    result = ex.fetch_fiat_withdrawals()
    json.dump(result, outfile)

# print(ex.exchange.fetch_deposits())

# print(ex.exchange.sapi_get_fiat_orders(params={'transactionType': 1}))