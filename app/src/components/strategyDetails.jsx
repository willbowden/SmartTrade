import React from 'react';
import { useState } from 'react';
import { Grid, Button, Typography, TextField } from '@mui/material';

export default function StrategyDetails(props) {
    const [strategyName, setStrategyName] = useState("");
    const [balance, setBalance] = useState(0);

    const handleSubmit = () => {
        if (strategyName.length < 1 || balance === 0) {
            alert("Please enter values for all fields!")
        } else {
            props.onComplete(strategyName, balance);
        }
    }

    return (
        <Grid container sx={{display: 'flex', justifyContent: 'center'}}>
            <Grid item xs={12}>
                <Typography variant="h3">Step 3: Provide Some Final Details</Typography>
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Strategy Name"
                    variant="outlined" 
                    value={strategyName}
                    onChange={(e) => setStrategyName(e.target.value)}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Strategy Start Balance"
                    variant="outlined" 
                    value={balance}
                    onChange={(e) => setBalance(e.target.value)}
                />
            </Grid>
            <Grid item xs={4}>
                <Button color="success" onClick={handleSubmit}>Submit</Button>
            </Grid>
        </Grid>
    )
}