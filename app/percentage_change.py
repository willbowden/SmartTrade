#################################################################################################################
#    Module for calculating the daily percentage changes that an asset makes and the average highs and lows.    #
#################################################################################################################

import pandas as pd
from SmartTrade.app import constants, configs, datasets
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculte_percentage_changes(dataset: pd.DataFrame, timeframe: str) -> dict:
    pointsInDay = constants.TIMEFRAME_MILLISECONDS['1d'] / constants.TIMEFRAME_MILLISECONDS[timeframe]
    pointsInDay = int(pointsInDay)
    results = {'dates': [], 'percentageChanges': [], 'highs': [], 'lows': [], 'highest': 0, 'lowest': 0, 'smallestHigh': 1000000, 'smallestLow': -1000000}
    for index, row in dataset.iterrows():
        if index >= pointsInDay:
            results['dates'].append(row['date'])
            current = row['open']
            change = ((dataset.iloc[[index - pointsInDay]]['close'].iat[0] - current) / current) * 100
            results['percentageChanges'].append(change)
            highestDaily = 0
            lowestDaily = 0
            for i in range(pointsInDay):
                newHigh = ((dataset.iloc[[index - i]]['high'].iat[0] - current) / current) * 100
                newLow = ((dataset.iloc[[index - i]]['low'].iat[0] - current) / current) * 100
                if newHigh > highestDaily:
                    highestDaily = newHigh
                if newLow < lowestDaily:
                    lowestDaily = newLow

            results['highs'].append(highestDaily)
            results['lows'].append(lowestDaily)

            if highestDaily > results['highest']:
                results['highest'] = highestDaily
            if results['lowest'] > lowestDaily:
                results['lowest'] = lowestDaily
            if lowestDaily > results['smallestLow']:
                results['smallestLow'] = change
            if highestDaily < results['smallestHigh']:
                results['smallestHigh'] = change

    avgChange = sum(results['percentageChanges']) / len(results['percentageChanges'])
    avgHigh = sum(results['highs']) / len(results['highs'])
    avgLow = sum(results['lows']) / len(results['lows'])
    results['avgHigh'] = avgHigh
    results['avgLow'] = avgLow
    results['avgChange'] = avgChange

    print(f"Highest Change: %{results['highest']}. Lowest Change: %{results['lowest']}. Avg High: %{results['avgHigh']}. Avg Low: %{results['avgLow']}. Average Change: %{results['avgChange']}")
    
    plot_percentage_changes(results)


def plot_percentage_changes(ds):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=ds['dates'],
        y=ds['percentageChanges'],
        name="Daily PNL",
        mode="lines",
        line_color="red"),
        row=1, col=1)
    fig.add_trace(go.Scatter(
        x=ds['dates'],
        y=ds['highs'],
        name='Highest Change In 24hrs from this point',
        mode='markers',
        line_color="green"), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=ds['dates'],
        y=ds['lows'],
        name='Lows Change In 24hrs from this point',
        mode='markers',
        line_color="red"), row=1, col=1)

    fig.show()