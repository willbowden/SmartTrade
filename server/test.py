import hashlib
import os

def hash_password(password, salt):
    key = hashlib.pbkdf2_hmac( # Hash the password we received from the client.
            'sha256', # The hashing algorithm
            password.encode('utf-8'), # Convert the password to bytes
            salt,
            100000 # Number of iterations of SHA-256
    )
 
    combo = key + salt # Combine new hash and old salt for comparison
 
    return combo

def check_password(password, storedHash):
    salt = storedHash[-32:] # Retrieve the saved salt from the second half of the hashed key.
    combo = hash_password(password, salt) # Create a hash from the newly provided password

    if combo == storedHash:
        return True
    else:
        return False

def test():
    salt = os.urandom(32) # Get random salt
    oldHash = hash_password("password", salt)
    result = check_password("wrongPassword", oldHash)
    print(f"Passwords the same: {result}")

test()