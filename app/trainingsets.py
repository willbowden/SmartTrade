########################################################################################
#    Module to gather and process datasets for training the machine learning model.    #
########################################################################################

import pandas as pd
from SmartTrade.app import constants, configs, datasets
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def score_dataset(ds: pd.DataFrame, timeframe: str) -> None:
    results = {'dates': [], 'scores': []}
    pointsInDay = int(constants.TIMEFRAME_MILLISECONDS['1d'] / constants.TIMEFRAME_MILLISECONDS[timeframe])
    lastIndex = len(ds.index) - pointsInDay
    for index, row in ds.iterrows():
        offset = 0
        if index <= lastIndex:
            candleCount = 1
            currentPrice = row['open']
            for i in range(pointsInDay):
                
                pass


def create_training_set():
    pass

def gather_datasets(symbols: list, timeframe: str, startDate: int) -> pd.DataFrame:
    config = {'requiredIndicators': constants.TRAININGSET_INDICATORS}
    total = {}
    for symbol in symbols:
        total[symbol] = {}
        total[symbol]['dataset'] = datasets.load_dataset(symbol, timeframe, startDate, config)
        total[symbol]['dates'] = total[symbol]['dataset']['date']

    return total

if __name__ == '__main__':
    ds = gather_datasets(['ETH/USDT'], '1h', 1618873200000)