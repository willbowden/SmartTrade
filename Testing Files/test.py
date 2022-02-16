from SmartTrade.server.user import User
from SmartTrade.server import datasets, dbmanager, strategy

u = User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
c = {'symbols': ['ETH/USDT'],
     'fee': 0.001}
s = strategy.Strategy('Test Strategy 1', 2094)
d = datasets.load_dataset(u, "ETH/USDT", "1h", 1634386628000, s.get_indicators())
s.check_buy(None, d, 0, 'ETH/USDT')