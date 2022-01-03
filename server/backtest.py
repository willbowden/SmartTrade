##########################################################################################
#    Class to conduct a backtest on a chosen strategy and return performance results.    #
##########################################################################################

import plotly.graph_objects as go
from SmartTrade.server import user, configs, datasets, bot, dbmanager


class Backtest:
    def __init__(self, user, startDate, strategyName, plotResults):
        self.owner = user
        self.config = configs.load_config(strategyName, self.owner.id)
        self.plotResults = plotResults
        self.info = {'strategyName': strategyName, 'userID': self.owner.id}
        self.startingBalance = self.config["startingBalance"]
        self.balance = self.config["startingBalance"]
        self.data = {}
        self.bot = bot.Bot(self, strategyName, True, self.config)
        for item in self.config['symbols']:
            self.data[item] = datasets.load_dataset(self.owner, item, self.config['timeframe'], startDate, self.config)
        
        self.__run()

    def __run(self):
        for symbol in self.config['symbols']:
            ds = self.data[symbol]
            print(ds)
            for index, row in ds.iterrows():
                self.bot.tick(ds, index, symbol)
        
        self.__get_results()
        
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
            fig.add_trace(go.Candlestick(x=self.data[item]['timestamp'],
            open=self.data[item]['open'],
            high=self.data[item]['high'],
            low=self.data[item]['low'],
            close=self.data[item]['close'],
            name="Price"))

            fig.add_trace(go.Scatter(
                x=self.data[item]['timestamp'],
                y=self.data[item]['ema'],
                mode='lines',
                name='EMA100',
                line_color="white"
            ))

            fig.add_trace(go.Scatter(
                    x=buyMarkers['timestamp'],
                    y=buyMarkers['price'],
                    mode='markers',
                    name='Buys',
                    text = "Buy",
                    line_color='yellow'))

            fig.add_trace(go.Scatter(
                    x=sellMarkers['timestamp'],
                    y=sellMarkers['price'],
                    mode='markers',
                    name='Sells',
                    text = "Sell",
                    line_color='purple'))

            fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)

            fig.show()



if __name__ == '__main__':
    u = user.User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
    b = Backtest(u, 1632956400000, 'sarScalp', True)