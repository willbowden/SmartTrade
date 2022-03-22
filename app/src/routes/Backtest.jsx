import React from "react";
import {useState} from 'react';
import '../App.css';
import { Typography } from '@mui/material';
import protectedFetch from "../auth/protectedFetch";
import {Navigate} from 'react-router-dom';
import CenteredPageContainer from "../components/centeredPageContainer";
import BacktestResults from "./BacktestResults.jsx";
import UserStrategies from './UserStrategies.jsx';
import BacktestOptions from "./BacktestOptions";
 
function Backtest() {
  const [redirectToLogin, setRedirect] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showOptions, setShowOptions] = useState(true);
  const [showResults, setShowResults] = useState(false);

  const startBacktest = (strategyName) => {
    protectedFetch("/api/run_backtest")
  }


    return (
      <CenteredPageContainer>
        { redirectToLogin ? <Navigate to="/login"></Navigate> : null}
        { showResults ? <BacktestResults results={{profit: 150.5, profitPercent: 25, numOrders: 37}}/> : <UserStrategies /> }
        { showOptions ? <BacktestOptions /> : null}
      </CenteredPageContainer>
    );
}
 
export default Backtest;