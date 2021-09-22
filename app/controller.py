# Class that coordinates other classes, updating data regularly and running live strategies.

import threading
from SmartTrade.server import dbmanager
from datetime import datetime
from SmartTrade.app.looper import Looper
from SmartTrade.app.user import User

class Controller:
    def __init__(self):
        self.load_users()

        synced = False
        while not synced:
            if datetime.now().second % 5 == 0:
                print("STARTING!")
                l = Looper(5, self.update)
                synced = True

    def load_users(self):
        self.users = []
        accountDicts = dbmanager.get_all_accounts()
        for item in accountDicts:
            self.users.append(User(item))

        for user in self.users:
            user.load_data()

    def save_users(self):
        for user in self.users:
            user.save_data()

    def get_user_value_data(self, userID):
        result = {}
        for user in self.users:
            if str(user.id) == str(userID):
                valueData = user.valueData
                result['values'] = [item['value'] for item in valueData]
                result['dates'] = [item['date'] for item in valueData]
        
        return result

    def update(self):
        self.save_users()

        if datetime.now().second % 5 == 0:
            for user in self.users:
                th = threading.Thread(target=user.update_value)
                th.start()

if __name__ == '__main__':
    pass