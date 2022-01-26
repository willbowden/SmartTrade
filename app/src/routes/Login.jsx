import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import { Box, Stack, TextField, Typography, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "../components/centeredPageContainer";

function Login() {
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
      setUsername(e.target.value)
    }
  
    const handlePasswordChange = (e) => {
      setPassword(e.target.value)
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
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              onChange={handlePasswordChange}
            />
            <Button sx={{marginTop: 1}} variant="contained" color="success" onClick={onSubmitClick}>Go</Button>
          </Stack>
        </Box>
        }
      </CenteredPageContainer>
    )
  }

  export default Login;

  // <div className="centered-div">
  //         <div id="login-div">
  //         {loading ? <LoadingOverlay /> : null }
  //           <h2>Login</h2>
  //           <form action="#" className="login-form">
  //           <div>
  //               <input id="usernameInput" type="text" 
  //                 placeholder="Username" 
  //                 onChange={handleUsernameChange}
  //                 value={username} />
  //             </div>
  //             <div>
  //               <input
  //                 id="passwordInput"
  //                 type="password"
  //                 placeholder="Password"
  //                 onChange={handlePasswordChange}
  //                 value={password}/>
  //             </div>
  //             <button onClick={onSubmitClick} type="submit">
  //               Login
  //             </button>
  //           </form>
  //             <div id="error-message">
  //               <p>{errorMessage}</p>
  //             </div>
  //         </div>
  //         </div>