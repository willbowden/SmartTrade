import React from "react";
import {useState} from 'react';
import '../App.css';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import CenteredPageContainer from "../components/centeredPageContainer";
import {FormControl, Grid, InputLabel, TextField, Button, Typography, MenuItem, Select, OutlinedInput} from '@mui/material';
import DatePicker from '@mui/lab/DatePicker';
import getUnixTime from 'date-fns/getUnixTime'
 
function BacktestOptions(props) {
    const availableTimeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M", "3M", "1y"]
    const availableSymbols = ["ETH/BUSD", "BTC/BUSD", "AVAX/BUSD", "LTC/BUSD", "ETH/USDT", "BTC/USDT", "ADA/BUSD", "ADA/USDT", "BTC/ETH"]
    const [startDate, setStartDate] = useState(1643673600000);
    const [endDate, setEndDate] = useState(1646006400000);
    const [timeframe, setTimeframe] = useState("4h");
    const [symbols, setSymbols] = useState([]);
    const [startingBalance, setStartingBalance] = useState(1000);
    const [fee, setFee] = useState(0.001);

    return (
        <CenteredPageContainer>
            <Grid item xs={12}>
                <Typography variant="h2">Backtesting Options</Typography>
            </Grid>
            <Grid item xs={2} sx={{width: '95%'}}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                        label="Start Date"
                        value={startDate}
                        onChange={(newValue) => {
                        setStartDate(getUnixTime(newValue) * 1000);
                        }}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
            </Grid>
            <Grid item xs={2} sx={{width: '95%'}}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                        label="End Date"
                        value={endDate}
                        onChange={(newValue) => {
                        setEndDate(getUnixTime(newValue) * 1000);
                        }}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
            </Grid>
            <Grid item xs={2}>
            <FormControl sx={{width: '95%'}}>
                    <InputLabel id="timeframe-selector">Timeframe</InputLabel>
                    <Select labelId="timeframe-selector"
                        value={timeframe}
                        label="Timeframe"
                        onChange={(e) => setTimeframe(e.target.value)}>
                        {availableTimeframes.map((object, i) => {
                            return <MenuItem key={object} value={object}>{object}</MenuItem>
                        })}
                    </Select>
                </FormControl>
            </Grid>
            <Grid item xs={3}>
            <FormControl sx={{width: '95%'}}>
                <InputLabel id="symbols-selector">Trading Pairs</InputLabel>
                <Select
                labelId="symbols-selector"
                id="symbols-selector"
                value={symbols}
                onChange={(e) => {setSymbols(e.target.value)}}
                input={<OutlinedInput label="Symbol" />}
                >
                {availableSymbols.map((name) => (
                    <MenuItem
                    key={name}
                    value={name}
                    >
                    {name}
                    </MenuItem>
                ))}
                </Select>
            </FormControl>
            </Grid>
            <Grid item xs={6} sx={{width: '95%'}}>
                <TextField 
                    label="Starting Balance"
                    inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                    variant="outlined"
                    value={startingBalance}
                    onChange={(e) => setStartingBalance(e.target.value)}
                />
            </Grid>
            <Grid item xs={3} sx={{width: '95%'}}>
                <TextField 
                    label="Fee"
                    inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                    variant="outlined"
                    value={fee}
                    onChange={(e) => setFee(e.target.value)}
                />
            </Grid>
            <Grid item xs={4}>
                <Button variant="contained" color="success" onClick={
                    () => props.startBacktest(startDate, endDate, timeframe, symbols, startingBalance, fee)}>Start Backtest</Button>
            </Grid>
        </CenteredPageContainer>
    );
}
 
export default BacktestOptions;