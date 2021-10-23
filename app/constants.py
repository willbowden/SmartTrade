####################################
#    Constants for the program.    #
####################################
import os
import talib

dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/save_data/'

# FILE PATH CONSTANTS
CONFIG_PATH = dirname + "strategy_configs/"
DATASET_PATH = dirname + "datasets/dataset_"
TRAININGSET_PATH = dirname + "trainingsets/trainingset_"
STRATEGY_PATH = dirname + "strategies/"
RESULTS_PATH = dirname + "backtest_results/"
MODELS_PATH = dirname + "models/"
SAVE_PATH = dirname + "saves/"
USER_DATA_PATH = dirname + "user_data/"

CRYPTO_EXCHANGES = ['aax', 'binance', 'bitfinex', 'bittrex', 'bitvavo', 'bytetrade', 'currencycom', 'eterbase', 'ftx', 'gopax', 'idex', 'kraken', 'wavesexchange', 'xena']

INDICATOR_FUNCTIONS = {'rsi': talib.RSI, 'sma': talib.SMA, 'ema': talib.EMA, 'ma': talib.MA, 'bb': talib.BBANDS, 'dema': talib.DEMA, 'ht_trendline': talib.HT_TRENDLINE,
'kama': talib.KAMA, 'mama': talib.MAMA, 'mavp': talib.MAVP, 'midpoint': talib.MIDPOINT, 'midprice': talib.MIDPRICE, 'sar': talib.SAR, 'sarext': talib.SAREXT,
't3': talib.T3, 'tema': talib.TEMA, 'trima': talib.TRIMA, 'wma': talib.WMA, 'adx': talib.ADX, 'adxr': talib.ADXR, 'apo': talib.APO, 'aroon': talib.AROON, 
'aroonosc': talib.AROONOSC, 'bop': talib.BOP, 'cci': talib.CCI, 'cmo': talib.CMO, 'dx': talib.DX, 'macd': talib.MACD, 'macdext': talib.MACDEXT, 'macdfix': talib.MACDFIX, 
'mfi': talib.MFI, 'minus_di': talib.MINUS_DI, 'minus_dm': talib.MINUS_DM, 'mom': talib.MOM, 'plus_di': talib.PLUS_DI, 'plus_dm': talib.PLUS_DM, 'ppo': talib.PPO,
'roc': talib.ROC, 'rocp': talib.ROCP, 'rocr': talib.ROCR, 'rocr100': talib.ROCR100, 'rsi': talib.RSI, 'stoch': talib.STOCH, 'stochf': talib.STOCHF, 'stochrsi': talib.STOCHRSI,
'trix': talib.TRIX, 'ultosc': talib.ULTOSC, 'willr': talib.WILLR, 'ad': talib.AD, 'adosc': talib.ADOSC, 'obv': talib.OBV, 'ht_dcperiod': talib.HT_DCPERIOD, 'ht_dcphase': talib.HT_DCPHASE,
'ht_phasor': talib.HT_PHASOR, 'ht_sine': talib.HT_SINE, 'ht_trendmode': talib.HT_TRENDMODE, 'avgprice': talib.AVGPRICE, 'medprice': talib.MEDPRICE, 'typprice': talib.TYPPRICE,
'wclprice': talib.WCLPRICE, 'atr': talib.ATR, 'natr': talib.NATR, 'trange': talib.TRANGE, 'beta': talib.BETA, 'correl': talib.CORREL, 'linearreg': talib.LINEARREG,
'linearreg_angle': talib.LINEARREG_ANGLE, 'linearreg_intercept': talib.LINEARREG_INTERCEPT, 'linearreg_slope': talib.LINEARREG_SLOPE, 'stddev': talib.STDDEV, 'tsf': talib.TSF, 'var': talib.VAR}
 
OHLCV_REQUEST_SIZE = 500

TIMEFRAME_MILLISECONDS = {'1m': 60000, '3m': 180000, '5m': 300000, '30m': 1800000, '1h': 3600000, '2h': 7200000,
 '4h': 14400000, '6h': 21600000, '8h': 28800000, '12h': 43200000, '1d': 86400000, '3d': 259200000, '1w': 604800000, '1M': 2419200000}
 
DATASET_INDICATORS = ['rsi', 'sma', 'ema', 'ma', 'bb', 'adx', 'adxr', 'apo', 'aroon', 'aroonosc', 'bop', 'cci', 'cmo', 'dx', 'macd',
'macdext', 'macdfix', 'mfi', 'minus_di', 'minus_dm', 'mom', 'plus_di', 'plus_dm', 'ppo', 'roc', 'rocp', 'rocr', 'rocr100', 'rsi', 
'stoch', 'stochf', 'stochrsi', 'trix', 'ultosc', 'willr', 'ad', 'adosc', 'obv', 'ht_dcperiod', 'ht_dcphase', 'ht_phasor', 'ht_sine', 
'ht_trendmode', 'avgprice', 'medprice', 'typprice', 'wclprice', 'atr', 'natr', 'trange', 'beta', 'correl', 'linearreg', 'linearreg_angle', 
'linearreg_intercept', 'linearreg_slope', 'stddev', 'tsf', 'var']

INDICATORS_REQUIRED_DATA = {'adx': 'hlc', 'adxr': 'hlc', 'aroon': 'hl', 'aroonosc': 'hl', 'bop': 'ohlc', 'cci': 'hlc', 'dx': 'hlc', 'mfi': 'hlcv',
 'minus_di': 'hlc', 'minus_dm': 'hl', 'plus_di': 'hlc', 'plus_dm': 'hl', 'stoch': 'hlc', 'stochf': 'hlc', 'ultosc': 'hlc', 'willr': 'hlc',
 'ad': 'hlcv', 'adosc': 'hlcv', 'obv': 'cv', 'avgprice': 'ohlc', 'medprice': 'hl', 'typprice': 'hlc', 'wclprice': 'hlc',
 'atr': 'hlc', 'natr': 'hlc', 'trange': 'hlc', 'beta': 'hl', 'correl': 'hl'}

# CONSTANTS FOR STRATEGY BUILDER
INDENT = "    "
CUSTOM_COMPARATORS = ['wre', 'wri', 'cmc']

# CONSTANTS FOR MACHINE LEARNING
TRAININGSET_INDICATORS = ['rsi']
TRAININGSET_SPLIT = 0.8