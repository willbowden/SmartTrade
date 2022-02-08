import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Select, FormControl, InputLabel, MenuItem, TextField, Box, IconButton } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';

export default function IndicatorBox(props) {
    const [name, setName] = useState("");
    const [chosen, setChosen] = useState({});
    const [showOptions, setShowOptions] = useState(false);

    const chooseIndicator = (name) => {
        setName(name)
        props.available.forEach((val, index) => {
            if (val.name === name) {
                setChosen(val);
            }
        })
    }

    useEffect(() =>
    {
        if (Object.keys(chosen).length > 0) {
            setShowOptions(true);
            updateParent();
        }
    }, [chosen])

    const updateArgs = (key, value) => {
        let temp = chosen;
        temp.arguments[key] = value;
        setChosen(temp)
    }
    
    const updateParent = () => {
        props.changerFunc(props.index, chosen);
    }

    return (
        <Box sx={{bgcolor: '#212121', padding: 1, borderRadius: 2, width: '90vw', diplay: 'flex', justifyContent: 'space-evenly'}}>
            <Grid container>
                <Grid item xs={11}>
                <FormControl sx={{width: '95%'}}>
                    <InputLabel id="indicator-selector">Indicator</InputLabel>
                    <Select labelId="indicator-selector"
                        value={name}
                        label="Indicator"
                        onChange={(e) => {chooseIndicator(e.target.value)}}
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
                { showOptions ?
                    <Grid item xs={12} sx={{paddingTop: 1.5}}>
                        {Object.keys(chosen.arguments).map((key, i) => {
                            return <TextField
                                key={key}
                                label={key.toUpperCase()}
                                variant="outlined"
                                value={chosen.arguments[key]}
                                onChange={(e) => updateArgs(key, e.target.value)}
                            />
                        })}
                    </Grid>
                 : null}
            </Grid>
        </Box>
    )  
}