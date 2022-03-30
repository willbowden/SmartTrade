########################################################################################
#    Module to allow web app and server app to communicate with an SQLite database.    #
########################################################################################

import sqlite3
import random

def __get_conn_and_cursor() -> tuple: # See comments section in document.
    connection = sqlite3.connect('smarttrade.sqlite')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    return connection, cursor

def create_account(username: str, password: str, nickname: str, apiKey: str, exchangeID: str, currency: str) -> int: # Creates new account
    id = __get_unique_id('tblUsers', 'userID')
    query = f"INSERT INTO tblUsers VALUES ({id}, '{username}', ?, '{nickname}', ?, '{exchangeID}', '{currency}')"
    __execute_query(query, (password, apiKey,))
    return id

def create_trade(creatorID: int, creator: str, date: int, symbol: str, tradeType: str, quantity: float, value: float, price: float, profit: float) -> None: # Creates new trade entry
    id = __get_unique_id('tblTrades', 'tradeID')
    query = f"INSERT INTO tblTrades VALUES ({id}, '{creator}', {date}, '{symbol}', '{tradeType}', {quantity}, {price}, {profit})"
    __execute_query(query)
    if creator is "backtest":
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

def __execute_query(query: str, args=None) -> None:
    conn, cursor = __get_conn_and_cursor()
    if args is None:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    conn.commit()
    cursor.close()

def __create_link(userID: int = None, strategyID: int = None, backtestID:int = None, tradeID: int = None) -> None: # Creates a link between objects in one of the link tables
    if backtestID is None and tradeID is None:
        query = f"INSERT INTO tblUserStrategy VALUES ({strategyID}, {userID})"
    elif tradeID is None and backtestID is not None:
        query = f"INSERT INTO tblStrategyBacktest VALUES ({backtestID}, {strategyID}, {userID})"
    elif backtestID is None and tradeID is not None:
        query = f"INSERT INTO tblUserTrades VALUES ({userID}, {tradeID})"
    elif userID is None and strategyID is None:
        query = f"INSERT INTO tblBacktestTrades VALUES ({backtestID}, {tradeID})"

    __execute_query(query)

def __remove_links(linkType: str, id: int):
    query = ""
    if linkType == "strategy":
        query = f"DELETE FROM tblUserStrategy WHERE strategyID={id}"
        __execute_query(query)
        query = f"DELETE FROM tblStrategyBacktest WHERE strategyID={id}"
    elif linkType == "backtest":
        query = f"DELETE FROM tblStrategyBacktest WHERE backtestID={id}"
        __execute_query(query)
        query = f"DELETE FROM tblBacktestTrades WHERE backtestID={id}"
    elif linkType == "trade":
        query = f"DELETE FROM tblUserTrades WHERE tradeID={id}"
    elif linkType == "user":
        query = f"DELETE FROM tblUserStrategy WHERE userID={id}"
        __execute_query(query)
        query = f"DELETE FROM tblUserTrades WHERE userID={id}"
        __execute_query(query)
        query = f"DELETE FROM tblStrategyBacktest WHERE userID={id}"
    
    if query is not "":
        __execute_query(query)


def delete_row(table:str, idName: str, id, tableIDName: str, linkType: str = None) -> None: # Delete a row
    if type(id) == str:
        id = f"'{id}'"
    try:
        if linkType is not None:
            toDelete = get_row_by_column(table, idName, id)
            toDeleteID = toDelete[tableIDName]
            __remove_links(linkType, toDeleteID)

        query = f"DELETE FROM {table} WHERE {idName}={id}"
        __execute_query(query)
    except Exception as e:
        print(e)
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

def get_backtest_trades(backtestID: int) -> list: # Return all trades associated with a backtest.
    return __get_linked_entities(
        'tblBacktest', 'tblTrades',
        'tblBacktestTrades', ['backtestID', 'tradeID'],
        backtestID
    )

def get_user_trades(userID: int) -> list: # Return all trades associated with a user.
    return __get_linked_entities(
        'tblUsers', 'tblTrades',
        'tblUserTrades', ['userID', 'tradeID'],
        userID
    )

def get_user_strategies(userID: int) -> list: # Return all trades associated with a backtest.
    return __get_linked_entities(
        'tblUsers', 'tblStrategies',
        'tblUserStrategy', ['userID', 'strategyID'],
        userID
    )

def get_strategy_backtests(strategyID: int) -> list: # Return all backtests associated with a strategy and the user who performed them.
    cursor = __get_conn_and_cursor()[1]
    query = f"""SELECT tblStrategyBacktest.strategyID, tblStrategyBacktest.backtestID, tblBacktests.backtestID
    FROM tblBacktests 
    INNER JOIN tblBacktests ON tblBacktests.backtestID = tblStrategyBacktest.backtestID
    WHERE tblStrategyBacktest.strategyID = {strategyID}
    """
    result = cursor.execute(query).fetchall()
    cursor.close()
    if result != None:
        final = [dict(item) for item in result]
        return final
    else:
        return None

def __get_linked_entities(table1: str, table2: str, linkTable: str, idNames: list, id: int) -> list: # Return all linked entities linked to another one.
    cursor = __get_conn_and_cursor()[1]
    query = f"""SELECT {table2}.*, {table1}.{idNames[0]} FROM {table2} 
    INNER JOIN {table1} ON {linkTable}.{idNames[0]} = {table1}.{idNames[0]}
    LEFT OUTER JOIN {linkTable} ON {linkTable}.{idNames[1]} = {table2}.{idNames[1]}
    WHERE {table1}.{idNames[0]} = {id}"""

    result = cursor.execute(query).fetchall()
    cursor.close()
    if result != None:
        final = [dict(item) for item in result]
        return final
    else:
        return None

def update_row_by_column(table: str, idName: str, id:int, column: str, value) -> None: # Update a row 
    if type(value) == str: 
        value = f"'{value}'" # Add quotes to value if string so we can put in database
    query = f"UPDATE {table} SET {column}={value} WHERE {idName}={id}"
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

def test():
    delete_row('tblStrategies', 'name', 'Bad Strategy 1', 'strategyID')


if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")
    test()
