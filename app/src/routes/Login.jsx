import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import { Box, Stack, TextField, Typography, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "../components/centeredPageContainer";

function Login() {
    const [usernameError, setUsernameError] = useState(false)
    const [passwordError, setPasswordError] = useState(false)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [errorMessage, setErrorMessage] = useState('')
    const[loading, setLoading] = useState(false);
    const navigate = useNavigate();
  
    const onSubmitClick = (e)=>{
      setLoading(true);
      e.preventDefault()
      let payload = {
        'username': username,
        'password': password
      }
      fetch('/auth', {
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      }).then(r => r.json())
        .then(result => {
          if (result.access_token){
            localStorage.setItem("isAuthenticated", "true");
            login(result);
            navigate('/dashboard');
          }
          else {
            setLoading(false);
            setErrorMessage('Wrong username/password');
          }
        })
    }
  
    const handleUsernameChange = (e) => {
      if (e.target.value.length < 4) {
        setUsernameError(true);
      } else {
        setUsernameError(false);
        setUsername(e.target.value);
      };
    }
  
    const handlePasswordChange = (e) => {
      if (e.target.value.length < 8) {
        setPasswordError(true);
      } else {
        setPasswordError(false);
        setPassword(e.target.value);
      };
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
            <Typography variant="h2">Login</Typography>
            <TextField
              label="Username"
              variant="outlined"
              onChange={handleUsernameChange}
              error={usernameError}
              helperText={usernameError ? "Please enter a value 4 or more characters long." : null}
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              onChange={handlePasswordChange}
              error={passwordError}
              helperText={passwordError ? "Please enter a value 8 or more characters long." : null}
            />
            <Button sx={{marginTop: 1}} variant="contained" color="success" onClick={onSubmitClick}>Go</Button>
            {errorMessage ? <Typography color="red" paragraph>{errorMessage}</Typography> : null}
          </Stack>
        </Box>
        }
      </CenteredPageContainer>
    )
  }

  export default Login;