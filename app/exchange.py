import ccxt
import datetime
import pandas as pd
from SmartTrade.app import conversions

class Exchange:
    def __init__(self, id, apiKey, secret=''):
        self.exchange_class = getattr(ccxt, id)
        self.last_request = datetime.datetime.now()
        self.exchange = self.exchange_class({
            'apiKey': apiKey,
            'secret': secret,
            'timeout': 30000,
            'enableRateLimit': True,
        })
        self.exchange.load_markets()

    def fetch_balance(self):
        if self.exchange.has['fetchBalance']:
            return self.exchange.fetchBalance()
        else:
            raise Exception('Exchange does not support fetching balance!')

    def fetch_ticker(self, symbol):
        if self.exchange.has['fetchTicker']:
            self.ticker=self.exchange.fetch_trades(symbol)
            return self.ticker
        else:
            raise Exception("Exchange does not support fetching tickers!")

    def fetch_ohlcv(self, symbol, timeframe, since = None):
        if isinstance(since, str):
            since = conversions.date_to_unix(since)
        if self.exchange.has['fetchOHLCV']:
            return self.exchange.fetch_ohlcv(symbol, timeframe, since)
        else:
            raise Exception("Exchange does not support fetching OHLCV!")
        
    def place_order(self, symbol, side, type, price, quantity):
        return
    
    def check_order(self):
        return

