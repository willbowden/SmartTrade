import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import '../App.css';
import './Login.css';

function Register() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [errorMessage, setErrorMessage] = useState('')
    const navigate = useNavigate();
  
    const onSubmitClick = (e)=>{
      e.preventDefault()
      let payload = {
        'username': username,
        'password': password,
        
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
            setErrorMessage(result.error_message);
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
      <div className="centered-div">
        <div id="login-div">
        <h2>Register</h2>
        <form action="#" className="login-form">
        <div>
          <input id="usernameInput" type="text" 
            placeholder="Username" 
            onChange={handleUsernameChange}
            value={username} />
        </div>
        <div>
          <input
            id="passwordInput"
            type="password"
            placeholder="Password"
            onChange={handlePasswordChange}
            value={password}/>
        </div>
        <button onClick={onSubmitClick} type="submit">
          Register
        </button>
      </form>
        <div id="error-message">
          <p>{errorMessage}</p>
        </div>
      </div>
      </div>
    )
  }

  export default Register;