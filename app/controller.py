# Class that coordinates other classes, updating data regularly and running live strategies.

from SmartTrade.app import account_data
import threading
from SmartTrade.server import dbmanager
from datetime import datetime, timedelta
from SmartTrade.app.looper import Looper
from SmartTrade.app.user import User

class Controller:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.load_users()

        synced = False
        while not synced:
            if datetime.now().second % 5 == 0:
                print("STARTING!")
                l = Looper(5, self.update)
                synced = True

    def update_activity(self, userID: int) -> None:
        for user in self.users:
            if str(user.id) == str(userID):
                user.lastActivity = datetime.now()

    def get_api_key(self, userID: int) -> str:
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

    def load_users(self) -> None:
        self.users = []
        accountDicts = dbmanager.get_all_accounts()
        for item in accountDicts:
            self.users.append(User(item))

        for user in self.users:
            user.load_data()

    def save_users(self) -> None:
        for user in self.users:
            user.save_data()

    def get_user_value_data(self, userID: int) -> dict:
        result = {}
        for user in self.users:
            if str(user.id) == str(userID):
                valueData = user.valueData
                result['values'] = [item['value'] for item in valueData]
                result['dates'] = [item['date'] for item in valueData]
        
        return result
    
    def get_user_holdings(self, userID: int) -> list:
        for user in self.users:
            if str(user.id) == str(userID):
                holdings = account_data.get_account_holdings(user.exchange)
                return holdings

    def update(self) -> None:
        self.save_users()

        for user in self.users:
            if user.isLoggedIn:
                if (datetime.now() - user.lastActivity).total_seconds() > 180: # When user times out, save their last recorded value and log them out
                    print(f"TIMING OUT USER {user.id}")
                    th = threading.Thread(target=user.save_updated_value)
                    th.start()
                    user.logout()

        if datetime.now().second % 5 == 0: # Every 5 seconds, update user account value to display on page
            for user in self.users:
                if user.isLoggedIn: # Only live update users who are currently viewing their account, this prevents wasting processing power
                    th = threading.Thread(target=user.update_value)
                    th.start()

        if datetime.now().minute == 0: # Every hour, save account value to database 
            for user in self.users:
                if not user.isLoggedIn: # If user not logged in, get a new value before we save as their value won't have updated above
                    th = threading.Thread(target=user.update_value)
                    th.start()
                
                th = threading.Thread(target=user.save_updated_value)
                th.start()

if __name__ == '__main__':
    pass