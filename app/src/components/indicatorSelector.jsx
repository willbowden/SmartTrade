import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Button, Stack, Typography } from '@mui/material';
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

    const deleteIndicator = (i) => {
        let temp = chosenIndicators;
        temp.splice(i, 1);
        setChosenIndicators(temp);
        temp = index - 1;
        setIndex(temp);
    }

    const handleSubmit = () => {
        if (Object.keys(chosenIndicators).length < 1) {
            alert("Please select an indicator!");
        } else {
            props.onComplete(chosenIndicators);
        }
    }

    return (
        <Stack>
            <Typography variant="h3" sx={{paddingBottom: 5}}>Step 1: Choose Your Indicators</Typography>
            <Grid item xs={12}>
                <Stack>
                    {Array.apply(null, Array(index)).map(function (x, i) { return i; }).map(
                        (x, i) => {
                            return <IndicatorBox key={i} changerFunc={changerFunc} onDelete={deleteIndicator} index={i} available={availableIndicators}></IndicatorBox>
                        }
                    )}
                </Stack>
            </Grid>
            <Grid item xs={12} sx={{display: 'flex', justifyContent: 'space-evenly'}}>
                <Button variant="contained" color="secondary" onClick={() => {addIndicator();}}>Add Another</Button>
                <Button variant="contained" color="success" onClick={handleSubmit}>Submit</Button>
            </Grid>
        </Stack>
    )  
}