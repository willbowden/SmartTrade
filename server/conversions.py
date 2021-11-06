import datetime
from SmartTrade.server import constants

def unix_to_date(unix):
    dt = datetime.datetime.fromtimestamp(unix/1000)
    return dt

def date_to_unix(date):
    if isinstance(date, str):
        dt = datetime.datetime.strptime(date, '%Y%m%d%H%M%S')
    else:
        dt = date
    unix = dt.timestamp() * 1000
    unix = int(unix)
    return unix

def unix_time_ago(timeframe, number):
    current = datetime.datetime.now(tz="UTC").timestamp()
    increment = constants.TIMEFRAME_MILLISECONDS[timeframe]
    ago = current - (increment * number)
    return ago

def time_increment(timeframe, time):
    number = constants.TIMEFRAME_MILLISECONDS[time] / constants.TIMEFRAME_MILLISECONDS[timeframe]
    return int(number)
        