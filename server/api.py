#######################################################################################################
#    Flask application that serves webpages to users and provides HTML endpoints for getting data.    #
#######################################################################################################

import os
from re import I
from flask import Flask, json, render_template, redirect, url_for, request, session, jsonify
from flask_jwt import JWT, jwt_required, current_identity
import dbmanager
import time
from datetime import timedelta
from SmartTrade.server.controller import Controller

class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return f'Userid={self.id}'

users = [
    User(2094, 'will', 'password')
]

username_table = {u.username: u for u in users}
userid_table = {u.username: u for u in users}

def authenticate(username, password):
    print(f"Attempting Login: {username, password}")
    user = username_table.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

def main():
    SECRET_KEY = os.urandom(32)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
    app.config['JWT_AUTH_PASSWORD_KEY'] = 'password'
    jwt = JWT(app, authenticate, identity)

    @app.route('/time')
    def get_current_time():
        return jsonify({'time': time.time()})

    app.run(debug=True)

if __name__=='__main__':
    main()