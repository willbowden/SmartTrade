from SmartTrade.server.user import User
from SmartTrade.server import account_data, dbmanager
import json

u = User(dbmanager.get_row_by_column('tblUsers', 'userID', 2094))
def test():
    result = account_data.get_account_holdings(u)
    with open('test.json', 'w') as outfile:
        json.dump(result, outfile)

test()