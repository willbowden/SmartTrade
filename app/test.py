
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from SmartTrade.app import datasets, constants

def score_dataset(ds: pd.DataFrame, timeframe: str) -> None:
    results = {'markers': [], 'dataset': ds}
    pointsInDay = int(constants.TIMEFRAME_MILLISECONDS['1d'] / constants.TIMEFRAME_MILLISECONDS[timeframe])
    lastIndex = len(ds.index) - pointsInDay - 1
    index = 0
    shift = 0
    while index + shift <= lastIndex:
        queue = [] # Queue of percentage changes
        openPrice = ds.iloc[[index + shift]]['open'].iat[0]
        openDate = ds.iloc[[index + shift]]['date'].iat[0]
        queue.append({'date': openDate, 'price': openPrice, 'change': 0})
        highestPrice = openPrice
        lowestPrice = 100000
        for i in range(pointsInDay):
            if index + i + shift <= lastIndex:
                shift += 1
                currentPrice = ds.iloc[[index + shift + i]]['close'].iat[0]
                currentDate = ds.iloc[[index + shift + i]]['date'].iat[0]
                if currentPrice > highestPrice:
                    highestPrice = currentPrice
                    if currentPrice >= 1.007 * openPrice:
                        queue.append({'date': currentDate, 'price': currentPrice, 'change': 1})
                    else:
                        queue.append({'date': currentDate, 'price': currentPrice, 'change': 0})
                elif currentPrice < highestPrice:
                    if currentPrice < lowestPrice:
                        lowestPrice = currentPrice
                    if currentPrice <= 0.995 * highestPrice and highestPrice != openPrice:
                        queue.append({'date': currentDate, 'price': currentPrice, 'change': -1})
                    else:
                        queue.append({'date': currentDate, 'price': currentPrice, 'change': 0})

        upPrices = [x['price'] for x in queue if x['change'] == 1]
        if upPrices == []:
            highestUpPrice = 0
        else:
            highestUpPrice = max(upPrices)
        downPrices = [x['price'] for x in queue if x['change'] == -1]
        if downPrices == []:
            lowestDownPrice = 0
        else:
            lowestDownPrice = min(downPrices)
        prices = [x['price'] for x in queue]
        dates = [x['date'] for x in queue]
        for j in range(len(prices)):
            if prices[j] == highestUpPrice:
                results['markers'].append({'date': dates[j], 'price': prices[j], 'score': 1})
            elif prices[j] == lowestDownPrice:
                results['markers'].append({'date': dates[j], 'price': prices[j], 'score': -1})

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


if __name__ == '__main__':
    ds = datasets.load_dataset('ETH/USDT', '1h', 1602975600000, {'requiredIndicators': ['rsi']})
    score_dataset(ds, '1h')