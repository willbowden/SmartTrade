########################################################################################
#    Module to allow web app and server app to communicate with an SQLite database.    #
########################################################################################

import sqlite3
import random

def __get_conn_and_cursor() -> tuple: # See comments section in document.
    connection = sqlite3.connect('smarttrade.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    return connection, cursor

def create_account(username: str, password: str, nickname: str) -> None: # Creates new account
    id = __get_unique_id('tblUsers', 'id')
    query = f"INSERT INTO tblUsers VALUES ({id}, '{username}', '{password}', '{nickname}', '', '', '', '')"
    __execute_query(query)

def create_trade(creatorID: int, creator: str, date: int, symbol: str, tradeType: str, quantity: float, value: float, price: float, profit: float) -> None: # Creates new trade entry
    id = __get_unique_id('tblTrades', 'tradeID')
    query = f"INSERT INTO tblTrades VALUES ({id}, '{creator}', {date}, '{symbol}', '{tradeType}', {quantity}, {price}, {profit})"
    __execute_query(query)
    if creatorID is "backtest":
        __create_link(backtestID=creatorID, strategyID=id)
    else:
        __create_link(userID=creatorID, backtestID=id)

def create_strategy(userID: int, name: str, avgWinRate: float = 0, avgReturn: float = 0) -> None: # Creates new strategy entry
    id = __get_unique_id('tblStrategies', 'strategyID')
    query = f"INSERT INTO tblStrategies VALUES ({id}, '{name}', {avgWinRate}, {avgReturn})"
    __execute_query(query)
    __create_link(strategyID=id, userID=userID)

def create_backtest(strategyID: int, symbols: str, start: int, end: int, buys: int, sells: int, winRate: float, startBalance: float, endBalance: float, gain: float) -> None: # Creates new backtest entry
    id = __get_unique_id('tblBacktests', 'backtestID')
    query = f"INSERT INTO tblBacktests VALUES ({id}, '{symbols}', {start}, {end}, {buys}, {sells}, {winRate}, {startBalance}, {endBalance}, {gain})"
    __execute_query(query)
    __create_link(strategyID=strategyID, backtestID=id)

def __get_unique_id(table: str, idName: str) -> int: # Get an ID that is unused
    uniqueIDFound = False
    while not uniqueIDFound:
        id = random.randrange(1, 10**8) # Generate random 8 digit ID
        if get_row_by_column(table, idName, id) == None:
            uniqueIDFound = True

    return id

def __execute_query(query: str) -> None:
    conn, cursor = __get_conn_and_cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

def __create_link(userID: int = None, strategyID: int = None, backtestID:int = None, tradeID: int = None) -> None: # Creates a link between objects in one of the link tables
    if backtestID is None and tradeID is None:
        query = f"INSERT INTO TABLE tblUserStrategy VALUES ({strategyID}, {userID})"
    elif tradeID is None and backtestID is not None:
        query = f"INSERT INTO TABLE tblStrategyBacktest VALUES ({backtestID}, {strategyID}, {userID})"
    elif backtestID is None and tradeID is not None:
        query = f"INSERT INTO TABLE tblUserTrades VALUES ({userID}, {tradeID})"
    elif userID is None and strategyID is None:
        query = f"INSERT INTO TABLE tblBacktestTrades VALUES ({backtestID}, {tradeID})"

    __execute_query(query)

def delete_row(table:str, id: int) -> None: # Delete a row
    try:
        query = f"DELETE FROM {table} WHERE id={id}"
        __execute_query(query)
    except:
        print("(delete_row): {id} not found!")

def get_row_by_column(table: str, column: str, value) -> dict: # Returns a row from a table by looking up a given field
    cursor = __get_conn_and_cursor()[1]
    if type(value) == str:
        value = f"'{value}'" # Add quotes to value if string so we can put in database
    query = f"SELECT * FROM {table} WHERE {column}={value}"
    result = cursor.execute(query).fetchone()
    cursor.close()
    if result != None: # Map result to dict if we find a row.
        final = dict(result)
        return final
    else:
        return None

def update_row_by_column(table: str, id:int, column: str, value) -> None: # Update a row 
    if type(value) == str: 
        value = f"'{value}'" # Add quotes to value if string so we can put in database
    query = f"UPDATE {table} SET {column}={value} WHERE id={id}"
    __execute_query(query)

def user_exists(username: str) -> bool: # Return true if user data is found in database
    result = get_row_by_column('tblUsers', 'username', username) # Gets account row from other function
    return result != None

def get_all_accounts() -> list: # Get all accounts in database as a dictionary
    cursor = __get_conn_and_cursor()[1]
    query = "SELECT * FROM tblUsers"
    result = cursor.execute(query).fetchall()
    cursor.close()
    accounts = [dict(item) for item in result]

    return accounts

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")