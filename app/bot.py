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
        self.assetHoldings = {}
        self.orderHistory = pd.DataFrame(columns=['date', 'symbol', 'side', 'quantity', 'value', 'price'])

    def __load_from_save(self, saveData) -> None:
        self.__generic_setup(saveData)
        self.startingBalance = saveData['startingBalance']
        self.startDate = datetime.strptime(saveData['startDate'], '%Y-%m-%d %H:%M:%S')
        self.daysRunning = saveData['daysRunning']
        self.assetHoldings = saveData['assetHoldings']
        self.orderHistory = pd.DataFrame(saveData['orderHistory'], columns=['date', 'symbol', 'side', 'quantity', 'value', 'price'])

    def __load_strategy(self, name) -> None:
        sys.path.append(constants.STRATEGY_PATH)
        self.strategy = importlib.import_module(name)

    def tick(self, data, symbol) -> None:
        self.currentSymbol = symbol
        self.strategy.check_buy(self, data)
        self.strategy.check_sell(self, data)

        self.__update_balances_and_pnl()

    def place_order(self, side, quantity, value, price, date) -> None:
        if side == "sell":
            self.__sell(quantity, value, price, date)
        elif side == "buy":
            self.__buy(quantity, value, price, date)
    
    def __sell(self, quantity, value, price, date) -> None:
        potentialOrder = {'date': date, 'symbol': self.currentSymbol, 'side': 'sell', 'value': value, 'price': price}
        if not self.dryRun:
            valid = self.owner.place_sell_order(quantity, value, price)
            if valid:
                self.balance += (value * 0.999)
                self.assetHoldings[self.currentSymbol]['balance'] -= quantity
                if self.assetHoldings[self.currentSymbol]['outstandingSpend'] < value:
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] = 0
                else:
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] -= value
                self.orderHistory = self.orderHistory.append(potentialOrder)
            else:
                print("Bot tried to execute sell order but exchange refused!")
        else:
            if self.assetHoldings[self.currentSymbol]['balance'] >= quantity:
                self.balance += (value * 0.999)
                self.assetHoldings[self.currentSymbol]['balance'] -= quantity
                if self.assetHoldings[self.currentSymbol]['outstandingSpend'] < value:
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] = 0
                else:
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] -= value
                self.orderHistory = self.orderHistory.append(potentialOrder)
            else:
                print(f"Bot tried to sell {self.currentSymbol} but didn't have a great enough balance!")


    def __buy(self, quantity, value, price, date) -> None:
        potentialOrder = {'date': date, 'symbol': self.currentSymbol, 'side': 'buy', 'value': value, 'price': price}
        if not self.dryRun:
            valid = self.owner.place_buy_order(quantity, value, price)
            if valid:
                self.balance -= (value)
                self.assetHoldings[self.currentSymbol]['balance'] += (quantity * 0.999)
                self.assetHoldings[self.currentSymbol]['outstandingSpend'] += value
                self.orderHistory = self.orderHistory.append(potentialOrder)
            else:
                print("Bot tried to execute buy order but exchange refused!")
        else:
            if self.balance >= value:
                self.balance -= (value)
                self.assetHoldings[self.currentSymbol]['balance'] += (quantity * 0.999)
                self.assetHoldings[self.currentSymbol]['outstandingSpend'] += value
                self.orderHistory = self.orderHistory.append(potentialOrder)
            else:
                print(f"Bot tried to buy {self.currentSymbol} but didn't have a great enough balance!")
                    
    def __save_progress(self) -> None:
        pass

    def __update_balances_and_pnl(self) -> None:
        pass

    def get_info(self) -> dict:
        pass