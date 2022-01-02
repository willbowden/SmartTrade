import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import {login} from "../auth"
import LoadingOverlay from "../components/loadingOverlay";
import './Login.css';

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
      <div className="centered-div">
        <div id="login-div">
        {loading ? <LoadingOverlay /> : null }
        <h2>Register</h2>
        <form action="#" className="login-form">
        <div>
          <input id="usernameInput" type="text" 
            placeholder="Username" 
            onChange={(e) => {setUsername(e.target.value)}}
            value={username} />
        </div>
        <div>
          <input
            id="nicknameInput"
            type = "text"
            placeholder="Nickname"
            onChange={(e) => {setNickname(e.target.value)}}
            value={nickname}/>
        </div>
        <div>
          <input
            id="passwordInput"
            type="password"
            placeholder="Password"
            onChange={(e) => {setPassword(e.target.value)}}
            value={password}/>
        </div>
        <div>
          <input
            id="apiKeyInput"
            type="password"
            placeholder="API Key"
            onChange={(e) => {setAPIKey(e.target.value)}}
            value={apiKey}/>
        </div>
        <div>
          <input
            id="secretKeyInput"
            type="password"
            placeholder="Private API Key"
            onChange={(e) => {setSecretKey(e.target.value)}}
            value={secretKey}/>
        </div>
        <div className="selectField">
          <label for="exchangeIDInput">Exchange</label>
          <select id="exchangeIDInput" name="Exchange" value={exchangeID} onChange={(e) => {setExchangeID(e.target.value)}}>
            <option value="binance">Binance</option>
          </select>
        </div>
        <div className="selectField">
          <label for="currencyInput">Currency</label>
          <select id="currencyInput" name="Currency" value={currency} onChange={(e) => {setCurrency(e.target.value)}}>
            <option value="usd">USD</option>
            <option value="gbp">GBP</option>
            <option value="eur">EUR</option>
            <option value="cny">CNY</option>
          </select>
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