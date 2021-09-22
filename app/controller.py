# Class that coordinates other classes, updating data regularly and running live strategies.

from datetime import datetime
from looper import Looper
import account_data

class Controller:
    def __init__(self):
        synced = False
        while not synced:
            if datetime.now().second == 0:
                print("STARTING!")
                l = Looper(60, self.update)
                synced = True

    def update(self):
        if datetime.now().minute % 15 == 0:
            account_data.update_account_value()