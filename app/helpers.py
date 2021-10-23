import os
import constants
import time
import numpy as np

def get_user_filepath(userID):
    fname = constants.USER_ACCOUNT_PATH + str(userID) + "_values.json"
    return fname

def get_dataset_filepath(symbol, timeframe):
    symbol_filename = symbol.replace("/", "_")
    fname = constants.DATASET_PATH + symbol_filename + "_" + timeframe + ".json"
    return fname

def get_model_path(symbol, config):
    model_name = generate_model_name(symbol, config)
    model_path = constants.MODELS_PATH + model_name
    return model_path

def generate_model_name(symbol, config):
    model_name = f"{time.strftime('%Y-%m-%d-%H-%M')}_{symbol}_{config['timeframe']}_lookup_{config['lookup_step']}_dropout_{config['dropout']}_units_{config['units']}_layers_{config['n_layers']}_features_{config['n_features']}_loss_{config['loss']}_optimizer_{config['optimizer']}"
    return model_name

def shift_array(array, value, filler):
    e = np.empty_like(array)
    if value >= 0:
        e[:value] = filler
        e[value:] = array[:-value]
    else:
        e[value:] = filler
        e[:value] = array[-value:]
    return e
        
def money_round(value):
    new = round(value, 2)
    if new > value:
        new -= 0.01
    return new