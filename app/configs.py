import json
from SmartTrade.app import constants

def load_config(strategyName: str, userID: int):
    filename = constants.CONFIG_PATH + str(userID) + "_" + strategyName.replace(" ", "_")
    try: 
        with open(filename, "r") as infile:
            config = json.load(infile)
            return config
    except:
        raise FileNotFoundError

def save_config(config, filename):
    with open(filename, "w") as outfile:
        json.dump(config, outfile)
