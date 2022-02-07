import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Select, FormControl, InputLabel, MenuItem, TextField } from '@mui/material';

export default function IndicatorBox(props) {
    const [name, setName] = useState(null);
    const [chosen, setChosen] = useState(null);
    const [showOptions, setShowOptions] = useState(false);

    const chooseIndicator = (name) => {
        setName(name)
        props.available.forEach((val, index) => {
            if (val.name.toUpperCase() === name) {
                setChosen(val);
                setShowOptions(true);
                updateParent()
            }
        })
    }

    const updateArgs = (key, value) => {
        let temp = chosen;
        temp.arguments[key] = value;
        setChosen(temp)
        updateParent()
    }
    
    const updateParent = () => {
        props.changerFunc(props.index, chosen);
    }

    return (
        <Grid item sx={6}>
            <FormControl sx={{width: '50vw'}}>
                <InputLabel id="indicator-selector">Indicator</InputLabel>
                <Select labelId="indicator-selector"
                    value={name}
                    label="Indicator"
                    onChange={(e) => {chooseIndicator(e.target.value);}}
                >
                    {props.available.map((object, i) => {
                        return <MenuItem value={object.name}>{object.name.toUpperCase()}</MenuItem>
                    })}
                </Select>
            </FormControl>
            <Grid item sx={12}>
                { showOptions ? chosen.arguments.map((key, i) => {
                    return <TextField
                        label={key.toUpperCase()}
                        variant="outlined"
                        key={key}
                        onChange={(e) => updateArgs(props.key, e.target.value)}
                    />
                }) : null}
            </Grid>
        </Grid>
    )  
}