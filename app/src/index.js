import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import Backtest from './routes/Backtest';
import Dashboard from './routes/Dashboard';
import Login from './routes/Login';
import RequireAuth from './auth/requireAuth.jsx';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <BrowserRouter>
    <Routes>
      <Route exact path="/" element={<App />}>
        <Route path='/dashboard' element={<RequireAuth><Dashboard/></RequireAuth>}/>
        <Route path="/backtest" element={<RequireAuth><Backtest /></RequireAuth>} />
        <Route path="/login" element={<Login />} />
      </Route>
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
