import os
import constants
import time
import configs
import numpy as np

config = configs.load_config()

def get_symbol_filepath(symbol, timeframe):
    script_dir = os.path.dirname(__file__)
    symbol_filename = symbol.replace("/", "_")
    fname = os.path.join(script_dir, (constants.DEFAULT_DATASET_PATH + symbol_filename + "_" + timeframe + ".json"))
    return fname

def get_ohlcv_filepath(symbol, timeframe):
    script_dir = os.path.dirname(__file__)
    symbol_filename = symbol.replace("/", "_")
    fname = os.path.join(script_dir, (constants.OHLCV_PATH + symbol_filename + "_" + timeframe + ".json"))
    return fname

def generate_model_path(symbol=config['symbol'], timeframe=config['timeframe']):
    model_name = generate_model_name(symbol, timeframe)
    model_path = constants.MODELS_PATH + model_name
    return model_path

def generate_model_name(symbol, timeframe):
    model_name = f"{time.strftime('%Y-%m-%d-%H-%M')}_{symbol}_{timeframe}_lookup_{config['lookup_step']}_dropout_{config['dropout']}_units_{config['units']}_layers_{config['n_layers']}_features_{config['n_features']}_loss_{config['loss']}_optimizer_{config['optimizer']}"
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