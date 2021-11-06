##########################################################################################
#    Class to conduct a backtest on a chosen strategy and return performance results.    #
##########################################################################################

import sys
import importlib
import plotly.graph_objects as go
from SmartTrade.server import constants, configs, datasets, bot


class Backtest:
    def __init__(self, symbols, timeframe, startDate, startingBalance, strategyName, userID, plotResults):
        self.plotResults = plotResults
        self.info = {'strategyName': strategyName, 'userID': userID}
        sys.path.append(constants.STRATEGY_PATH)
        self.strategy = importlib.import_module(strategyName)
        self.startingBalance = startingBalance
        self.balance = startingBalance
        self.config = configs.load_config(strategyName, userID)
        self.config['startingBalance'] = startingBalance
        self.config['symbols'] = symbols
        self.data = {}
        self.bot = bot.Bot(self, strategyName, True, self.config)
        for item in self.config['symbols']:
            self.data[item] = datasets.load_dataset(item, timeframe, startDate, self.config)
        
        self.__run()

    def __run(self):
        for symbol in self.config['symbols']:
            ds = self.data[symbol]
            for index, row in ds.iterrows():
                self.bot.tick(ds, index, symbol)
        
        self.__get_results()

    # NO LONGER USED FOR PERFORMANCE REASONS
    # def __prepare_block(self, symbol, index):
    #     block = self.data[symbol].iloc[[index]]
    #     if index >= (self.config['pastDataSteps'] - 1):
    #         for i in range(1, self.config['pastDataSteps']):
    #             block = block.append(self.data[symbol].iloc[[index-i]])

    #     return block
        
    def __get_results(self):
        results = self.bot.get_info()
        print(f"Balance: ${round(results['balance'], 2)}. Profit: ${round(results['profit'], 2)}, {round(results['profitPercent'], 2)}%. Number of Trades: {results['numOrders']}.")
        print(self.bot.assetHoldings)
        print(self.bot.orderHistory)

        if self.plotResults:
            self.__plot_results(results)


    def __plot_results(self, results):
        for item in self.config['symbols']:
            buyMarkers = results['orderHistory'][results['orderHistory']['side'] == 'buy']
            sellMarkers = results['orderHistory'][results['orderHistory']['side'] == 'sell']
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=self.data[item]['date'],
            open=self.data[item]['open'],
            high=self.data[item]['high'],
            low=self.data[item]['low'],
            close=self.data[item]['close'],
            name="Price"))

            fig.add_trace(go.Scatter(
                x=self.data[item]['date'],
                y=self.data[item]['ma7'],
                mode='lines',
                name='MA 7',
                line_color="orange"
            ))

            fig.add_trace(go.Scatter(
                x=self.data[item]['date'],
                y=self.data[item]['ma99'],
                mode='lines',
                name='MA 99',
                line_color="purple"
            ))

            fig.add_trace(go.Scatter(
                    x=buyMarkers['date'],
                    y=buyMarkers['price'],
                    mode='markers',
                    name='Scores',
                    text = "Buy",
                    line_color='yellow'))

            fig.add_trace(go.Scatter(
                    x=sellMarkers['date'],
                    y=sellMarkers['price'],
                    mode='markers',
                    name='Scores',
                    text = "Sell",
                    line_color='purple'))

            fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)

            fig.show()



if __name__ == '__main__':
    b = Backtest(['ETH/USDT'], '5m', 1632956400000, 1000, 'rsiStrategy', 2194, True)