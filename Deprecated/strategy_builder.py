#########################################################################
#    Module for converting JSON strings in to python strategy files.    #
#########################################################################

from SmartTrade.server import constants

def build(jsonData, strategyName) -> None:
    pyString = "def check_buy(bot, data, index, symbol):\n"
    pyString += __build_conditions(jsonData['buy'], 'buy')
    pyString += "\n\ndef check_sell(bot, data, index, symbol):\n"
    pyString += __build_conditions(jsonData['sell'], 'sell')
    
    with open(constants.STRATEGY_PATH + strategyName + ".py", 'w') as outfile:
        outfile.write(pyString)

    print("Finished Successfully.")

def __build_conditions(rawString, side) -> str:
    outString = "" + constants.INDENT
    splitString = rawString.split(" ")
    quantityBoughtOrSold = splitString.pop(-1)
    if len(splitString) // 3 > 1:
        for i in range(0, len(splitString), 3):
            comparison = __construct_comparison(splitString[i], splitString[i+1], splitString[i+2])
            if i != len(splitString) - 3:
                outString += comparison
                outString += constants.INDENT * ((i // 3) + 2)
            else:
                outString += comparison
                outString += constants.INDENT * ((i // 3) + 2)
                outString += f"bot.place_order('{side}')"
    else:
        comparison = __construct_comparison(splitString[0], splitString[1], splitString[2])
        outString += comparison
        outString += constants.INDENT * 2
        if side == "buy":
            outString += f"bot.place_order('{side}', ({quantityBoughtOrSold}*bot.balance)/data['close'].iat[index], {quantityBoughtOrSold}*bot.balance, data['close'].iat[index], data['date'].iat[index])"
        elif side == "sell":
            outString += f"bot.place_order('{side}', ({quantityBoughtOrSold}*bot.assetHoldings[symbol]['balance']), ({quantityBoughtOrSold}*bot.assetHoldings[symbol]['balance']*data['close'].iat[index]), data['close'].iat[index], data['date'].iat[index])"

    return outString

def __construct_comparison(indicator, comparator, value) -> str:
    if comparator not in constants.CUSTOM_COMPARATORS:
        outString = f"if data['{indicator}'].iat[index] "
        outString += f"{comparator} {value}:\n"
    elif comparator == "wre":
        outString = f"if {__within_range_excluding(value, indicator)}:\n"
    elif comparator == "wri":
        outString = f"if {__within_range_including(value, indicator)}:\n"

    return outString

def __within_range_excluding(valueString, indicator) -> str:
    values = valueString.split(",")
    outString = f"data['{indicator}'].iat[index] > {values[0]} and data['{indicator}'].iat[index] < {values[1]}"
    return outString

def __within_range_including(valueString, indicator) -> str:
    values = valueString.split(",")
    outString = f"data['{indicator}'].iat[index] >= {values[0]} and data['{indicator}'].iat[index] <= {values[1]}"
    return outString

if __name__ == '__main__':
    test = {
        'buy': 'rsi < 30 0.3',
        'sell': 'rsi > 70 1'
    }
    build(test, "testStrategy")