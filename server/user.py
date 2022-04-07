######################################################################
#    Class to represent user that is being managed by the system.    #
######################################################################

import dbm
from numpy import save
from SmartTrade.server.exchange import Exchange
import json
from SmartTrade.server import constants, dbmanager, account_data, conversions
from datetime import datetime
import pandas as pd
import dotenv

class User: # Class to represent a user in the system, containing their account balances and active strategies
    def __init__(self, infoDict):
        self.infoDict = infoDict
        self.id = infoDict['userID']
        self.username = infoDict['username']
        self.loggedIn = False
        self.tradeHistory = None
        self.tradedPairs = None
        self.load_data()

    def __getattr__(self, name):
        # It takes some time to initialise the exchange object and to get the user's holdings, 
        #    but they're not always needed instantly.
        # Instead, only initialise them when it is first accessed.
        # This will significantly reduce the time it takes to login.
        if name == 'exchange':
            self.exchange = Exchange(self.infoDict['exchangeID'], self.infoDict['apiKey'], dotenv.dotenv_values("./server/.env")[f"{self.id}_SECRET_KEY"])
            return self.exchange
        elif name == 'holdings':
            self.holdings = account_data.get_account_holdings(self)
            return self.holdings
        else:
            raise NotImplementedError

    def save_data(self) -> None: # Save info about self to a JSON file 
        fname = f"{constants.USER_DATA_PATH}{str(self.id)}_data.json"

        result = {
            'holdings': self.holdings,
            'loggedIn': self.loggedIn,
            'tradedPairs': self.tradedPairs
        }

        with open(fname, "w") as outfile:
            json.dump(result, outfile)

    def load_data(self) -> None: # Load saved data from a JSON file
        fname = f"{constants.USER_DATA_PATH}{str(self.id)}_data.json"
        try: 
            with open(fname, "r") as infile:
                inJSON = json.load(infile)

            for key in inJSON.keys():
                exec(f"self.{key} = {inJSON[key]}") # Programatically load data from JSON into instance variables.
        except:
            self.save_data()

    def get_holdings(self) -> list: # Get new data about a user's balances and their value
        self.holdings = account_data.get_account_holdings(self)
        return self.holdings

    def get_trade_history(self): # Return user's trade history. Calculate it if it doesn't exist.
        if self.id == 9227090:
            with open("C:/Users/willb/Desktop/Coding/SmartTrade/Testing Files/trades.json", 'r') as infile:
                asDf = pd.read_json(infile, orient='columns')
                return asDf.to_json(orient='records')
        if self.tradedPairs is None:
            self.tradedPairs = account_data.get_traded_pairs(self)
            self.save_data()

        savedTrades = dbmanager.get_user_trades(self.id)
        if len(savedTrades) <= 0:
            self.tradeHistory = self.__create_trade_history()
        else:
            savedTrades = pd.DataFrame(savedTrades, columns=['tradeID', 'creator', 'date', 'symbol', 'type', 'quantity', 'value', 'price', 'profit'])
            lastDate = savedTrades['date'].iat[-1]
            currentTimestamp = conversions.date_to_unix(datetime.now())
            if (currentTimestamp - lastDate.value) >= 86400000: # Update our trade history.
                newTrades = account_data.assemble_transactions(user=self, since=lastDate)
                savedTrades = savedTrades.append(newTrades)
                savedTrades = savedTrades.drop_duplicates(subset=['date'])
                self.__update_trade_database(savedTrades, lastDate)
                self.tradeHistory = savedTrades
            else:
                self.tradeHistory = savedTrades

        return self.tradeHistory.to_json(orient='records')

    def __create_trade_history(self): # Create a user's trade history 
        result = account_data.assemble_transactions(self, tradedPairs=self.tradedPairs)
        self.__update_trade_database(result, 0)
        return

    def __update_trade_database(self, trades, lastDate): # Update the database with new trade entries.
        toAdd = trades.loc[trades['date'] > lastDate]
        for index, row in toAdd.iterrows():
            dbmanager.create_trade(self.id, 'user',
            row['date'], row['symbol'], row['type'],
            row['quantity'], row['value'], row['price'], 0)


    def login(self) -> None:
        self.loggedIn = True

    def logout(self) -> None:
        self.loggedIn = False
