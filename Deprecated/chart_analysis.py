####################################################################################################################
#    Module containing functions that allow us to analyse a price chart, marking key points and chart patterns.    #
####################################################################################################################

import pandas as pd

from SmartTrade.server import datasets, user, dbmanager
import chart_plot

def mark_swings(ds: pd.DataFrame, config) -> dict:
    # Mark swing highs and lows on the dataset. I.e points where price movement reverses.
    results = {'markers': [], 'dataset': ds}
    highest = {'timestamp': '', 'price': 0}
    lowest = {'timestamp': '', 'price': 1000000}
    for index, row in ds.iterrows():
        if row['close'] < 0.995 * highest['price'] and highest['price'] != 0 and lowest['price'] != 1000000 and highest['price'] >= config['profit_aim'] * lowest['price']:
            if highest['timestamp'] > lowest['timestamp']:
                results['markers'].append({'timestamp': lowest['timestamp'], 'price': lowest['price'], 'score': 1})
                results['markers'].append({'timestamp': highest['timestamp'], 'price': highest['price'], 'score': -1})
                highest = {'timestamp': '', 'price': 0}
                lowest = {'timestamp': '', 'price': 1000000}
            else:
                highest = {'timestamp': row['timestamp'], 'price': row['close']}

        if row['high'] > highest['price']:
            highest = {'timestamp': row['timestamp'], 'price': row['high']}
        if row['low'] < lowest['price']:
            lowest = {'timestamp': row['timestamp'], 'price': row['low']}

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
                    lastTestDate = point['timestamp']

        if closeCount > 4:
            alreadyFoundDates = [x['start'] for x in ds['structures']]
            if start['timestamp'] not in alreadyFoundDates:
                ds['structures'].append({'start': start['timestamp'], 'end': lastTestDate, 'top': topLimit, 'bottom': bottomLimit})
                    
    return ds


if __name__ == "__main__":
    u = user.User(dbmanager.get_row_by_column('tblUsers', 'userID', '2094'))
    config = {'requiredIndicators': ['rsi'], 'profit_aim': 1.05, 'candleType': 'candles'}
    ds = datasets.load_dataset(u, "ETH/USDT", "1h", 1620777600000,  config)
    swings = mark_swings(ds, config)
    #out = mark_structure(swings)

    chart_plot.plot_swings(swings).show()    
