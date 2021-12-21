import json
from SmartTrade.server.user import User
import time
from SmartTrade.server import dbmanager
from server.dbmanager import get_user_strategies

u = User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
ex = u.exchange

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

def get_transactions(user, tradedPairs):
    trades = []
    for pair in tradedPairs:
        balances = []
        pairTrades = user.exchange.fetch_trades(pair)
        with open('trades.json', 'w') as outfile:
            json.dump(pairTrades, outfile)






            
