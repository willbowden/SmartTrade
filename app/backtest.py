##########################################################################################
#    Class to conduct a backtest on a chosen strategy and return performance results.    #
##########################################################################################

import sys
import importlib
import json
import pandas as pd
from datetime import datetime
from SmartTrade.app import constants, configs


class Backtest:
    def __init__(self, symbol, timeframe, startingBalance, strategyName, userID):
        self.info = {'strategyName': strategyName, 'userID': userID}
        sys.path.append(constants.STRATEGY_PATH)
        self.strategy = importlib.import_module(strategyName)
        self.startingBalance, self.balance = startingBalance
        self.config = configs.load_config(strategyName, userID)

