##################################################################################
#    Module to download, process and retrieve datasets containing price data.    #
##################################################################################

from SmartTrade.server import constants, helpers, dbmanager
from SmartTrade.server.user import User

import talib
import pandas as pd
import json
import numpy as np

def populate_dataset(dataset: pd.DataFrame, indicators) -> pd.DataFrame: # Calculate & add indicators to the dataset.
    overlaps = ['ma', 'ema']
    with open(constants.DEFAULT_INDICATORS, 'r') as infile: # Load default indicators from file
        defaultIndicators = json.load(infile)

    for item in indicators: # Iterate over all the required indicators
        if type(item) == str: # If we've just been given the name of an indicator, load its default info
            item = defaultIndicators[item]
            
        indicator_args = item['arguments'] # Collect the arguments for calculation (e.g timeperiod)
        if item['data'] is not ["close"]: # Check if the calculation requires more than just "close" price data.
            indicator_data = [] 
            for required_data in item['data']: # Iterate over all required price data and add it to a list.
                indicator_data.append(dataset[required_data].to_numpy()) # Convert all the OHLCV data to numpy arrays, as that's what ta-lib works with.
            indicator_data = tuple(indicator_data) # Convert that list to a tuple so we can pass it as an argument.
            
            # Unwrap the tuple into individual arguments, and unwrap indicator_args into keyword arguments. Use the..
            #   ..corresponding function to calculate the indicator.  
            func = getattr(talib, item['name'].upper())
            result = func(*indicator_data, **indicator_args)
        else:
            indicator_data = dataset['close'].to_numpy() # Otherwise, only provide close price data and calculate the indicator.
            func = getattr(talib, item['name'].upper())
            result = func(indicator_data, **indicator_args)

        if isinstance(result, tuple): # Some indicators return multiple outputs, so we'll separate them out.
            # Iterate over all the results and add a named column to the dataset to..
            #   ..allow us to identify the output.
            for index, column in enumerate(result):                     
                name = f"{item['name']}_{item['output'][index]}"
                if item['name'] in overlaps:
                    name += f"_{indicator_args['timeperiod']}"
                dataset.loc[:, name] = column # Add the indicator to the dataset.
        else:
            name = f"{item['name']}_{item['name']}"
            if item['name'] in overlaps:
                name += f"_{indicator_args['timeperiod']}"
            dataset.loc[:, name] = result 

    return dataset

def dataset_exists(symbol: str, timeframe: str, startDate: int) -> bool: # Check if a dataset exists and if it contains the start date specified by the user.
    fname = helpers.get_dataset_filepath(symbol, timeframe) # As defined above
    startDatePandas = pd.Timestamp(startDate, unit='ms') # Pandas stores timestamps as a unique object, so I'll..
    #  ..have to convert between my integer timestamp and Pandas' format.
    try:
        with open(fname, 'r') as infile: # Attempt to open the file
            dataset = pd.read_json(infile)
            searchForStartDate = np.where(dataset['timestamp'] >= startDatePandas)[0]
            if len(searchForStartDate) > 0: # Check that the start date is included in the dataframe
                return True, None
            else:
                return False, dataset['timestamp'].iat[0] # Return the earliest date in the dataset so we can append it.
    except: # If we can't, assume it doesnt exist or doesn't contain the start date.
        return False, None


# def modify_candles(dataframe, candleType) -> pd.DataFrame:
#     if candleType == 'heikin_ashi':
#         newDataframe = dataframe.apply(lambda x: (x['open'] + x['high'] + x['low'] + x['close']) / 4 if x.name == 'close' else x, axis=1)
#         newOpen = []
#         for i in range(len(newDataframe['open'])):
#             if i == 0:
#                 newOpen.append(newDataframe['open'].iat[i])
#             else:
#                 newOpen.append(((newOpen[i-1] + newDataframe['close'].iat[i-1]) / 2))

#         newDataframe['open'] = newOpen
#         newDataframe = newDataframe.apply(lambda x: max(x['open'], x['high'], x['low'], x['close']) if x.name == 'high' else x, axis=1)
#         newDataframe = newDataframe.apply(lambda x: min(x['open'], x['high'], x['low'], x['close']) if x.name == 'low' else x, axis=1)
#         print(newDataframe)
#         exit() 


def load_dataset(user, symbol: str, timeframe: str, startDate: int, requiredIndicators: dict) -> pd.DataFrame: # Load a dataset from a .json file
    startDate = startDate - (10 * constants.TIMEFRAME_MILLISECONDS[timeframe]) # So that the start date is actually included in the data. Prevents errors.
    fname = helpers.get_dataset_filepath(symbol, timeframe) # As defined above
    datasetExists = dataset_exists(symbol, timeframe, startDate)
    if datasetExists[0]: # If we've already downloaded the dataset for the given symbol, and it includes the start date, load it.
        with open(fname, 'r') as infile:
            datasetWithoutIndicators = pd.read_json(infile) # Read the raw dataset with just OHLCV data (no indicators)
    else: # Otherwise, create a new one
        print(f"Dataset for {symbol} does not exist or does not contain start date! Creating...")
        if datasetExists[1] is not None:
            startDate = datasetExists[1]
        datasetWithoutIndicators = create_new_dataset(user, symbol, timeframe, startDate) # Read the raw dataset with just OHLCV data (no indicators)
        datasetWithoutIndicators.loc[:, 'timestamp'] = pd.to_datetime(datasetWithoutIndicators['timestamp'], unit="ms")
    # Find the index closest to our startdate.
    searchForStartDate = np.where(datasetWithoutIndicators['timestamp'] >= pd.to_datetime(startDate, unit='ms'))[0]

    if len(searchForStartDate) > 0:
        indexOfStartDate = searchForStartDate[0]
    else:
        indexOfStartDate = 0

    dataset = datasetWithoutIndicators.iloc[indexOfStartDate:] # Select only parts of the dataset from the start date onwards

    dataset = populate_dataset(dataset, requiredIndicators ) # Populate the dataset with the required indicators that were provided in the config.
    dataset = dataset.dropna() # Remove all rows from the dataset that contain a "Not A Number" value.
    dataset.reset_index(inplace=True, drop=True) # Reset and delete the index.
    dataset = dataset.drop_duplicates()

    return dataset

def save_dataset(symbol: str, timeframe: str, dataset: pd.DataFrame) -> None: # Saves dataset to file.
    fname = helpers.get_dataset_filepath(symbol, timeframe) # As defined above.
    with open(fname, "w") as outfile:
        jsonified = dataset.to_json() # Convert the dataset to json so it can be saved.
        outfile.write(jsonified) # Write our dataset to the file.


def create_new_dataset(user, symbol: str, timeframe: str, startTimeStamp: int) -> pd.DataFrame:
    newStartTimeStamp = startTimeStamp - (10 * constants.TIMEFRAME_MILLISECONDS[timeframe]) # Set the start timestamp a while before..
    #  ..the requested one so that we can ensure the start time will exist in the dataset.
    dataset = user.exchange.fetch_ohlcv(symbol, timeframe, newStartTimeStamp) # Get the historical OHLCV data.
    dataset = dataset.dropna(0) # Remove "Not A Number" values from the dataset.
    dataset.reset_index(inplace=True)
    del dataset['index'] # Delete the index
    save_dataset(symbol, timeframe, dataset) # Save the newly created dataset
    return dataset

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")