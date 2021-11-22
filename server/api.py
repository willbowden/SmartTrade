#######################################################################################################
#    Flask application that serves webpages to users and provides HTML endpoints for getting data.    #
#######################################################################################################

import os
from re import I
from flask import Flask, jsonify
from flask_jwt import JWT, jwt_required, current_identity
import dbmanager
import time
from datetime import timedelta
from SmartTrade.server.controller import Controller
from SmartTrade.server.user import User

def authenticate_user(username, password):
    print(f"Attempting Login: {username, password}")
    if dbmanager.user_exists(username):
        user = User(dbmanager.get_account_by_column('username', username))
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

    app.run(debug=True)

if __name__=='__main__':
    main()