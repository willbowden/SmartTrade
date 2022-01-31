import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import { Box, Stack, TextField, Select, FormControl, FormHelperText, MenuItem, InputLabel, Typography, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "../components/centeredPageContainer";

function Register() {
    const [username, setUsername] = useState(null)
    const [inputErrors, setInputErrors] = useState({currency: true, exchangeID: true})
    const [password, setPassword] = useState(null)
    const [nickname, setNickname] = useState(null)
    const [apiKey, setAPIKey] = useState(null)
    const [secretKey, setSecretKey] = useState(null)
    const [exchangeID, setExchangeID] = useState(null)
    const [currency, setCurrency] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)
    const[loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const checkInput = function (field, value, minLength, maxLength, changerFunc) {
      if (minLength <= value.length && value.length <= maxLength) {
        let temp = inputErrors;
        temp[field] = false;
        setInputErrors(temp);
        changerFunc(value);
      } else {
        let temp = inputErrors;
        temp[field] = true;
        setInputErrors(temp);
        changerFunc(value);
      }
     console.log(inputErrors['username'])
    }
  
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
              onChange={(e) => checkInput("username", e.target.value, 4, 20, setUsername)}
              error={inputErrors.username}
              helperText={inputErrors.username ? "Please enter a value of 4-20 characters in length." : null}
            />
            <TextField
              label="Nickname"
              variant="outlined"
              onChange={(e) => checkInput("nickname", e.target.value, 4, 20, setNickname)}
              error={inputErrors.nickname}
              helperText={inputErrors.nickname ? "Please enter a value of 4-20 characters in length." : null}
            />
            </Box>
            <Box>
              <TextField
                label="Password"
                type="password"
                variant="outlined"
                onChange={(e) => checkInput("password", e.target.value, 8, 20, setPassword)}
                error={inputErrors.password}
              helperText={inputErrors.password ? "Please enter a value of 8-20 characters in length." : null}
              />
              <FormControl sx={{m: 1, width: '47.5%'}}>
              <InputLabel id="exchange-selector">Exchange</InputLabel>
              <Select labelID="exchange-selector"
                value={exchangeID}
                label="Exchange"
                onChange={(e) => checkInput("exchangeID", e.target.value, 4, 20, setExchangeID)}
                error={inputErrors.exchangeID}>
                  <MenuItem value={'binance'}>Binance</MenuItem>
                </Select>
                {inputErrors.exchangeID ? <FormHelperText>Please select a value.</FormHelperText> : null}
              </FormControl>
            </Box>
            <Box>
              <TextField
                label="API Key"
                type="password"
                variant="outlined"
                onChange={(e) => checkInput("apiKey", e.target.value, 64, 64, setAPIKey)}
                error={inputErrors.apiKey}
                helperText={inputErrors.apiKey ? "Your API Key should be 64 characters in length." : null}
              />
              <TextField
                label="Private API Key"
                type="password"
                variant="outlined"
                onChange={(e) => checkInput("secretKey", e.target.value, 64, 64, setSecretKey)}
                error={inputErrors.secretKey}
                helperText={inputErrors.secretKey ? "Your Private API Key should be 64 characters characters in length." : null}
              />
            </Box>
            <FormControl sx={{m: 1, width: '97.5%'}}>
              <InputLabel id="currency-selector">Local Currency</InputLabel>
              <Select labelID="currency-selector"
                value={currency}
                label="Currency"
                onChange={(e) => checkInput("currency", e.target.value, 3, 3, setCurrency)}
                error={inputErrors.currency}>
                  <MenuItem value={'usd'}>USD</MenuItem>
                  <MenuItem value={'gbp'}>GBP</MenuItem>
                  <MenuItem value={'eur'}>EUR</MenuItem>
                  <MenuItem value={'cny'}>CNY</MenuItem>
                </Select>
                {inputErrors.currency ? <FormHelperText>Please select a value.</FormHelperText> : null}
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