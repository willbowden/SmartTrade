import datetime
import constants, configs, conversions
import pandas as pd

config = configs.load_config()

# LOAD EXCHANGE IN CONTROLLER
    
def fetch_ticker(exchange, symbol: str): # Fetches current data for a symbol, only ~50 datapoints
    return exchange.fetch_ticker(symbol)

def fetch_historical(exchange, symbol: str, timeframe: str, since: int=None) -> pd.DataFrame: #Fetches OHLCV data from a chosen start date, can only fetch ~500 datapoints at once
    raw_trades = exchange.fetch_ohlcv(symbol, timeframe, since)
    dataframe = pd.DataFrame(raw_trades, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    return dataframe

def download_historical(symbol: str, timeframe: str, since: int=None) -> pd.DataFrame: # Uses pagination to download backtesting/training data
    now = conversions.date_to_unix(datetime.datetime.now())
    date = now - ((config["ohlcv_request_size"] - 1) * constants.TIMEFRAME_MILLISECONDS[timeframe])
    leftToFetch = int(round(((now-since)/constants.TIMEFRAME_MILLISECONDS[timeframe]), 0))
    oldest = now
    whole = None
    print(f'Downloading historical data for {symbol}. Approximate number of datapoints to fetch: {leftToFetch}')
    while (conversions.unix_to_date(oldest) > conversions.unix_to_date(since)):
        dataframe = fetch_historical(symbol, timeframe, date)
        whole = dataframe.append(whole)
        oldest = whole['date'].iloc[0] # Use the end date from the last page of data to start the nexchanget page
        date = oldest - ((config["ohlcv_request_size"] - 1) * constants.TIMEFRAME_MILLISECONDS[timeframe])
        progress = ((len(whole) / leftToFetch) * 100)
        print(f'{conversions.unix_to_date(oldest)} | {str(round(progress, 1))}% | {len(whole)} points downloaded.')
        #print(f'{round(progress, 2)}% Complete ({len(whole)} fetched)')
    whole.set_indexchange(['date', 'open', 'high', 'low', 'close', 'volume'])
    whole.reset_indexchange(inplace=True)
    del whole['indexchange']
    return whole

if __name__ == '__main__':
    print(f"Please don't run {__file__} on its own! Use 'py run.py' to interact with the program.")