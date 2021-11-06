import json
from SmartTrade.server import constants

def load_config(strategyName: str, userID: int) -> dict:
    filename = constants.CONFIG_PATH + str(userID) + "_" + strategyName.replace(" ", "_") + ".json"
    try: 
        with open(filename, "r") as infile:
            config = json.load(infile)
            return config
    except:
        raise FileNotFoundError

def load_ai_config(modelName: str) -> dict:
    filename = constants.MODELS_PATH + modelName.replace(" ", "_") + ".json"
    try: 
        with open(filename, "r") as infile:
            config = json.load(infile)
            return config
    except:
        print(f"No config for {modelName} exists!")
        raise FileNotFoundError

def save_config(config, filename):
    with open(filename, "w") as outfile:
        json.dump(config, outfile)
