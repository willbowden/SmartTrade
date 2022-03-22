import React from "react";
import {useState} from 'react';
import '../App.css';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import CenteredPageContainer from "../components/centeredPageContainer";
import {FormControl, Grid, InputLabel, TextField, Typography, MenuItem} from '@mui/material';
import DatePicker from '@mui/lab/DatePicker';
 
function BacktestOptions() {
    const [startDate, setStartDate] = useState("");
    const [timeframe, setTimeframe] = useState("");
    const [symbols, setSymbols] = useState([]);
    const [fee, setFee] = useState(0);

    return (
        <CenteredPageContainer>
            <Typography>HELLo</Typography>
            <Grid item xs={4}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                        label="Start Date"
                        value={startDate}
                        onChange={(newValue) => {
                        setStartDate(newValue);
                        }}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
            </Grid>
        </CenteredPageContainer>
    );
}
 
export default BacktestOptions;