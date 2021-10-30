highestBuyPrice = 0

def check_buy(bot, data, index, symbol):
    global highestBuyPrice
    if data['rsi'].iat[index-1] < 40 and data['rsi'].iat[index] >= 40 and data['ma7'].iat[index] < data['ma99'].iat[index]:
        lastBuyPrice = data['close'].iat[index]
        if lastBuyPrice > highestBuyPrice:
            highestBuyPrice = lastBuyPrice
        bot.place_order('buy', (0.3*bot.balance)/lastBuyPrice, 0.3*bot.balance, lastBuyPrice, data['date'].iat[index])

def check_sell(bot, data, index, symbol):
    global highestBuyPrice
    if data['close'].iat[index] > 1.01 * highestBuyPrice:
        highestBuyPrice = 0
        bot.place_order('sell', (1*bot.assetHoldings[symbol]['balance']), (1*bot.assetHoldings[symbol]['balance']*data['close'].iat[index]), data['close'].iat[index], data['date'].iat[index])