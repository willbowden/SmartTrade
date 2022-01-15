import hashlib
from SmartTrade.server import constants
import time
import numpy as np

def hash_password(password, salt):
    key = hashlib.pbkdf2_hmac( # Hash the password we received from the client.
            'sha256', # The hashing algorithm
            password.encode('utf-8'), # Convert the password to bytes
            salt,
            100000 # Number of iterations of SHA-256
        )

    combo = key + salt # Combine new hash and old salt for comparison

    return combo

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
    model_name = f"{time.strftime('%Y-%m-%d-%H-%M')}_{symbol}_{config['timeframe']}"
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

def split_letters_and_numbers(inString: str) -> list:
    head = inString.rstrip('0123456789')
    tail = inString[len(head):]
    return [head, tail]