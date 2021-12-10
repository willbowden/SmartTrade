##########################################################################
#    Class to allow program to interact with user's exchange accounts    #
##########################################################################

import ccxt
import datetime
import pandas as pd
from SmartTrade.server import conversions

class Exchange: # Class to represent an exchange object. This is necessary as each user has their own unique exchange object linked to their API key
    def __init__(self, id, apiKey, secret):
        exchange_class = getattr(ccxt, id)
        self.last_request = datetime.datetime.now()
        self.exchange = exchange_class({
            'apiKey': apiKey,
            'secret': secret,
            'timeout': 30000,
            'enableRateLimit': True,
        })
        self.markets = self.exchange.load_markets()

    def fetch_balance(self): # Get a user's cryptocurrency balances
        if self.exchange.has['fetchBalance']:
            return self.exchange.fetchBalance()
        else:
            raise Exception('Exchange does not support fetching balance.')

    def fetch_ticker(self, symbol): # Get the most recent ~50 price points for a given symbol
        if self.exchange.has['fetchTicker']:
            self.ticker=self.exchange.fetch_trades(symbol)
            return self.ticker
        else:
            raise Exception("Exchange does not support fetching tickers.")

    def fetch_ohlcv(self, symbol, timeframe, since = None): # Get open, high, low, close, volume data for a given symbol and from a given date. Can only return ~500 datapoints at once
        if isinstance(since, str):
            since = conversions.date_to_unix(since)
        if self.exchange.has['fetchOHLCV']:
            return self.exchange.fetch_ohlcv(symbol, timeframe, since)
        else:
            raise Exception("Exchange does not support fetching OHLCV.")

    def fetch_trades(self, symbol=None, since=None, limit=None) -> list: # Fetch all of a user's trades since a given start date.
        if self.exchange.has['fetchMyTrades']:
            return self.exchange.fetch_my_trades(symbol=symbol, since=since, limit=limit)
        else:
            raise Exception("Exchange does not support fetching user trades.")

    def fetch_orders(self, symbol=None, since=None, limit=None) -> list: # Fetch all of a user's trades since a given start date.
        if self.exchange.has['fetchOrders']:
            return self.exchange.fetch_orders(symbol=symbol, since=since, limit=limit)
        else:
            raise Exception("Exchange does not support fetching user trades.")


    def fetch_deposits(self, symbol=None, since=None, limit=None) -> list: # Fetch all of a user's deposits since a given start date.
        if self.exchange.has['fetchDeposits']:
            return self.exchange.fetch_deposits(symbol=symbol, since=since, limit=limit)
        else:
            raise Exception("Exchange does not support fetching deposits.")

    def fetch_withdrawals(self, symbol=None, since=None, limit=None) -> list: # Fetch all of a user's withdrawals since a given start date.
        if self.exchange.has['fetchWithdrawals']:
            return self.exchange.fetch_withdrawals(symbol=symbol, since=since, limit=limit)
        else:
            raise Exception("Exchange does not support fetching withdrawals.")

    def place_order(self, symbol, side, type, price, quantity): # Places an order on the exchange on behalf of a user
        return

