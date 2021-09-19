import os
from flask import Flask, render_template, redirect, url_for, request, session

accounts = [{'username': "admin", "password": "password", "id": 1}] # FOR TEMPORARY TESTING USE. NOT FINAL.

def main():
    SECRET_KEY = os.urandom(32)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route("/", methods=['GET', 'POST'])
    def login(): # Login page
        global accounts # NOT FINAL I KNOW GLOBALS ARE BAD
        msg = False
        if session.get('loggedIn') == True: # If already logged in just go to home page
            return redirect(url_for('home'))
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form: # Only attempt login if method=post and form was filled.
            for account in accounts:
                if account['username'] == request.form['username']:
                    if account['password'] == request.form['password']:
                        # Create session data
                        session['loggedIn'] = True
                        session['id'] = account['id']
                        session['username'] = account['username']
                        return redirect(url_for('home'))
            if session.get('loggedIn') == None:
                msg = 'Incorrect username/password'

        return render_template("index.html", msg=msg)

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



    app.run()

if __name__=='__main__':
    main()