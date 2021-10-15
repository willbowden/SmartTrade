def check_buy(bot, data, symbol):
    if data['rsi'] < 30:
        bot.place_order('buy', (0.3*bot.balance)/data['close'], 0.3*bot.balance, data['close'], data['date'])

def check_sell(bot, data, symbol):
    if data['rsi'] > 70:
        bot.place_order('sell', (1*bot.assetHoldings[symbol]['balance']), (1*bot.assetHoldings[symbol]['balance']*data['close']), data['close'], data['date'])