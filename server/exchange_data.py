# Module to retrieve public price data from the exchange

import datetime
from SmartTrade.server import constants, exchange, conversions
import pandas as pd

def get_current_price(exchange, symbol: str) -> float: # Just return most recent close price from ticker
    return fetch_ticker(exchange, symbol)[-1]['price']

def fetch_ticker(exchange, symbol: str): # Fetches current data for a symbol, only ~50 datapoints
    return exchange.fetch_ticker(symbol)

def fetch_historical(exchange, symbol: str, timeframe: str, since: int=None, limit:int=500) -> pd.DataFrame: #Fetches OHLCV data from a chosen start date, can only fetch ~500 datapoints at once
    raw_trades = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    dataframe = pd.DataFrame(raw_trades, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    return dataframe

def fetch_price_at_time(exchange, symbol: str, date: int): # Fetches the price of a given asset at any single point in time.
    data = fetch_historical(exchange, symbol, '1m', date, limit=1)
    return data['close']

def download_historical(symbol: str, timeframe: str, since: int=None) -> pd.DataFrame: # Uses pagination to download backtesting/training data
    ex = exchange.Exchange('binance', 'LsyXkKspvvpsPe7xHJFQB2hXr03iUdFMwCRi1BRgQgHGHILKkv8ETf07ESbCCwkK', '') # Use my apiKey to access public info
    now = conversions.date_to_unix(datetime.datetime.now())
    date = now - ((constants.OHLCV_REQUEST_SIZE - 1) * constants.TIMEFRAME_MILLISECONDS[timeframe])
    leftToFetch = int(round(((now-since)/constants.TIMEFRAME_MILLISECONDS[timeframe]), 0))
    oldest = now
    whole = None
    print(f'Downloading historical data for {symbol}. Approximate number of datapoints to fetch: {leftToFetch}')
    while (conversions.unix_to_date(oldest) > conversions.unix_to_date(since)):
        dataframe = fetch_historical(ex, symbol, timeframe, date)
        whole = dataframe.append(whole)
        oldest = whole['date'].iloc[0] # Use the end date from the last page of data to start the nexchanget page
        date = oldest - ((constants.OHLCV_REQUEST_SIZE - 1) * constants.TIMEFRAME_MILLISECONDS[timeframe])
        progress = ((len(whole) / leftToFetch) * 100)
        print(f'{conversions.unix_to_date(oldest)} | {str(round(progress, 1))}% | {len(whole)} points downloaded.')
    whole.set_index(['date', 'open', 'high', 'low', 'close', 'volume']) # Set the column headers for the price data
    whole.reset_index(inplace=True) # Reset the numerical index 
    del whole['index'] # Remove it, as it's not needed.
    return whole

if __name__ == '__main__':
    print(f"Please don't run {__file__} on its own! Use 'py run.py' to interact with the program.")