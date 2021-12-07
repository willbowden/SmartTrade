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
        self.isLoggedIn = False
        self.lastActivity = datetime.now()

    def save_data(self) -> None: # Save info about self to a JSON file 
        # As yet unimplemented. 
        # Will load data from a .json file pertaining to the user.

        raise NotImplementedError

    def load_data(self) -> None: # Load saved data from a JSON file
        # As yet unimplemented. 
        # Will load the data outlined above from the JSON file into instance attributes

        raise NotImplementedError

    def update_holdings(self) -> None: # Get new data about a user's balances and their value
        self.holdings = account_data.get_account_holdings(self.exchange)

    def login(self) -> None:
        self.isLoggedIn = True

    def logout(self) -> None:
        self.isLoggedIn = False

    

