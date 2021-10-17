from datetime import datetime
import pandas as pd

totalDays = 0
lastDate = None
alreadyBought = False

def check_buy(bot, data, symbol):
    global totalDays
    global lastDate
    global alreadyBought
    if lastDate is None:
        lastDate = pd.to_datetime(data['date'], unit='ms')
    currentDate = pd.to_datetime(data['date'], unit='ms')
    if currentDate.day != lastDate.day:
        alreadyBought = False
        totalDays += 1
        lastDate = pd.to_datetime(data['date'], unit='ms')
    if totalDays % 7 == 0 and not alreadyBought:
        bot.place_order('buy', (145.70)/data['close'], 145.70, data['close'], data['date'])
        alreadyBought = True

def check_sell(bot, data, symbol):
    pass