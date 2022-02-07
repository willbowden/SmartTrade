import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Button, Stack, Typography } from '@mui/material';
import IndicatorBox from './indicatorBox';
import Rule from './rule';

export default function RuleMaker(props) {
    const [buyIndex, setBuyIndex] = useState(0);
    const [sellIndex, setSellIndex] = useState(0);
    const [buyRules, setBuyRules] = useState([]);
    const [sellRules, setSellRules] = useState([]);

    const addRule = (type) => {
        if (type == 'buy') {
            let temp = buyIndex + 1;
            setBuyIndex(temp);
        } else if (type == 'sell') {
            let temp = sellIndex + 1;
            setSellIndex(temp);
        }
    }
    
    const changeRules = (type, i, value) => {
        if (type == 'sell') {
            let temp = sellRules;
            temp[i] = value;
            setSellRules(temp);
        } else if (type == 'buy') {
            let temp = buyRules;
            temp[i] = value;
            setBuyRules(temp);
        }
    }

    const deleteRule = (type, i) => {
        if (type == 'sell') {
            let temp = sellRules;
            temp.splice(i, 1);
            setSellRules(temp);
            temp = sellIndex - 1;
            setSellIndex(temp)
        } else if (type == 'buy') {
            let temp = buyRules;
            temp.splice(i, 1);
            setBuyRules(temp);
            temp = buyIndex - 1;
            setBuyIndex(temp)
        }
    }

    return (
        <Stack>
            <Typography variant="h3" sx={{paddingBottom: 5}}>Step 2: Define Your Rules</Typography>
            <Grid item xs={12}>
                <Stack>
                    <Typography variant="h5">Buy Rules</Typography>
                    {Array.apply(null, Array(buyIndex)).map(function (x, i) { return i; }).map(
                        (x, i) => {
                            return <Rule type="buy" changerFunc={changeRules} indicators={props.indicators} onDelete={deleteRule} index={i}></Rule>
                        }
                    )}
                </Stack>
            </Grid>
            <Grid item xs={12}>
                <Stack>
                    <Typography variant="h5">Sell Rules</Typography>
                    {Array.apply(null, Array(sellIndex)).map(function (x, i) { return i; }).map(
                        (x, i) => {
                            return <Rule type="sell" changerFunc={changeRules} indicators={props.indicators} onDelete={deleteRule} index={i}></Rule>
                        }
                    )}
                </Stack>
            </Grid>
            <Grid item xs={12} sx={{display: 'flex', justifyContent: 'space-evenly'}}>
                <Button variant="contained" color="secondary" onClick={() => {addRule("buy");}}>Add Buy Rule</Button>
                <Button variant="contained" color="secondary" onClick={() => {addRule("sell");}}>Add Sell Rule</Button>
                <Button variant="contained" color="success" onClick={() => props.onComplete(buyRules, sellRules)}>Submit</Button>
            </Grid>
        </Stack>
    )  
}