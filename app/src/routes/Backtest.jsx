import React from "react";
import {useState} from 'react';
import '../App.css';
import { CircularProgress } from '@mui/material';
import protectedFetch from "../auth/protectedFetch";
import {Navigate} from 'react-router-dom';
import CenteredPageContainer from "../components/centeredPageContainer";
import BacktestResults from "./BacktestResults.jsx";
import UserStrategies from './UserStrategies.jsx';
import BacktestOptions from "./BacktestOptions";
import { fromUnixTime } from "date-fns";
 
function Backtest() {
  const [redirectToLogin, setRedirect] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [selectedStrategy, setSelectedStrategy] = useState("");
  const [results, setResults] = useState({});

  const selectStrategy = (strategyName) => {
    setSelectedStrategy(strategyName);
    setShowOptions(true);
  }


  const startBacktest = (startDate, endDate, timeframe, symbols, startingBalance, fee) => {
    setShowOptions(false);
    setLoading(true);
    let payload = {
      strategyName: selectedStrategy,
      startDate: startDate,
      endDate: endDate,
      timeframe: timeframe,
      symbols: symbols,
      startingBalance: startingBalance,
      fee: fee
    }
    protectedFetch("/api/run_backtest", {
      method: 'POST',
      body: JSON.stringify(payload)
    }).then((results) => {
      const parsedRows = JSON.parse(results.orderHistory);
      let id = 0;
      let newOrderHistory = []
      parsedRows.forEach((row) => {
        let newRow = row;
        newRow.id = id;
        newRow.timestamp = fromUnixTime(newRow.timestamp / 1000);
        newOrderHistory.push(newRow)
        id += 1;
      })
      results.orderHistory = newOrderHistory;
      setResults(results);
      setLoading(false);
      setShowResults(true);
    })
  }


    return (
        <CenteredPageContainer>
          {loading ? <CircularProgress /> : null}
          { redirectToLogin ? <Navigate to="/login"></Navigate> : null}
          { showOptions ? <BacktestOptions startBacktest={startBacktest} /> : null}
          { showResults ? <BacktestResults results={results} /> : null }
          { !showResults && <UserStrategies selectStrategy={selectStrategy}/>}
        </CenteredPageContainer>
    );
}
 
export default Backtest;