########################################################################################################
#    Class that automates a user's strategy, keeping track of balances, profits and placing orders.    #
########################################################################################################

import sys
import importlib
from datetime import datetime
from numpy import save
import pandas as pd
from SmartTrade.app import constants
from SmartTrade.app import account_data

class Bot:
    def __init__(self, owner, strategyName, dryRun, config, saveData=None) -> None:
        self.owner = owner
        self.config = config
        self.dryRun = dryRun
        if saveData is not None:
            self.__load_from_save(saveData)
        else:
            self.__first_time_setup()

        self.__load_strategy(strategyName)

    def get_tick_frequency(self) -> int:
        return self.config['tickFrequency']

    def __first_time_setup(self) -> None:
        self.balance = self.config['startingBalance']
        self.startingBalance = self.balance
        self.startDate = datetime.now()
        self.daysRunning = 1
        self.assetHoldings = {}
        for symbol in self.config['symbols']:
            self.assetHoldings[symbol] = {'balance': 0, 'value': 0, 'outstandingSpend': 0}
        self.profit = 0
        self.profitPercent = 0
        self.accountValue = 0
        self.orderHistory = pd.DataFrame(columns=['date', 'symbol', 'side', 'quantity', 'value', 'price'])

    def __load_from_save(self, saveData) -> None:
        self.balance = saveData['balance']
        self.accountValue = saveData['value']
        self.startingBalance = saveData['startingBalance']
        self.startDate = datetime.strptime(saveData['startDate'], '%Y-%m-%d %H:%M:%S')
        self.daysRunning = saveData['daysRunning']
        self.assetHoldings = saveData['assetHoldings']
        self.profit = saveData['profit']
        self.profitPercent = saveData['profitPercent']
        self.orderHistory = pd.DataFrame(saveData['orderHistory'], columns=['date', 'symbol', 'side', 'quantity', 'value', 'price'])

    def __load_strategy(self, name) -> None:
        sys.path.append(constants.STRATEGY_PATH)
        self.strategy = importlib.import_module(name)

    def tick(self, data, index, symbol) -> None:
        self.currentSymbol = symbol
        self.strategy.check_buy(self, data, index, symbol)
        self.strategy.check_sell(self, data, index, symbol)

        self.__update_balances_and_pnl(data, symbol)

    def place_order(self, side, quantity, value, price, date) -> None:
        if side == "sell":
            self.__sell(quantity, value, price, date)
        elif side == "buy":
            self.__buy(quantity, value, price, date)
    
    def __sell(self, quantity, value, price, date) -> None:
        potentialOrder = {'date': date, 'symbol': self.currentSymbol, 'side': 'sell', 'quantity': quantity, 'value': value, 'price': price}
        if value >= 10:
            if not self.dryRun:
                valid = self.owner.place_sell_order(quantity, value, price)
                if valid:
                    self.balance += (value * 0.999)
                    self.assetHoldings[self.currentSymbol]['balance'] -= quantity
                    if self.assetHoldings[self.currentSymbol]['outstandingSpend'] < value:
                        self.assetHoldings[self.currentSymbol]['outstandingSpend'] = 0
                    else:
                        self.assetHoldings[self.currentSymbol]['outstandingSpend'] -= value
                    self.orderHistory = self.orderHistory.append(potentialOrder, ignore_index=True)
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
                    self.orderHistory = self.orderHistory.append(potentialOrder, ignore_index=True)
                else:
                    print(f"Bot tried to sell {self.currentSymbol} but didn't have a great enough balance!")


    def __buy(self, quantity, value, price, date) -> None:
        potentialOrder = {'date': date, 'symbol': self.currentSymbol, 'side': 'buy', 'quantity': quantity, 'value': value, 'price': price}
        if value >= 10:
            if not self.dryRun:
                valid = self.owner.place_buy_order(quantity, value, price)
                if valid:
                    self.balance -= (value)
                    self.assetHoldings[self.currentSymbol]['balance'] += (quantity * 0.999)
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] += value
                    self.orderHistory = self.orderHistory.append(potentialOrder, ignore_index=True)
                else:
                    print("Bot tried to execute buy order but exchange refused!")
            else:
                if self.balance >= value:
                    self.balance -= (value)
                    self.assetHoldings[self.currentSymbol]['balance'] += (quantity * 0.999)
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] += value
                    self.orderHistory = self.orderHistory.append(potentialOrder, ignore_index=True)
                else:
                    print(f"Bot tried to buy {self.currentSymbol} but didn't have a great enough balance!")
                    
    def __save_progress(self) -> None:
        pass

    def __update_balances_and_pnl(self, data: dict, symbol: str) -> None:
        totalValue = 0
        for symbol in self.assetHoldings.keys():
            newValue = (self.assetHoldings[symbol]['balance'] * data['close'].iat[-1])
            self.assetHoldings[symbol]['value'] = newValue
            totalValue += newValue

        totalValue += self.balance
        self.accountValue = totalValue
        self.profit = self.accountValue - self.startingBalance
        self.profitPercent = (self.profit / self.startingBalance) * 100

    def get_info(self) -> dict:
        results = {}
        results['holdings'] = {}
        for symbol in self.assetHoldings.keys():
            holding = {'balance': self.assetHoldings[symbol]['balance'], 'value': self.assetHoldings[symbol]['value']}
            results['holdings'][symbol] = holding
        
        results['balance'] = self.balance
        results['profit'] = self.profit
        results['profitPercent'] = self.profitPercent
        results['orderHistory'] = self.orderHistory 
        numOrders = len(self.orderHistory.index)
        results['numOrders'] = numOrders

        return results