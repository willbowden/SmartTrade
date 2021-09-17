AI_NAME = "2021-08-11-11-20_BTC_BUSD_1h_lookup_12_dropout_0.4_units_256_layers_2_features_6_loss_mean_absolute_error_optimizer_rmsprop"

def execute(sim, row):
    spend = 0.01 * sim.balance
    if row['predicted'] > row['current']:
        sim.place_order('buy', spend, row['current'], row['date'])
    elif row['predicted'] < row['current']:
        if sim.lastSignal == "sell":
            spend = sim.cryptoBalance
            sim.place_order('sell', spend, row['current'], row['date'])
        sim.lastSignal = "sell"

CONFIG = {
    "name": "buy_if_predicted_rise_sell_if_last_signal_sell",

    "symbol": "BTC/BUSD",
    "timeframe": "1h",
    "exchange_id": "binance",
    "api_key": "",
    "secret": "",
    "ohlcv_request_size": 500,

    "take_profit": 0.05,
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