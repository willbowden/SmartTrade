import React from "react";
import '../App.css';
import {useState} from 'react';
import CenteredPageContainer from "../components/centeredPageContainer";
import CandlestickChart from '../components/candlestickChart.jsx';
import { Grid, Typography, Card, CardContent} from '@mui/material';
import {red, teal, cyan} from '@mui/material/colors';
 
function BacktestResults(props) {
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [selectedGraph, setSelectedGraph] = useState("");
  const [results, setResults] = useState(props.results);

  const profitTextColour = props.results.profit > 0 ? teal[500] : red[500];

  return (
    <CenteredPageContainer>
      <Grid item xs={12}>
        <Typography variant="h2">Backtest Results</Typography>
      </Grid>
      <Grid item xs={4}>
        <Card>
          <CardContent>
            <Typography variant="h3">Profit</Typography>
            <Typography variant="h4" color={profitTextColour}>${props.results.profit}</Typography>
            <Typography variant="body1" color={profitTextColour}>{props.results.profitPercent}%</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={4}>
        <Card>
          <CardContent>
            <Typography variant="h3">Number Of Orders</Typography>
            <Typography variant="h4" color={cyan[500]}>{props.results.numOrders}</Typography>
          </CardContent>
        </Card>
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default BacktestResults;