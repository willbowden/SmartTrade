import React, { Component } from 'react';
import { useState, useEffect } from 'react';
import { Grid, Button, Stack, Typography } from '@mui/material';
import IndicatorBox from './indicatorBox';
import { v4 as uuidv4 } from 'uuid';


export default function IndicatorSelector(props) {
    const [chosenIndicators, setChosenIndicators] = useState({});
    const availableIndicators = [
        {
            "name": "rsi",
            "properName": "Relative Strength Index",
            "functionName": "talib.RSI",
            "plot": null,
            "data": ["close"],
            "arguments": {
                "timeperiod": 14
            },
            "output": [
                "rsi"
            ]
        },
        {
            "name": "bbands",
            "properName": "Bolinger Bands",
            "functionName": "talib.BBANDS",
            "plot": {
                "objects": [
                    {
                        "name": "upperband",
                        "type": "LineSeries",
                        "lineWidth": 2,
                        "colour": "#e38e27",
                        "value": "upperband"
                    },
                    {
                        "name": "middleband",
                        "type": "LineSeries",
                        "lineWidth": 3,
                        "colour": "#0000ff",
                        "value": "middleband"
                    },
                    {
                        "name": "lowerband",
                        "type": "LineSeries",
                        "lineWidth": 2,
                        "colour": "#e38e27",
                        "value": "lowerband"
                    }
                ]
            },
            "data": ["close"],
            "arguments": {
                "timeperiod": 5, 
                "nbdevup": 2, 
                "nbdevdn": 2,
                "matype": 0
            },
            "output": [
                "upperband",
                "middleband",
                "lowerband"
            ]
        },
        {
            "name": "ema",
            "properName": "Exponential Moving Average",
            "functionName": "talib.EMA",
            "plot": {
                "objects": [
                    {
                        "name": "ema",
                        "type": "LineSeries",
                        "lineWidth": 2,
                        "colour": "#e38e27",
                        "value": "ema"
                    }
                ]
            },
            "data": ["close"],
            "arguments": {
                "timeperiod": 9
            },
            "output": [
                "ema"
            ]
        },
        {
            "name": "ma",
            "properName": "Simple Moving Average",
            "functionName": "talib.MA",
            "plot": {
                "objects": [
                    {
                        "name": "ma",
                        "type": "LineSeries",
                        "lineWidth": 2,
                        "colour": "#e38e27",
                        "value": "ma"
                    }
                ]
            },
            "data": ["close"],
            "arguments": {
                "timeperiod": 9
            },
            "output": [
                "ma"
            ]
        }
    ]

    // useEffect(() => {
    //     fetch('/api/available_indicators').then(r => r.json()).then(data => {
    //         setAvailableIndicators(data);
    //     })
    // }, [])

    // useEffect(() => {
    //     console.log(chosenIndicators);
    // }, [chosenIndicators])

    const addIndicator = (val) => {
        const newDict = {...chosenIndicators};
        newDict[uuidv4()] = val;
        console.log(availableIndicators);
        setChosenIndicators(newDict);
    }
    
    const updateOptions = (i, key, value) => {
        const newDict = {...chosenIndicators};
        newDict[i].arguments[key] = value;    
        setChosenIndicators(newDict);
    }

    const chooseIndicator = (i, name) => {
        const toPreventMutation = [...availableIndicators]
        toPreventMutation.forEach((val, index) => {
            const name1 = val.name
            if (name1 === name) {
                const temp = {...chosenIndicators};
                temp[i] = val;
                console.log("Choosing " + name1);
                console.log(temp);
                setChosenIndicators(temp);
            }
        })
    }

    const deleteIndicator = (i) => {
        const temp = {...chosenIndicators};
        delete temp[i]
        setChosenIndicators(temp);
    }

    const handleSubmit = () => {
        if (Object.keys(chosenIndicators).length < 1) {
            alert("Please select an indicator!");
        } else {
            const asArray = [];
            for (var key in chosenIndicators) {
                asArray.push(chosenIndicators[key])
            }
            props.onComplete(asArray);
        }
    }

    return (
        <Stack>
            <Typography variant="h3" sx={{paddingBottom: 5}}>Step 1: Choose Your Indicators</Typography>
            <Grid item xs={12}>
                <Stack>
                    {Object.keys(chosenIndicators).map(
                        (key, i) => {
                            return <IndicatorBox key={key} indicator={chosenIndicators[key]} chooseIndicator={chooseIndicator} updateOptions={updateOptions} onDelete={deleteIndicator} index={key} available={[...availableIndicators]}></IndicatorBox>
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