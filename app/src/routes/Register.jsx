import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import { Box, Stack, TextField, Select, FormControl, MenuItem, InputLabel, Typography, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "../components/centeredPageContainer";

function Register() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [nickname, setNickname] = useState('')
    const [apiKey, setAPIKey] = useState('')
    const [secretKey, setSecretKey] = useState('')
    const [exchangeID, setExchangeID] = useState('binance')
    const [currency, setCurrency] = useState('')
    const [errorMessage, setErrorMessage] = useState('')
    const[loading, setLoading] = useState(false);
    const navigate = useNavigate();
  
    const onSubmitClick = (e)=>{
      e.preventDefault()
      let payload = {
        'username': username,
        'password': password,
        'nickname': nickname,
        'apiKey': apiKey,
        'secretKey': secretKey,
        'exchangeID': exchangeID,
        'currency': currency
      }
      fetch('/api/register', {
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      }).then(r => r.json())
        .then(result => {
          if (result.access_token){
            console.log(result);
            login(result);
            navigate('/dashboard');
          }
          else {
            setLoading(false);
            setErrorMessage(result.error_message);
          }
        })
    }
  
    return (
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
            <Typography variant="h2">Register</Typography>
            <Box>
            <TextField
              label="Username"
              variant="outlined"
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              label="Nickname"
              variant="outlined"
              onChange={(e) => setNickname(e.target.value)}
            />
            </Box>
            <Box>
              <TextField
                label="Password"
                type="password"
                variant="outlined"
                onChange={(e) => setPassword(e.target.value)}
              />
              <FormControl sx={{m: 1, width: '47.5%'}}>
              <InputLabel id="exchange-selector">Exchange</InputLabel>
              <Select labelID="exchange-selector"
                value={exchangeID}
                label="Exchange"
                onChange={(e) => setExchangeID(e.target.value)}>
                  <MenuItem value={'binance'}>Binance</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box>
              <TextField
                label="API Key"
                type="password"
                variant="outlined"
                onChange={(e) => setAPIKey(e.target.value)}
              />
              <TextField
                label="Private API Key"
                type="password"
                variant="outlined"
                onChange={(e) => setSecretKey(e.target.value)}
              />
            </Box>
            <FormControl sx={{m: 1, width: '97.5%'}}>
              <InputLabel id="currency-selector">Local Currency</InputLabel>
              <Select labelID="currency-selector"
                value={currency}
                label="Currency"
                onChange={(e) => setCurrency(e.target.value)}>
                  <MenuItem value={'usd'}>USD</MenuItem>
                  <MenuItem value={'gbp'}>GBP</MenuItem>
                  <MenuItem value={'eur'}>EUR</MenuItem>
                  <MenuItem value={'cny'}>CNY</MenuItem>
                </Select>
              </FormControl>
            <Button sx={{marginTop: 1}} variant="contained" color="success" onClick={onSubmitClick}>Go</Button>
          </Stack>
          <Typography variant="h5">{errorMessage}</Typography>
        </Box>
        }
      </CenteredPageContainer>
      
    )
  }

  export default Register;