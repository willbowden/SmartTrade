import json
from SmartTrade.server.user import User
import time
from SmartTrade.server import dbmanager
import pandas as pd

### 
##    DATATYPE ISSUES IN TIMESTAMP COLUMN. SOME ARE RECEIVED AS STRINGS AND COERCED TO "NULL".
### 


u = User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
ex = u.exchange

def get_traded_pairs(user):
    tradedPairs = []
    toCheck = list(user.exchange.markets.keys()) # Get all available trading pairs on the exchange.
    while toCheck != []:
        print(f"Checking {toCheck[0]}.")
        time.sleep(0.05) # Only allowed ~1200 requests per minute, so to avoid getting blocked from the API we will wait a bit.
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

def __assemble_transactions(user, tradedPairs, trades=None):
    # 'txns' is short for 'transactions'. Just quicker to type.
    if trades is None: # If not provided a user's trades, download a new set from exchange.
        trades = pd.DataFrame()
        for pair in tradedPairs: # Get all the user's crypto trades
            print(f"Getting {pair}")
            pairTrades = user.exchange.fetch_crypto_trades(pair)
            trades = trades.append(pd.DataFrame(pairTrades)) # Append to dataframe

        trades = trades.drop(columns=[col for col in trades if col not in ['timestamp', 'symbol', 'side', 'price', 'amount', 'cost', 'fee', 'type']]) # Extract needed info
        trades = trades.rename(columns={"side": "type"}) # Rename column to conform with deposits & withdrawals
        trades['coin'] = ''

        trades = trades.append(user.exchange.fetch_fiat_trades()) # Get their fiat trades.

    if 'timestamp' not in str(type(trades['timestamp'].iat[0])):
        trades['timestamp'] = pd.to_datetime(trades['timestamp'], unit='ms') # Make sure all timestamps are in the right format, for sorting.

    txns = trades.append(__get_all_deposits_and_withdrawals(user)) # Combine with deposits and withdrawals.
    txns = txns.astype({'timestamp': 'datetime64[ms]', 'symbol': 'str', 'price': 'float64', 'amount': 'float64', 'cost': 'float64', 'fee': 'object', 'type': 'str', 'coin': 'str'}) # Convert columns to correct datatypes
 
    txns = txns.sort_values(by='timestamp') # Order data chronologically
    txns.reset_index(inplace=True, drop=True) # Reset index

    return txns

def track_transactions(user, tradedPairs, trades=None):
    txns = __assemble_transactions(user, tradedPairs, trades)

    tradeHistory = pd.DataFrame(columns=['timestamp', 'type', 'symbol', 'cost', 'amount', 'profit'])
    def __add_trade(tradeHistory, txn: pd.DataFrame, coin: str, cost: float, profit: float):
        print("Adding Trade.")
        timestamp = int(txn['timestamp'].value / 1e6)
        tradeHistory = tradeHistory.append({'timestamp': timestamp, 'type': txn['type'], 'symbol': coin, 'cost': cost, 'amount': txn['amount'], 'profit': profit}, ignore_index=True)
        return tradeHistory

    balances = {}
    for pair in tradedPairs:
        coins = pair.split("/") # Separate trading pairs into base and quote currency
        for coin in coins:
            if coin not in balances: # Add records for the balance of each coin.
                balances[coin] = []

    for index, txn in txns.iterrows():
        timestamp = int(txn['timestamp'].value / 1e6)
        if txn['type'] in ['fiatBuy']: # If we're working with a trading pair..
            base, quote = txn['symbol'].split("/") # .. separate into base and quote currencies.
            quoteValue = user.exchange.fetch_price_at_time(quote, timestamp)
            baseValue = user.exchange.fetch_price_at_time(base, timestamp)


        if txn['type'] == 'deposit':
            cost = user.exchange.fetch_price_at_time(txn['coin'], timestamp, txn['amount'])
            balances = __increase_balances(balances, txn, txn['coin'], cost, cost)
            tradeHistory = __add_trade(tradeHistory, txn, txn['coin'], cost, 0)

        if txn['type'] == 'withdrawal':
            balances, profit = __decrease_balances(user, balances, txn['coin'], txn['amount'], 0)
            tradeHistory = __add_trade(tradeHistory, txn, txn['coin'], 0, 0)

        if txn['type'] == 'fiatBuy':
            balances = __increase_balances(balances, txn, base, quoteValue, txn['cost'])
            tradeHistory = __add_trade(tradeHistory, txn, txn['symbol'], (txn['price'] * txn['amount']), 0)
        
        if txn['type'] == 'buy':
            balances = __increase_balances(balances, txn, base, baseValue, (quoteValue * txn['cost']))
            balances, profit = __decrease_balances(user, balances, quote, txn['cost'], quoteValue)
            tradeHistory = __add_trade(tradeHistory, txn, txn['symbol'], txn['cost'], 0)

        if txn['type'] == 'sell':
            balances = __increase_balances(balances, txn, quote, baseValue, (quoteValue * txn['cost']))
            balances, profit = __decrease_balances(user, balances, base, txn['cost'], baseValue)
            tradeHistory = __add_trade(tradeHistory, txn, txn['symbol'], txn['cost'], profit)

    print(tradeHistory)
    print(balances)

    return tradeHistory
            

def __increase_balances(balances: dict, txn: pd.DataFrame, coin: str, price: float, cost: float) -> dict:
    timestamp = int(txn['timestamp'].value / 1e6)
    balances[coin].append({'timestamp': timestamp, 'price': price, 'cost': cost, 'amount': txn['amount']})
    return balances
        
def __decrease_balances(user, balances: dict, coin: str, amount: float, value:float) -> pd.DataFrame:
    profit = 0
    while amount > 0:
        try:
            if balances[coin][0]['amount'] < amount:
                spent = balances[coin][0]['amount']
                cost = balances[coin][0]['cost']
                amount -= balances[coin][0]['amount']
                balances[coin].pop(0)
            else:
                spent = amount
                cost = balances[coin][0]['cost'] * spent
                amount = 0
                balances[coin][0]['amount'] -= spent

                if value != 0:
                    profit += ((spent * value) - (cost))

        except Exception as e:
            print(e)
            print(f"Failed To Decrease Balance For: {coin}. Continuing")
            return balances, profit

    return balances, profit




trades = pd.read_json('./Testing Files/trades.json')
with open('./Testing Files/tradedPairs.json', 'r') as infile:
    tradedPairs = json.load(infile)

with open('./Testing Files/trades.json', 'r') as infile:
    trades = pd.read_json(infile)

out = track_transactions(u, tradedPairs, trades)
# with open('tradeHistory.json', 'w') as outfile:
#     out.to_json(outfile)