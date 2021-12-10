import json
from SmartTrade.server.exchange import Exchange
import time

ex = Exchange('binance', 'bpSmvc8AxJsYRRTehCADJV1hF8fSJ9zjfcdbCAqNTeLbGZ30abBa7eTrq65rPEvz', )

with open ("trades.json", "w") as outfile:
    json.dump(ex.fetch_trades("AXS/USDT"), outfile)

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

def get_transactions(exchange: Exchange):
    pass



            
