######################################################################
#    Class to represent user that is being managed by the system.    #
######################################################################

from SmartTrade.server import account_data
from SmartTrade.server.exchange import Exchange
import json
from SmartTrade.server import constants
from datetime import datetime

class User: # Class to represent a user in the system, containing their account balances and active strategies
    def __init__(self, infoDict):
        self.id = infoDict['id']
        self.username = infoDict['username']
        self.exchange = Exchange(infoDict['exchangeID'], infoDict['binanceKey'], infoDict['secretKey'])
        self.loggedIn = False
        self.tradedPairs = []
        self.transactions = [] # Load from database
        self.holdings = {} # Will be loaded in the load_data() function.
        self.isLive = False
        self.lastActivity = datetime.now()

    def save_data(self) -> None: # Save info about self to a JSON file 
        fname = f"{constants.USER_DATA_PATH}{str(self.id)}_data.json"

        result = {
            'holdings': self.holdings,
            'transactions': self.transactions,
            'loggedIn': self.loggedIn,
            'lastActivity': self.lastActivity,
            'isLive': self.isLive
        }

        with open(fname, "w") as outfile:
            json.dump(result, outfile)

    def load_data(self) -> None: # Load saved data from a JSON file
        fname = f"{constants.USER_DATA_PATH}{str(self.id)}_data.json"

        with open(fname, "r") as infile:
            inJSON = json.load(infile)

        for key in inJSON.keys():
            exec(f"self.{key} = {inJSON[key]}")

    def update_holdings(self) -> None: # Get new data about a user's balances and their value
        # As yet unimplemented.
        # Will check for the user's currency holdings and update their stored value.
        
        raise NotImplementedError

    def calculate_history(self) -> None: # Get a user's trade history and calculate profit etc.
        # As yet unimplemented.
        # Will download all of a user's past transactions, save them and calculate profits.

        raise NotImplementedError

    def login(self) -> None:
        self.loggedIn = True

    def logout(self) -> None:
        self.loggedIn = False
