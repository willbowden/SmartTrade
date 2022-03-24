########################################################################################################
#    Class that automates a user's strategy, keeping track of balances, profits and placing orders.    #
########################################################################################################

from datetime import datetime
import pandas as pd
import json
from SmartTrade.server import strategy, constants

class Bot:
    def __init__(self, owner, strategyName, dryRun, config, saveData=None) -> None:
        self.owner = owner
        self.__config = config
        self.strategy = strategy.Strategy(strategyName, self.owner.id)
        self.__dryRun = dryRun
        self.inPosition = False
        self.__lastBuyPrice = 0
        self.__winners = 0
        self._saveName = f"{self.owner.id}_{strategyName.replace(' ', '_')}_BOT.json"
        if saveData is not None:
            self.__load_from_save(saveData) # Load from save if we're given data
        else:
            try:
                with open(constants.SAVE_PATH+self._saveName, 'r') as infile: # Or load from save if file exists
                    self.__load_from_save(json.load(infile))
            except:
                self.__first_time_setup()

    def __first_time_setup(self) -> None:
        # Setup all initial variables 
        self.balance = self.strategy.get_starting_balance()
        self.startingBalance = self.balance
        self.startDate = datetime.now()
        self.daysRunning = 1
        self.assetHoldings = {}
        for symbol in self.__config['symbols']:
            self.assetHoldings[symbol] = {'balance': 0, 'value': 0, 'outstandingSpend': 0}
        self.profit = 0
        self.profitPercent = 0
        self.accountValue = 0
        self.orderHistory = pd.DataFrame(columns=['timestamp', 'symbol', 'side', 'quantity', 'value', 'price', 'profit'])

    def __load_from_save(self, saveData) -> None:
        # Or, load them from a save file (for example if the program was interrupted)
        self.balance = saveData['balance']
        self.accountValue = saveData['value']
        self.startingBalance = saveData['startingBalance']
        self.startDate = datetime.strptime(saveData['startDate'], '%Y-%m-%d %H:%M:%S')
        self.daysRunning = saveData['daysRunning']
        self.assetHoldings = saveData['assetHoldings']
        self.profit = saveData['profit']
        self.profitPercent = saveData['profitPercent']
        self.orderHistory = pd.DataFrame(saveData['orderHistory'], columns=['timestamp', 'symbol', 'side', 'quantity', 'value', 'price', 'profit'])

    def __save_progress(self) -> None:
        # Save important information to JSON save file
        toSave = {
            'balance': self.balance,
            'value': self.accountValue,
            'startingBalance': self.startingBalance,
            'startDate': self.startDate.strftime('%Y-%m-%d %H:%M:%S'),
            'daysRunning': self.daysRunning,
            'assetHoldings': self.assetHoldings,
            'profit': self.profit,
            'profitPercent': self.profitPercent,
            'orderHistory': self.orderHistory.to_json()
        }
        
        with open(constants.SAVE_PATH+self._saveName, 'w') as outfile:
            json.dump(toSave, outfile)

    def tick(self, data, index, symbol) -> None:
        # Given a new index in the dataset, check the strategy's
        #   buy and sell rules. Then, update balances and PNL
        #   (profit 'n' loss).
        self.currentSymbol = symbol
        if self.inPosition == False:
            self.strategy.check_buy(self, data, index, symbol)
        if self.inPosition:
            self.strategy.check_sell(self, data, index, symbol)

        self.__update_balances_and_pnl(data, symbol)

    def place_order(self, side, quantity, price, timestamp) -> None:
        value = quantity * price # Work out the value of bought/sold assets in quote currency
        if side == "sell":
            self.__sell(quantity, value, price, timestamp)
        elif side == "buy":
            self.__buy(quantity, value, price, timestamp)
    
    def __sell(self, quantity, value, price, timestamp) -> None:
        potentialOrder = {'timestamp': timestamp, 'symbol': self.currentSymbol, 'side': 'sell', 'quantity': quantity, 'value': value, 'price': price}
        if value >= 10:
            if not self.__dryRun: # If we're using real money
                valid = self.owner.place_sell_order(quantity, value, price) # Place a real money order
            else:
                valid = True
            if valid and self.assetHoldings[self.currentSymbol]['balance'] >= quantity:
                self.balance += (value * (1 - self.__config['fee'])) # Increase our balance taking into account the fee
                self.assetHoldings[self.currentSymbol]['balance'] -= quantity
                if self.assetHoldings[self.currentSymbol]['outstandingSpend'] < value: # Reduce our 'outstanding spend'
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] = 0
                else:
                    self.assetHoldings[self.currentSymbol]['outstandingSpend'] -= value
                profitOnOrder = (price - self.__lastBuyPrice) * quantity
                potentialOrder['profit'] = profitOnOrder
                self.orderHistory = self.orderHistory.append(potentialOrder, ignore_index=True) # Add the order to history
                self.inPosition = False
                if price > self.__lastBuyPrice:
                    self.__winners += 1
            elif not valid:
                print("Bot tried to execute sell order but exchange refused!")
            else:
                print(f"Bot tried to sell {self.currentSymbol} but didn't have a great enough balance!")

    def __buy(self, quantity, value, price, timestamp) -> None:
        # Identical to above, but we're buying instead.
        potentialOrder = {'timestamp': timestamp, 'symbol': self.currentSymbol, 'side': 'buy', 'quantity': quantity, 'value': value, 'price': price, 'profit': 0}
        if value >= 10:
            if not self.__dryRun: # If we're using real money
                valid = self.owner.place_sell_order(quantity, value, price) # Place a real money order
            else:
                valid = True
            if valid and self.assetHoldings[self.currentSymbol]['balance'] >= quantity:
                self.balance -= (value)
                self.assetHoldings[self.currentSymbol]['balance'] += (quantity * (1 - self.__config['fee']))
                self.assetHoldings[self.currentSymbol]['outstandingSpend'] += value
                self.orderHistory = self.orderHistory.append(potentialOrder, ignore_index=True)
                self.inPosition = True
                self.__lastBuyPrice = price
            elif not valid:
                print("Bot tried to execute buy order but exchange refused!")
            else:
                print(f"Bot tried to buy {self.currentSymbol} but didn't have a great enough balance!")

    def __update_balances_and_pnl(self, data: dict, symbol: str) -> None:
        # Re-calculate the value of the entire account, and then calculate  
        #   profit and/or losses from that.
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
        # Return some important performance metrics as a dictionary
        results = {}
        results['holdings'] = {}
        for symbol in self.assetHoldings.keys():
            holding = {'balance': self.assetHoldings[symbol]['balance'], 'value': self.assetHoldings[symbol]['value']}
            results['holdings'][symbol] = holding

        results['startingBalance'] = self.startingBalance
        results['balance'] = self.balance
        results['profit'] = self.profit
        results['profitPercent'] = self.profitPercent
        results['orderHistory'] = self.orderHistory 
        numOrders = len(self.orderHistory.index)
        results['numBuys'] = self.orderHistory['side'].value_counts()['buy']
        results['numSells'] = self.orderHistory['side'].value_counts()['sell']
        results['numOrders'] = numOrders
        results['winRate'] = (self.__winners / numOrders) * 100

        return results