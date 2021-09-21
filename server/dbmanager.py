import sqlite3
import random
from sqlite3.dbapi2 import connect

class DBManager: # Class to allow web app and server app to communicate with an SQLite database
    def __get_conn_and_cursor(self):
        connection = sqlite3.connect('smarttrade.db')
        cursor = connection.cursor()
        return connection, cursor

    def user_exists(self, username: str): # Return true if user data is found in database
        result = self.get_account_by_column('username', username) # Gets account row from other function
        return result != None
        
    def get_account_by_column(self, column: str, value: str): # Returns user account by looking up a given field
        cursor = self.__get_conn_and_cursor()[1]
        if type(value) == str:
            value = f"'{value}'"
        query = f"SELECT * FROM tblUsers WHERE {column}={value}"
        result = cursor.execute(query).fetchone()
        cursor.close()
        if result != None:
            account = {'id': result[0], 'username': result[1], 'password': result[2], 'nickname': result[3]}
            return account
        else:
            return None

    def create_account(self, username: str, password: str, nickname: str): # Creates new account entry by checking if randomly generated ID already exists
        uniqueIDFound = False
        conn, cursor = self.__get_conn_and_cursor()
        while not uniqueIDFound:
            id = random.randrange(1, 10**4)
            if self.get_account_by_column('userID', id) == None:
                uniqueIDFound = True
    
        query = f"INSERT INTO tblUsers VALUES ({id}, '{username}', '{password}', '{nickname}', '')"
        cursor.execute(query)
        conn.commit()
        cursor.close()

    # def create_table(self):
    #     conn, cursor = self.__get_conn_and_cursor()
    #     query = """
    #     CREATE TABLE tblUsers (
    #         userID INT PRIMARY KEY,
    #         username VARCHAR(20) NOT NULL,
    #         password VARCHAR(20) NOT NULL,
    #         nickname VARCHAR(20),
    #         binanceKey VARCHAR(64)
    #     )
    #     """
    #     cursor.execute(query)
    #     cursor.close()

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")