####
#
####

from SmartTrade.server import constants
import pandas as pd

class Strategy:
    def __init__(self, name: str, ownerID: int) -> None:
        self.name = name
        self.ownerID = ownerID

    def __load_from_json(self) -> None:
        self.indicators = loaded['indicators']
        self.rules = loaded['rules']

    def save_to_json(self) -> None:
        pass

    def check_buy(self, bot: object, data: pd.DataFrame, index: int, symbol: str) -> None:
        pass

    def check_sell(self, bot: object, data: pd.DataFrame, index: int, symbol: str) -> None:
        pass
