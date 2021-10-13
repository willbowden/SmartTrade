##########################################################################################
#    Class to conduct a backtest on a chosen strategy and return performance results.    #
##########################################################################################

import sys
import importlib
import json
import pandas as pd
from datetime import datetime
from SmartTrade.app import constants, configs, datasets, bot


class Backtest:
    def __init__(self, symbols, timeframe, startDate, startingBalance, strategyName, userID):
        self.info = {'strategyName': strategyName, 'userID': userID}
        sys.path.append(constants.STRATEGY_PATH)
        self.strategy = importlib.import_module(strategyName)
        self.startingBalance, self.balance = startingBalance
        self.config = configs.load_config(strategyName, userID)
        self.config['startingBalance'] = startingBalance
        self.symbols = symbols
        self.data = {}
        self.bot = bot.Bot(self, strategyName, self.config)
        for item in self.symbols:
            self.data[item] = datasets.load_dataset(item, timeframe, startDate)
        
        self.__run()

    def __run(self):
        for symbol in self.symbols:
            ds = self.data[symbol]
            for _, row in ds.iterrows():
                self.bot.tick(row)
        

