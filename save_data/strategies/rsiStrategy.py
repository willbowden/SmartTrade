import configs

MODEL_NAME = "2021-08-11-11-20_BTC_BUSD_1h_lookup_12_dropout_0.4_units_256_layers_2_features_6_loss_mean_absolute_error_optimizer_rmsprop"
USES_AI = False

config = configs.load_config()

lastRSI = [0, 0]
above70 = False

def check_buy(ag, row): # Buy crypto if bot believes future price will be higher
    global lastRSI
    lastRSI.append(row['rsi'])
    lastRSI.pop(0)
    spend = config['spend_percent'] * ag.balance
    if row['rsi'] <= 35 and lastRSI[0] <= 35 and lastRSI[1] <= 35:
        ag.place_order('buy', spend, row['current'], row['date'])

def check_sell(ag, row): # Sell all crypto if bot believes future price will be lower AND take profit is triggered
    global lastRSI
    global above70
    lastRSI.append(row['rsi'])
    lastRSI.pop(0)
    potentialEarnings = ag.currentHolding['cryptoBalance'] * row['close']
    cryptoBalance = ag.currentHolding['cryptoBalance']
    if row['rsi'] > 70:
        above70 = True
    if row['rsi'] <= 70 and above70 == True and potentialEarnings > ag.currentHolding['spent']:
        above70 = False
        ag.place_order('sell', cryptoBalance, row['current'], row['date'])