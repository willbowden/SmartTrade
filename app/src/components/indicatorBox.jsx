import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Select, FormControl, InputLabel, MenuItem, TextField, Box, IconButton, Typography } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';

export default function IndicatorBox(props) {

    const choose = (name) => {
        props.chooseIndicator(props.index, name);
    }

    return (
        <Box sx={{bgcolor: '#212121', padding: 1, borderRadius: 2, width: '90vw', diplay: 'flex', justifyContent: 'space-evenly'}}>
            <Grid container>
                <Typography variant="body2">{props.index}</Typography>
                <Grid item xs={11}>
                <FormControl sx={{width: '95%'}}>
                    <InputLabel id="indicator-selector">Indicator</InputLabel>
                    <Select labelId="indicator-selector"
                        value={props.indicator.name}
                        label="Indicator"
                        onChange={(e) => {choose(e.target.value)}}
                    >
                        {props.available.map((object, i) => {
                            return <MenuItem key={object.name} value={object.name}>{object.properName}</MenuItem>
                        })}
                    </Select>
                </FormControl>
                </Grid>
                <Grid item sx={{padding: 1}}>
                    <IconButton onClick={() => props.onDelete(props.index)}>
                        <ClearIcon />
                    </IconButton>
                </Grid>
                { props.indicator.arguments ? 
                    <Grid item xs={12} sx={{paddingTop: 1.5}}>
                        {Object.keys(props.indicator.arguments).map((key, i) => {
                            return <TextField
                                key={key}
                                label={key.toUpperCase()}
                                value={props.indicator.arguments[key] ? props.indicator.arguments[key] : 0}
                                variant="outlined"
                                onChange={(e) => props.updateOptions(props.index, key, parseInt(e.target.value))}
                            />
                        })}
                    </Grid>
                 : null}
            </Grid>
        </Box>
    )  
}