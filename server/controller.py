####################################################################################################
#    Class that coordinates other classes, updating data regularly and running live strategies.    #
####################################################################################################

from SmartTrade.server import account_data
import threading
from SmartTrade.server import dbmanager
from datetime import datetime, timedelta
from SmartTrade.server.looper import Looper
from SmartTrade.server.user import User

class Controller:
    _instance = None

    def __new__(cls, *args, **kwargs): # Return already existing instance if trying to initialise a new one
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.load_users()

        synced = False
        while not synced: # Start a repeating process that calls self.update() every 5 seconds.
            if datetime.now().second % 5 == 0:
                print("STARTING!")
                l = Looper(5, self.update)
                synced = True

    def update_activity(self, userID: int) -> None: # Set the user's last action timestamp, to prevent timeout
        for user in self.users:
            if str(user.id) == str(userID):
                user.lastActivity = datetime.now()

    def get_api_key(self, userID: int) -> str: # Get binance API key for user
        account = dbmanager.get_account_by_column('userID', userID)
        key = account['binanceKey']
        return key

    def login_user(self, userID: int) -> None:
        for user in self.users:
            if str(user.id) == str(userID):
                print(f"LOGGING IN USER {userID}")
                user.login()

    def logout_user(self, userID: int) -> None:
        for user in self.users:
            if str(user.id) == str(userID):
                user.logout()

    def load_users(self) -> None: # Load saved user data like live trading status
        self.users = []
        accountDicts = dbmanager.get_all_accounts()
        for item in accountDicts:
            self.users.append(User(item))

        for user in self.users:
            user.load_data()

    def save_users(self) -> None: # Save user data like live trading status
        for user in self.users:
            user.save_data()

    def get_user_value_data(self, userID: int) -> dict: # Get a matrix of dates and values to be plotted on a graph
        result = {}
        for user in self.users:
            if str(user.id) == str(userID):
                valueData = user.valueData
                result['values'] = [item['value'] for item in valueData]
                result['dates'] = [item['date'] for item in valueData]
        
        return result
    
    def get_user_holdings(self, userID: int) -> list: # Get the user's balances and their values.
        for user in self.users:
            if str(user.id) == str(userID):
                return user.holdings

    def update(self) -> None: # Save data about users and update their activity.
        self.save_users() 

        for user in self.users:
            if user.isLoggedIn: # Only run these functions on logged-in users
                if (datetime.now() - user.lastActivity).total_seconds() > 180: # When user times out, log them out
                    print(f"TIMING OUT USER {user.id}")
                    user.logout()

if __name__ == '__main__':
    pass