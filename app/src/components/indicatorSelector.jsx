import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Button, Stack, Typography } from '@mui/material';
import IndicatorBox from './indicatorBox';


export default function IndicatorSelector(props) {
    const [chosenIndicators, setChosenIndicators] = useState([]);
    const [availableIndicators, setAvailableIndicators] = useState([]);

    useEffect(() => {
        fetch('/api/available_indicators').then(r => r.json()).then(data => {
            setAvailableIndicators(data);
        }
        )
    }, [])

    useEffect(() => {
        console.log(chosenIndicators);
    }, [chosenIndicators])

    const addIndicator = (val) => {
        let temp = [...chosenIndicators];
        temp.push(val);
        setChosenIndicators(temp);
    }
    
    const updateOptions = (i, key, value) => {
        let temp = [...chosenIndicators];
        temp[i].arguments[key] = value;
        setChosenIndicators(temp);
    }

    const chooseIndicator = (i, name) => {
        availableIndicators.forEach((val, index) => {
            if (val.name === name) {
                let temp = [...chosenIndicators];
                temp[i] = val;
                console.log("Choosing " + val.name)
                setChosenIndicators(temp);
            }
        })
    }

    const deleteIndicator = (i) => {
        let temp = [...chosenIndicators];
        temp.splice(i, 1);
        setChosenIndicators(temp);
    }

    const handleSubmit = () => {
        if (chosenIndicators.length < 1) {
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
                    {chosenIndicators.map(
                        (indicator, i) => {
                            return <IndicatorBox key={i} indicator={indicator} chooseIndicator={chooseIndicator} updateOptions={updateOptions} onDelete={deleteIndicator} index={i} available={availableIndicators}></IndicatorBox>
                        }
                    )}
                </Stack>
            </Grid>
            <Grid item xs={12} sx={{display: 'flex', justifyContent: 'space-evenly'}}>
                <Button variant="contained" color="secondary" onClick={() => {addIndicator({});}}>Add Another</Button>
                <Button variant="contained" color="success" onClick={handleSubmit}>Submit</Button>
            </Grid>
        </Stack>
    )  
}