#######################################################################################################
#    Flask application that serves webpages to users and provides HTML endpoints for getting data.    #
#######################################################################################################

import random
import os
import hashlib
import requests
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
import dbmanager
import json
import time
from SmartTrade.server.user import User
from SmartTrade.server.strategy import Strategy 
from SmartTrade.server import conversions, account_data, datasets
from SmartTrade.server.backtest import Backtest
from datetime import datetime

def authenticate_user(username, password): # Verify a user's credentials 
    print(f"Attempting Login For: {username}")
    user = None # Return nothing if we can't log the user in.
    if dbmanager.user_exists(username):
        userInfo = dbmanager.get_row_by_column('tblUsers', 'username', username) # Get the prospective user's info.
        salt = userInfo['password'][-32:] # Retrieve the saved salt from the second half of the hashed key.
        combo = hash_password(password, salt) # Create a hash from the newly provided password

        if combo == userInfo['password']: # If the hashed combo matches the one in the database, the user entered the right password.
            user = User(userInfo) # Convert the dictionary of user info into a User object.
    
    return user

def get_user_by_id(payload): # Return a user given their ID
    user_id = payload['identity']
    return User(dbmanager.get_row_by_column('tblUsers', 'userID', user_id))

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

    with open('./server/available_indicators.json', 'r') as infile:
        AVAILABLEINDICATORS = json.load(infile)

    @app.route('/time', methods=["GET"])
    @jwt_required()
    def get_current_time():
        print(current_identity)
        return jsonify({'time': time.time()})

    @app.route('/api/available_indicators', methods=["GET"])
    def get_available_indicators():
        return jsonify(AVAILABLEINDICATORS)

    @app.route('/api/run_backtest', methods=["GET", "POST"])
    @jwt_required()
    def run_backtest():
        payload = request.json
        config = {'startDate': payload['startDate'],
        'endDate': payload['endDate'],
        'symbols': [payload['symbols']],
        'timeframe': payload['timeframe'],
        'startingBalance': float(payload['startingBalance']),
        'fee': float(payload['fee'])}

        strategyID = dbmanager.get_row_by_column('tblStrategies', 'name', payload['strategyName'])['strategyID']
        b = Backtest(current_identity, config, payload['strategyName'])
        b.run()
        results = b.get_results()

        # Add backtest to database
        backtestID  = dbmanager.create_backtest(strategyID, current_identity.id, payload['symbols'],
            payload['startDate'], payload['endDate'], results['numBuys'],
            results['numSells'], results['winRate'], results['startingBalance'],
            results['balance'], results['profit'])

        # Add backtest trades to database
        for index, order in results['orderHistory'].iterrows(): # Add trades to database
            dbmanager.create_trade(backtestID, 'backtest', order['timestamp'].value, order['symbol'],
            order['side'], order['quantity'], order['value'], order['price'], order['profit'])


        # Recalculate average winrate and returns
        backTests = dbmanager.get_strategy_backtests(strategyID)
        numberOfBacktests = len(backTests)
        print(backTests)
        totalWinRate = sum([bt['winRate'] for bt in backTests])
        totalReturn = sum([bt['return'] for bt in backTests])

        if numberOfBacktests > 0:
            avgWinRate = (totalWinRate) / numberOfBacktests
            avgReturn = (totalReturn) / numberOfBacktests

        # Update entries in database
        dbmanager.update_row_by_column('tblStrategies', 'strategyID', strategyID, 'avgWinRate', avgWinRate)
        dbmanager.update_row_by_column('tblStrategies', 'strategyID', strategyID, 'avgReturn', avgReturn)

        results['orderHistory'] = results['orderHistory'].to_json(orient='records')
        return jsonify(results), 200


    @app.route('/api/create_strategy', methods=["GET", "POST"])
    @jwt_required()
    def create_strategy():
        payload = request.json
        alreadyExisting = dbmanager.get_user_strategies(current_identity.id)
        nameClash = False
        for strat in alreadyExisting:
            if strat['name'] == payload['name']:
                nameClash = True
                
        if nameClash:
            payload['name'] += '_2'

        s = Strategy(payload['name'], current_identity.id, payload)
        s.save_to_json()
        dbmanager.create_strategy(current_identity.id, payload['name'])
        return jsonify({'response': 'Ok'}), 200

    @app.route("/api/delete_strategy", methods=['GET', 'POST'])
    @jwt_required()
    def delete_strategy():
        payload = request.json
        print(payload)
        dbmanager.delete_row('tblStrategies', 'name', payload['strategyName'], 'strategyID', 'strategy')
        return jsonify({'response': 'Ok'}), 200

    @app.route('/api/get_strategies', methods=["GET"])
    @jwt_required()
    def get_user_strategies():
        res = dbmanager.get_user_strategies(current_identity.id)
        return jsonify(res), 200

    @app.route('/api/verify_token', methods=['GET'])
    @jwt_required()
    def verify_token():
        return jsonify({'response': 'ok'}), 200

    @app.route('/api/test_candlestick_chart', methods=['POST'])
    @jwt_required()
    def get_dataset():
        payload = request.json
        print(payload)
        print(f"Gathering dataset for: {payload['symbol']}")
        dataset = datasets.load_dataset(current_identity, payload['symbol'], payload['timeframe'],
         int(payload['startDate']), conversions.date_to_unix(datetime.now()), payload['requiredIndicators'])
        dataset = dataset.rename(columns={"timestamp": "time"})
        dataset = dataset.fillna(0)
        out = dataset.to_json(orient="records", date_unit="s")
        return jsonify(out)

    @app.route('/api/get_backtest_results', methods=['POST'])
    @jwt_required()
    def get_backtest_results():
        payload = request.json
        backtestInfo = dbmanager.get_row_by_column('tblBacktests', 'backtestID', payload['backtestID'])
        backtestTrades = dbmanager.get_backtest_trades(payload['backtestID'])
        result = backtestInfo
        result['profit'] = result['return']
        result['profitPercent'] = (result.pop('return') / result['startingBalance']) * 100
        result['numOrders'] = result['numBuys'] + result['numSells']
        result['id'] = result.pop('backtestID')
        result['orderHistory'] = backtestTrades
        for row in result['orderHistory']:
            row['side'] = row.pop('type')
        


        return jsonify(result), 200

    @app.route('/api/get_strategy_backtests', methods=['POST'])
    @jwt_required()
    def get_strategy_backtests():
        payload = request.json
        strategyID = dbmanager.get_row_by_column('tblStrategies', 'name', payload['strategyName'])['strategyID']
        result = dbmanager.get_strategy_backtests(strategyID)
        for row in result:
            row['id'] = row.pop('backtestID')
        return jsonify(result), 200

    @app.route('/api/get_user_holdings', methods=["GET"])
    @jwt_required()
    def get_user_holdings():
        print(f"Fetching Balances For: {current_identity.id}")
        return jsonify(current_identity.get_holdings()), 200

    @app.route('/api/get_user_trades', methods=['GET'])
    @jwt_required()
    def get_user_trade_history():
        #### WARNIIIIIIIIIIIING
        inc = random.randint(4, 12)
        time.sleep(inc)
        ########################
        return jsonify(current_identity.get_trade_history()), 200

    @app.route('/api/register', methods=['POST'])
    def register():
        payload = request.json
        if not dbmanager.user_exists(payload['username']):
            salt = os.urandom(32) # Generate random salt
            combo = hash_password(payload['password'], salt) # Create hashed password
            # Store hash and other details in database
            userID = dbmanager.create_account(payload['username'], combo, payload['nickname'], payload['apiKey'], payload['exchangeID'], payload['currency'])
            
            with open('./server/.env', 'a') as outfile: # Write the user's secret key to the .env file
                outfile.write(f"\n{userID}_SECRET_KEY={payload['secretKey']}\n")
        
            requestObj = {'username': payload['username'], 'password': payload['password']} # Create an object for sending authentication data to our /auth endpoint
            token = requests.post('http://localhost:5000/auth', json=requestObj) # Automatically log the user in with their new details
            return jsonify({'access_token': token})

        else:
            return jsonify({'error_message': 'User already exists!'})

    app.run(debug=True)

if __name__=='__main__':
    main()