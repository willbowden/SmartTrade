# SmartTrade

  SmartTrade is a full-stack app that allows you to create rules-based trading strategies and test them on Cryptocurrency trading datasets, taken from Binance.

> **WARNING**: Being a few years old, there will likely be dependency or version issues with this project. Please see [Deprecation Warning](#deprecation-warning)

# Install

## Node Modules

Install the necessary packages for the frontend:

```bash
cd app
npm install
```

## Python Packages

Install the necessary packages for the backend:

```bash
cd server
python -m pip install -r requirements.txt
```

# Usage

## Launch the server

Run the Python Flask backend:

```bash
cd server
python api.py
```

## Launch the React app:

```bash
cd app
npm start
```

## Accessing the app:

- Navigate to `localhost`, or your configured URL of the React app.
- Click "Register".
- Create an account.
- Take a look around!

# Deprecation Warning

Given that this project was written a few years ago, it is incredibly likely that packages for both Node.js and Python have been updated, introducing dependency or compatibility issues with the project as it stands today. 

I'm afraid I've moved onto future projects, so can't promise to ever fix these issues. However, should some party be interested in resolving them, I'm open to pull requests.