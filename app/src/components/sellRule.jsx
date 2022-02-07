import React from 'react';
import { useState, useEffect } from 'react';
import { Grid, Select, Container, FormControl, InputLabel, MenuItem, TextField, Box, IconButton } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';

export default function SellRule(props) {
    const [indicator, setIndicator] = useState("")

    return (
        <Box sx={{bgcolor: '#212121', padding: 1, borderRadius: 2, width: '50vw'}}>
            <Grid container>
                <Grid item xs={4}>
                <FormControl sx={{width: '100%'}}>
                    <InputLabel id="indicator-selector">Indicator</InputLabel>
                    <Select labelId="indicator-selector"
                        value={indicator}
                        label="Indicator"
                        onChange={(e) => {setIndicator(e.target.value)}}
                    >
                        {props.indicators.map((object, i) => {
                            return <MenuItem value={object.name}>{object.name.toUpperCase()}</MenuItem>
                        })}
                    </Select>
                </FormControl>
                </Grid>
                <Grid item xs={1}>
                    <IconButton onClick={() => props.onDelete("sell", props.index)}>
                        <ClearIcon />
                    </IconButton>
                </Grid>
            </Grid>
        </Box>
    )
}