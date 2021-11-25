import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Backtest from './routes/Backtest';
import Dashboard from './routes/Dashboard';
import Login from './routes/Login';
import PrivateRoute from './auth/protectedRoute';

ReactDOM.render(
  <BrowserRouter>
    <Routes>
      <Route exact path="/" element={<App />}>
        <Route exact path='/dashboard' element={<PrivateRoute />}>
            <Route exact path='/dashboard' element={<Dashboard />}/>
        </Route>
        <Route path="/backtest" element={<Backtest />} />
        <Route path="/login" element={<Login />} />
      </Route>
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);