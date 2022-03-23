import React from "react";
import {useState} from 'react';
import '../App.css';
import { Typography, CircularProgress } from '@mui/material';
import protectedFetch from "../auth/protectedFetch";
import {Navigate} from 'react-router-dom';
import CenteredPageContainer from "../components/centeredPageContainer";
import BacktestResults from "./BacktestResults.jsx";
import UserStrategies from './UserStrategies.jsx';
import BacktestOptions from "./BacktestOptions";
 
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

  const startBacktest = (startDate, timeframe, symbols, fee) => {
    setShowOptions(false);
    setLoading(true);
    let payload = {
      strategyName: selectedStrategy,
      startDate: startDate,
      timeframe: timeframe,
      symbols: symbols,
      fee: fee
    }
    protectedFetch("/api/run_backtest", {
      method: 'POST',
      body: JSON.parse(payload)
    }).then((results) => {
      setResults(results);
    }).catch(() => {
      return <Navigate to="/login" />
    })
  }


    return (
      loading ? <CircularProgress /> : 
        <CenteredPageContainer>
          { redirectToLogin ? <Navigate to="/login"></Navigate> : null}
          { showOptions ? <BacktestOptions startBacktest={startBacktest} /> : null}
          { showResults ? <BacktestResults /> : null }
          { !showOptions && <UserStrategies selectStrategy={selectStrategy}/>}
        </CenteredPageContainer>
    );
}
 
export default Backtest;