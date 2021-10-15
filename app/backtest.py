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
        self.startingBalance = startingBalance
        self.balance = startingBalance
        self.config = configs.load_config(strategyName, userID)
        self.config['startingBalance'] = startingBalance
        self.config['symbols'] = symbols
        self.data = {}
        self.bot = bot.Bot(self, strategyName, True, self.config)
        for item in self.config['symbols']:
            self.data[item] = datasets.load_dataset(item, timeframe, startDate, self.config)
        
        self.__run()

    def __run(self):
        for symbol in self.config['symbols']:
            ds = self.data[symbol]
            for index, row in ds.iterrows():
                self.bot.tick(row, symbol)
        
        self.__get_results()

    # def __prepare_row(self, symbol, index):
    #     row = self.data[symbol].iat[index]
    #     return row
        
    def __get_results(self):
        results = self.bot.get_info()
        print(f"Balance: ${results['balance']}. Profit: ${results['profit']}. Number of Trades: {results['numOrders']}.")
        print(self.bot.assetHoldings)
        print(self.bot.orderHistory)


if __name__ == '__main__':
    b = Backtest(['ETH/USDT', 'BTC/USDT'], '1h', 1602630000000, 1000, 'testStrategy', 2194)