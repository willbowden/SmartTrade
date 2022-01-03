buyPrice = 0

def check_crossover(greater, lower, lookup, index):
    for i in range(lookup):
        if greater.iat[index-(i+1)] > lower.iat[index-(i+1)]:
            if greater.iat[index-(i)] < lower.iat[index-(i)]:
                return True
    
    return False


def check_buy(bot, data, index, symbol):
    global buyPrice

    if data['close'].iat[index] > data['ema'].iat[index]:
        if data['macd_macd'].iat[index] > data['macd_macdsignal'].iat[index] and check_crossover(data['macd_macd'], data['macd_macdsignal'], 3, index):
            buyPrice = data['close'].iat[index]
            bot.place_order('buy', (bot.balance / data['close'].iat[index]), bot.balance, data['close'].iat[index], data['timestamp'].iat[index])

def check_sell(bot, data, index, symbol):
    global buyPrice
    if data['close'].iat[index] >= (1.0075 * buyPrice) or data['close'].iat[index] <= (0.995 * buyPrice):
        buyPrice = 0
        bot.place_order('sell', (1*bot.assetHoldings[symbol]['balance']), (1*bot.assetHoldings[symbol]['balance']*data['close'].iat[index]), data['close'].iat[index], data['timestamp'].iat[index])