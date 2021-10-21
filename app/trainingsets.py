########################################################################################
#    Module to gather and process datasets for training the machine learning model.    #
########################################################################################

import pandas as pd
from SmartTrade.app import constants, configs, datasets
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def score_dataset(ds: pd.DataFrame, timeframe: str) -> None:
    results = {'markers': [], 'dataset': ds}
    pointsInDay = int(constants.TIMEFRAME_MILLISECONDS['1d'] / constants.TIMEFRAME_MILLISECONDS[timeframe])
    lastIndex = len(ds.index) - pointsInDay - 1
    index = 0
    while index <= lastIndex:
        queue = []
        startPrice = ds.iloc[[index]]['open'].iat[0]
        startDate = ds.iloc[[index]]['date'].iat[0]
        highest = startPrice
        lowest = 1000000
        markerFound = False
        shift = 1
        while not markerFound:
            if index + shift + 1 <= lastIndex:
                currentPrice = ds.iloc[[index + shift]]['close'].iat[0]
                currentDate = ds.iloc[[index + shift]]['date'].iat[0]
                if currentPrice > highest:
                    highest = currentPrice
                elif currentPrice < lowest:
                    lowest = currentPrice
                
                if currentPrice == highest and highest != startPrice:
                    if highest >= 1.007 * startPrice:
                        if ds.iloc[[index + shift + 1]]['close'].iat[0] <= 0.993 * currentPrice:
                            results['markers'].append({'date': startDate, 'price': startPrice, 'score': 1})
                            results['markers'].append({'date': currentDate, 'price': currentPrice, 'score': -1})
                            index += shift
                            markerFound = True
                if currentPrice == lowest and lowest != 1000000:
                    if lowest <= 0.993 * startPrice:
                        results['markers'].append({'date': startDate, 'price': startPrice, 'score': -1})
                        index += shift
                        markerFound = True

                shift += 1
            else:
                markerFound = True
        
        index += 1

    plot_results(results)



def plot_results(results):
    buyMarkers = [x for x in results['markers'] if x['score'] == 1]
    sellMarkers = [x for x in results['markers'] if x['score'] == -1]
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=results['dataset']['date'], y=results['dataset']['close'], name="Price", line_color="black"), row=1, col=1)
    fig.add_trace(go.Scatter(
            x=[x['date'] for x in buyMarkers],
            y=[x['price'] for x in buyMarkers],
            mode='markers',
            name='Scores',
            text = "BUY",
            line_color='green'), row=1, col=1)

    fig.add_trace(go.Scatter(
            x=[x['date'] for x in sellMarkers],
            y=[x['price'] for x in sellMarkers],
            mode='markers',
            name='Scores',
            text = "SELL",
            line_color='red'), row=1, col=1)

    fig.show()


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
    ds = datasets.load_dataset('ETH/USDT', '1h', 1602975600000, {'requiredIndicators': ['rsi']})
    score_dataset(ds, '1h')