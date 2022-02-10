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
        self.__load_from_json(data)

    def __load_from_json(self, data=None) -> None:
        if data is None:
            with open(f"{constants.STRATEGY_PATH}{self.ownerID}_{self.name.replace(' ', '_')}.json") as infile:
                loaded = json.load(infile)
        self.indicators = loaded['indicators']
        self.rules = loaded['rules']

    def save_to_json(self) -> None:
        pass

    def check_buy(self, bot: object, data: pd.DataFrame, index: int, symbol: str) -> None:
        pass

    def check_sell(self, bot: object, data: pd.DataFrame, index: int, symbol: str) -> None:
        pass
