import os
from flask import Flask, render_template, redirect, url_for, request, flash
import webforms

def main():
    SECRET_KEY = os.urandom(32)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route("/", methods=['GET', 'POST'])
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