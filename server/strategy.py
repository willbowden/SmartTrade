####
#
####

from SmartTrade.server import constants
import json
import pandas as pd

class Strategy:
    def __init__(self, name: str, ownerID: int, data=None) -> None:
        self.name = name
        self.ownerID = ownerID
        self._fileName = f"{constants.STRATEGY_PATH}{self.ownerID}_{self.name.replace(' ', '_')}.json"
        self.__load_from_json(data)

    def __load_from_json(self, data=None) -> None:
        if data is None:
            with open(self._fileName, 'r') as infile:
                loaded = json.load(infile)
        self.indicators = loaded['indicators']
        self.startingBalance = loaded['startingBalance']
        self.rules = loaded['rules']

    def save_to_json(self) -> None:
        asDict = {
            'indicators': self.indicators,
            'rules': self.rules,
            'startingBalance': self.startingBalance
        }

        with open(self._fileName, 'w') as outfile:
            json.dump(asDict, outfile)

    def check_buy(self, bot: object, data: pd.DataFrame, index: int, symbol: str) -> None:
        raise NotImplementedError
            
    def check_sell(self, bot: object, data: pd.DataFrame, index: int, symbol: str) -> None:
        raise NotImplementedError

    def __check_rule(data: pd.DataFrame, index: int, rule: list) -> bool:
        raise NotImplementedError
