#######################################################################################################
#    Flask application that serves webpages to users and provides HTML endpoints for getting data.    #
#######################################################################################################

import os
import hashlib
import requests
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
import dbmanager
import time
from SmartTrade.server.user import User

def authenticate_user(username, password): # Verify a user's credentials 
    print(f"Attempting Login For: {username}")
    user = None # Return nothing if we can't log the user in.
    if dbmanager.user_exists(username):
        userInfo = dbmanager.get_account_by_column('username', username) # Get the prospective user's info.
        salt = userInfo['password'][-32:] # Retrieve the saved salt from the second half of the hashed key.
        combo = hash_password(password, salt) # Create a hash from the newly provided password

        if combo == userInfo['password']: # If the hashed combo matches the one in the database, the user entered the right password.
            user = User(userInfo) # Convert the dictionary of user info into a User object.
    
    return user

def get_user_by_id(payload): # Return a user given their ID
    user_id = payload['identity']
    return User(dbmanager.get_account_by_column('id', user_id))

def hash_password(password, salt): # Create a password hash, combining the hashed key and the salt
    key = hashlib.pbkdf2_hmac(
                'sha256', # The hashing algorithm
                password.encode('utf-8'), # Convert the password to bytes
                salt,
                100000 # Number of iterations of SHA-256
            )
    combo = key + salt # Combine key and salt for storage

    return combo


def main():
    SECRET_KEY = os.urandom(32) # Get a random key to sign our JWT tokens with.

    app = Flask(__name__) # Create the app and set config values
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
    app.config['JWT_AUTH_PASSWORD_KEY'] = 'password'
    jwt = JWT(app, authenticate_user, get_user_by_id) # Create our JWT auth manager

    @app.route('/time', methods=["GET"])
    @jwt_required()
    def get_current_time():
        print(current_identity)
        return jsonify({'time': time.time()})

    @app.route('/api/register', methods=['POST'])
    def register():
        payload = request.json
        if not dbmanager.user_exists(payload['username']):
            salt = os.urandom(32) # Generate random salt
            combo = hash_password(payload['password'], salt) # Create hashed password
            dbmanager.create_account(payload['username'], combo, payload['nickname']) # Store hash in database
        
            requestObj = {'username': payload['username'], 'password': combo} # Create an object for sending authentication data to our /auth endpoint
            token = requests.post('http://localhost:5000/auth', json=requestObj) # Automatically log the user in with their new details
            return jsonify({'access_token': token})

        else:
            return jsonify({'error_message': 'User already exists!'})

    app.run(debug=True)

if __name__=='__main__':
    main()