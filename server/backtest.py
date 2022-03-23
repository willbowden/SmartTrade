##########################################################################################
#    Class to conduct a backtest on a chosen strategy and return performance results.    #
##########################################################################################

from SmartTrade.server import user, configs, datasets, bot, dbmanager

class Backtest:
    def __init__(self, user, config, strategyName):
        self.__owner = user
        self.__config = config
        self.id = self.__owner.id
        # Initialise the bot
        self.bot = bot.Bot(self, strategyName, True, config)
        self.info = {'strategyName': strategyName, 'userID': self.__owner.id}
        self.startingBalance = self.bot.startingBalance
        self.data = {}
        for item in self.__config['symbols']:
            self.data[item] = datasets.load_dataset(self.__owner, item, self.__config['timeframe'], self.__config['startDate'], self.bot.strategy.get_indicators())


    def run(self):
        # Iterate over each row of every dataset and check the buy/sell rules of the bot.
        for symbol in self.__config['symbols']:
            ds = self.data[symbol]
            for index, row in ds.iterrows():
                self.bot.tick(ds, index, symbol)
        
        return self.__get_results()
        
    def __get_results(self):
        # Return the results from the backtest such as remaining balance, profit etc.
        results = self.bot.get_info()
        print(f"Balance: ${round(results['balance'], 2)}. Profit: ${round(results['profit'], 2)}, {round(results['profitPercent'], 2)}%. Number of Trades: {results['numOrders']}.")
        results['chosenIndicators'] = self.bot.strategy.get_indicators()
        results['datasets'] = self.data
        print(self.bot.assetHoldings)
        print(self.bot.orderHistory)
        
        return results



    # def __plot_results(self, results):
    #     for item in self.config['symbols']:
    #         buyMarkers = results['orderHistory'][results['orderHistory']['side'] == 'buy']
    #         sellMarkers = results['orderHistory'][results['orderHistory']['side'] == 'sell']
    #         fig = go.Figure()
    #         fig.add_trace(go.Candlestick(x=self.data[item]['timestamp'],
    #         open=self.data[item]['open'],
    #         high=self.data[item]['high'],
    #         low=self.data[item]['low'],
    #         close=self.data[item]['close'],
    #         name="Price"))

    #         fig.add_trace(go.Scatter(
    #             x=self.data[item]['timestamp'],
    #             y=self.data[item]['ema'],
    #             mode='lines',
    #             name='EMA100',
    #             line_color="white"
    #         ))

    #         fig.add_trace(go.Scatter(
    #                 x=buyMarkers['timestamp'],
    #                 y=buyMarkers['price'],
    #                 mode='markers',
    #                 name='Buys',
    #                 text = "Buy",
    #                 line_color='yellow'))

    #         fig.add_trace(go.Scatter(
    #                 x=sellMarkers['timestamp'],
    #                 y=sellMarkers['price'],
    #                 mode='markers',
    #                 name='Sells',
    #                 text = "Sell",
    #                 line_color='purple'))

    #         fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)

    #         fig.show()



if __name__ == '__main__':
    u = user.User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
    b = Backtest(u, {'startDate': 1644537600000,
    'symbols': ["ETH/USDT"],
    'timeframe': '1h',
    'fee': 0.001}, 'Test Strategy 1')
    b.run()