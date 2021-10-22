########################################################################################
#    Module to gather and process datasets for training the machine learning model.    #
########################################################################################

import pandas as pd
from SmartTrade.app import constants, configs, datasets
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def score_dataset(ds: pd.DataFrame) -> None:
    results = {'markers': [], 'dataset': ds}
    highest = {'date': '', 'price': 0}
    lowest = {'date': '', 'price': 1000000}
    for index, row in ds.iterrows():
        if row['close'] < 0.995 * highest['price'] and highest['price'] != 0 and lowest['price'] != 1000000 and highest['price'] >= 1.007 * lowest['price']:
            if highest['date'] > lowest['date']:
                results['markers'].append({'date': lowest['date'], 'price': lowest['price'], 'score': 1})
                results['markers'].append({'date': highest['date'], 'price': highest['price'], 'score': -1})
                highest = {'date': '', 'price': 0}
                lowest = {'date': '', 'price': 1000000}
            else:
                highest = {'date': row['date'], 'price': row['close']}

        if row['close'] > highest['price']:
            highest = {'date': row['date'], 'price': row['close']}
        if row['close'] < lowest['price']:
            lowest = {'date': row['date'], 'price': row['close']}

    
    plot_results(results)


def plot_results(results):
    totalPnl = 1.0
    buyMarkers = [x for x in results['markers'] if x['score'] == 1]
    sellMarkers = [x for x in results['markers'] if x['score'] == -1]
    for i in range(len(sellMarkers)):
        change = sellMarkers[i]['price'] / buyMarkers[i]['price']
        totalPnl *= change
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=results['dataset']['date'],
     open=results['dataset']['open'],
     high=results['dataset']['high'],
     low=results['dataset']['low'],
     close=results['dataset']['close'],
     name="Price"))
    fig.add_trace(go.Scatter(
            x=[x['date'] for x in buyMarkers],
            y=[x['price'] for x in buyMarkers],
            mode='markers',
            name='Scores',
            text = "BUY",
            line_color='yellow'))

    fig.add_trace(go.Scatter(
            x=[x['date'] for x in sellMarkers],
            y=[x['price'] for x in sellMarkers],
            mode='markers',
            name='Scores',
            text = "SELL",
            line_color='purple'))

    fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)

    print(f"Total change if following markers: %{round(totalPnl*100, 2)}")
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
    ds = datasets.load_dataset('ADA/USDT', '1h', 1602975600000, {'requiredIndicators': ['rsi']})
    score_dataset(ds)