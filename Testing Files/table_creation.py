import sqlite3

conn = sqlite3.connect('smarttrade.db')
cursor = conn.cursor()

query = """
    CREATE TABLE tblUsers (
        userID INT PRIMARY KEY NOT NULL UNIQUE,
        username VARCHAR(20) NOT NULL,
        password BLOB(96) NOT NULL,
        nickname VARCHAR(20),
        apiKey CHAR(64) NOT NULL,
        exchangeID VARCHAR(10) NOT NULL,
        currency VARCHAR(4)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblStrategies (
        strategyID INT PRIMARY KEY NOT NULL UNIQUE,
        name VARCHAR(20) NOT NULL,
        avgWinRate FLOAT NOT NULL,
        avgReturn FLOAT NOT NULL
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblUserStrategy (
        strategyID INT NOT NULL UNIQUE,
        userID INT NOT NULL,
        FOREIGN KEY (strategyID) REFERENCES tblStrategies(strategyID),
        FOREIGN KEY (userID) REFERENCES tblUsers(userID),
        PRIMARY KEY (strategyID, userID)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblBacktests (
        backtestID INT PRIMARY KEY NOT NULL UNIQUE,
        symbols VARCHAR(150) NOT NULL,
        startTimestamp BIGINT NOT NULL,
        endTimestamp BIGINT NOT NULL,
        numBuys INT NOT NULL,
        numSells INT NOT NULL,
        winRate FLOAT NOT NULL,
        startingBalance FLOAT NOT NULL,
        endingBalance FLOAT NOT NULL,
        return FLOAT NOT NULL
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblStrategyBacktest (
        backtestID INT NOT NULL UNIQUE,
        strategyID INT NOT NULL UNIQUE,
        userID INT NOT NULL UNIQUE,
        FOREIGN KEY (backtestID) REFERENCES tblBacktests(backtestID),
        FOREIGN KEY (strategyID) REFERENCES tblStrategies(strategyID),
        FOREIGN KEY (userID) REFERENCES tblUsers(userID),
        PRIMARY KEY(backtestID, strategyID, userID)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblTrades (
        tradeID INT PRIMARY KEY NOT NULL UNIQUE,
        creator TEXT CHECK( creator IN ("user", "botDry", "botLive", "backtest") ) NOT NULL,
        date BIGINT NOT NULL,
        symbol VARCHAR(15) NOT NULL,
        type TEXT CHECK (type IN ("buy", "sell", "income", "disposal") ) NOT NULL,
        quantity FLOAT NOT NULL,
        value FLOAT NOT NULL,
        price FLOAT NOT NULL,
        profit FLOAT
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblUserTrades (
        userID INT NOT NULL UNIQUE,
        tradeID INT NOT NULL UNIQUE,
        FOREIGN KEY (userID) REFERENCES tblUsers(userID),
        FOREIGN KEY (tradeID) REFERENCES tblTrades(tradeID),
        PRIMARY KEY(userID, tradeID)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblBacktestTrades (
        backtestID INT NOT NULL UNIQUE,
        tradeID INT NOT NULL UNIQUE,
        FOREIGN KEY (backtestID) REFERENCES tblBacktests(backtestID),
        FOREIGN KEY (tradeID) REFERENCES tblTrades(tradeID),
        PRIMARY KEY(backtestID, tradeID)
    )
    """
cursor.execute(query)
conn.commit()