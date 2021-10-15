######################################################################
#    Class to represent user that is being managed by the system.    #
######################################################################

from SmartTrade.app import account_data
from SmartTrade.app.exchange import Exchange
import json
from SmartTrade.app import constants
from datetime import datetime

class User: # Class to represent a user in the system, containing their account balances and active strategies
    def __init__(self, infoDict):
        self.id = infoDict['userID']
        self.username = infoDict['username']
        self.exchange = Exchange(infoDict['exchangeID'], infoDict['binanceKey'], infoDict['secretKey'])
        self.isLoggedIn = False
        self.lastActivity = datetime.now()
        self.holdings = account_data.get_account_holdings(self.exchange)
        self.valueData = account_data.load_account_value_data(self.id)
        if self.valueData == []:
            val = account_data.get_account_value(self.id, self.exchange)
            account_data.save_account_value(self.id, val)
            self.valueData = account_data.load_account_value_data(self.id)
            self.valueData.append({'date': '', 'value': 0.0}) # Append fake data to end of list so it can be overwritten in update_value()
        self.load_data()

    def load_data(self) -> None: # Load saved data from a JSON file
        fname = constants.USER_DATA_PATH + str(self.id) + "_data.json"
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
        fname = constants.USER_DATA_PATH + str(self.id) + "_data.json"

        output = {'isLive': self.isLive}

        with open(fname, "w") as outfile:
            json.dump(output, outfile)

