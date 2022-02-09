import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Select, FormControl, InputLabel, MenuItem, TextField, Box, IconButton, Typography } from '@mui/material';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import ClearIcon from '@mui/icons-material/Clear';

export default function Rule(props) {
    const [indicator, setIndicator] = useState("");
    const [comparison, setComparison] = useState("=");
    const [value, setValue] = useState(0);
    const [numericalValue, setNumericalValue] = useState(null);
    const [duration, setDuration] = useState(1);
    const events = ["crossup", "crossdown"];
    const price = ["high", "low", "close", "open"];
    const overlaps = ["ema", "ma"];
    const type = props.type
    const index = props.index

    useEffect(() => {
        let asArray = [indicator, comparison, value];
        if (numericalValue !== null) {
            asArray.push(numericalValue);
            asArray.push(duration);
        } else {
            asArray.push(duration);
        }
        console.log(asArray);
        props.changerFunc(type, index, asArray);
    }, [indicator, comparison, value, duration, numericalValue])

    const getOutputValue = (object, outputName) => {
        if (overlaps.includes(object.name)) {
            return object.name + "_" + outputName + "_" + object.arguments[Object.keys(object.arguments)[0]]
        } else {
            return object.name + "_" + outputName
        }
    }

    const getProperName = (object, outputName) => {
        if (overlaps.includes(object.name)) {
            return object.name + ": " + outputName + " " + object.arguments[Object.keys(object.arguments)[0]]
        } else {
            return object.name + ": " + outputName
        }
    }

    return (
        <Box sx={{bgcolor: '#212121', padding: 1, borderRadius: 2, width: '90vw'}}>
            <Grid container sx={{display: 'flex', justifyContent: 'space-evenly'}}>
                <Typography variant="h5" sx={{paddingTop: 1.5}}>{props.type} when </Typography>
                <Grid item xs={2}>
                <FormControl sx={{width: '100%'}}>
                    <InputLabel id="indicator-selector">Indicator</InputLabel>
                    <Select labelId="indicator-selector"
                        value={indicator}
                        label="Indicator"
                        onChange={(e) => {setIndicator(e.target.value)}}
                    >
                        {props.indicators.map((object, i) => {
                            return object.output.map((name, i) => {
                                return <MenuItem key={getOutputValue(object, name)} value={getOutputValue(object, name)}>{getProperName(object, name)}</MenuItem>
                        })
                        })}
                        <MenuItem value={"open"}>Open Price</MenuItem>
                        <MenuItem value={"high"}>High Price</MenuItem>
                        <MenuItem value={"low"}>Low Price</MenuItem>
                        <MenuItem value={"close"}>Close Price</MenuItem>
                        {props.type == "sell" && (
                            <MenuItem value={"profit"}>Profit</MenuItem>
                        )}
                        {props.type == "sell" && (
                            <MenuItem value={"tradeDuration"}>Time In Trade</MenuItem>
                        )}
                    </Select>
                </FormControl>
                </Grid>
                {!events.includes(comparison) ?
                    <Typography variant="h5" sx={{paddingTop: 1.5}}>is</Typography>
                : null}
                <Grid item xs={2}>
                <FormControl sx={{width: '100%'}}>
                    <InputLabel id="comparison-selector">Comparison</InputLabel>
                    <Select labelId="comparison-selector"
                        value={comparison}
                        label="Comparison"
                        onChange={(e) => {setComparison(e.target.value)}}
                    >
                        <MenuItem value={"=="}>Equal To</MenuItem>
                        <MenuItem value={">"}>Greater Than</MenuItem>
                        <MenuItem value={"<"}>Less Than</MenuItem>
                        <MenuItem value={">="}>Greater Than Or Equal To</MenuItem>
                        <MenuItem value={"<="}>Less Than Or Equal To</MenuItem>
                        <MenuItem value={"!="}>Not Equal To</MenuItem>
                        <MenuItem value={"crossup"}>Crosses Above</MenuItem>
                        <MenuItem value={"crossdown"}>Crosses Below</MenuItem>
                    </Select>
                </FormControl>
                </Grid>
                <Grid item xs={2}>
                <FormControl sx={{width: '100%'}}>
                    <InputLabel id="value-selector">Indicator</InputLabel>
                    <Select labelId="value-selector"
                        value={value}
                        label="Indicator"
                        onChange={(e) => {setValue(e.target.value)}}
                    >
                        <MenuItem value={"numerical"}>Numerical Value</MenuItem>
                        {price.includes(indicator) ? null :
                        <MenuItem value={"percentage"}>Percentage Of Close Price</MenuItem>
                        }   
                        {props.indicators.map((object, i) => {
                            return object.output.map((name, i) => {
                                return <MenuItem key={object.name+"_"+name} value={object.name+"_"+name}>{object.name+"_"+name}</MenuItem>
                        })
                        })}
                    </Select>
                </FormControl>
                {value === "numerical" || value === "percentage" ? 
                    <Grid item><ArrowDownwardIcon />
                    <TextField
                        label={"Value"}
                        variant="outlined" 
                        value={numericalValue}
                        onChange={(e) => setNumericalValue(e.target.value)}
                    /></Grid> : null}
                </Grid>
                <IconButton sx={{padding: 1}} onClick={() => props.onDelete(props.type, props.index)}>
                    <ClearIcon />
                </IconButton>
            </Grid>
        </Box>
    )
}