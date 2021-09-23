import os
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import dbmanager
from SmartTrade.app.controller import Controller

def main():
    controller = Controller()
    SECRET_KEY = os.urandom(32)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route("/", methods=['GET', 'POST'])
    def login(): # Login page
        msg = False
        if session.get('loggedIn') == True: # If already logged in just go to home page
            return redirect(url_for('home'))
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form: # Only attempt login if method=post and form was filled.
            if dbmanager.user_exists(request.form['username']):
                account = dbmanager.get_account_by_column(column="username", value=request.form['username'])
                if account['username'] == request.form['username']:
                    if account['password'] == request.form['password']: # If login details correct
                        # Create session data
                        session['loggedIn'] = True
                        session['userID'] = account['userID']
                        session['username'] = account['username']
                        controller.login_user(account['userID'])
                        return redirect(url_for('home'))
                    else:
                        msg = 'Incorrect username/password'
            else:
                msg = 'Account does not exist. Please register.'

        return render_template("index.html", msg=msg)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        msg = False
        if session.get('loggedIn') == True: # If already logged in just go to home page
            return redirect(url_for('home'))
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'nickname' in request.form: # Only attempt login if method=post and form was filled.
            if not dbmanager.user_exists(request.form['username']):
                dbmanager.create_account(request.form['username'], request.form['password'], request.form['nickname'])
                account = dbmanager.get_account_by_column('username', request.form['username'])
                session['loggedIn'] = True
                session['userID'] = account['userID']
                session['username'] = account['username']
                controller.login_user(account['userID'])
                return redirect(url_for('home'))
            else:
                msg = 'Account already exists! Please log in.'

        return render_template("register.html", msg=msg)

    @app.route("/home", methods=['GET', 'POST'])
    def home():
        if request.method == "POST":
            for item in request.form.listvalues():
                buttonPressed = item[0]
            
            if buttonPressed == "backtest":
                return redirect(url_for('backtest'))
            elif buttonPressed == "strategy_editor":
                return redirect(url_for('strategy_editor'))
            return redirect(url_for('home'))
        else:
            return render_template("home.html")

    @app.route("/backtest")
    def backtest():
        return render_template("backtest.html")

    @app.route("/strategy_editor")
    def strategy_editor():
        return render_template("strategy_editor.html")

    @app.route("/account_value_data")
    def get_account_value_data():
        userID = request.args.get('userID')
        valueData = controller.get_user_value_data(userID)
        controller.update_activity(userID)
        return jsonify(valueData)

    app.run(debug=True)

if __name__=='__main__':
    main()