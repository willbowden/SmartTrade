########################################################################################################
#    Class that automates a user's strategy, keeping track of balances, profits and placing orders.    #
########################################################################################################

import sys
import importlib
import json
from datetime import datetime
import pandas as pd
from SmartTrade.app import constants
from SmartTrade.app import account_data

class Bot:
    def __init__(self, owner, strategyName, config, saveData=None) -> None:
        self.owner = owner
        self.config = config
        if saveData is not None:
            self.__load_from_save(saveData)
        else:
            self.__first_time_setup()

        self.__load_strategy(strategyName)

    def __generic_setup(self, data) -> None:
        self.balance = data['balance']
        self.accountValue = data['value']
        self.dryRun = data['dryRun']

    def get_tick_frequency(self) -> int:
        return self.config['tickFrequency']

    def __first_time_setup(self) -> None:
        self.__generic_setup(self.config)
        self.startingBalance = self.balance
        self.startDate = datetime.now()
        self.daysRunning = 1
        self.assetHoldings = []

    def __load_from_save(self, saveData) -> None:
        self.__generic_setup(saveData)
        self.startingBalance = saveData['startingBalance']
        self.startDate = datetime.strptime(saveData['startDate'], '%Y-%m-%d %H:%M:%S')
        self.daysRunning = saveData['daysRunning']
        self.assetHoldings = saveData['assetHoldings']
        self.orderHistory = pd.DataFrame(saveData['orderHistory'], columns=['date', 'side', 'quantity', 'value', 'price'])

    def __load_strategy(self, name) -> None:
        sys.path.append(constants.STRATEGY_PATH)
        self.strategy = importlib.import_module(name)

    def tick(self, data) -> None:
        self.strategy.check_buy(self, data)
        self.strategy.check_sell(self, data)

    def __save_progress(self) -> None:
        pass

    def __update_balances_and_pnl(self) -> None:
        pass