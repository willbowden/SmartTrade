def check_buy(bot, row, symbol):
    if row['rsi'] < 30:
        bot.place_order('buy', (0.3*bot.balance)/row['close'], 0.3*bot.balance, row['close'], row['date'])

def check_sell(bot, row, symbol):
    if row['rsi'] > 70:
        bot.place_order('sell', (1*bot.assetHoldings[symbol]['balance']), (1*bot.assetHoldings[symbol]['balance']*row['close']), row['close'], row['date'])