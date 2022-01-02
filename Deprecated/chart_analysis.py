####################################################################################################################
#    Module containing functions that allow us to analyse a price chart, marking key points and chart patterns.    #
####################################################################################################################

from os import close
import pandas as pd

from SmartTrade.server import constants, configs, datasets, chart_plot

def mark_swings(ds: pd.DataFrame, config) -> dict:
    # Mark swing highs and lows on the dataset. I.e points where price movement reverses.
    results = {'markers': [], 'dataset': ds}
    highest = {'date': '', 'price': 0}
    lowest = {'date': '', 'price': 1000000}
    for index, row in ds.iterrows():
        if row['close'] < 0.995 * highest['price'] and highest['price'] != 0 and lowest['price'] != 1000000 and highest['price'] >= config['profit_aim'] * lowest['price']:
            if highest['date'] > lowest['date']:
                results['markers'].append({'date': lowest['date'], 'price': lowest['price'], 'score': 1})
                results['markers'].append({'date': highest['date'], 'price': highest['price'], 'score': -1})
                highest = {'date': '', 'price': 0}
                lowest = {'date': '', 'price': 1000000}
            else:
                highest = {'date': row['date'], 'price': row['close']}

        if row['high'] > highest['price']:
            highest = {'date': row['date'], 'price': row['high']}
        if row['low'] < lowest['price']:
            lowest = {'date': row['date'], 'price': row['low']}

    return results

def mark_structure(ds: dict):
    ds['structures'] = []
    for start in ds['markers']:
        topLimit = (1.01 * start['price'])
        bottomLimit = (0.99 * start['price'])
        closeCount = 1
        lastTestDate = None
        for point in ds['markers']:
            if point['price'] != start['price']:
                if point['price'] <= topLimit and point['price'] >= bottomLimit:
                    closeCount += 1
                    lastTestDate = point['date']

        if closeCount > 4:
            alreadyFoundDates = [x['start'] for x in ds['structures']]
            if start['date'] not in alreadyFoundDates:
                ds['structures'].append({'start': start['date'], 'end': lastTestDate, 'top': topLimit, 'bottom': bottomLimit})
                    
    return ds


if __name__ == "__main__":
    config = {'requiredIndicators': ['rsi'], 'profit_aim': 1.1}
    ds = datasets.load_dataset("ETH/USDT", "4h", 1620777600000,  config)
    swings = mark_swings(ds, config)
    #out = mark_structure(swings)

    chart_plot.plot_swings(swings).show()    
