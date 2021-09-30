# Module to allow web app and server app to communicate with an SQLite database
import sqlite3
import random
from sqlite3.dbapi2 import connect

def __get_conn_and_cursor() -> tuple: # See comments section in document.
    connection = sqlite3.connect('smarttrade.db')
    cursor = connection.cursor()
    return connection, cursor

def create_account(username: str, password: str, nickname: str) -> None: # Creates new account entry by checking if randomly generated ID already exists
    uniqueIDFound = False
    conn, cursor = __get_conn_and_cursor()
    while not uniqueIDFound:
        id = random.randrange(1, 10**4)
        if get_account_by_column('userID', id) == None:
            uniqueIDFound = True

    query = f"INSERT INTO tblUsers VALUES ({id}, '{username}', '{password}', '{nickname}', '', '', '', '')"
    cursor.execute(query)
    conn.commit()
    cursor.close()

def delete_account(userID: int) -> None:
    conn, cursor = __get_conn_and_cursor()
    try:
        query = f"DELETE FROM tblUsers WHERE userID={userID}"
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except:
        print("(delete_account): User not found!")

def user_exists(username: str) -> bool: # Return true if user data is found in database
    result = get_account_by_column('username', username) # Gets account row from other function
    return result != None
    
def get_account_by_column(column: str, value) -> dict: # Returns user account by looking up a given field
    cursor = __get_conn_and_cursor()[1]
    if type(value) == str:
        value = f"'{value}'" # Add quotes to value if string so we can put in database
    query = f"SELECT * FROM tblUsers WHERE {column}={value}"
    result = cursor.execute(query).fetchone()
    cursor.close()
    if result != None: # Map result to dict if we find an account
        account = map_account_to_dict(result)
        return account
    else:
        return None

def map_account_to_dict(accountTuple):
    account = {'userID': accountTuple[0], 'username': accountTuple[1], 'password': accountTuple[2],
         'nickname': accountTuple[3], 'binanceKey': accountTuple[4],
         'secretKey': accountTuple[5], 'exchangeID': accountTuple[6], 'currency': accountTuple[7]}
    return account

def get_all_accounts() -> list:
    accounts = []
    cursor = __get_conn_and_cursor()[1]
    query = "SELECT * FROM tblUsers"
    result = cursor.execute(query).fetchall()
    for item in result:
        account = map_account_to_dict(item)
        accounts.append(account)

    return accounts

def update_account_by_column(id:int, column: str, value) -> None: # Update a user's info 
    conn, cursor = __get_conn_and_cursor()
    if type(value) == str: 
        value = f"'{value}'" # Add quotes to value if string so we can put in database
    query = f"UPDATE tblUsers SET {column}={value} WHERE userID={id}"
    cursor.execute(query)
    conn.commit()
    cursor.close()

def add_account_value(userID: int, date: str, value: float) -> None:
    conn, cursor = __get_conn_and_cursor()
    query = f"INSERT INTO tblAccountValue VALUES ({userID}, '{date}', {value})"
    cursor.execute(query)
    conn.commit()
    cursor.close()

def load_account_values(userID: int) -> list:
    values = []
    cursor = __get_conn_and_cursor()[0]
    query = f"SELECT * FROM tblAccountValue WHERE userID={userID}"
    result = cursor.execute(query).fetchall()
    for item in result:
        value = {'date': item[1], 'value': item[2]}
        values.append(value)

    return values
    
def __add_column_to_table(table:str, columnName:str, datatype:str) -> None: # Add new column to tables
    conn, cursor = __get_conn_and_cursor()
    query = f"ALTER TABLE {table} ADD COLUMN {columnName} {datatype}"
    try:
        cursor.execute(query)
        conn.commit()
        cursor.close()
        print("Success adding column to table.")
    except:
        print("Failed adding column to table.")

def create_table():
    conn, cursor = __get_conn_and_cursor()
    query = """
    CREATE TABLE tblStrategies (
        strategyID INT,
        userID INT,
        PRIMARY KEY (strategyID, userID)
    )
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print("Success.")

def drop_table(tblName: str) -> None:
    conn, cursor = __get_conn_and_cursor()
    query = f"DROP TABLE {tblName}"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print("Success.")

def clear_table(tblName: str) -> None:
    conn, cursor = __get_conn_and_cursor()
    query = f"DELETE FROM {tblName}"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print("Success.")

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")