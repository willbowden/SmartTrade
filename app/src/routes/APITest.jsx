import React, { useState } from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import '../App.css';
import { Box, Stack, TextField, Button, Typography, CircularProgress } from '@mui/material';
import CenteredPageContainer from '../components/centeredPageContainer.jsx';

function APITest() {

    const[loading, setLoading] = useState(false);
    const[result, setResult] = useState('');
    const[endPoint, setEndPoint] = useState('/time');

    const sendRequest = (e) => { // Send a request to the api endpoint of choice
        e.preventDefault();
        console.log(endPoint);
        setLoading(true);
        protectedFetch(endPoint).then(data => {
            setResult(JSON.stringify(data)); // Stringify response and display it to screen
            setLoading(false);
        })
    };

    return(
        <CenteredPageContainer>
            {loading ? <CircularProgress /> :  
            <Box
            component="form"
            sx={{
              '& .MuiTextField-root': { m: 1, width: '25ch' },
              backgroundColor: '#212121',
              borderRadius: 2,
              padding: 3
            }}
            noValidate
            autoComplete="off"
            >
                <Stack>
                    <TextField label="Endpoint" value={endPoint} onChange={(e) => setEndPoint(e.target.value)}></TextField>
                    <Button variant="contained" color="success" onClick={sendRequest} disabled={loading?true:null}>Test</Button>
                    <Typography paragraph variant="subtitle1">Result: {result}</Typography>
                </Stack>
            </Box>
        }
        </CenteredPageContainer>
    );
}

export default APITest;