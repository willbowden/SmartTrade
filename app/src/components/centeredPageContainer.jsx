import React from 'react';
import Grid from '@mui/material/Grid'

export default function CenteredPageContainer(props) {
    return (
    <Grid         
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justifyContent="center"
        style={{ minHeight: '92vh', width: '100vw' }}
    >
        {props.children}
    </Grid>);
};