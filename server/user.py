######################################################################
#    Class to represent user that is being managed by the system.    #
######################################################################

from SmartTrade.server import account_data
from SmartTrade.server.exchange import Exchange
import json
from SmartTrade.server import constants
from datetime import datetime
import dotenv

class User: # Class to represent a user in the system, containing their account balances and active strategies
    def __init__(self, infoDict):
        self.infoDict = infoDict
        self.id = infoDict['userID']
        self.username = infoDict['username']
        self.loggedIn = False
        self.tradedPairs = []
        self.isLive = False
        self.lastActivity = datetime.now()

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
            exec(f"self.{key} = {inJSON[key]}") # Programatically load data from JSON into instance variables.

    def get_holdings(self) -> None: # Get new data about a user's balances and their value
        self.holdings = account_data.get_account_holdings(self)
        return self.holdings

    def login(self) -> None:
        self.loggedIn = True

    def logout(self) -> None:
        self.loggedIn = False
