from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Bidirectional
from collections import deque

import joblib
import plotly.graph_objects as go
import tensorflow as tf
import numpy as np
import datasets
import configs, constants, helpers

__MODEL_NAME = "testModel"

def model_exists(modelName):
    try:
        model = tf.keras.models.load_model(constants.MODELS_PATH + modelName)
        del model
        return True
    except:
        return False

def load_model(modelName = __MODEL_NAME):
    model = tf.keras.models.load_model(constants.MODELS_PATH + modelName)
    return model

def create_model(sequence_length=config['sequence_length'], n_features=config['n_features'], units=config['units'], 
    cell=LSTM, n_layers=config['n_layers'], dropout=config['dropout'],
                loss=config['loss'], optimizer=config['optimizer'], bidirectional=config['bidirectional']):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            # first layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
            else:
                model.add(cell(units, return_sequences=True, batch_input_shape=(None, sequence_length, n_features)))
        elif i == n_layers - 1:
            # last layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=False)))
            else:
                model.add(cell(units, return_sequences=False))
        else:
            # hidden layers
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        # add dropout after each layer
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["accuracy", "mean_absolute_error"], optimizer=optimizer)
    symbolName = config['symbol'].replace("/", "_")
    model_path = helpers.generate_model_path(symbolName)
    model.save(model_path)
    return model

def train_model(model, dataset):
    model.fit(dataset['xTrain'], dataset['yTrain'], batch_size=config['batch_size'], epochs=config['epochs'], verbose=1)
    symbolName = config['symbol'].replace("/", "_")
    model_path = helpers.generate_model_path(symbolName)
    model.save(model_path)
    print("Trained model saved!")
    return model
    
def plot_graph(test_df): # Some fuckery to put the data in the right forms

    fig = go.Figure(go.Scatter(x=test_df['testDates'], y=test_df['trueFuture'], 
    name="Real Price", mode='lines', line_color='red'))
    fig.add_trace(go.Scatter(x=test_df['shiftedDates'], y=['predicted'], name="predicted Price",
    mode="lines", line_color='blue'))
    fig.update_layout(
        title="Performance Graph",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        legend_title="Legend"
    )
    fig.show()
    symbolName = config['symbol'].replace("/", "_")
    resultName = helpers.generate_model_name(symbolName)
    fig.write_html((constants.RESULTS_PATH + resultName + ".html"))

def create_sequences(df):
    sequence_data = [] # Separate the dataset into sets of (50 sets of n features, one future price target)
    sequences = deque(maxlen=config['sequence_length'])
    for entry, target in zip(df.iloc[:, :-1].values, df['future'].values):
        sequences.append(entry)
        if len(sequences) == config['sequence_length']:
            sequence_data.append([np.array(sequences), target])
    x, y = [], []
    for seq, target in sequence_data:
        x.append(seq)
        y.append(target)
    
    x = np.array(x)
    y = np.array(y)

    return x, y

def prepare_dataset(symbol, timeframe, split_dataset=config['split_dataset']):
    df = datasets.load_dataset(symbol, timeframe)
    result = {}
    result['originalDF'] = df
    result['date'] = df['date'] # Save the dates separately
    df = df[config['feature_columns']] # Extract only the desired features (as well as "Futures")
    result['df'] = df # Save this whole dataset separately for future usage

    x, y = create_sequences(df)
    result['x'] = x
    result['y'] = y
    
    if split_dataset:
        train_samples = int((1 - config['test_ratio']) * len(x)) # Divide into test and train sets by ratio in config.json
        result['xTrain'] = x[:train_samples]
        result['yTrain'] = y[:train_samples]
        result['xTest'] = x[train_samples:]
        result['testDates'] = result['date'][train_samples:]
        result['current'] = result['df']['close'][train_samples:]
        result['yTest'] = y[train_samples:]
    else:
        result['current'] = result['df']['close']
        result['xTest'] = x
        result['yTest'] = y
        result['testDates'] = result['date']

    return result

def get_final_dataset(ds):
    sc = joblib.load(constants.SCALER_PATH)
    temp_price_array = ds['yTest'].reshape((-1, 1)) # Turn into 2D array to inverse transform
    real_price = sc.inverse_transform(temp_price_array)
    real_price = real_price.reshape(-1) # Return to 1D arrays to plot properly on graph
    current_price = sc.inverse_transform(ds['current'].to_numpy().reshape((-1, 1)))
    ds['current'] = current_price
    ds['trueFuture'] = real_price
    ds['predicted'] = ds['predicted'].reshape(-1)
    while len(ds['predicted']) < len(ds['testDates']):
        ds['predicted'] = np.append(ds['predicted'], None)
    while len(ds['trueFuture']) < len(ds['testDates']):
        ds['trueFuture'] = np.append(ds['trueFuture'], None)
    ds['shiftedDates'] = helpers.shift_array(ds['testDates'].tolist(), -config['lookup_step'], None)
    for name, data in ds['df'].iteritems():
        if name != "Date":
            temp = ds['df'].loc[:, name].to_numpy().reshape((-1, 1))
            inverted = sc.inverse_transform(temp)
            ds['df'].loc[:, name] = inverted.reshape(-1)

    return ds

def test_model(model, dataset, staringBalance=config['testing_starting_balance']):
    dataset['predicted'] = predict(model, dataset['xTest'])
    final = get_final_dataset(dataset)

    plot_graph(final)

def predict(model, data):
    yPred = model.predict(data)

    return yPred