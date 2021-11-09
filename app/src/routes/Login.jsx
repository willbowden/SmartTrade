import React, {useState} from "react";
import Clock from "../components/clock.jsx";
import '../App.css';

function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
  
    const onSubmitClick = (e)=>{
      e.preventDefault()
      console.log("You pressed login")
      let payload = {
        'username': username,
        'password': password
      }
      //console.log(payload)
      fetch('/auth', {
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      }).then(r => r.json())
        .then(token => {
          if (token.access_token){
            console.log(token)          
          }
          else {
            console.log("Please type in correct username/password")
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
      <div>
        <h2>Login</h2>
        <form action="#">
          <div>
            <input type="text" 
              placeholder="Username" 
              onChange={handleUsernameChange}
              value={username} 
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              onChange={handlePasswordChange}
              value={password}
            />
          </div>
          <button onClick={onSubmitClick} type="submit">
            Login
          </button>
        </form>
      </div>
    )
  }

  export default Login