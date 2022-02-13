####
#
####

from SmartTrade.server import constants, bot
import json
import pandas as pd

class Strategy:
    def __init__(self, name: str, ownerID: int, data=None) -> None:
        self.name = name
        self.ownerID = ownerID
        self._fileName = f"{constants.STRATEGY_PATH}{self.ownerID}_{self.name.replace(' ', '_')}.json"
        self.__load_from_json(data)

    def __load_from_json(self, data=None) -> None:
        # Load an already saved strategy.
        if data is None:
            with open(self._fileName, 'r') as infile:
                loaded = json.load(infile)
        else:
            loaded = data

        self.__indicators = loaded['indicators']
        self.__startingBalance = loaded['startingBalance']
        self.__rules = loaded['rules']
        self.__positionSize = loaded['positionSize']

    def get_starting_balance(self) -> float: # Getters
        return self.__startingBalance

    def get_indicators(self) -> list:
        return self.__indicators

    def save_to_json(self) -> None:
        # Save all important data to a JSON file.
        asDict = {
            'name': self.name,
            'ownerID': self.ownerID,
            'indicators': self.__indicators,
            'rules': self.__rules,
            'startingBalance': self.__startingBalance,
            'positionSize': self.__positionSize
        }

        with open(self._fileName, 'w') as outfile:
            json.dump(asDict, outfile)

    def check_buy(self, bot: bot.Bot, data: pd.DataFrame, index: int, symbol: str) -> None:
        valid = True
        for rule in self.__rules['buy']: # Check all of the buy rules
            if not self.__check_rule(data, index, rule):
                valid = False

        if valid:
            # Place an order, buying as much as the __positionSize can afford.
            bot.place_order('buy', (self.__positionSize / data['close'].iat[index], data['close'].iat[index], data['timestamp'].iat[index]))
            
    def check_sell(self, bot: bot.Bot, data: pd.DataFrame, index: int, symbol: str) -> None:
        valid = True
        for rule in self.__rules['sell']: # Check all of the sell rules
            if not self.__check_rule(data, index, rule):
                valid = False

        if valid:
            # Place an order, selling the bot's entire position.
            bot.place_order('sell', bot.assetHoldings[symbol].balance, data['close'].iat[index], data['timestamp'].iat[index])

    def __check_rule(self, data: pd.DataFrame, index: int, rule: list) -> bool:
        first = data[rule[0]].iat[index]
        second = data[rule[2]].iat[index]
        # An ugly method for checking all the possible comparisons, but it works.
        if rule[1] == 'crossup' or rule[1] == 'crossdown':
            return self.__check_crossover(rule[1], data, index, rule)
        elif rule[1] == "==":
            return first == second
        elif rule[1] == ">":
            return first > second
        elif rule[1] == "<":
            return first < second
        elif rule[1] == ">=":
            return first >= second
        elif rule[1] == "<=":
            return first <= second
        elif rule[1] == "!=":
            return first != second
        else:
            return False

    def __check_crossover(self, direction: str, data: pd.DataFrame, index: int, rule: list) -> bool:
        # For a crossover to occur, one value has to be below/above another value in one time step,
        #   and then be on the opposite side the following timestep. This method checks for that.
        if index <= 0: 
            return False
        if direction == 'crossup':
            if data[rule[0]].iat[index-1] <= data[rule[2]].iat[index-1]:
                if data[rule[0]].iat[index] > data[rule[2]].iat[index]:
                    return True
        elif direction == 'crossdown':
            if data[rule[0]].iat[index-1] >= data[rule[2]].iat[index-1]:
                if data[rule[0]].iat[index] < data[rule[2]].iat[index]:
                    return True

        return False

