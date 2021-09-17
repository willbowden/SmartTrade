import configs

MODEL_NAME = "2021-08-11-11-20_BTC_BUSD_1h_lookup_12_dropout_0.4_units_256_layers_2_features_6_loss_mean_absolute_error_optimizer_rmsprop"

config = configs.load_config()

midnightPrice = 0
currentPnl = 0

def update_pnl(row):
    global midnightPrice
    global currentPnl
    if row['date'].hour == 0:
        midnightPrice = row['current']

    if midnightPrice != 0:
        currentPnl = ((row['current'] - midnightPrice) / midnightPrice) * 100

def check_buy(ag, row): # Buy crypto if bot believes future price will be higher
    update_pnl(row)
    spend = config['spend_percent'] * ag.balance
    if currentPnl <= -3:
        ag.place_order('buy', spend, row['current'], row['date'])

def check_sell(ag, row): # Sell all crypto if bot believes future price will be lower AND take profit is triggered
    update_pnl(row)
    potentialEarnings = ag.currentHolding['cryptoBalance'] * row['current']
    if potentialEarnings >= (1.02 * ag.currentHolding['spent']):
        ag.place_order('sell', ag.currentHolding['cryptoBalance'], row['current'], row['date'])