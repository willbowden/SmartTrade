##################################################################################
#    Module to download, process and retrieve datasets containing price data.    #
##################################################################################

from SmartTrade.server import configs, constants, helpers, exchange_data

import joblib
import pandas as pd
import joblib
import datetime
import numpy as np

def populate_dataset(dataset: pd.DataFrame, indicators) -> pd.DataFrame: # Calculate & add indicators to the dataset.
    for item in indicators: # Iterate over all the required indicators
        indicator_args = item['arguments'] # Collect the arguments for calculation (e.g timeperiod)
        if item['data'] is not ["close"]: # Check if the calculation requires more than just "close" price data.
            indicator_data = [] 
            for required_data in item['data']: # Iterate over all required price data and add it to a list.
                indicator_data.append(dataset[required_data].to_numpy()) # Convert all the OHLCV data to numpy arrays, as that's what ta-lib works with.
            indicator_data = tuple(indicator_data) # Convert that list to a tuple so we can pass it as an argument.
            
            # Unwrap the tuple into individual arguments, and unwrap indicator_args into keyword arguments. Use the..
            #   ..corresponding function to calculate the indicator.  
            result = constants.INDICATOR_FUNCTIONS[item['name']](*indicator_data, **indicator_args)
        else:
            indicator_data = dataset['close'].to_numpy() # Otherwise, only provide close price data and calculate the indicator.
            result = constants.INDICATOR_FUNCTIONS[item['name']](indicator_data, **indicator_args)

        if isinstance(result, tuple): # Some indicators return multiple outputs, so we'll separate them out.
            # Iterate over all the results and add a named column to the dataset to..
            #   ..allow us to identify the output.
            for index, column in enumerate(result): 
                name = f"{item['name']}_{item['output'][index]}"
                dataset.loc[:, name] = column # Add the indicator to the dataset.
        else:
            dataset.loc[:, item['name']] = result 

    return dataset

def dataset_exists(symbol: str, timeframe: str, startDate: int) -> bool: # Check if a dataset exists and if it contains the start date specified by the user.
    okay = True
    fname = helpers.get_dataset_filepath(symbol, timeframe) # As defined above
    startDatePandas = pd.Timestamp(startDate, unit='ms') # Pandas stores timestamps as a unique object, so I'll..
    #  ..have to convert between my integer timestamp and Pandas' format.
    try:
        with open(fname, 'r') as infile: # Attempt to open the file
            dataset = pd.read_json(infile)
            if startDatePandas > dataset['date'][0]: # Check that the start date is included in the dataframe
                return okay
            else:
                okay = False
    except: # If we can't, assume it doesnt exist or doesn't contain the start date.
        okay = False

    return okay


def load_dataset(symbol: str, timeframe: str, startDate: int, config: dict) -> pd.DataFrame: # Load a dataset from a .json file
    startDate = startDate - (5 * constants.TIMEFRAME_MILLISECONDS[timeframe]) # So that the start date is actually included in the data. Prevents errors.
    fname = helpers.get_dataset_filepath(symbol, timeframe) # As defined above
    if dataset_exists(symbol, timeframe, startDate): # If we've already downloaded the dataset for the given symbol, and it includes the start date, load it.
        with open(fname, 'r') as infile:
            datasetWithoutIndicators = pd.read_json(infile) # Read the raw dataset with just OHLCV data (no indicators)
    else: # Otherwise, create a new one
        print(f"Dataset for {symbol} does not exist or does not contain start date! Creating...")
        datasetWithoutIndicators = create_new_dataset(symbol, timeframe, startDate) # Read the raw dataset with just OHLCV data (no indicators)
    # Find the index closest to our startdate.
    indexOfStartDate = np.where(datasetWithoutIndicators['date'] >= pd.to_datetime(startDate, unit='ms'))[0][0] 

    dataset = datasetWithoutIndicators.iloc[indexOfStartDate:] # Select only parts of the dataset from the start date onwards
    dataset = populate_dataset(dataset, config['requiredIndicators']) # Populate the dataset with the required indicators that were provided in the config.
    dataset = dataset.dropna(0) # Remove all rows from the dataset that contain a "Not A Number" value.
    dataset.reset_index(inplace=True, drop=True) # Reset and delete the index.

    return dataset

def save_dataset(symbol: str, timeframe: str, dataset: pd.DataFrame) -> None: # Saves dataset to file.
    fname = helpers.get_dataset_filepath(symbol, timeframe) # As defined above.
    with open(fname, "w") as outfile:
        jsonified = dataset.to_json() # Convert the dataset to json so it can be saved.
        outfile.write(jsonified) # Write our dataset to the file.


def create_new_dataset(symbol: str, timeframe: str, startTimeStamp: int) -> pd.DataFrame:
    newStartTimeStamp = startTimeStamp - (10 * constants.TIMEFRAME_MILLISECONDS[timeframe]) # Set the start timestamp a while before..
    #  ..the requested one so that we can ensure the start time will exist in the dataset.
    dataset = exchange_data.download_historical(symbol, timeframe, newStartTimeStamp) # Get the historical OHLCV data.
    dataset = dataset.dropna(0) # Remove "Not A Number" values from the dataset.
    dataset.reset_index(inplace=True)
    del dataset['index'] # Delete the index
    save_dataset(symbol, timeframe, dataset) # Save the newly created dataset
    return dataset

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")