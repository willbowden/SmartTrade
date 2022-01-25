import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import LoadingOverlay from "../components/loadingOverlay.jsx";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';

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
      <Box component="form"
      sx={{flexGrow: 1}}
      autoComplete="off"
      >
        <TextField
          id="outlined-password-input"
          label="Password"
          type="password"
          autoComplete="current-password"
        />
      </Box>
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