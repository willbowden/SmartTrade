import React from 'react';
import Grid from '@mui/material/Grid'

export default function CenteredPageContainer(props) {
    return (
    <Grid         
        container
        spacing={0}
        alignItems="center"
        textAlign="center"
        justifyContent="center"
        style={{ minHeight: '92vh', width: '100vw' }}
    >
        {props.children}
    </Grid>);
};