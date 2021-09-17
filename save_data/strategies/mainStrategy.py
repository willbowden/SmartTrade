import configs

MODEL_NAME = "2021-08-11-11-20_BTC_BUSD_1h_lookup_12_dropout_0.4_units_256_layers_2_features_6_loss_mean_absolute_error_optimizer_rmsprop"
USES_AI = True

config = configs.load_config()

lastTakeProfit = 0

def check_buy(ag, row): # Buy crypto if bot believes future price will be higher
    spend = config['spend_percent'] * ag.balance
    if row['predicted'] > row['current']:
        ag.place_order('buy', spend, row['current'], row['date'])

def check_sell(ag, row): # Sell all crypto if bot believes future price will be lower AND take profit is triggered
    global lastTakeProfit
    cryptoBalance = ag.currentHolding['cryptoBalance']
    if row['predicted'] < row['current']:
        potentialEarnings = cryptoBalance * row['current']
        if potentialEarnings > ag.currentHolding['spent']:
            if lastTakeProfit == 0:
                lastTakeProfit = row['current']
        if lastTakeProfit != 0:
            if row['current'] <= (config["take_profit"] * lastTakeProfit) and potentialEarnings > ag.currentHolding['spent']:
                ag.place_order('sell', cryptoBalance, row['current'], row['date'])
                lastTakeProfit = 0
            elif row['current'] > lastTakeProfit:
                lastTakeProfit = row['current']