########################################################################################
#    Module to gather and process datasets for training the machine learning model.    #
########################################################################################

import pandas as pd
import numpy as np
from SmartTrade.app import constants, configs, datasets
import plotly.graph_objects as go
from collections import deque

def plot_scores(results):
    buyMarkers = [x for x in results['markers'] if x['score'] == 1]
    sellMarkers = [x for x in results['markers'] if x['score'] == -1]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=results['dataset']['date'],
     open=results['dataset']['open'],
     high=results['dataset']['high'],
     low=results['dataset']['low'],
     close=results['dataset']['close'],
     name="Price"))

    fig.add_trace(go.Scatter(x=results['dataset']['date'],
     y=results['dataset']['close'],
     mode='markers',
     name="Score",
     text=results['dataset']['score']))

    # fig.add_trace(go.Scatter(
    #         x=[x['date'] for x in buyMarkers],
    #         y=[x['price'] for x in buyMarkers],
    #         mode='markers',
    #         name='Scores',
    #         text = "BUY",
    #         line_color='yellow'))

    # fig.add_trace(go.Scatter(
    #         x=[x['date'] for x in sellMarkers],
    #         y=[x['price'] for x in sellMarkers],
    #         mode='markers',
    #         name='Scores',
    #         text = "SELL",
    #         line_color='purple'))

    fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)

    fig.show()

def score_dataset(ds: pd.DataFrame, config) -> dict:
    results = {'markers': [], 'dataset': ds}
    scores = []
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
    
    scoredBuys = [x['date'] for x in results['markers'] if x['score'] == 1]
    scoredSells = [x['date'] for x in results['markers'] if x['score'] == -1]
    numMarkers = len(scoredBuys)
    padding = 0
    for index, row in ds.iterrows():
        if row['date'] in scoredBuys or row['date'] in scoredSells:
            break
        else:
            padding += 1

    scores += [0 for x in range(padding)]
    for i in range(numMarkers):
        timeDifference = int(pd.Timedelta(scoredSells[i] - scoredBuys[i]).seconds / (constants.TIMEFRAME_MILLISECONDS[config['timeframe']] / 1000))
        print(timeDifference)
        if timeDifference % 2 == 0:
            startScore = 1
            halfNumber = int(timeDifference / 2)
            for j in range(halfNumber):
                scores.append(startScore - (j * 0.15))
            endScore = -1 + (halfNumber * 0.15)
            for k in range(halfNumber):
                scores.append(endScore - (k * 0.15))
        elif timeDifference % 2 != 0:
            startScore = 1
            halfNumber = int((timeDifference+1) / 2)
            for j in range(halfNumber):
                scores.append(startScore - (j * 0.15))
            endScore = -1 + (halfNumber * 0.15)
            for k in range(halfNumber):
                scores.append(endScore - (k * 0.15))

    results['dataset']['score'] = scores

    return results

def create_sequences(ds, config):
    sequence_data = [] # Separate the dataset into sets of (50 sets of n features, one score target)
    sequences = deque(maxlen=config['sequence_length'])
    for entry, target in zip(ds.iloc[:, :-1].values, ds['score'].values):
        sequences.append(entry)
        if len(sequences) == config['sequence_length']:
            sequence_data.append([np.array(sequences), target])
    x, y = [], []
    for seq, target in sequence_data:
        x.append(seq)
        y.append(target)
    
    x = np.array(x)
    y = np.array(y)

    return x, y

def score_and_condense_datasets(ds, config):
    total = {}
    for symbol in config['training_symbols']:
        scoredDataset = score_dataset(ds[symbol], config)['dataset']
        plot_scores(score_dataset(ds[symbol]))
        splitDataset = split_train_and_test(scoredDataset, config)
        for key in splitDataset.keys():
            try:
                total[key] = total[key].append(splitDataset[key])
            except:
                total[key] = splitDataset[key]

    return total

def split_train_and_test(ds, config):
    result = {}
    result['originalDS'] = ds
    result['date'] = ds['date'] # Save the dates separately
    ds = ds[config['feature_columns']] # Extract only the desired features (as well as "Scores")
    result['ds'] = ds # Save this whole dataset separately for score usage

    x, y = create_sequences(ds, config)
    result['x'] = x
    result['y'] = y
    
    if config['split_dataset']:
        train_samples = int((1 - config['test_ratio']) * len(x)) # Divide into test and train sets by ratio in config.json
        result['xTrain'] = x[:train_samples]
        result['yTrain'] = y[:train_samples]
        result['xTest'] = x[train_samples:]
        result['testDates'] = result['date'][train_samples:]
        result['testClose'] = result['originalDS']['close'][train_samples:]
        result['yTest'] = y[train_samples:]
    else:
        result['xTest'] = x
        result['yTest'] = y
        result['testDates'] = result['date']

    return result

def gather_datasets(symbols: list, timeframe: str, startDate: int, modelConfig: dict) -> pd.DataFrame:
    config = {'requiredIndicators': modelConfig['trainingset_indicators']}
    total = {}
    for symbol in symbols:
        total[symbol] = datasets.load_dataset(symbol, timeframe, startDate, config)

    return total

def create_training_set(modelName: str, startDate: int):
    config = configs.load_ai_config(modelName)
    ds = gather_datasets(config['training_symbols'], config['timeframe'], startDate, config) # Get data from multiple symbols
    total = score_and_condense_datasets(ds, config)

    return total
    
if __name__ == '__main__':
    create_training_set('testModel', 1603407600000)