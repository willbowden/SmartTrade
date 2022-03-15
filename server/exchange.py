##########################################################################
#    Class to allow program to interact with user's exchange accounts    #
##########################################################################

import ccxt
import datetime
import pandas as pd
import time
from forex_python.converter import CurrencyRates
from SmartTrade.server import conversions, constants

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
        self.fiatConverter = CurrencyRates()

    def __getattr__(self, name): 
        # It takes a long time to load markets, but they're not used often.
        # To save time, I'll only load markets when they're needed.
        if name == 'markets':
            self.markets = self.exchange.load_markets()
            return self.markets
        else:
            raise NotImplementedError

    # General purpose function to download data using pagination
    def __use_pagination(self, func, since, timeArgName, kwargs={}) -> list:
        end = self.exchange.milliseconds() - 1000 # Use the current time as the end date.
        whole = []
        sameSinceCount = 0
        while since < end and sameSinceCount < 3: 
            # If the latest data point is earlier than the end date,
            #   we'd get stuck in a loop. So keep count of repeating data.

            if 'params' in kwargs: # Handling custom API requests such as fetching fiat trades.
                kwargs['params']['beginTime'] = since
                new  = func(kwargs['params'])
            else:
                kwargs['since'] = since
                new = func(**kwargs) # Request data from exchange using provided function.

            if new == []:
                return whole
            latestDate = int(new[-1][timeArgName])
            if latestDate == since: # If we see a repeated date, don't append repeated data.
                sameSinceCount += 1
            else:
                whole += new
                since = latestDate

        return whole

    # Use pagination to gather data by working backwards.
    def __reverse_pagination(self, func, start, timeArgName, endArgName, params={}, kwargs={}) -> list:
        # Since we don't know how much data is available, we'll have to stop searching when getting repeated data
        whole = []
        sameSinceCount = 0
        while sameSinceCount < 3: 
            params[endArgName] = start
            new = func(params=params, **kwargs)

            if new == []:
                return whole
            earliestDate = int(new[0][timeArgName]) # Get the first (earliest) date.
            if earliestDate == start: # If we see a repeated date, don't append repeated data.
                sameSinceCount += 1
            else:
                whole += new
                start = earliestDate

        return whole

    # Allows me to make API calls that aren't included in every exchange and
    #   treat them the same as every other call.
    def __custom_api_caller(self, func):
        def temp(params): # Return a temporary function
            try:
                result = func(params)['data'] # Only extract and return the data part of a response
            except Exception as e:
                print(e)
                result = []

            return result
        
        return temp
        
    # Get a user's cryptocurrency balances
    def fetch_balances(self):
        if self.exchange.has['fetchBalance']:
            return self.exchange.fetchBalance()
        else:
            raise Exception('Exchange does not support fetching balance.')

    # Get the most recent ~50 price points for a given symbol
    def fetch_ticker(self, symbol): 
        if self.exchange.has['fetchTicker']:
            self.ticker=self.exchange.fetch_trades(symbol)
            return self.ticker
        else:
            raise Exception("Exchange does not support fetching tickers.")

    # Get open, high, low, close, volume data for a given symbol and from a given date. Can only return ~500 datapoints at once
    def fetch_ohlcv(self, symbol, timeframe, since=1230768000000, limit=None) -> pd.DataFrame: 
        if isinstance(since, str):
            since = conversions.date_to_unix(since)

        if self.exchange.has['fetchOHLCV']: # Use pagination to fetch historical OHLCV data. Default start date is as early as possible.
            whole = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            sameSinceCount = 0
            end = self.exchange.milliseconds() - 1000
            # Estimate the number of datapoints to download.
            print(since, end)
            toFetch = int(round(((end-since)/constants.TIMEFRAME_MILLISECONDS[timeframe]), 0))
            print(f'Downloading historical data for {symbol}. Approximate number of datapoints to fetch: {toFetch}')
            while since < end and sameSinceCount < 3:
                toAppend = pd.DataFrame(self.exchange.fetch_ohlcv(symbol, timeframe, since, limit), columns=whole.columns) # Fetch data
                if toAppend.empty:
                    break
                if since == toAppend['timestamp'].iat[-1]:
                    sameSinceCount += 1
                else:
                    since = toAppend['timestamp'].iat[-1]
                    whole = whole.append(toAppend, ignore_index=True) # Append
                    progress = ((len(whole) / toFetch) * 100) # Calculate progress
                    print(f'{conversions.unix_to_date(since)} | {str(round(progress, 1))}% | {len(whole)} points downloaded.')

        
            whole.reset_index(inplace=True, drop=True) # Reset and remove the numerical index
            return whole
        else:
            raise Exception("Exchange does not support fetching OHLCV.")

    # Fetches the price of a given asset at any single point in time.
    def fetch_price_at_time(self, symbol: str, date: int, amount: float=None) -> float: 
        print(f"Fetching Price For {symbol}")
        if "/" not in symbol:
            return self.__get_dollar_value_at_time(symbol, date, amount)
        else:
            data = self.exchange.fetch_ohlcv(symbol, '1m', date, limit=1)

        return data[0][4] # Fetch the close price from the returned list

    def __get_dollar_value_at_time(self, coin: str, date: int, amount) -> float:
        # Gets the dollar value of an asset, useful for tracking profits
        print(f"Fetching Dollar Value For {coin}")
        found = False
        quotes = ['BUSD', 'USDC', 'USDT', 'USD'] # Iterate over all possible dollar-based currencies
        if coin in quotes:
            return amount
        counter = 0
        while not found:
            try: # Keep trying until we find an answer
                if counter > len(quotes)-1:
                    # If we can't find a value on the exchange, try to convert from fiat to USD
                    return self.__fiat_to_usd(coin, date, amount)
                symbol = f"{coin}/{quotes[counter]}"
                data = self.exchange.fetch_ohlcv(symbol, '1m', date, limit=1)
                if len(data) > 0:
                    found = True
                else:
                    counter += 1
            except Exception as e:
                print(e)
                counter += 1

        return data[0][4] # Fetch the close price from the returned list

    def __fiat_to_usd(self, coin: str, date:int, amount: float):
        print(date)
        date = datetime.datetime.fromtimestamp(date/1e3) # Convert from milliseconds to seconds
        print(f"Performing Fiat Conversion For {coin} to USD at time {date}")
        found = False
        while not found:
            try:
                rate = self.fiatConverter.get_rate(coin, 'USD', date)
                result = amount * rate
                found = True
                return result
            except Exception as e:
                print(e)
                return amount

    # Just return most recent close price from ticker
    def fetch_current_price(self, symbol: str) -> float: 
        return self.fetch_ticker(symbol)[-1]['price']

    # Collect fiat trades using pagination. Default start date is as early as possible.
    def fetch_fiat_trades(self, since=1230768000000, limit=None) -> pd.DataFrame: 
        fiatBuys = self.__use_pagination(self.__custom_api_caller(self.exchange.sapi_get_fiat_payments),
            since, 'updateTime', {'params': {'transactionType': "0", 'beginTime': since}, 'rows': limit})
        fiatSells = self.__use_pagination(self.__custom_api_caller(self.exchange.sapi_get_fiat_payments),
            since, 'updateTime', {'params': {'transactionType': "1", 'beginTime': since}, 'rows': limit})
        
        fiatBuys = pd.DataFrame(fiatBuys)
        fiatSells =  pd.DataFrame(fiatSells)
        fiatBuys['type'] = 'fiatBuy' # Set their types
        fiatSells['type'] = 'fiatSell'
        fiatTrades = fiatBuys.append(fiatSells) # Combine them
        
        fiatTrades = fiatTrades[fiatTrades['status'] == 'Completed'] # Only consider successful orders
        # Combine fiat and crypto currency symbols to make a pair e.g "BTC/GBP"
        symbolPairs = [f"{row['cryptoCurrency']}/{row['fiatCurrency']}" for index, row in fiatTrades.iterrows()]
        fiatTrades['symbol'] = symbolPairs # Add the pairs as a column
        # Only take the columns we're interested in. Drop the rest
        fiatTrades = fiatTrades.drop(columns=[col for col in fiatTrades if col not in ['symbol', 'updateTime', 'sourceAmount', 'obtainAmount', 'price', 'totalFee', 'type']])
        # Rename the columns to conform with the rest of the data.
        fiatTrades = fiatTrades.rename(columns={'updateTime': 'timestamp', 'sourceAmount': 'cost', 'obtainAmount': 'amount', 'totalFee': 'fee'})
        fiatTrades = fiatTrades.sort_values(by=['timestamp']) # Sort into chronological order.
        fiatTrades['timestamp'] = pd.to_datetime(fiatTrades['timestamp'], unit='ms')
        fiatTrades.reset_index(inplace=True, drop=True)

        return fiatTrades

    # Use pagination to fetch all crypto trades for a symbol since a given start date. Default is as early as possible.
    def fetch_crypto_trades(self, symbol=None, since=1230768000000, limit=None) -> list:
        if self.exchange.has['fetchMyTrades']:
            return self.__use_pagination(self.exchange.fetch_my_trades, since, 'timestamp', {'symbol': symbol, 'limit': limit})
        else:
            raise Exception("Exchange does not support fetching user crypto trades.")
        
    # Use pagination to fetch all of a user's orders for a symbol since a given start date. Default is earliest possible date.
    def fetch_orders(self, symbol=None, since=1230768000000, limit=None) -> list: 
        if self.exchange.has['fetchOrders']:
            return self.__use_pagination(self.exchange.fetch_orders, since, 'timestamp', {'symbol': symbol, 'limit': limit})
        else:
            raise Exception("Exchange does not support fetching user trades.")

    # Fetch all of a user's deposits prior to a given start date. Default is latest possible date.
    def fetch_crypto_deposits(self, latestDate=None) -> list: 
        if self.exchange.has['fetchDeposits']:
            if latestDate is None:
                latestDate = self.exchange.milliseconds()
            return self.__reverse_pagination(self.exchange.fetch_deposits, latestDate, 'timestamp', 'endTime')
        else:
            raise Exception("Exchange does not support fetching deposits.")

    # Fetch all of a user's withdrawals prior to a given start date. Default is latest possible date.
    def fetch_crypto_withdrawals(self, latestDate=None) -> list: 
        if self.exchange.has['fetchWithdrawals']:
            if latestDate is None:
                latestDate = self.exchange.milliseconds()
            return self.__reverse_pagination(self.exchange.fetch_withdrawals, latestDate, 'timestamp', 'endTime')
        else:
            raise Exception("Exchange does not support fetching withdrawals.")

    # Fetch all of a user's fiat deposits since a given start date. Default is earliest possible date.
    def fetch_fiat_deposits(self, latestDate=None) -> list:
        if latestDate is None:
                latestDate = self.exchange.milliseconds()
        fiatDeposits = self.__reverse_pagination(self.__custom_api_caller(self.exchange.sapi_get_fiat_orders),
            latestDate, 'updateTime', 'endTime', {'transactionType': "0"})
        return fiatDeposits

    # Fetch all of a user's fiat withdrawals since a given start date. Default is earliest possible date.
    def fetch_fiat_withdrawals(self, latestDate=None) -> list:
        if latestDate is None:
                latestDate = self.exchange.milliseconds()
        fiatWithdrawals = self.__reverse_pagination(self.__custom_api_caller(self.exchange.sapi_get_fiat_orders),
            latestDate, 'updateTime', 'endTime', {'transactionType': "1"})
        return fiatWithdrawals

    # Places an order on the exchange on behalf of a user
    def place_order(self, symbol, side, type, price, quantity): 
        return


