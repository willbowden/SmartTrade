import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Button, Stack, Typography } from '@mui/material';
import IndicatorBox from './indicatorBox';
import { v4 as uuidv4 } from 'uuid';


export default function IndicatorSelector(props) {
    const [chosenIndicators, setChosenIndicators] = useState({});
    const [availableIndicators, setAvailableIndicators] = useState([]);

    useEffect(() => {
        fetch('/api/available_indicators').then(r => r.json()).then(data => {
            setAvailableIndicators(data);
        })
    }, [])

    const addIndicator = (val) => {
        const newDict = chosenIndicators;
        newDict[uuidv4()] = val;
        setChosenIndicators(newDict);
    }
    
    const updateOptions = (i, key, value) => {
        const newDict = {...chosenIndicators};
        newArray[i].arguments[key] = value;    
        setChosenIndicators(newArray);
    }

    const chooseIndicator = (i, name) => {
        availableIndicators.forEach((val, index) => {
            if (val.name === name) {
                const temp = {...chosenIndicators};
                temp[i] = val;
                console.log("Choosing " + val.name);
                console.log(temp);
                setChosenIndicators(temp);
            }
        })
    }

    const deleteIndicator = (i) => {
        const temp = {...chosenIndicators};
        temp[i] = null;
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
                    {Object.keys(chosenIndicators).map(
                        (key, i) => {
                            return <IndicatorBox key={key} indicator={chosenIndicators[key]} chooseIndicator={chooseIndicator} updateOptions={updateOptions} onDelete={deleteIndicator} index={key} available={availableIndicators}></IndicatorBox>
                        }
                    )}
                </Stack>
            </Grid>
            <Grid item xs={12} sx={{display: 'flex', justifyContent: 'space-evenly'}}>
                <Button variant="contained" color="secondary" onClick={() => {addIndicator(availableIndicators[0])}}>Add Another</Button>
                <Button variant="contained" color="success" onClick={handleSubmit}>Submit</Button>
            </Grid>
        </Stack>
    )  
}