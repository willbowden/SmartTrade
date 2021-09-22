import json
from SmartTrade.app import constants

def load_config(filename = constants.DEFAULT_CONFIG_PATH):
    with open(filename, "r") as infile:
        config = json.load(infile)
        return config

def save_config(config, filename):
    with open(filename, "w") as outfile:
        json.dump(config, outfile)
