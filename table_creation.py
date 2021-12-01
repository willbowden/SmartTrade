import sqlite3

conn = sqlite3.connect('smarttrade.db')
cursor = conn.cursor()

query = """
    CREATE TABLE IF NOT EXISTS tblUsers (
        id INT PRIMARY KEY NOT NULL,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(20) NOT NULL,
        nickname VARCHAR(20),
        binanceKey CHAR(64),
        secretKey VARCHAR(20),
        exchangeID VARCHAR(10),
        currency VARCHAR(4)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblStrategies (
        strategyID INT PRIMARY KEY NOT NULL,
        name VARCHAR(20) NOT NULL,
        avgWinRate FLOAT,
        avgReturn FLOAT
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblUserStrategy (
        strategyID INT,
        userID INT,
        FOREIGN KEY (strategyID) REFERENCES tblStrategies(strategyID),
        FOREIGN KEY (userID) REFERENCES tblUsers(id),
        PRIMARY KEY (strategyID, userID)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblBacktests (
        backtestID INT PRIMARY KEY NOT NULL,
        symbols VARCHAR(150) NOT NULL,
        numBuys INT,
        numSells INT,
        winRate FLOAT,
        startingBalance FLOAT,
        endingBalance FLOAT,
        return FLOAT
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblStrategyBacktest (
        backtestID INT,
        strategyID INT,
        userID INT,
        FOREIGN KEY (backtestID) REFERENCES tblBacktests(backtestID),
        FOREIGN KEY (strategyID) REFERENCES tblStrategies(strategyID),
        FOREIGN KEY (userID) REFERENCES tblUsers(id),
        PRIMARY KEY(backtestID, strategyID, userID)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblTrades (
        tradeID INT PRIMARY KEY NOT NULL,
        type TEXT CHECK( type IN ("user", "botDry", "botLive", "backtest") ) NOT NULL,
        date BIGINT NOT NULL,
        symbol VARCHAR(15) NOT NULL,
        side TEXT CHECK (side IN ("buy", "sell") ) NOT NULL,
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
        userID INT,
        tradeID INT,
        FOREIGN KEY (userID) REFERENCES tblUsers(id),
        FOREIGN KEY (tradeID) REFERENCES tblTrades(tradeID),
        PRIMARY KEY(userID, tradeID)
    )
    """
cursor.execute(query)
conn.commit()

query = """
    CREATE TABLE tblBacktestTrades (
        backtestID INT,
        tradeID INT,
        FOREIGN KEY (backtestID) REFERENCES tblBacktests(backtestID),
        FOREIGN KEY (tradeID) REFERENCES tblTrades(tradeID),
        PRIMARY KEY(backtestID, tradeID)
    )
    """
cursor.execute(query)
conn.commit()