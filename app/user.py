# Class to represent user that is being managed by the system.
from SmartTrade.app import account_data
from SmartTrade.app.exchange import Exchange
import json
from SmartTrade.app import constants

class User:
    def __init__(self, infoDict):
        self.id = infoDict['userID']
        self.username = infoDict['username']
        self.exchange = Exchange(infoDict['exchangeID'], infoDict['binanceKey'], infoDict['secretKey'])
        self.isLoggedIn = False
        self.valueData = account_data.load_account_value_data(self.id)
        if self.valueData == []:
            account_data.update_account_value(self.id, self.exchange)
            self.valueData = account_data.load_account_value_data(self.id)
            self.valueData.append({'userID': 0000, 'date': '', 'value': 0.0, 'currency': ''}) # Append fake data to end of list so it can be overwritten in update_value()
        self.load_data()

    def load_data(self):
        fname = constants.USER_DATA_PATH + str(self.id) + "_data.json"
        with open(fname) as infile:
            data = json.load(infile)

        self.isLive = data['isLive'] # Is currently running a live strategy (fake and/or real money)

    def update_value(self):
        newValue = account_data.get_account_value(self.id)
        self.valueData[-1] = newValue

    def save_updated_value(self):
        account_data.save_account_value(self.valueData[-1])

    def update_holdings(self):
        pass

    def login(self):
        self.isLoggedIn = True

    def logout(self):
        self.isLoggedIn = True

    def save_data(self):
        fname = constants.USER_DATA_PATH + str(self.id) + "_data.json"

        output = {'isLive': self.isLive}

        with open(fname, "w") as outfile:
            json.dump(output, outfile)

