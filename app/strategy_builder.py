#########################################################################
#    Module for converting JSON strings in to python strategy files.    #
#########################################################################

INDENT = "    " # To use for structuring python files
CUSTOM_COMPARATORS = ['wre', 'wri', 'cmc']

def build(jsonData):
    pyString = "def check_buy(bot, row):\n"
    pyString += __build_conditions(jsonData['buy'], 'buy')
    pyString += "\n\ndef check_sell(bot, row):\n"
    pyString += __build_conditions(jsonData['sell'], 'sell')
    return pyString

def __build_conditions(rawString, side):
    outString = "" + INDENT
    splitString = rawString.split(" ")
    comparison = __construct_comparison(splitString[0], splitString[1], splitString[2])
    outString += comparison
    outString += INDENT * 2
    outString += f"bot.place_order('{side}')"
    return outString

def __construct_comparison(indicator, comparator, value):
    if comparator not in CUSTOM_COMPARATORS:
        outString = f"if row['{indicator}'][-1] "
        outString += f"{comparator} {value}:\n"
    elif comparator == "wre":
        outString = f"if {__within_range_excluding(value, indicator)}:\n"
    elif comparator == "wri":
        outString = f"if {__within_range_including(value, indicator)}:\n"

    return outString

def __within_range_excluding(valueString, indicator):
    values = valueString.split(",")
    outString = f"row['{indicator}'][-1] > {values[0]} and row['{indicator}'][-1] < {values[1]}"
    return outString

def __within_range_including(valueString, indicator):
    values = valueString.split(",")
    outString = f"row['{indicator}'][-1] >= {values[0]} and row['{indicator}'][-1] <= {values[1]}"
    return outString

if __name__ == '__main__':
    test = {
        'buy': 'rsi wri 25,40',
        'sell': 'rsi >= 70'
    }
    print(build(test))