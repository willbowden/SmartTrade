import sqlite3
import os
import hashlib

connection = sqlite3.connect('smarttrade.db')
cursor = connection.cursor()

password = "password"
salt = os.urandom(32)

key = hashlib.pbkdf2_hmac(
    'sha256', # The hashing algorithm
    password.encode('utf-8'), # Convert the password to bytes
    salt,
    100000 # Number of iterations of SHA-256
)

combo = key + salt

print(salt)
print("---")
print(combo)

query = "INSERT INTO tblUsers VALUES (2094, 'admin', ?, 'Will', 'suekvJG6DdYCPx334a5m4IroMK3oqF80Dto03LSSSacUpFRFQOkNR2NVQpO2bPJD', 'binance', 'USD')"

cursor.execute(query, (combo,)) # Pass our combo (which is a bytestring) as an argument for SQLite to parse.
connection.commit() # Save changes and close
connection.close()