import sqlite3
import random

class DBManager: # Class to allow web app and server app to communicate with an SQLite database
    def __get_cursor(self):
        connection = sqlite3.connect('smarttrade.db')
        return connection.cursor()

    def user_exists(self, username: str): # Return true if user data is found in database
        result = self.get_account_by_column('username', username) # Gets account row from other function
        return result != None
        
    def get_account_by_column(self, column: str, value: str): # Returns user account by looking up a given field
        cursor = self.__get_cursor()
        if type(value) == str:
            value = f"'{value}'"
        query = f"SELECT * FROM tblUsers WHERE {column}={value}"
        result = cursor.execute(query).fetchone()
        cursor.close()
        return result

    def create_account(self, username: str, password: str, nickname: str): # Creates new account entry by checking if randomly generated ID already exists
        uniqueIDFound = False
        cursor = self.__get_cursor()
        while not uniqueIDFound:
            id = random.randrange(1, 10**4)
            if self.get_account_by_column('userID', id) == None:
                uniqueIDFound = True
    
        query = f"INSERT INTO tblUsers VALUES ({id}, '{username}', '{password}', '{nickname}')"
        cursor.execute(query)
        cursor.close()

    # def create_table(self):
    #     cursor = self.__get_cursor()
    #     query = """
    #     CREATE TABLE tblUsers (
    #         userID INT PRIMARY KEY,
    #         username VARCHAR(20) NOT NULL,
    #         password VARCHAR(20) NOT NULL,
    #         nickname VARCHAR(20)
    #     )
    #     """
    #     cursor.execute(query)
    #     cursor.close()

if __name__ == '__main__':
    print(f"Please do not run {__file__} directly.")