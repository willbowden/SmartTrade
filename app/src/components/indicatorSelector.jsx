import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Button, Stack } from '@mui/material';
import IndicatorBox from './indicatorBox';
export default function IndicatorSelector(props) {
    const [index, setIndex] = useState(0);
    const [chosenIndicators, setChosenIndicators] = useState([]);
    const [availableIndicators, setAvailableIndicators] = useState([]);

    useEffect(() => {
        fetch('/api/available_indicators').then(r => r.json()).then(data => {
            setAvailableIndicators(data);
            console.log(data);
        }
        )
    }, [])

    const addIndicator = () => {
        let temp = index + 1; 
        setIndex(temp);
    }
    
    const changerFunc = (i, value) => {
        let temp = chosenIndicators;
        temp[i] = value;
        setChosenIndicators(temp);
    }

    return (
        <Stack>
            <Grid item xs={12}>
                <Stack>
                    {Array.apply(null, Array(index)).map(function (x, i) { return i; }).map(
                        (x, i) => {
                            return <IndicatorBox changerFunc={changerFunc} index={i} available={availableIndicators}></IndicatorBox>
                        }
                    )}
                </Stack>
            </Grid>
            <Grid item xs={12}>
                <Button variant="contained" color="secondary" onClick={() => {addIndicator();}}>Add Another</Button>
                <Button variant="contained" color="success">Submit</Button>
            </Grid>
        </Stack>
    )  
}