#########################################################################
#    Module for converting JSON strings in to python strategy files.    #
#########################################################################

from SmartTrade.app import constants

def build(jsonData, strategyName) -> None:
    pyString = "def check_buy(bot, row):\n"
    pyString += __build_conditions(jsonData['buy'], 'buy')
    pyString += "\n\ndef check_sell(bot, row):\n"
    pyString += __build_conditions(jsonData['sell'], 'sell')
    
    with open(constants.STRATEGY_PATH + strategyName + ".json", 'w') as outfile:
        outfile.write(pyString)

def __build_conditions(rawString, side) -> str:
    outString = "" + constants.INDENT
    splitString = rawString.split(" ")
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
        outString += f"bot.place_order('{side}')"
    return outString

def __construct_comparison(indicator, comparator, value) -> str:
    if comparator not in constants.CUSTOM_COMPARATORS:
        outString = f"if row['{indicator}'][-1] "
        outString += f"{comparator} {value}:\n"
    elif comparator == "wre":
        outString = f"if {__within_range_excluding(value, indicator)}:\n"
    elif comparator == "wri":
        outString = f"if {__within_range_including(value, indicator)}:\n"

    return outString

def __within_range_excluding(valueString, indicator) -> str:
    values = valueString.split(",")
    outString = f"row['{indicator}'][-1] > {values[0]} and row['{indicator}'][-1] < {values[1]}"
    return outString

def __within_range_including(valueString, indicator) -> str:
    values = valueString.split(",")
    outString = f"row['{indicator}'][-1] >= {values[0]} and row['{indicator}'][-1] <= {values[1]}"
    return outString

if __name__ == '__main__':
    test = {
        'buy': 'rsi wri 25,40 bbl <= 40 bb1 >= 70 bb2 == 5 bb4 >= 6',
        'sell': 'rsi >= 70'
    }
    print(build(test, "testStrategy"))