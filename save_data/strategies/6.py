MODEL_NAME = "2021-08-11-11-20_BTC_BUSD_1h_lookup_12_dropout_0.4_units_256_layers_2_features_6_loss_mean_absolute_error_optimizer_rmsprop"

def execute(sim, row):
    spend = 0.01 * sim.balance
    if row['predicted'] > row['current']:
        sim.place_order('buy', spend, row['current'], row['date'])
    elif row['predicted'] < row['current']:
        potentialEarnings = sim.cryptoBalance * row['current']
        if potentialEarnings > sim.currentHolding['spent']:
            if sim.lastTakeProfit == 0:
                sim.lastTakeProfit = row['current']
        if sim.lastTakeProfit != 0:
            if row['current'] <= (CONFIG["take_profit"] * sim.lastTakeProfit):
                sim.place_order('sell', sim.cryptoBalance, row['current'], row['date'])
                sim.lastTakeProfit = 0
            elif row['current'] > sim.lastTakeProfit:
                sim.lastTakeProfit = row['current']

#COOPERATE BUY AND SELL


CONFIG = {
    "name": "trailing_take_profit_098",

    "symbol": "BTC/BUSD",
    "timeframe": "1h",
    "exchange_id": "binance",
    "api_key": "",
    "secret": "",
    "ohlcv_request_size": 500,

    "take_profit": 0.98,
    "testing_starting_balance": 10000,
    "split_dataset": False,
    "scale_dataset": True,
    "sequence_length": 50,
    "lookup_step": 12,
    "scale": True,
    "test_ratio": 0.2,
    "n_layers": 2,
    "units": 256,
    "dropout": 0.4,
    "bidirectional": False,
    "loss": "mean_absolute_error",
    "optimizer": "rmsprop",
    "batch_size": 64,
    "epochs": 500,
    "n_features": 6,
    "feature_columns": ["open", "high", "low", "close", "volume", "rsi", "future"]
}