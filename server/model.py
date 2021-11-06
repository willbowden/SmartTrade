from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.metrics import Precision
from collections import deque

import statistics
import plotly.graph_objects as go
import tensorflow as tf
import numpy as np
import datasets
from SmartTrade.server import configs, constants, helpers, trainingsets

def model_exists(modelName):
    try:
        model = tf.keras.models.load_model(constants.MODELS_PATH + modelName)
        del model
        return True
    except:
        return False

def load_model(modelName):
    model = tf.keras.models.load_model(constants.MODELS_PATH + modelName)
    return model

def create_model(modelName: str):
    config = configs.load_ai_config(modelName)

    model = Sequential()
    model.add(LSTM(config['units'], return_sequences=True, batch_input_shape=(None, config['sequence_length'], config['n_features'])))
    model.add(Dropout(config['dropout']))
    model.add(LSTM(config['units'], return_sequences=False))
    model.add(Dropout(config['dropout']))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(loss=config['loss'], metrics=[Precision(), 'accuracy'], optimizer=config['optimizer'])
    symbolName = "_".join(config['training_symbols']).replace("/", "_")
    model_path = helpers.get_model_path(symbolName, config)
    model.save(model_path)
    return model

def train_model(dataset, model, modelName):
    config = configs.load_ai_config(modelName)
    model.fit(dataset['xTrain'], dataset['yTrain'], batch_size=config['batch_size'], epochs=config['epochs'], verbose=1)
    symbolName = "_".join(config['training_symbols']).replace("/", "_")
    model_path = helpers.get_model_path(symbolName, config)
    model.save(model_path)
    print("Trained model saved!")
    return model
    
# def plot_graph(test_df):
#     fig = go.Figure(go.Scatter(x=test_df['testDates'], y=test_df['trueFuture'], 
#     name="Real Price", mode='lines', line_color='red'))
#     fig.add_trace(go.Scatter(x=test_df['shiftedDates'], y=['predicted'], name="predicted Price",
#     mode="lines", line_color='blue'))
#     fig.update_layout(
#         title="Performance Graph",
#         xaxis_title="Date",
#         yaxis_title="Price ($)",
#         legend_title="Legend"
#     )
#     fig.show()
#     symbolName = config['symbol'].replace("/", "_")
#     resultName = helpers.generate_model_name(symbolName)
#     fig.write_html((constants.RESULTS_PATH + resultName + ".html"))=

def get_final_dataset(ds):
    np.savetxt('predicted.txt', ds['predicted'])
    return ds

def test_model(model, dataset):
    dataset.loc[:, 'predicted'] = predict(model, dataset['xTest'])
    final = get_final_dataset(dataset)
    #final['dataset'] = final['originalDS']
    #markers = []
    #for i in range(len(final['clamped'])):
    #    marker = {'date': dataset['testDates'].iat[i], 'price': dataset['testClose'].iat[i], 'score': final['clamped'][i]}
    #    markers.append(marker)
    
    #final['markers'] = markers
    #trainingsets.plot_scores(final)


def predict(model, data):
    yPred = model.predict(data)

    return yPred

if __name__ == '__main__':
    modelPathName = "2021-10-23-14-27_ETH_USDT_BTC_USDT_ADA_USDT_SOL_USDT_1h_lookup_0_dropout_0.4_units_256_layers_2_features_6_loss_mean_absolute_error_optimizer_rmsprop"
    model = create_model('testModel')
    #model = load_model(modelPathName)
    ds = trainingsets.create_training_set('testModel', 1603407600000)
    model = train_model(ds, model, 'testModel')
    test_model(model, ds)