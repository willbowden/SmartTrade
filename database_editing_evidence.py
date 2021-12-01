import sqlite3

connection = sqlite3.connect('smarttrade.db')
cursor = connection.cursor()

query = """INSERT INTO tblUsers VALUES (2094, 'admin', 'password', 'Will', 'LsyXkKspvvpsPe7xHJFQB2hXr03iUdFMwCRi1BRgQgHGHILKkv8ETf07ESbCCwkK', '', 'binance', 'USD')"""

cursor.execute(query)
connection.commit()
connection.close()