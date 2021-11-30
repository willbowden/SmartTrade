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
        #self.exchange = Exchange(infoDict['exchangeID'], infoDict['binanceKey'], infoDict['secretKey'])
        self.isLoggedIn = False
        self.lastActivity = datetime.now()

    def load_data(self) -> None: # Load saved data from a JSON file
        fname = f"{constants.USER_DATA_PATH}{str(self.id)}_data.json"
        with open(fname) as infile:
            data = json.load(infile)

        self.isLive = data['isLive'] # Is currently running a live strategy (fake and/or real money)

        self.update_value()

    def update_value(self):
        self.valueData[-1] = account_data.get_account_value(self.id, self.exchange)

    def save_updated_value(self) -> None: # Save an account value datapoint to the database
        account_data.save_account_value(self.id, self.valueData[-1])
        self.valueData.append({'date': '', 'value': 0.0}) # Append empty value to be replaced in future

    def update_holdings(self) -> None: # Get new data about a user's balances and their value
        self.holdings = account_data.get_account_holdings(self.exchange)

    def login(self) -> None:
        self.isLoggedIn = True

    def logout(self) -> None:
        self.isLoggedIn = False

    def save_data(self) -> None: # Save info about self to a JSON file
        fname = f"{constants.USER_DATA_PATH}{str(self.id)}_data.json"

        output = {'isLive': self.isLive}

        with open(fname, "w") as outfile:
            json.dump(output, outfile)

