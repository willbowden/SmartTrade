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

    query = f"INSERT INTO tblUsers VALUES ({id}, '{username}', '{password}', '{nickname}', '')"
    cursor.execute(query)
    conn.commit()
    cursor.close()

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
        account = {'userID': result[0], 'username': result[1], 'password': result[2], 'nickname': result[3]}
        return account
    else:
        return None

def get_all_accounts() -> list:
    accounts = []
    cursor = __get_conn_and_cursor()[1]
    query = "SELECT * FROM tblUsers"
    result = cursor.execute(query).fetchall()
    for item in result:
        account = {'userID': item[0], 'username': item[1], 'password': item[2],
         'nickname': item[3], 'binanceKey': item[4],
         'secretKey': item[5], 'exchangeID': item[6]}
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

def add_account_value(userID: int, date: str, value: float, currency: str) -> None:
    conn, cursor = __get_conn_and_cursor()
    query = f"INSERT INTO tblAccountValue VALUES ({userID}, '{date}', {value}, '{currency}')"
    cursor.execute(query)
    conn.commit()
    cursor.close()

def load_account_values(userID: int) -> list:
    values = []
    cursor = __get_conn_and_cursor()[0]
    query = f"SELECT * FROM tblAccountValue WHERE userID={userID}"
    result = cursor.execute(query).fetchall()
    for item in result:
        value = {'date': item[1], 'value': item[2], 'currency': item[3]}
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
    CREATE TABLE tblAccountValue (
        userID INT,
        date VARCHAR(20),
        value REAL,
        currency VARCHAR(6),
        FOREIGN KEY(userID) REFERENCES tblUsers(userID)
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