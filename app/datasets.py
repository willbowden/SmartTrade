##################################################################################
#    Module to download, process and retrieve datasets containing price data.    #
##################################################################################

from SmartTrade.app import configs, constants, helpers, exchange_data

import joblib
import pandas as pd
import joblib
import datetime


def load_dataset(symbol: str, timeframe: str, startDate: int, config: dict) -> pd.DataFrame: 
    fname = helpers.get_dataset_filepath(symbol, timeframe)
    if dataset_exists(symbol, timeframe, startDate):
        with open(fname, 'r') as infile:
            dataset = pd.read_json(infile)
    else:
        print(f"Dataset for {symbol} does not exist or does not contain start date! Creating...")
        create_new_dataset(symbol, timeframe, startDate, config)
    return dataset

def save_dataset(symbol: str, timeframe: str, dataset: pd.DataFrame): # Saves dataset to file
    fname = helpers.get_symbol_filepath(symbol, timeframe)
    with open(fname, "w") as outfile:
        jsonified = dataset.to_json()
        outfile.write(jsonified)

def populate_dataset(dataset: pd.DataFrame, indicators) -> pd.DataFrame:
    open_data = dataset['open'].to_numpy()
    high = dataset['high'].to_numpy()
    low = dataset['high'].to_numpy()
    close = dataset['close'].to_numpy()
    volume = dataset['volume'].to_numpy()
    to_calculate = indicators
    for item in to_calculate:
        if item in constants.INDICATORS_REQUIRED_DATA.keys():
            indicator_args = []
            for letter in constants.INDICATORS_REQUIRED_DATA[item]:
                if letter == "o":
                    indicator_args.append(open_data)
                elif letter == "h":
                    indicator_args.append(high)
                elif letter == "l":
                    indicator_args.append(low)
                elif letter == "c":
                    indicator_args.append(close)
                elif letter == "v":
                    indicator_args.append(volume)
            indicator_args = tuple(indicator_args)
            result = constants.INDICATOR_FUNCTIONS[item](*indicator_args)
        else:
            indicator_args = close
            result = constants.INDICATOR_FUNCTIONS[item](indicator_args)

        if isinstance(result, tuple):
            j = 0
            for column in result:
                if j == 0:
                    name = item
                else:
                    name = item + str(j)
                dataset[name] = column
                j += 1
        else:
            dataset[item] = result
    return dataset


def calculate_futures(dataset: pd.DataFrame, config: dict) -> pd.DataFrame:
    futures = []
    datasetLength = len(dataset.index)
    for index, row in dataset.iterrows():
        if index <= datasetLength - config['lookup_step']:
            futureIndex = (index + config['lookup_step']) - 1
            futures.append(dataset.at[futureIndex, 'close'])
        else:
            futures.append(None)
    dataset['future'] = futures
    return dataset

def dataset_exists(symbol: str, timeframe: str, startDate: int) -> bool: # Check if a dataset exists and if it contains the start date specified by the user.
    okay = True
    fname = helpers.get_dataset_filepath(symbol, timeframe)
    try:
        with open(fname, 'r') as infile:
            dataset = pd.read_json(infile)
            if startDate in dataset['date']:
                return okay
            else:
                okay = False
    except:
        okay = False

    return okay


def create_new_dataset(symbol: str, timeframe: str, starttimestamp: int, config: dict) -> pd.DataFrame:
    ohlcv = exchange_data.download_historical(symbol, timeframe, starttimestamp)
    dataset = populate_dataset(ohlcv)
    dataset = calculate_futures(dataset, config)
    dataset = dataset.dropna(0)
    dataset.reset_index(inplace=True)
    del dataset['index']
    save_dataset(symbol, timeframe, dataset)

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")