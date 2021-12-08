import datetime

def unix_to_date(unix): # Convert a unix timestamp to a datetime object
    dt = datetime.datetime.fromtimestamp(unix/1000) # Divide by 1000 because received timestamps are in milliseconds whereas fromtimestamp() expects seconds.
    return dt

def date_to_unix(date): # Convert a datetime object into a timestamp
    if isinstance(date, str): # If we've been passed a string rather than a datetime object, convert it into one.
        dt = datetime.datetime.strptime(date, '%Y%m%d%H%M%S') # This will convert a string into a date with the format (YEAR:MONTH:DAY HOUR:MINUTE:SECOND)
    else:
        dt = date
    unix = dt.timestamp() * 1000 # Multiply it by 1000 to get milliseconds for use with exchanges.
    unix = int(unix)
    return unix
        