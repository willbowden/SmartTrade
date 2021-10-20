def check_buy(bot, data, index, symbol):
    if data['rsi'].iat[index] < 30:
        bot.place_order('buy', (0.3*bot.balance)/data['close'].iat[index], 0.3*bot.balance, data['close'].iat[index], data['date'].iat[index])

def check_sell(bot, data, index, symbol):
    if data['rsi'].iat[index] > 70:
        bot.place_order('sell', (1*bot.assetHoldings[symbol]['balance']), (1*bot.assetHoldings[symbol]['balance']*data['close'].iat[index]), data['close'].iat[index], data['date'].iat[index])