#######################################################################################################
#    Flask application that serves webpages to users and provides HTML endpoints for getting data.    #
#######################################################################################################

import os
import hashlib
import requests
from re import I
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
import dbmanager
import time
from datetime import timedelta
from SmartTrade.server.controller import Controller
from SmartTrade.server.user import User

def authenticate_user(username, password):
    print(f"Attempting Login: {username, password}")
    if dbmanager.user_exists(username):
        userInfo = dbmanager.get_account_by_column('username', username) # Get the prospective user's info.
        salt = userInfo['password'][32:] # Retrieve the saved salt from the second half of the hashed key.
        key = hashlib.pbkdf2_hmac( # Hash the password we received from the client.
            'sha256', # The hashing algorithm
            password.encode('utf-8'), # Convert the password to bytes
            salt,
            100000 # Number of iterations of SHA-256
        )

        combo = key + salt # Comine new hash and old salt for comparison

        if combo == userInfo['password']: # If the hashed combo matches the one in the database, the user entered the right password.
            user = User(userInfo) # Convert the dictionary of user info into a User object.
    else:
        user = None
    
    return user

def get_user_by_id(payload):
    user_id = payload['identity']
    return User(dbmanager.get_account_by_column('id', user_id))

def main():
    SECRET_KEY = os.urandom(32)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
    app.config['JWT_AUTH_PASSWORD_KEY'] = 'password'
    jwt = JWT(app, authenticate_user, get_user_by_id)

    @app.route('/time', methods=["GET"])
    @jwt_required()
    def get_current_time():
        print(current_identity)
        return jsonify({'time': time.time()})

    @app.route('/api/register', methods=['POST'])
    def register():
        payload = request.json
        if not dbmanager.user_exists(payload['username']):
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac(
                'sha256', # The hashing algorithm
                payload['password'].encode('utf-8'), # Convert the password to bytes
                salt,
                100000 # Number of iterations of SHA-256
            )

            combo = key + salt # Combine the salt and the key to be stored in the password column so we can re-use the salt

            dbmanager.create_account(payload['username'], combo, payload['nickname'])
        
            requestObj = {'username': payload['username'], 'password': combo}
            token = requests.post('/auth', data=requestObj)
            return jsonify({'access_token': token})

        else:
            return jsonify({'error_message': 'User already exists!'})

    app.run(debug=True)

if __name__=='__main__':
    main()